# DOMAIN OWNER ARCHITECTURAL REVIEW & AUTHORITATIVE VERDICT
## Cluster 02: GenerationJob Lifecycle & Two-Tier State Machine

**DOMAIN_OWNER:** R02 (Reliability Specialist)  
**AFFILIATION:** AI Video Factory Architecture Council — C02R Genuine Adversarial Cross-Examination  
**TARGET_SPEC_VERSION:** v1.0.0 Freeze Candidate  
**DOCUMENT_STATUS:** AUTHORITATIVE_VERDICT  
**DATE:** 2026-08-15  
**CORRESPONDING_FINDINGS:** FINDING_002, FINDING_019, FINDING_044, TECH-005  
**TARGET_FILE:** `review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW/CLUSTER_02_DOMAIN_OWNER_R02.md`

---

## 1. Executive Summary & Domain Authority Statement

As the Reliability Specialist and designated Domain Owner for **Cluster 02 (GenerationJob Lifecycle & Two-Tier State Machine)**, I have conducted an exhaustive, rigorous evaluation of the architectural defense submitted by Proponent **R02 (Reliability Specialist)** in [`CLUSTER_02_PROPONENT_R02.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW/CLUSTER_02_PROPONENT_R02.md) and the deep structural critique submitted by Challenger **R03 (Workflow Specialist)** in [`CLUSTER_02_CHALLENGER_R03.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW/CLUSTER_02_CHALLENGER_R03.md).

In a high-throughput, distributed AI video production factory, state machine design is not merely a classification problem—it is the bedrock of system determinism, financial integrity, error isolation, and operational safety. Early specification revisions suffered from severe architectural deficiencies:
1. An irreconcilable contradiction between the coarse 6-state status enum in `domain-entities.schema.json` and the 12 procedural steps listed in `STATUS_STATE_MACHINES.md`.
2. Undefined boundaries between transactional PostgreSQL domain records (`avf-core-state`) and durable orchestrator histories (`avf-workflow` / Temporal).
3. The lack of execution-level fencing for third-party browser and API workers, creating zombie worker execution races and double-spend billing leaks.
4. Coarse error modeling that conflated evaluator infrastructure failures (e.g., CUDA OOM) with creative quality rejections, poisoning upstream prompt compiler feedback loops.

This document delivers the definitive Domain Owner adjudication. I confirm the adoption of the **Hierarchical Two-Tier State Machine Architecture**, uphold the critical distributed systems remediations raised by Challenger R03, specify the exact mathematical mapping matrix and PostgreSQL DDL, and establish binding implementation directives for the v1.0.0 freeze candidate.

---

## 2. Tier 1 (PostgreSQL Domain Core) vs Tier 2 (Execution Stage Telemetry)

### 2.1 The Two-Tier Architectural Model

The AI Video Factory enforces a strict separation of concerns between **Durable Business Truth** and **Transient Operational Orchestration**:

```
+---------------------------------------------------------------------------------------------------+
| TIER 1: CANONICAL LIFECYCLE STATUS (PostgreSQL / avf-core-state)                                 |
| Owned by: avf-core-state | Storage: generation_jobs.status | 7 Coarse States                     |
| Invariant: Transactional, billing-authoritative, immutable terminal sinks, indexed for analytics  |
+---------------------------------------------------------------------------------------------------+
       ▲                                                                                     ▲
       │                                                                                     │
   (Surjective                                                                           (Surjective
    Projection)                                                                           Projection)
       │                                                                                     │
+---------------------------------------------------------------------------------------------------+
| TIER 2: EXECUTION STAGE TELEMETRY (Temporal Activities / Event Bus / Operator UI)                 |
| Emitted by: avf-workflow, avf-browser-worker, avf-qc | Stored: generation_jobs.execution_stage   |
| 11 Canonical Stages (17 Sub-states across all operational & terminal phases)                     |
| Invariant: Monotonically forward within RUNNING, activity-retryable, telemetry streaming          |
+---------------------------------------------------------------------------------------------------+
```

### 2.2 Tier 1: The 7 Canonical Database Lifecycle States

The PostgreSQL database in `avf-core-state` is the sole transactional authority for business state. The `status` column of table `generation_jobs` uses a strict 7-state type:

```sql
CREATE TYPE canonical_lifecycle_status AS ENUM (
    'QUEUED',
    'RESERVED',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'CANCELLED',
    'RECONCILED'
);
```

#### State Invariants & Operational Boundaries:
1. **`QUEUED` (Non-Terminal Initial State):**
   - **Domain Meaning:** The `GenerationJob` has been canonically registered, bound to immutable `ShotVersion` and `PromptVersion` IDs.
   - **System Invariants:** No worker lease is assigned; no financial budget reservation or GPU capacity slot is locked. Upstream asset ingests may still be completing.
   - **Valid Outgoing Transitions:** $\to$ `RESERVED`, `CANCELLED`, `FAILED`.

2. **`RESERVED` (Non-Terminal Budget Hold):**
   - **Domain Meaning:** Two-phase credit reservation has succeeded in `avf-core-state` budget ledger (`estimated_cost_credits` locked). Concurrency rate limits have allocated an execution token.
   - **System Invariants:** Satisfies System Invariant 18: No external provider dispatch is permitted without an active reservation lock.
   - **Valid Outgoing Transitions:** $\to$ `RUNNING`, `CANCELLED`, `FAILED`.

3. **`RUNNING` (Active Execution State):**
   - **Domain Meaning:** The job is actively executing across the distributed pipeline (prompt compilation, provider dispatch, browser automation, media streaming, or QC validation).
   - **System Invariants:** Must hold an active worker lease (`lease_token`, `lease_expires_at`). The worker must continuously heartbeat. Internal activity retries (e.g. download retry, CDN refresh) occur *within* this state without mutating Tier 1.
   - **Valid Outgoing Transitions:** $\to$ `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`.

4. **`COMPLETED` (Terminal Absorbing Sink):**
   - **Domain Meaning:** The video has been rendered by provider, downloaded, verified for bitwise integrity (SHA-256), passed automated QC acceptance criteria, and registered as a canonical `Take`.
   - **System Invariants:** Absolutely immutable. Reserved budget is settled to `actual_cost_credits`.
   - **Valid Outgoing Transitions:** None ($\emptyset$).

5. **`FAILED` (Terminal Absorbing Sink):**
   - **Domain Meaning:** The job suffered a fatal, non-retryable provider error, unrecoverable workflow abort, or hard QC rejection exceeding the shot retry budget.
   - **System Invariants:** Must record a structured `normalized_error` payload with an explicit `error_domain`. Financial settlement is processed (refunded if unspent, settled if provider billed).
   - **Valid Outgoing Transitions:** None ($\emptyset$).

6. **`CANCELLED` (Terminal Absorbing Sink):**
   - **Domain Meaning:** An explicit operator command (via `R13_OPERATOR_CONSOLE`) or system supervisor shutdown terminated the job prior to completion.
   - **System Invariants:** Active worker leases are revoked; budget hold is refunded. Cancellation metadata (`cancelled_by`, `cancellation_reason`, `cancelled_at`) is persisted.
   - **Valid Outgoing Transitions:** None ($\emptyset$).

7. **`RECONCILED` (Terminal Recovery Settlement):**
   - **Domain Meaning:** The job experienced a worker crash, network partition, or lease timeout during an ambiguous external operation (e.g. during `SUBMITTING`), and the Reconciliation Engine has completed a post-mortem audit.
   - **System Invariants:** Resolves the distributed split. If provider generated media, it is imported (`RECONCILED_SUCCESS`); if the provider task is dead/nonexistent, resources are refunded (`RECONCILED_TERMINAL`).
   - **Valid Outgoing Transitions:** None ($\emptyset$).

---

### 2.3 Tier 2: The Canonical Execution Stages

While `CanonicalLifecycleStatus` governs durable business and financial state, orchestrators (Temporal / `avf-workflow`), browser workers (`avf-browser-worker`), and QC engines (`avf-qc`) progress through granular execution stages.

The schema formalizes 11 core execution stages, spanning 17 exact sub-states across preparation, execution, and terminal resolution:

```sql
CREATE TYPE execution_stage AS ENUM (
    -- Preparation & Reservation
    'WAITING_FOR_ASSETS',
    'PROMPT_READY',
    'BUDGET_RESERVED',
    
    -- Active Execution Progression
    'SUBMITTING',
    'SUBMITTED',
    'GENERATING',
    'DOWNLOADING',
    'DOWNLOADED',
    'QC_RUNNING',
    
    -- Success Terminal
    'APPROVED',
    
    -- Failure Terminals
    'EXECUTION_FAILED',
    'QC_REJECTED',
    'TIMEOUT',
    
    -- Cancellation Terminals
    'ABORTED_BY_USER',
    'ABORTED_BY_SYSTEM',
    
    -- Reconciliation Terminals
    'RECONCILED_SUCCESS',
    'RECONCILED_TERMINAL'
);
```

---

## 3. Deterministic State Mapping Matrix & Split-Brain Prevention

### 3.1 Formal Surjective Mapping Definition

To mathematically eliminate split-brain states (such as `status = COMPLETED` while `execution_stage = SUBMITTING`), the architecture defines a formal surjective mapping function:

$$\mathcal{M}: \text{ExecutionStage} \longrightarrow \text{CanonicalLifecycleStatus}$$

Every execution stage maps to exactly one canonical lifecycle status.

### 3.2 Authoritative Parent-Child Mapping Matrix

| Tier 1 Status (`status`) | Tier 2 Permitted Stages (`execution_stage`) | Operational Phase | Concurrency & Resource Invariant |
|---|---|---|---|
| **`QUEUED`** | `WAITING_FOR_ASSETS`<br>`PROMPT_READY` | Ingestion & Compilation | No worker lease. No credit reservation. AST hash verified. |
| **`RESERVED`** | `BUDGET_RESERVED` | Two-Phase Ledger Lock | Credit hold locked in `cost_usage_records`. Concurrency slot claimed. |
| **`RUNNING`** | `SUBMITTING`<br>`SUBMITTED`<br>`GENERATING`<br>`DOWNLOADING`<br>`DOWNLOADED`<br>`QC_RUNNING` | Active Distributed Execution | Valid `lease_token` required. Active heartbeat ($T \le 30\text{s}$). Stage progression is monotonic within `RUNNING`. Transient activity failures retry internally. |
| **`COMPLETED`** | `APPROVED` | Success Settlement | `Take` entity registered; SHA-256 verified; budget settled from reserved to actual. |
| **`FAILED`** | `EXECUTION_FAILED`<br>`QC_REJECTED`<br>`TIMEOUT` | Failure Settlement | Mandatory `normalized_error` with `error_domain`. Worker lease released. Financial two-phase settlement executed. |
| **`CANCELLED`** | `ABORTED_BY_USER`<br>`ABORTED_BY_SYSTEM` | Explicit Abort | Worker lease revoked. Temporal workflow signaled. Cancellation audit log created. |
| **`RECONCILED`** | `RECONCILED_SUCCESS`<br>`RECONCILED_TERMINAL` | Post-Mortem Settlement | Lease expired ($T > 90\text{s}$). Emitted exclusively by Reconciliation Engine. |

### 3.3 Multi-Layer Enforcement Architecture

Split-brain states are prevented through four distinct defensive layers:

```
[Layer 1: Contract Schema] --> JSON Schema allOf conditional validation in domain-entities.schema.json
          │
          ▼
[Layer 2: API Ingress]     --> avf-core-state validates STAGE_TO_STATUS_MAP[stage] === status (422 Unprocessable)
          │
          ▼
[Layer 3: DB Constraint]   --> PostgreSQL hard CHECK constraint (chk_status_stage_consistency)
          │
          ▼
[Layer 4: Outbox Telemetry]--> Monotonic sequence_no & vector clocks on JobStageChanged events
```

---

## 4. Resolution of Challenger (R03) Attack Vectors

Challenger R03 presented three profound attack vectors targeting distributed failure modes. Below is the domain owner evaluation and technical resolution for each:

```
+---------------------------------------------------------------------------------------------------+
| SUMMARY OF CHALLENGER R03 ATTACKS & DOMAIN OWNER RESOLUTIONS                                      |
+---------------------------------------------------------------------------------------------------+
| 1. Dual-Write Split-Brain: PostgreSQL vs Temporal Activity Partial Failures                       |
|    --> RESOLVED via Idempotent RPCs, Entity Version Fencing, and Outbox Sequence Numbers.          |
+---------------------------------------------------------------------------------------------------+
| 2. Zombie Worker & Double-Billing: Lease Expiration during Provider Submission                    |
|    --> RESOLVED via Local Pre-Execution Fencing (5s safety margin) & Bi-Directional Signaling.    |
+---------------------------------------------------------------------------------------------------+
| 3. Pipeline Error Provenance Erasure: Downloader Glitches & Evaluator Crashes                      |
|    --> RESOLVED via Internal Activity Retries, Discriminated error_domain, and Two-Phase Billing.  |
+---------------------------------------------------------------------------------------------------+
```

---

### 4.1 Resolution of Attack Vector 1: Dual-Write Asynchrony & Event Ordering

#### Challenger Critique:
1. If a worker commits a DB update (`entity_version = 4`) and then crashes before acknowledging Temporal, Temporal retries with `entity_version = 3`, hitting an unhandled `409 Conflict` and stalling the workflow.
2. If an operator cancels a job via REST API while a browser worker is running, the browser worker finishes 4 minutes later, generating media that gets dropped and billed without a `Take` record.
3. Outbox event re-ordering can cause the Operator Console to display regressions (e.g., `DOWNLOADING` $\to$ `SUBMITTING`).

#### Domain Owner Adjudication & Defense:
1. **Idempotent Stage Transition RPCs:**
   - `avf-core-state` state transition endpoints MUST accept the `idempotency_key` and current `workflow_activity_id`.
   - If an update is received where `expected_version < current_version`, but the request's target `execution_stage` matches the already committed `execution_stage` for this activity, `avf-core-state` returns HTTP `200 OK` with the current entity state rather than throwing a `409 Conflict`.
2. **Outbox Telemetry Monotonic Sequencing:**
   - Every `JobStageChanged` event published from the outbox table includes an incrementing `sequence_no` (derived from PostgreSQL `entity_version`) and a `transition_timestamp`.
   - The Operator Console (`R13_OPERATOR_CONSOLE`) discards any received WebSocket event where `incoming.sequence_no <= last_seen.sequence_no`, mathematically preventing UI regressions from out-of-order message delivery.

---

### 4.2 Resolution of Attack Vector 2: Zombie Worker Leases & Distributed Fencing

#### Challenger Critique:
PostgreSQL row leases protect only DB writes. If Worker A stalls (e.g. during large asset hashing), misses heartbeats, and its lease expires, Worker B takes over the job. Worker A then wakes up and clicks "Generate" on Google Flow, causing double generation, double billing ($0.50 + $0.50), and quota exhaustion.

```
CHALLENGER SCENARIO: The Unfenced Zombie Browser Worker
Worker A (Stalled)  ═══════════════════════════════════════► Clicks "Generate" (Costs $0.50) [ZOMBIE!]
PostgreSQL Lease    ──[Lease Expires]──► Worker B Claims Lease ──► Clicks "Generate" (Costs $0.50)
```

#### Domain Owner Adjudication & Mandatory Remediations:
To convert the database lease from a passive *write-fence* into an active *execution-fence*, the following two distributed controls are mandatory:

#### 1. Local Pre-Execution Fencing (Client-Side Guard):
In `R09_BROWSER_WORKER` and `R07_PROVIDER_SDK`, every worker maintains an in-memory `local_lease_expires_at` timer updated by its background heartbeat thread (15s interval).
Before executing any non-idempotent external action (e.g. clicking "Generate", submitting a multipart form, or calling a third-party paid REST endpoint), the worker MUST execute a synchronous local pre-condition check:

$$\text{NOW}() < \text{local\_lease\_expires\_at} - \Delta_{\text{safety}} \quad (\text{where } \Delta_{\text{safety}} = 5000\text{ms})$$

If the heartbeat failed or the lease is within 5 seconds of expiration, the worker immediately cancels the browser action, closes the browser context, and aborts locally without emitting external network traffic.

#### 2. Bi-Directional Temporal Reconciliation Signaling:
When the `avf-core-state` Lease Reaper detects an expired lease (`lease_expires_at < NOW()`) and assigns the job to a Reconciliation Worker:
1. The Reaper immediately sends a `SignalWorkflowExecution` (`SignalName: "LeaseRevokedSignal"`, payload: `{ "job_id": UUID, "revoked_lease_token": UUID, "reason": "HEARTBEAT_TIMEOUT" }`) directly to the Temporal workflow execution handle.
2. The running Temporal workflow intercepts `LeaseRevokedSignal`, immediately issues a cancel context to all running child activities, and yields execution to the `ReconciliationWorkflow`.
3. This guarantees that stalled activities are cancelled inside Temporal before any takeover worker is dispatched.

---

### 4.3 Resolution of Attack Vector 3: Pipeline Failure Provenance & Activity Retries

#### Challenger Critique:
1. Downloader TCP reset at 90% in `DOWNLOADING` stage transitions the entire `GenerationJob` to terminal `FAILED`. This forces a brand new `GenerationJob` attempt, triggering full prompt re-compilation and re-paying $1.20 to the provider for a video that was already rendered successfully.
2. Evaluator CUDA OOM in `QC_RUNNING` is categorized as `QC_REJECTED`, causing the creative feedback loop to modify valid prompts due to an infrastructure glitch.

```
THE FLAW: Downstream Ingestion Glitch Forcing Upstream Re-Generation
Provider Render (SUCCESS, $1.20) ──► Download TCP Drop ──► Mark Job FAILED ──► Rerun Shot (Billed $1.20 AGAIN!)
```

#### Domain Owner Adjudication & Mandatory Remediations:

#### 1. Decoupling Activity Retries from Job Lifecycle Status:
- `DOWNLOADING` and `QC_RUNNING` are **downstream pipeline activities** within the `RUNNING` canonical lifecycle status.
- A transient transport network failure (TCP reset, CDN 403, S3 timeout) MUST NOT immediately transition `GenerationJob` to `FAILED`.
- Temporal activity retry policies govern `DownloadMediaActivity`:
  - The worker retries the download up to 5 times with exponential backoff against the existing `provider_job_id` / `cdn_url`.
  - If the CDN URL expires, a dedicated `RefreshDownloadUrlActivity` is invoked against the provider API before any failure escalation.
- Only if the provider reports that the rendered asset has been purged from remote storage does the job fail with `error_domain = INGEST_TRANSPORT`.

#### 2. Strict Error Domain Discrimination in `NormalizedError`:
To prevent infrastructure crashes from poisoning creative prompt compilation, `NormalizedError` MUST include a mandatory, typed `error_domain` discriminator:

```json
{
  "error_domain": {
    "type": "string",
    "enum": [
      "PROVIDER_EXECUTION",
      "INGEST_TRANSPORT",
      "QC_EVALUATOR_INFRASTRUCTURE",
      "QC_SEMANTIC_REJECTION",
      "ORCHESTRATION_LEASE"
    ]
  }
}
```

#### Architectural Invariants on Error Handling:
- **Rule 1 (Prompt Integrity):** `R05_PROMPT_COMPILER` and creative retry policies MUST inspect `error_domain`. If `error_domain` $\in$ {`INGEST_TRANSPORT`, `QC_EVALUATOR_INFRASTRUCTURE`, `ORCHESTRATION_LEASE`}, prompt compilation AST and parameters MUST NOT be modified. The prompt is valid; only infrastructure failed.
- **Rule 2 (Take Preservation):** If an evaluator crashes during `QC_RUNNING` with `QC_EVALUATOR_INFRASTRUCTURE`, the candidate `Take` record and its downloaded media binary remain intact in storage with `qc_status = 'PENDING'`. The QC activity is simply rescheduled on an available GPU worker.
- **Rule 3 (Two-Phase Financial Ledger Settlement):** If a job terminates with `error_domain = INGEST_TRANSPORT` or `QC_EVALUATOR_INFRASTRUCTURE` after the provider confirmed completion, `actual_cost_credits` MUST be committed to `cost_usage_records`. The external GPU cost is finalized on the ledger, preventing vendor billing drift.

---

## 5. Authoritative PostgreSQL 15+ Schema Specification

The complete, production-grade PostgreSQL DDL for `avf-core-state` is specified below:

```sql
-- =============================================================================
-- AVF CORE STATE: GENERATION JOB & STATE MACHINE DDL
-- Author: R02 Reliability Specialist (Domain Owner)
-- Version: 1.0.0 Freeze Candidate
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- 1. Canonical Lifecycle Types
CREATE TYPE canonical_lifecycle_status AS ENUM (
    'QUEUED',
    'RESERVED',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'CANCELLED',
    'RECONCILED'
);

CREATE TYPE execution_stage AS ENUM (
    'WAITING_FOR_ASSETS',
    'PROMPT_READY',
    'BUDGET_RESERVED',
    'SUBMITTING',
    'SUBMITTED',
    'GENERATING',
    'DOWNLOADING',
    'DOWNLOADED',
    'QC_RUNNING',
    'APPROVED',
    'EXECUTION_FAILED',
    'QC_REJECTED',
    'TIMEOUT',
    'ABORTED_BY_USER',
    'ABORTED_BY_SYSTEM',
    'RECONCILED_SUCCESS',
    'RECONCILED_TERMINAL'
);

CREATE TYPE error_domain AS ENUM (
    'PROVIDER_EXECUTION',
    'INGEST_TRANSPORT',
    'QC_EVALUATOR_INFRASTRUCTURE',
    'QC_SEMANTIC_REJECTION',
    'ORCHESTRATION_LEASE'
);

-- 2. Generation Jobs Table
CREATE TABLE generation_jobs (
    generation_job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    prompt_version_id UUID NOT NULL,
    provider_id VARCHAR(64) NOT NULL,
    flow_track VARCHAR(32) NOT NULL DEFAULT 'TRACK_A', -- 'TRACK_A', 'TRACK_B', 'DIRECT_API'
    attempt_no INTEGER NOT NULL DEFAULT 1,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    
    -- Two-Tier State Model
    status canonical_lifecycle_status NOT NULL DEFAULT 'QUEUED',
    execution_stage execution_stage NOT NULL DEFAULT 'WAITING_FOR_ASSETS',
    
    -- Provider Handles
    provider_job_id VARCHAR(256) NULL,
    browser_session_id UUID NULL,
    
    -- Distributed Lease & Fencing
    lease_token UUID NULL,
    lease_expires_at TIMESTAMPTZ NULL,
    heartbeat_sequence BIGINT NOT NULL DEFAULT 0,
    
    -- Financial Ledger Tracking
    estimated_cost_credits NUMERIC(10, 4) NOT NULL DEFAULT 0.0000,
    actual_cost_credits NUMERIC(10, 4) NULL,
    
    -- Error Domain & Normalized Payload
    error_domain error_domain NULL,
    normalized_error JSONB NULL,
    
    -- Timestamps & Concurrency Control
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMPTZ NULL,
    completed_at TIMESTAMPTZ NULL,
    entity_version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT ck_generation_jobs_attempt CHECK (attempt_no >= 1 AND attempt_no <= max_attempts),
    CONSTRAINT ck_generation_jobs_flow_track CHECK (flow_track IN ('TRACK_A', 'TRACK_B', 'DIRECT_API')),
    CONSTRAINT chk_status_stage_consistency CHECK (
        (status = 'QUEUED' AND execution_stage IN ('WAITING_FOR_ASSETS', 'PROMPT_READY')) OR
        (status = 'RESERVED' AND execution_stage IN ('BUDGET_RESERVED')) OR
        (status = 'RUNNING' AND execution_stage IN ('SUBMITTING', 'SUBMITTED', 'GENERATING', 'DOWNLOADING', 'DOWNLOADED', 'QC_RUNNING')) OR
        (status = 'COMPLETED' AND execution_stage IN ('APPROVED')) OR
        (status = 'FAILED' AND execution_stage IN ('EXECUTION_FAILED', 'QC_REJECTED', 'TIMEOUT')) OR
        (status = 'CANCELLED' AND execution_stage IN ('ABORTED_BY_USER', 'ABORTED_BY_SYSTEM')) OR
        (status = 'RECONCILED' AND execution_stage IN ('RECONCILED_SUCCESS', 'RECONCILED_TERMINAL'))
    ),
    CONSTRAINT chk_lease_integrity CHECK (
        (status = 'RUNNING' AND lease_token IS NOT NULL AND lease_expires_at IS NOT NULL) OR
        (status != 'RUNNING')
    ),
    CONSTRAINT chk_terminal_error CHECK (
        (status = 'FAILED' AND normalized_error IS NOT NULL AND error_domain IS NOT NULL) OR
        (status != 'FAILED')
    )
);

-- 3. High-Performance Indexing
CREATE INDEX idx_gen_jobs_lookup ON generation_jobs (shot_id, attempt_no);
CREATE INDEX idx_gen_jobs_status_fast ON generation_jobs (status) WHERE status IN ('QUEUED', 'RESERVED', 'RUNNING');
CREATE INDEX idx_gen_jobs_lease_reaper ON generation_jobs (status, lease_expires_at) WHERE status = 'RUNNING';
CREATE INDEX idx_gen_jobs_provider ON generation_jobs (provider_id, provider_job_id);

-- 4. Cost Usage Records (Financial Audit Ledger)
CREATE TABLE cost_usage_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    generation_job_id UUID NOT NULL REFERENCES generation_jobs(generation_job_id) ON DELETE RESTRICT,
    project_id UUID NOT NULL,
    provider_id VARCHAR(64) NOT NULL,
    reservation_amount NUMERIC(10, 4) NOT NULL,
    settled_amount NUMERIC(10, 4) NULL,
    is_refunded BOOLEAN NOT NULL DEFAULT FALSE,
    settled_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cost_record_job UNIQUE (generation_job_id)
);
```

---

### 5.1 Atomic Concurrency Queries in `avf-core-state`

#### Atomic Lease Acquisition & Transition to RUNNING:
```sql
UPDATE generation_jobs
SET 
    status = 'RUNNING',
    execution_stage = 'SUBMITTING',
    lease_token = $new_lease_token,
    lease_expires_at = NOW() + INTERVAL '45 seconds',
    heartbeat_sequence = 1,
    entity_version = entity_version + 1,
    updated_at = NOW()
WHERE 
    generation_job_id = $job_id
    AND status = 'RESERVED'
    AND entity_version = $expected_version;
```

#### Atomic Heartbeat Renewal:
```sql
UPDATE generation_jobs
SET 
    lease_expires_at = NOW() + INTERVAL '45 seconds',
    heartbeat_sequence = heartbeat_sequence + 1,
    updated_at = NOW()
WHERE 
    generation_job_id = $job_id
    AND lease_token = $active_lease_token
    AND status = 'RUNNING';
```

#### Atomic Intermediate Stage Progression (Within RUNNING):
```sql
UPDATE generation_jobs
SET 
    execution_stage = $new_stage,
    provider_job_id = COALESCE($provider_job_id, provider_job_id),
    submitted_at = CASE WHEN $new_stage = 'SUBMITTED' AND submitted_at IS NULL THEN NOW() ELSE submitted_at END,
    entity_version = entity_version + 1,
    updated_at = NOW()
WHERE 
    generation_job_id = $job_id
    AND lease_token = $active_lease_token
    AND status = 'RUNNING'
    AND entity_version = $expected_version;
```

#### Atomic Terminal Transition (Immutability Enforced):
```sql
UPDATE generation_jobs
SET 
    status = $terminal_status, -- 'COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED'
    execution_stage = $terminal_stage,
    lease_token = NULL,
    lease_expires_at = NULL,
    actual_cost_credits = $actual_cost,
    error_domain = $error_domain,
    normalized_error = $normalized_error,
    completed_at = NOW(),
    entity_version = entity_version + 1,
    updated_at = NOW()
WHERE 
    generation_job_id = $job_id
    AND entity_version = $expected_version
    AND status NOT IN ('COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED');
```

---

## 6. Contract Specifications in JSON Schema

To guarantee cross-repository protocol conformance, `avf-contracts/domain-entities.schema.json` must be updated with the following definitions:

```json
{
  "$defs": {
    "CanonicalLifecycleStatus": {
      "type": "string",
      "enum": [
        "QUEUED",
        "RESERVED",
        "RUNNING",
        "COMPLETED",
        "FAILED",
        "CANCELLED",
        "RECONCILED"
      ]
    },
    "ExecutionStage": {
      "type": "string",
      "enum": [
        "WAITING_FOR_ASSETS",
        "PROMPT_READY",
        "BUDGET_RESERVED",
        "SUBMITTING",
        "SUBMITTED",
        "GENERATING",
        "DOWNLOADING",
        "DOWNLOADED",
        "QC_RUNNING",
        "APPROVED",
        "EXECUTION_FAILED",
        "QC_REJECTED",
        "TIMEOUT",
        "ABORTED_BY_USER",
        "ABORTED_BY_SYSTEM",
        "RECONCILED_SUCCESS",
        "RECONCILED_TERMINAL"
      ]
    },
    "ErrorDomain": {
      "type": "string",
      "enum": [
        "PROVIDER_EXECUTION",
        "INGEST_TRANSPORT",
        "QC_EVALUATOR_INFRASTRUCTURE",
        "QC_SEMANTIC_REJECTION",
        "ORCHESTRATION_LEASE"
      ]
    },
    "NormalizedError": {
      "type": "object",
      "required": [
        "error_domain",
        "error_code",
        "message",
        "retryable",
        "timestamp"
      ],
      "properties": {
        "error_domain": {
          "$ref": "#/$defs/ErrorDomain"
        },
        "error_code": {
          "type": "string"
        },
        "message": {
          "type": "string"
        },
        "retryable": {
          "type": "boolean"
        },
        "http_status": {
          "type": ["integer", "null"]
        },
        "provider_raw_code": {
          "type": ["string", "null"]
        },
        "timestamp": {
          "type": "string",
          "format": "date-time"
        }
      },
      "additionalProperties": false
    },
    "GenerationJob": {
      "type": "object",
      "required": [
        "generation_job_id",
        "project_id",
        "shot_id",
        "shot_version_id",
        "prompt_version_id",
        "provider_id",
        "flow_track",
        "attempt_no",
        "idempotency_key",
        "status",
        "execution_stage",
        "entity_version",
        "created_at",
        "updated_at"
      ],
      "properties": {
        "generation_job_id": { "type": "string", "format": "uuid" },
        "project_id": { "type": "string", "format": "uuid" },
        "shot_id": { "type": "string", "format": "uuid" },
        "shot_version_id": { "type": "string", "format": "uuid" },
        "prompt_version_id": { "type": "string", "format": "uuid" },
        "provider_id": { "type": "string" },
        "flow_track": { "type": "string", "enum": ["TRACK_A", "TRACK_B", "DIRECT_API"] },
        "attempt_no": { "type": "integer", "minimum": 1 },
        "max_attempts": { "type": "integer", "minimum": 1 },
        "idempotency_key": { "type": "string" },
        "status": { "$ref": "#/$defs/CanonicalLifecycleStatus" },
        "execution_stage": { "$ref": "#/$defs/ExecutionStage" },
        "provider_job_id": { "type": ["string", "null"] },
        "lease_token": { "type": ["string", "null"], "format": "uuid" },
        "lease_expires_at": { "type": ["string", "null"], "format": "date-time" },
        "estimated_cost_credits": { "type": "number", "minimum": 0 },
        "actual_cost_credits": { "type": ["number", "null"], "minimum": 0 },
        "error_domain": { "type": ["string", "null"], "enum": ["PROVIDER_EXECUTION", "INGEST_TRANSPORT", "QC_EVALUATOR_INFRASTRUCTURE", "QC_SEMANTIC_REJECTION", "ORCHESTRATION_LEASE"] },
        "normalized_error": { "type": ["object", "null"], "$ref": "#/$defs/NormalizedError" },
        "entity_version": { "type": "integer", "minimum": 1 },
        "requested_at": { "type": "string", "format": "date-time" },
        "submitted_at": { "type": ["string", "null"], "format": "date-time" },
        "completed_at": { "type": ["string", "null"], "format": "date-time" },
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" }
      },
      "allOf": [
        {
          "if": { "properties": { "status": { "const": "QUEUED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["WAITING_FOR_ASSETS", "PROMPT_READY"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "RESERVED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["BUDGET_RESERVED"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "RUNNING" } } },
          "then": { "properties": { "execution_stage": { "enum": ["SUBMITTING", "SUBMITTED", "GENERATING", "DOWNLOADING", "DOWNLOADED", "QC_RUNNING"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "COMPLETED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["APPROVED"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "FAILED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["EXECUTION_FAILED", "QC_REJECTED", "TIMEOUT"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "CANCELLED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["ABORTED_BY_USER", "ABORTED_BY_SYSTEM"] } } }
        },
        {
          "if": { "properties": { "status": { "const": "RECONCILED" } } },
          "then": { "properties": { "execution_stage": { "enum": ["RECONCILED_SUCCESS", "RECONCILED_TERMINAL"] } } }
        }
      ]
    }
  }
}
```

---

## 7. Exhaustive Evaluation of Challenger Arguments & Defenses

| Challenger Critique (R03) | Domain Owner Evaluation | Technical Remediations Applied |
|---|---|---|
| **1. Dual-Write Asynchrony Stalls Workflows on Activity Re-dispatch** | **UPHELD & REMEDIATED.** When Temporal re-dispatches an activity whose DB write previously succeeded, strict version checks throw false 409s. | `avf-core-state` state update endpoints now accept `workflow_activity_id` and return idempotent `200 OK` if the requested stage already matches current stage. |
| **2. Out-of-Order Outbox Telemetry Causes UI Regressions** | **UPHELD & REMEDIATED.** Asynchronous event workers can deliver `JobStageChanged` events out of sequence to the dashboard. | All `JobStageChanged` events carry a monotonic `sequence_no` (equal to `entity_version`). `R13_OPERATOR_CONSOLE` discards stale sequence events. |
| **3. Stalled Workers Cause Zombie Double-Spend Submissions** | **UPHELD & REMEDIATED.** Database lease heartbeats are write-fences, not execution-fences. Stalled browser workers can wake up and click "Generate" after lease expiration. | Mandated Local Pre-Execution Fencing ($\text{NOW}() < \text{lease\_expires\_at} - 5\text{s}$) in `R09`/`R07` and Bi-directional `LeaseRevokedSignal` to Temporal from the Lease Reaper. |
| **4. Ingestion Network Glitch Forces Expensive Re-generation** | **UPHELD & REMEDIATED.** Failing the job during `DOWNLOADING` forces a new attempt, throwing away successful provider renders. | Decoupled activity retries from Job status. Transient download network drops retry internally up to 5 times (including CDN URL refresh) without failing the `GenerationJob`. |
| **5. Evaluator Infrastructure Crashes Poison Creative Prompt Compiler** | **UPHELD & REMEDIATED.** Generic `FAILED` states cause `R05_PROMPT_COMPILER` to rewrite valid prompts when an evaluator runs out of VRAM. | Introduced typed `error_domain`. `R05` mutates prompts ONLY on `error_domain = QC_SEMANTIC_REJECTION`. For infrastructure failures, the media Take is preserved and QC re-evaluated. |
| **6. Partial Pipeline Failures Leak Financial Costs** | **UPHELD & REMEDIATED.** If a job fails during `DOWNLOADING`, budget reservation was released without billing the rendered GPU cost. | Two-Phase Financial Settlement commits `actual_cost_credits` whenever external provider generation has occurred, regardless of downstream ingestion outcome. |

---

## 8. Formal Domain Owner Verdict & Binding Directives

### 8.1 Authoritative Verdict
**STATUS: CONFIRMED_WITH_RELIABILITY_DIRECTIVES**  
The Hierarchical Two-Tier State Machine Architecture is formally approved for the v1.0.0 Spec Freeze. The incorporation of Local Pre-Execution Fencing, Discriminated Error Domains, Idempotent Activity Stage Transitions, and Two-Phase Settlement resolves all distributed systems failure modes identified in C02R.

### 8.2 Binding Implementation Directives for C03R / C04R

1. **Directive to R01 (`avf-contracts`):**
   - Update `STATUS_STATE_MACHINES.md` to reflect the exact 7-state CanonicalLifecycleStatus and 11-stage ExecutionStage matrix.
   - Update `domain-entities.schema.json` with the complete `$defs/GenerationJob`, `$defs/CanonicalLifecycleStatus`, `$defs/ExecutionStage`, and `$defs/NormalizedError` schemas defined in §6.

2. **Directive to R02 (`avf-core-state`):**
   - Implement the PostgreSQL DDL, check constraints (`chk_status_stage_consistency`, `chk_lease_integrity`, `chk_terminal_error`), and partial indexes specified in §5.
   - Implement idempotent stage update handlers returning `200 OK` for matching activity re-dispatches.
   - Deploy the background Lease Reaper running every 15 seconds to detect expired leases and emit `LeaseRevokedSignal`.

3. **Directive to R06 (`avf-workflow`):**
   - Configure activity retry policies for `DownloadMediaActivity` and `RunQCEvaluationActivity` (5 retries with backoff) to prevent premature `GenerationJob` failures.
   - Implement handlers for `LeaseRevokedSignal` in workflow definitions to immediately terminate cancelled child activities.

4. **Directive to R07 (`avf-provider-sdk`) & R09 (`avf-browser-worker`):**
   - Implement Local Pre-Execution Fencing: synchronously verify $\text{NOW}() < \text{local\_lease\_expires\_at} - 5000\text{ms}$ before executing any non-idempotent provider request or browser UI click.

5. **Directive to R11 (`avf-qc`):**
   - Tag all execution exceptions with structured `error_domain` (`QC_EVALUATOR_INFRASTRUCTURE` vs `QC_SEMANTIC_REJECTION`).
   - Preserve candidate `Take` media in storage when infrastructure crashes occur.

6. **Directive to R13 (`avf-operator-console`):**
   - Implement sequence-checked event consumption for WebSocket progress updates to eliminate out-of-order stage regressions.

---
**DOMAIN OWNER SIGN-OFF:**  
*R02 — Lead Reliability Specialist, AI Video Factory Architecture Council*  
*Timestamp: 2026-08-15T21:35:00Z*
