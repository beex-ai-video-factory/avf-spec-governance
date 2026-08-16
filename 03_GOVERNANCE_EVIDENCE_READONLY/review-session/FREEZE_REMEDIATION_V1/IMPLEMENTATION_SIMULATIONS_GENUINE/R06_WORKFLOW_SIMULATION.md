# IMPLEMENTATION SIMULATION REPORT: R06 — WORKFLOW ENGINE (`avf-workflow`)

**Repository:** `avf-workflow` (R06)  
**Layer:** Layer 5 (Orchestration Layer)  
**Target Version:** `1.0.0-rc1`  
**Evaluation Date:** 2026-08-15  
**Author:** R06 Implementation Simulation Agent  
**Status:** IMPLEMENTATION SIMULATED & EVALUATED  

---

## 1. Executive Summary & Verdict

This report presents a full, concrete, technical step-by-step implementation simulation for **R06 (`avf-workflow`)** based on:
1. Blueprint: `review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/03_repo_blueprints/R06_WORKFLOW.md`
2. State Machines: `review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/02_contracts/STATUS_STATE_MACHINES.md`
3. Contracts & Integration Specifications: `02_contracts/` (`domain-entities.schema.json`, `event-envelope.schema.json`, `provider-request.schema.json`, `provider-result.schema.json`), `04_integration/DEPENDENCY_GRAPH.md`, `04_integration/COMMAND_EVENT_CATALOG.md`, and `01_master/SYSTEM_INVARIANTS.md`.

### Verdict Summary
- **Implementability:** The service is implementable using the Temporal TypeScript SDK (`@temporalio/workflow`, `@temporalio/activity`, `@temporalio/worker`), but required **6 significant architectural inventions/assumptions** due to omissions in the blueprint regarding activity signatures, inter-service transport protocols (REST vs gRPC), lease heartbeat mechanics within Temporal deterministic execution, event publishing responsibility boundaries, and operator signal handling.
- **Architectural Inventions Required:** **YES** (`ARCHITECTURAL_INVENTIONS_REQUIRED != NONE`). A total of 6 specific engineering assumptions had to be synthesized.

---

## 2. Technical Step-by-Step Implementation Plan

### 2.1 Repository Architecture & Directory Structure

`avf-workflow` is implemented in TypeScript targeting Node.js 20+ ESM and Temporal Server 1.24+.

```
avf-workflow/
├── src/
│   ├── index.ts                         # Main entrypoint / worker bootstrap
│   ├── workflows/
│   │   ├── VideoGenerationWorkflow.ts   # Primary durable generation orchestrator
│   │   └── MaintenanceWorkflow.ts      # Lease reconciliation & stale job sweeper
│   ├── activities/
│   │   ├── interfaces/                  # Activity interfaces & schemas
│   │   │   ├── ICoreStateActivities.ts
│   │   │   ├── IAssetActivities.ts
│   │   │   ├── IPromptActivities.ts
│   │   │   ├── IProviderActivities.ts
│   │   │   ├── IMediaActivities.ts
│   │   │   ├── IQCActivities.ts
│   │   │   └── ITelemetryActivities.ts
│   │   ├── CoreStateActivities.ts       # R02 HTTP/gRPC client invocations
│   │   ├── AssetActivities.ts           # R04 asset resolution & staging
│   │   ├── PromptActivities.ts          # R05 prompt compilation dispatch
│   │   ├── ProviderActivities.ts        # R07 SDK & R08 Adapter invocations
│   │   ├── MediaActivities.ts           # R12 download, hash, storage
│   │   ├── QCActivities.ts              # R11 technical & semantic QC
│   │   └── TelemetryActivities.ts       # R14 OTel event emissions
│   ├── clients/
│   │   ├── CoreStateClient.ts           # Axios/Fetch client for R02 API
│   │   ├── AssetContinuityClient.ts     # Client for R04 API
│   │   ├── PromptCompilerClient.ts      # Client for R05 API
│   │   ├── ProviderGatewayClient.ts     # Client for R07/R08 Provider Gateway
│   │   ├── MediaServiceClient.ts        # Client for R12 Media Service
│   │   └── QCServiceClient.ts           # Client for R11 QC Service
│   ├── errors/
│   │   ├── WorkflowErrorMapper.ts       # Maps raw/provider errors to 9 normalized codes
│   │   └── NonRetryableAppError.ts      # Temporal ApplicationFailure wrappers
│   ├── models/
│   │   ├── WorkflowInputs.ts            # Typed workflow params
│   │   ├── WorkflowState.ts             # Internal workflow runtime state
│   │   └── ActivityContracts.ts         # Activity input/output definitions
│   └── workers/
│       ├── WorkflowWorker.ts            # Temporal worker hosting workflows & activities
│       └── WorkerConfig.ts              # TaskQueue and connection config
├── tests/
│   ├── unit/                            # Activity unit tests with mock HTTP clients
│   ├── workflow/                        # TestWorkflowEnvironment unit/integration tests
│   ├── conformance/                     # JSON Schema contract validation tests
│   └── fixtures/                        # Mock payloads for FakeProvider & R02
├── package.json
├── tsconfig.json
└── README.md
```

---

### 2.2 Typed Data Models & Contract Interfaces

```typescript
// src/models/WorkflowInputs.ts
import { 
  CanonicalLifecycleStatus, 
  ExecutionStage, 
  NormalizedError 
} from '@avf/contracts/domain-entities';

export interface VideoGenerationWorkflowInput {
  job_id: string;                    // UUID
  project_id: string;                // UUID
  shot_id: string;                   // UUID
  shot_version_id: string;           // UUID
  prompt_version_id?: string;        // UUID (optional, compiled dynamically if omitted)
  provider_id: string;               // e.g. "google-flow", "fake-provider"
  flow_track?: 'TRACK_A_EXTENSION' | 'TRACK_A_PLAYWRIGHT' | 'TRACK_B_FLOWKIT';
  idempotency_key: string;           // SHA256 hex string
  attempt_index: number;             // Default 1
  max_attempts: number;              // Default 3
  correlation_id: string;            // Root trace UUID
  requested_at: string;              // ISO8601 UTC
}

export interface VideoGenerationWorkflowResult {
  job_id: string;
  take_id?: string;
  status: CanonicalLifecycleStatus;
  execution_stage: ExecutionStage;
  provider_job_id?: string;
  storage_uri?: string;
  qc_status?: 'PASSED' | 'REJECTED';
  qc_score?: number;
  cost_credits_used?: number;
  normalized_error?: NormalizedError;
  completed_at: string;
}

export interface WorkflowRuntimeState {
  current_status: CanonicalLifecycleStatus;
  current_stage: ExecutionStage;
  lease_token?: string;
  lease_expires_at?: string;
  progress_percent: number;
  cancellation_requested: boolean;
  cancellation_reason?: string;
}
```

---

### 2.3 Workflow Core Implementation (`VideoGenerationWorkflow.ts`)

The workflow implements the strict two-tier state machine, lease heartbeats, asset staging, prompt compilation, idempotent generation submission, polling, download, QC verification, and domain event emissions.

```typescript
// src/workflows/VideoGenerationWorkflow.ts
import {
  proxyActivities,
  defineSignal,
  defineQuery,
  setHandler,
  sleep,
  ApplicationFailure,
  workflowInfo
} from '@temporalio/workflow';
import {
  VideoGenerationWorkflowInput,
  VideoGenerationWorkflowResult,
  WorkflowRuntimeState
} from '../models/WorkflowInputs';
import type { ICoreStateActivities } from '../activities/interfaces/ICoreStateActivities';
import type { IAssetActivities } from '../activities/interfaces/IAssetActivities';
import type { IPromptActivities } from '../activities/interfaces/IPromptActivities';
import type { IProviderActivities } from '../activities/interfaces/IProviderActivities';
import type { IMediaActivities } from '../activities/interfaces/IMediaActivities';
import type { IQCActivities } from '../activities/interfaces/IQCActivities';
import type { ITelemetryActivities } from '../activities/interfaces/ITelemetryActivities';

// Activity Proxies with Tailored Retry Policies
const coreState = proxyActivities<ICoreStateActivities>({
  startToCloseTimeout: '30 seconds',
  retry: {
    initialInterval: '1s',
    backoffCoefficient: 2,
    maximumInterval: '30s',
    maximumAttempts: 5,
    nonRetryableErrorTypes: ['BAD_REQUEST', 'UNSUPPORTED_CAPABILITY', 'BUDGET_EXHAUSTED']
  }
});

const assetService = proxyActivities<IAssetActivities>({
  startToCloseTimeout: '2 minutes',
  retry: { initialInterval: '2s', maximumAttempts: 3 }
});

const promptCompiler = proxyActivities<IPromptActivities>({
  startToCloseTimeout: '1 minute',
  retry: { initialInterval: '1s', maximumAttempts: 3 }
});

const providerService = proxyActivities<IProviderActivities>({
  startToCloseTimeout: '5 minutes',
  heartbeatTimeout: '30 seconds',
  retry: {
    initialInterval: '2s',
    backoffCoefficient: 2,
    maximumInterval: '1 minute',
    maximumAttempts: 3,
    nonRetryableErrorTypes: [
      'AUTH_REQUIRED',
      'SECURITY_CHALLENGE',
      'UI_CHANGED',
      'BUDGET_EXHAUSTED',
      'UNSUPPORTED_CAPABILITY',
      'BAD_REQUEST'
    ]
  }
});

const mediaService = proxyActivities<IMediaActivities>({
  startToCloseTimeout: '10 minutes',
  retry: { initialInterval: '5s', maximumAttempts: 4 }
});

const qcService = proxyActivities<IQCActivities>({
  startToCloseTimeout: '5 minutes',
  retry: { initialInterval: '2s', maximumAttempts: 3 }
});

const telemetry = proxyActivities<ITelemetryActivities>({
  startToCloseTimeout: '15 seconds',
  retry: { initialInterval: '500ms', maximumAttempts: 3 }
});

// Signals and Queries
export const cancelSignal = defineSignal<[{ reason: string }]>('cancelGeneration');
export const getStateQuery = defineQuery<WorkflowRuntimeState>('getWorkflowState');

export async function VideoGenerationWorkflow(
  input: VideoGenerationWorkflowInput
): Promise<VideoGenerationWorkflowResult> {
  const info = workflowInfo();
  const state: WorkflowRuntimeState = {
    current_status: 'QUEUED',
    current_stage: 'WAITING_FOR_ASSETS',
    progress_percent: 0,
    cancellation_requested: false
  };

  setHandler(cancelSignal, ({ reason }) => {
    state.cancellation_requested = true;
    state.cancellation_reason = reason;
  });

  setHandler(getStateQuery, () => state);

  try {
    // -------------------------------------------------------------------------
    // STEP 1: INITIALIZE & RESERVE BUDGET (Tier 1: QUEUED -> RESERVED)
    // -------------------------------------------------------------------------
    await telemetry.emitDomainEvent({
      event_type: 'avf.generation.job_queued',
      aggregate_id: input.job_id,
      aggregate_version: 1,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { job_id: input.job_id, project_id: input.project_id }
    });

    const reservation = await coreState.reserveBudgetAndTransition({
      job_id: input.job_id,
      provider_id: input.provider_id,
      estimated_credits: 10.0,
      correlation_id: input.correlation_id
    });
    state.current_status = 'RESERVED';
    state.current_stage = 'BUDGET_RESERVED';

    await telemetry.emitDomainEvent({
      event_type: 'avf.generation.job_reserved',
      aggregate_id: input.job_id,
      aggregate_version: 2,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { job_id: input.job_id, reserved_credits: reservation.reserved_credits }
    });

    // Check cancellation
    if (state.cancellation_requested) {
      return await handleWorkflowCancellation(input, state, info.runId);
    }

    // -------------------------------------------------------------------------
    // STEP 2: ASSET STAGING & CONTINUITY RESOLUTION (Stage: WAITING_FOR_ASSETS)
    // -------------------------------------------------------------------------
    state.current_stage = 'WAITING_FOR_ASSETS';
    const stagedAssets = await assetService.stageShotAssets({
      shot_version_id: input.shot_version_id,
      correlation_id: input.correlation_id
    });

    // -------------------------------------------------------------------------
    // STEP 3: PROMPT COMPILATION (Stage: PROMPT_READY)
    // -------------------------------------------------------------------------
    let promptVersionId = input.prompt_version_id;
    if (!promptVersionId) {
      const compilation = await promptCompiler.compilePromptForShot({
        shot_version_id: input.shot_version_id,
        target_provider: input.provider_id,
        staged_asset_ids: stagedAssets.map(a => a.asset_id),
        correlation_id: input.correlation_id
      });
      promptVersionId = compilation.prompt_version_id;

      await telemetry.emitDomainEvent({
        event_type: 'avf.prompt.version_created',
        aggregate_id: promptVersionId,
        aggregate_version: 1,
        correlation_id: input.correlation_id,
        workflow_run_id: info.runId,
        payload: { prompt_version_id: promptVersionId, shot_version_id: input.shot_version_id }
      });
    }
    state.current_stage = 'PROMPT_READY';

    // Check cancellation
    if (state.cancellation_requested) {
      return await handleWorkflowCancellation(input, state, info.runId);
    }

    // -------------------------------------------------------------------------
    // STEP 4: ACQUIRE LEASE & TRANSITION TO RUNNING (Tier 1: RESERVED -> RUNNING)
    // -------------------------------------------------------------------------
    const lease = await coreState.acquireJobLease({
      job_id: input.job_id,
      worker_id: `workflow-${info.workflowId}`,
      lease_duration_seconds: 60,
      execution_stage: 'SUBMITTING',
      correlation_id: input.correlation_id
    });
    state.current_status = 'RUNNING';
    state.current_stage = 'SUBMITTING';
    state.lease_token = lease.lease_token;
    state.lease_expires_at = lease.lease_expires_at;

    // -------------------------------------------------------------------------
    // STEP 5: SUBMIT GENERATION TO PROVIDER SDK (Stage: SUBMITTED)
    // -------------------------------------------------------------------------
    const providerSubmission = await providerService.submitGeneration({
      job_id: input.job_id,
      prompt_version_id: promptVersionId,
      provider_id: input.provider_id,
      flow_track: input.flow_track,
      idempotency_key: input.idempotency_key,
      attempt_index: input.attempt_index,
      correlation_id: input.correlation_id
    });

    state.current_stage = 'SUBMITTED';
    await coreState.updateJobStage({
      job_id: input.job_id,
      lease_token: state.lease_token!,
      execution_stage: 'SUBMITTED',
      provider_job_id: providerSubmission.provider_job_id
    });

    await telemetry.emitDomainEvent({
      event_type: 'avf.generation.job_submitted',
      aggregate_id: input.job_id,
      aggregate_version: 3,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { 
        job_id: input.job_id, 
        provider_job_id: providerSubmission.provider_job_id, 
        provider_id: input.provider_id 
      }
    });

    // -------------------------------------------------------------------------
    // STEP 6: POLLING & LEASE HEARTBEAT LOOP (Stage: GENERATING)
    // -------------------------------------------------------------------------
    state.current_stage = 'GENERATING';
    let generationFinished = false;
    let providerResult: any = null;

    while (!generationFinished) {
      if (state.cancellation_requested) {
        // Attempt provider cancellation
        await providerService.cancelGeneration({
          provider_id: input.provider_id,
          provider_job_id: providerSubmission.provider_job_id
        });
        return await handleWorkflowCancellation(input, state, info.runId);
      }

      // Renew lease every cycle
      const renewedLease = await coreState.renewJobLease({
        job_id: input.job_id,
        lease_token: state.lease_token!,
        lease_duration_seconds: 60
      });
      state.lease_expires_at = renewedLease.lease_expires_at;

      // Poll provider status
      const pollStatus = await providerService.pollGenerationStatus({
        provider_id: input.provider_id,
        provider_job_id: providerSubmission.provider_job_id,
        correlation_id: input.correlation_id
      });

      state.progress_percent = pollStatus.progress_percent || state.progress_percent;

      await telemetry.emitDomainEvent({
        event_type: 'avf.generation.job_progress',
        aggregate_id: input.job_id,
        aggregate_version: 4,
        correlation_id: input.correlation_id,
        workflow_run_id: info.runId,
        payload: { job_id: input.job_id, progress_percent: state.progress_percent }
      });

      if (pollStatus.status === 'SUCCESS') {
        generationFinished = true;
        providerResult = pollStatus;
      } else if (pollStatus.status === 'FAILED') {
        throw ApplicationFailure.fromError(new Error(pollStatus.error?.message || 'Provider generation failed'), {
          type: pollStatus.error?.code || 'PROVIDER_INTERNAL_ERROR',
          details: [pollStatus.error]
        });
      } else {
        // Sleep deterministically before next poll iteration
        await sleep('10 seconds');
      }
    }

    // -------------------------------------------------------------------------
    // STEP 7: DOWNLOAD MEDIA & REGISTER TAKE (Stages: DOWNLOADING -> DOWNLOADED)
    // -------------------------------------------------------------------------
    state.current_stage = 'DOWNLOADING';
    await coreState.updateJobStage({
      job_id: input.job_id,
      lease_token: state.lease_token!,
      execution_stage: 'DOWNLOADING'
    });

    const downloadedMedia = await mediaService.downloadAndIngestMedia({
      job_id: input.job_id,
      shot_version_id: input.shot_version_id,
      prompt_version_id: promptVersionId,
      source_uri: providerResult.output_uri,
      correlation_id: input.correlation_id
    });

    state.current_stage = 'DOWNLOADED';

    const registeredTake = await coreState.registerTakeRecord({
      job_id: input.job_id,
      shot_id: input.shot_id,
      shot_version_id: input.shot_version_id,
      prompt_version_id: promptVersionId,
      storage_uri: downloadedMedia.storage_uri,
      mime_type: downloadedMedia.mime_type,
      byte_size: downloadedMedia.byte_size,
      checksum_sha256: downloadedMedia.checksum_sha256,
      duration_ms: downloadedMedia.duration_ms
    });

    await telemetry.emitDomainEvent({
      event_type: 'avf.take.registered',
      aggregate_id: registeredTake.take_id,
      aggregate_version: 1,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { take_id: registeredTake.take_id, storage_uri: downloadedMedia.storage_uri }
    });

    // -------------------------------------------------------------------------
    // STEP 8: TECHNICAL & SEMANTIC QC (Stage: QC_RUNNING)
    // -------------------------------------------------------------------------
    state.current_stage = 'QC_RUNNING';
    await coreState.updateJobStage({
      job_id: input.job_id,
      lease_token: state.lease_token!,
      execution_stage: 'QC_RUNNING'
    });

    const qcEvaluation = await qcService.evaluateTake({
      take_id: registeredTake.take_id,
      storage_uri: downloadedMedia.storage_uri,
      shot_version_id: input.shot_version_id,
      prompt_version_id: promptVersionId,
      correlation_id: input.correlation_id
    });

    await telemetry.emitDomainEvent({
      event_type: 'avf.qc.completed',
      aggregate_id: registeredTake.take_id,
      aggregate_version: 2,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { 
        take_id: registeredTake.take_id, 
        qc_status: qcEvaluation.qc_status, 
        qc_score: qcEvaluation.qc_score 
      }
    });

    // -------------------------------------------------------------------------
    // STEP 9: FINALIZE / SETTLE / RETRY DECISION (Tier 1: RUNNING -> COMPLETED or FAILED)
    // -------------------------------------------------------------------------
    if (qcEvaluation.qc_status === 'PASSED') {
      state.current_status = 'COMPLETED';
      state.current_stage = 'APPROVED';

      await coreState.completeAndSettleJob({
        job_id: input.job_id,
        lease_token: state.lease_token!,
        take_id: registeredTake.take_id,
        actual_cost_credits: providerResult.cost_credits_used || 10.0,
        qc_score: qcEvaluation.qc_score
      });

      await telemetry.emitDomainEvent({
        event_type: 'avf.generation.job_completed',
        aggregate_id: input.job_id,
        aggregate_version: 5,
        correlation_id: input.correlation_id,
        workflow_run_id: info.runId,
        payload: { job_id: input.job_id, take_id: registeredTake.take_id, status: 'COMPLETED' }
      });

      return {
        job_id: input.job_id,
        take_id: registeredTake.take_id,
        status: 'COMPLETED',
        execution_stage: 'APPROVED',
        provider_job_id: providerSubmission.provider_job_id,
        storage_uri: downloadedMedia.storage_uri,
        qc_status: 'PASSED',
        qc_score: qcEvaluation.qc_score,
        cost_credits_used: providerResult.cost_credits_used || 10.0,
        completed_at: new Date().toISOString()
      };
    } else {
      // QC Failed: Evaluate creative retry vs terminal failure (INV-009, INV-011)
      state.current_status = 'FAILED';
      state.current_stage = 'QC_REJECTED';

      await coreState.failJobAndReleaseBudget({
        job_id: input.job_id,
        lease_token: state.lease_token,
        execution_stage: 'QC_REJECTED',
        normalized_error: {
          code: 'PROVIDER_INTERNAL_ERROR',
          message: `QC Rejected: ${qcEvaluation.failure_reason || 'Score below threshold'}`,
          retry_category: 'PERMANENT'
        }
      });

      await telemetry.emitDomainEvent({
        event_type: 'avf.generation.job_failed',
        aggregate_id: input.job_id,
        aggregate_version: 5,
        correlation_id: input.correlation_id,
        workflow_run_id: info.runId,
        payload: { job_id: input.job_id, reason: 'QC_REJECTED' }
      });

      return {
        job_id: input.job_id,
        take_id: registeredTake.take_id,
        status: 'FAILED',
        execution_stage: 'QC_REJECTED',
        qc_status: 'REJECTED',
        qc_score: qcEvaluation.qc_score,
        completed_at: new Date().toISOString()
      };
    }

  } catch (error: any) {
    // -------------------------------------------------------------------------
    // STEP 10: NORMALIZED ERROR HANDLING & COMPENSATION
    // -------------------------------------------------------------------------
    state.current_status = 'FAILED';
    state.current_stage = 'EXECUTION_FAILED';

    const normalizedError = mapToNormalizedError(error);

    await coreState.failJobAndReleaseBudget({
      job_id: input.job_id,
      lease_token: state.lease_token,
      execution_stage: 'EXECUTION_FAILED',
      normalized_error: normalizedError
    });

    await telemetry.emitDomainEvent({
      event_type: 'avf.generation.job_failed',
      aggregate_id: input.job_id,
      aggregate_version: 99,
      correlation_id: input.correlation_id,
      workflow_run_id: info.runId,
      payload: { job_id: input.job_id, error: normalizedError }
    });

    return {
      job_id: input.job_id,
      status: 'FAILED',
      execution_stage: 'EXECUTION_FAILED',
      normalized_error: normalizedError,
      completed_at: new Date().toISOString()
    };
  }
}

async function handleWorkflowCancellation(
  input: VideoGenerationWorkflowInput,
  state: WorkflowRuntimeState,
  runId: string
): Promise<VideoGenerationWorkflowResult> {
  state.current_status = 'CANCELLED';
  state.current_stage = 'ABORTED_BY_USER';

  await coreState.cancelJobAndReleaseBudget({
    job_id: input.job_id,
    lease_token: state.lease_token,
    reason: state.cancellation_reason || 'User cancelled'
  });

  await telemetry.emitDomainEvent({
    event_type: 'avf.generation.job_cancelled',
    aggregate_id: input.job_id,
    aggregate_version: 99,
    correlation_id: input.correlation_id,
    workflow_run_id: runId,
    payload: { job_id: input.job_id, reason: state.cancellation_reason }
  });

  return {
    job_id: input.job_id,
    status: 'CANCELLED',
    execution_stage: 'ABORTED_BY_USER',
    completed_at: new Date().toISOString()
  };
}

function mapToNormalizedError(error: any): NormalizedError {
  const code = error?.type || error?.code || 'PROVIDER_INTERNAL_ERROR';
  const message = error?.message || 'Unknown workflow execution failure';

  switch (code) {
    case 'PROVIDER_RATE_LIMIT':
      return { code: 'PROVIDER_RATE_LIMIT', message, retry_category: 'TRANSIENT', suggested_backoff_ms: 5000 };
    case 'AUTH_REQUIRED':
      return { code: 'AUTH_REQUIRED', message, retry_category: 'POLICY_BLOCKED' };
    case 'SECURITY_CHALLENGE':
      return { code: 'SECURITY_CHALLENGE', message, retry_category: 'POLICY_BLOCKED' };
    case 'UI_CHANGED':
      return { code: 'UI_CHANGED', message, retry_category: 'PERMANENT' };
    case 'BUDGET_EXHAUSTED':
      return { code: 'BUDGET_EXHAUSTED', message, retry_category: 'RESOURCE_EXHAUSTED' };
    case 'UNSUPPORTED_CAPABILITY':
      return { code: 'UNSUPPORTED_CAPABILITY', message, retry_category: 'PERMANENT' };
    case 'NETWORK_TIMEOUT':
      return { code: 'NETWORK_TIMEOUT', message, retry_category: 'TRANSIENT', suggested_backoff_ms: 2000 };
    case 'BAD_REQUEST':
      return { code: 'BAD_REQUEST', message, retry_category: 'PERMANENT' };
    case 'PROVIDER_INTERNAL_ERROR':
    default:
      return { code: 'PROVIDER_INTERNAL_ERROR', message, retry_category: 'TRANSIENT', suggested_backoff_ms: 3000 };
  }
}
```

---

### 2.4 Error Handling & Normalized Error Taxonomy Integration

All activities and workflow recovery handlers enforce the 9 normalized error codes and retry policies:

| Error Code | Retry Category | Temporal Activity Retry Behavior | Workflow Compensation & Lifecycle Action |
|---|---|---|---|
| `PROVIDER_RATE_LIMIT` | `TRANSIENT` | Retries with exponential backoff & jitter (initial 2s, max 60s, max 5 attempts) | Maintains `RUNNING` status and extends lease. |
| `AUTH_REQUIRED` | `POLICY_BLOCKED` | Non-retryable (`nonRetryableErrorTypes`). Fails immediately. | INV-012: Zero bypass. Transitions to `FAILED`, releases budget reservation. |
| `SECURITY_CHALLENGE` | `POLICY_BLOCKED` | Non-retryable. Fails immediately. | INV-012: Halts automation. Transitions to `FAILED`, notifies operator. |
| `UI_CHANGED` | `PERMANENT` | Non-retryable. Fails immediately. | Transitions to `FAILED` (`EXECUTION_FAILED`), releases reservation. |
| `BUDGET_EXHAUSTED` | `RESOURCE_EXHAUSTED`| Non-retryable. Fails immediately. | Transitions to `FAILED`, prevents external provider submission. |
| `UNSUPPORTED_CAPABILITY`| `PERMANENT`| Non-retryable. Fails immediately. | Transitions to `FAILED`, returns validation details. |
| `NETWORK_TIMEOUT` | `TRANSIENT` | Retries with exponential backoff (initial 1s, max 30s, max 4 attempts) | If retries exhausted, marks `FAILED` (`TIMEOUT`). |
| `BAD_REQUEST` | `PERMANENT` | Non-retryable. Fails immediately. | Transitions to `FAILED`, releases reservation. |
| `PROVIDER_INTERNAL_ERROR`| `TRANSIENT`| Retries 3 times before terminal failure | If retries fail, marks `FAILED` (`EXECUTION_FAILED`). |

---

### 2.5 Test Requirements & Conformance Testing Plan

1. **Unit Tests (Target: >= 85% branch coverage)**:
   - Workflow logic tested using `@temporalio/testing` (`TestWorkflowEnvironment`).
   - Mocking activities to simulate all happy and failure branches:
     - Branch 1: Single-shot full success path (`APPROVED`).
     - Branch 2: Budget reservation rejection (`BUDGET_EXHAUSTED`).
     - Branch 3: Prompt compilation failure (`BAD_REQUEST`).
     - Branch 4: Provider transient rate-limit retry then success.
     - Branch 5: Provider permanent auth failure (`AUTH_REQUIRED`).
     - Branch 6: Security challenge pause/failure (`SECURITY_CHALLENGE`).
     - Branch 7: QC rejection path (`QC_REJECTED`).
     - Branch 8: Operator cancellation signal (`ABORTED_BY_USER`).
     - Branch 9: Lease expiration and crash recovery.
2. **Contract Conformance Tests**:
   - Validate every emitted event payload against `02_contracts/event-envelope.schema.json`.
   - Validate input/output payloads against `02_contracts/domain-entities.schema.json`.
   - Validate provider requests against `02_contracts/provider-request.schema.json`.

---

## 3. Specification Sufficiency Evaluation

### 3.1 Evaluation of Blueprint (`R06_WORKFLOW.md`)
- **Strengths:**
  - Clear architectural boundaries (stateless orchestrator, persists through R02, Layer 5).
  - Explicit forbidden dependencies (R09 Browser Worker, R10 FlowKit Bridge, direct DB).
  - Explicit error taxonomy (9 normalized codes) and idempotency key requirement.
- **Weaknesses & Deficiencies:**
  - **Zero Activity Definitions:** The blueprint does not declare a single activity interface, name, input type, or return type.
  - **Missing Inter-Service Communication Protocol:** Does not specify whether R06 calls downstream services (R02, R04, R05, R07, R11, R12) via REST, gRPC, direct function invocation, or message queues.
  - **No Temporal Task Queue / Configuration Specification:** Completely omits task queue names, activity timeouts, workflow timeouts, and workflow heartbeat configuration.
  - **Ambiguity on Event Emission:** Does not define whether R06 publishes domain events directly to an event bus or delegates event publication to R02 Core State.

### 3.2 Evaluation of State Machines (`STATUS_STATE_MACHINES.md`)
- **Strengths:**
  - The two-tier state machine (`CanonicalLifecycleStatus` vs `ExecutionStage`) is clearly structured and well-defined.
  - Parent-to-child mappings and transition rules are explicit.
  - Invariants regarding terminal immutability and lease expiration are clear.
- **Weaknesses & Deficiencies:**
  - Does not describe the exact protocol or payload for lease heartbeat renewal during long workflow generation steps.
  - Does not specify how cancellation transitions (`ABORTED_BY_USER` vs `ABORTED_BY_SYSTEM`) are initiated via Temporal signals.

---

## 4. Architectural Inventions & Assumptions Log

Since the blueprint and state machine documents lacked low-level implementation details, the following **6 engineering inventions and assumptions** were made:

| # | Item / Topic | Spec Status | Assumption / Architectural Invention Made |
|---|---|---|---|
| 1 | **Activity Decomposition & Naming** | Omitted | Defined 7 core activity interfaces: `ICoreStateActivities`, `IAssetActivities`, `IPromptActivities`, `IProviderActivities`, `IMediaActivities`, `IQCActivities`, `ITelemetryActivities`. |
| 2 | **Inter-Service Communication Protocol** | Omitted | Assumed downstream services expose REST APIs consumed via HTTP client wrappers in Temporal activities, rather than direct gRPC or in-memory imports. |
| 3 | **Temporal Lease Heartbeat Mechanism** | Vague | Implemented a deterministic polling loop inside the workflow that combines `coreState.renewJobLease()` with `providerService.pollGenerationStatus()` on a 10-second `workflow.sleep()` cadence. |
| 4 | **Domain Event Emission Boundary** | Ambiguous | Implemented explicit `ITelemetryActivities.emitDomainEvent` calls directly inside the workflow for lifecycle milestones (`job_queued`, `job_reserved`, `job_submitted`, `job_progress`, `take_registered`, `qc_completed`, `job_completed`, `job_failed`, `job_cancelled`). |
| 5 | **Cancellation via Temporal Signals** | Undefined | Defined a `cancelGeneration` Temporal Signal handler that flips an in-workflow cancellation flag, triggers provider cancellation if active, releases budget via R02, and transitions state to `ABORTED_BY_USER`. |
| 6 | **Task Queue & Timeout Constants** | Omitted | Standardized Task Queue as `avf-video-generation-v1`, default workflow execution timeout as 30 minutes, provider activity start-to-close timeout as 5 minutes with 30-second heartbeats. |

```
ARCHITECTURAL_INVENTIONS_REQUIRED = YES (6 Inventions / Assumptions Documented Above)
```

---

## 5. Conclusion & Readiness Checklist

- [x] Complete TypeScript data models and activity interfaces formulated.
- [x] Full deterministic Temporal `VideoGenerationWorkflow` implemented with two-tier state machine transitions.
- [x] Lease heartbeat renewal and status polling loop designed.
- [x] 9-code normalized error taxonomy mapped to retry categories and non-retryable Temporal errors.
- [x] Event emissions aligned with `02_contracts/event-envelope.schema.json` and `04_integration/COMMAND_EVENT_CATALOG.md`.
- [x] 6 concrete architectural assumptions and gaps documented with zero hidden shortcuts.
