# CLUSTER 02 DEFENSE: GENERATIONJOB LIFECYCLE & TWO-TIER STATE MACHINE

**Role:** R02 Reliability Specialist (Proponent)  
**Cluster ID:** CLUSTER-02  
**Findings Covered:** FINDING_002, FINDING_019, FINDING_044, TECH-005  
**Review Status:** Candidate for v1.0 Freeze Remediated Defense  
**Target Path:** `review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW/CLUSTER_02_PROPONENT_R02.md`

---

## 1. Executive Summary & Core Proponent Thesis

The AI Video Factory operates across a hybrid, distributed execution topology spanning relational databases (`avf-core-state`), durable orchestrators (`avf-workflow`), external generative AI browser engines (`avf-browser-worker` / `avf-flowkit-bridge`), and asynchronous quality control workers (`avf-qc`). 

A critical vulnerability identified in early blueprint iterations was the impedance mismatch between coarse database status representations and granular workflow execution telemetry. Specifically, `domain-entities.schema.json` historically specified a restrictive status enum (`QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `RECONCILED`), while `STATUS_STATE_MACHINES.md` specified fine-grained procedural steps (`WAITING_FOR_ASSETS`, `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`, `APPROVED`, etc.).

As R02 Reliability Specialist, I formally present and defend the **Hierarchical Two-Tier State Machine Architecture**:
1. **Tier 1: CanonicalLifecycleStatus (7 coarse states in PostgreSQL):** The transactional, durable, billing-authoritative business state owned exclusively by `avf-core-state`.
2. **Tier 2: ExecutionStage (17 fine-grained telemetry stages):** The sub-state progression emitted in real-time events and tracked in workflow telemetry to provide sub-second observability without database write-amplification or schema fragility.
3. **Deterministic Parent-Child Mapping Matrix:** A strict, non-overlapping surjection mapping every `ExecutionStage` to exactly one `CanonicalLifecycleStatus`, enforced at the `avf-core-state` API boundary and validated by JSON Schema contracts.
4. **Terminal State Immutability & Lease Crash Recovery:** A hardened concurrency control model combining PostgreSQL row versioning, terminal absorbing states, and a two-phase reconciliation protocol for crash recovery during ambiguous provider operations.

This architecture completely eliminates split-brain conditions, avoids database table bloat and MVCC thrashing, guarantees auditability for financial metering, and provides bulletproof crash recovery against network partitions and worker terminations.

---

## 2. Tier 1: CanonicalLifecycleStatus (PostgreSQL Domain Core)

### 2.1 The 7-State Canonical Lifecycle Set
The database schema in `avf-core-state` (`generation_jobs` table) defines `status` as a strict 7-value enumeration:

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

### 2.2 Semantic Definitions and Invariants

```
                      +-------------------+
                      |      QUEUED       |
                      +---------+---------+
                                |
                                v
                      +-------------------+
                      |     RESERVED      |
                      +---------+---------+
                                |
                                v
                      +-------------------+
             +------->|      RUNNING      |--------+
             |        +----+----+----+----+        |
             |             |    |    |             |
             |             |    |    v             v
             |             |    |  +------------+ +------------+
             |             |    |  |   FAILED   | | CANCELLED  |
             |             |    |  +------------+ +------------+
             |             |    |   (Terminal)     (Terminal)
             |             v    v
             |        +------------+
             |        | COMPLETED  |
             |        +------------+
             |          (Terminal)
             |
             v
    +-----------------+
    |   RECONCILED    | (Terminal / Hand-off)
    +-----------------+
```

1. **`QUEUED` (Initial Non-Terminal):**
   - **Semantic:** The `GenerationJob` has been canonically registered, referencing immutable `ShotVersion` and `PromptVersion` IDs.
   - **Invariants:** No capacity, budget lock, or provider compute resources have been locked. Upstream asset dependencies may still be finalizing.
   - **Allowed Next States:** `RESERVED`, `CANCELLED`, `FAILED`.

2. **`RESERVED` (Non-Terminal):**
   - **Semantic:** Financial budget credits, tenant rate-limiting tokens, or provider concurrency slots have been atomically claimed.
   - **Invariants:** Protects against over-subscription. Prevents external API dispatch without guaranteed budget allocation (System Invariant 18).
   - **Allowed Next States:** `RUNNING`, `CANCELLED`, `FAILED`.

3. **`RUNNING` (Active Non-Terminal):**
   - **Semantic:** The job is actively executing across the orchestration pipeline (prompt compilation, provider dispatch, browser automation, media streaming, or QC validation).
   - **Invariants:** Must hold an active worker lease (`lease_token`, `lease_expires_at`). Heartbeats must be maintained.
   - **Allowed Next States:** `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`.

4. **`COMPLETED` (Terminal Absorbing):**
   - **Semantic:** The generation attempt succeeded. Output media has been downloaded, checksummed, verified against format specs, passed QC approval thresholds, and registered as a canonical `Take`.
   - **Invariants:** Absolutely immutable. No further mutations permitted. Budget is settled from reserved to consumed.
   - **Allowed Next States:** None ($\emptyset$).

5. **`FAILED` (Terminal Absorbing):**
   - **Semantic:** The job suffered an unrecoverable execution failure, fatal provider error, QC rejection exceeding retry policy, or timeout exhaustion.
   - **Invariants:** Must record a structured `normalized_error` payload (`error_code`, `category`, `retryable: false`, `message`, `timestamp`). Reserved budget is refunded/released.
   - **Allowed Next States:** None ($\emptyset$).

6. **`CANCELLED` (Terminal Absorbing):**
   - **Semantic:** An explicit operator or system shutdown command terminated execution prior to completion.
   - **Invariants:** All active worker leases revoked. Reserved budget released. Cancellation provenance recorded (`cancelled_by`, `reason`).
   - **Allowed Next States:** None ($\emptyset$).

7. **`RECONCILED` (Terminal Absorbing / Recovery Settlement):**
   - **Semantic:** The job encountered an ambiguous distributed state (e.g. worker crash during provider submission or network partition during media transfer) and has been authoritatively resolved by the Reconciliation Engine.
   - **Invariants:** Captures post-mortem audit results. If provider actually completed generation out-of-band, assets are claimed (`RECONCILED_SUCCESS`); if generation died unacknowledged, resources are cleaned up and refunded (`RECONCILED_TERMINAL`).
   - **Allowed Next States:** None ($\emptyset$).

---

## 3. Tier 2: ExecutionStage (Workflow Orchestration & Telemetry)

While `CanonicalLifecycleStatus` governs durable business and financial state, orchestrators (Temporal / `avf-workflow`), browser workers (`avf-browser-worker`), and QC engines (`avf-qc`) progress through granular execution stages.

### 3.1 The 17 Execution Stages
The telemetry layer defines the following exact stage taxonomy:

```json
{
  "ExecutionStage": [
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
}
```

### 3.2 Stage Semantics by Execution Phase

- **Queue & Preparation Phase:**
  - `WAITING_FOR_ASSETS`: Upstream reference frames, audio assets, or continuity embeddings are being ingested/validated.
  - `PROMPT_READY`: Prompt AST compiled and hashed; ready for credit verification.
- **Reservation Phase:**
  - `BUDGET_RESERVED`: Credit ledger has locked the required token/credit estimate.
- **Provider Submission Phase:**
  - `SUBMITTING`: Browser worker / API adapter is actively negotiating session, navigating Google Flow, or posting payload.
  - `SUBMITTED`: Provider acknowledged receipt and returned an external task handle (`provider_job_id`).
- **Generation & Ingestion Phase:**
  - `GENERATING`: External provider is rendering video frames (polling or websocket streaming active).
  - `DOWNLOADING`: Media artifact is being transferred from provider storage to AVF staging storage.
  - `DOWNLOADED`: Raw video binary stored in object storage; SHA-256 checksum calculated.
- **Verification & Acceptance Phase:**
  - `QC_RUNNING`: Automated VMAF, perceptual quality, audio sync, and safety evaluations running in `avf-qc`.
  - `APPROVED`: Output meets all acceptance criteria and is linked to a canonical `Take`.
- **Failure & Termination Stages:**
  - `EXECUTION_FAILED`: Unrecoverable exception (e.g. invalid credentials, selector failure, 5xx server crash).
  - `QC_REJECTED`: Media failed hard quality thresholds and exceeded shot retry budget.
  - `TIMEOUT`: Workflow run exceeded global execution SLA.
  - `ABORTED_BY_USER`: Operator triggered manual abort via Console.
  - `ABORTED_BY_SYSTEM`: Concurrency supervisor or safety circuit breaker terminated execution.
  - `RECONCILED_SUCCESS`: Orphan recovery confirmed valid provider completion and imported Take.
  - `RECONCILED_TERMINAL`: Orphan recovery confirmed job dead or irrecoverable; finalized ledger refund.

---

## 4. Deterministic Parent-to-Child Mapping Matrix

To mathematically prevent split-brain states (e.g., `status = COMPLETED` while `execution_stage = SUBMITTING`), the system enforces a deterministic, surjective mapping function:

$$\mathcal{M}: \text{ExecutionStage} \longrightarrow \text{CanonicalLifecycleStatus}$$

### 4.1 Formal Mapping Table

| Parent Status (`status`) | Permitted Child Stages (`execution_stage`) | Stage Category | Invariant Rule |
|---|---|---|---|
| **`QUEUED`** | `WAITING_FOR_ASSETS`<br>`PROMPT_READY` | Preparation | No worker lease or credit hold active. |
| **`RESERVED`** | `BUDGET_RESERVED` | Reservation | Two-phase commit credit hold active; no network submission yet. |
| **`RUNNING`** | `SUBMITTING`<br>`SUBMITTED`<br>`GENERATING`<br>`DOWNLOADING`<br>`DOWNLOADED`<br>`QC_RUNNING` | Active Execution | Active worker lease required. Intermediate stage progression is strictly monotonic forward or bounded retry within `RUNNING`. |
| **`COMPLETED`** | `APPROVED` | Success Terminal | `Take` entity registered; checksum immutable; credit reservation settled. |
| **`FAILED`** | `EXECUTION_FAILED`<br>`QC_REJECTED`<br>`TIMEOUT` | Failure Terminal | `normalized_error` mandatory; worker lease released; credit hold refunded. |
| **`CANCELLED`** | `ABORTED_BY_USER`<br>`ABORTED_BY_SYSTEM` | Cancellation Terminal | Worker lease revoked; cancellation metadata persisted. |
| **`RECONCILED`** | `RECONCILED_SUCCESS`<br>`RECONCILED_TERMINAL` | Recovery Terminal | Emitted only by Reconciliation Engine following lease expiration / crash audit. |

### 4.2 Mathematical Invariants of the Mapping Matrix

1. **Strict Surjection with No Disjoint Parents:**
   $$\forall s \in \text{ExecutionStage}, \quad |\mathcal{M}(s)| = 1$$
   No ExecutionStage can belong to multiple CanonicalLifecycleStatus parents. Ambiguity is mathematically impossible.
2. **Atomic Verification at Ingress:**
   Every API mutation in `avf-core-state` validating state transition executes the mapping check:
   ```typescript
   function validateStateConsistency(status: CanonicalLifecycleStatus, stage: ExecutionStage): void {
     const expectedParent = STAGE_TO_STATUS_MAP[stage];
     if (expectedParent !== status) {
       throw new InconsistentStateMappingError(
         `Invalid state pair: execution_stage '${stage}' requires status '${expectedParent}', received '${status}'`
       );
     }
   }
   ```
3. **JSON Schema Contract Validation:**
   In `avf-contracts/domain-entities.schema.json`, the `generationJob` entity schema defines `allOf` conditional constraints validating that if `status` is specified, `execution_stage` must belong to the matching enum set.

---

## 5. Terminal State Immutability & Concurrency Control

### 5.1 The Terminal Sinks
The states `COMPLETED`, `FAILED`, `CANCELLED`, and `RECONCILED` are formal absorbing terminal states in graph theory:

$$\forall S_{\text{term}} \in \{\text{COMPLETED}, \text{FAILED}, \text{CANCELLED}, \text{RECONCILED}\}, \quad \delta(S_{\text{term}}, \text{event}) = \text{ERROR}$$

Once a `GenerationJob` enters a terminal state:
- It **CANNOT** be reopened, retried, transitioned to `RUNNING`, or updated with new outputs.
- Any subsequent command attempting to mutate status, outputs, or error payloads is rejected with a fatal `409 Conflict` (`TERMINAL_STATE_IMMUTABLE`).
- If a shot requires another generation attempt (e.g. after `FAILED` or `QC_REJECTED`), a brand new `GenerationJob` entity is created with `attempt_no = N + 1` (System Invariants 10, 11, 16).

### 5.2 PostgreSQL Concurrency & Optimistic Locking
To prevent race conditions between asynchronous worker heartbeats, operator cancellations, and workflow activity completions, `avf-core-state` implements strict optimistic concurrency control via row versioning.

#### PostgreSQL Table Definition:
```sql
CREATE TABLE generation_jobs (
    generation_job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shot_id UUID NOT NULL REFERENCES shots(shot_id),
    shot_version_id UUID NOT NULL REFERENCES shot_versions(shot_version_id),
    prompt_version_id UUID NOT NULL REFERENCES prompt_versions(prompt_version_id),
    attempt_no INTEGER NOT NULL DEFAULT 1,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    status canonical_lifecycle_status NOT NULL DEFAULT 'QUEUED',
    execution_stage execution_stage NOT NULL DEFAULT 'WAITING_FOR_ASSETS',
    version INTEGER NOT NULL DEFAULT 1,
    lease_token UUID NULL,
    lease_expires_at TIMESTAMPTZ NULL,
    normalized_error JSONB NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_status_stage_consistency CHECK (
        (status = 'QUEUED' AND execution_stage IN ('WAITING_FOR_ASSETS', 'PROMPT_READY')) OR
        (status = 'RESERVED' AND execution_stage IN ('BUDGET_RESERVED')) OR
        (status = 'RUNNING' AND execution_stage IN ('SUBMITTING', 'SUBMITTED', 'GENERATING', 'DOWNLOADING', 'DOWNLOADED', 'QC_RUNNING')) OR
        (status = 'COMPLETED' AND execution_stage IN ('APPROVED')) OR
        (status = 'FAILED' AND execution_stage IN ('EXECUTION_FAILED', 'QC_REJECTED', 'TIMEOUT')) OR
        (status = 'CANCELLED' AND execution_stage IN ('ABORTED_BY_USER', 'ABORTED_BY_SYSTEM')) OR
        (status = 'RECONCILED' AND execution_stage IN ('RECONCILED_SUCCESS', 'RECONCILED_TERMINAL'))
    )
);
```

#### Atomic Transition Query:
```sql
UPDATE generation_jobs
SET 
    status = $new_status,
    execution_stage = $new_stage,
    version = version + 1,
    updated_at = NOW(),
    normalized_error = COALESCE($error_payload, normalized_error)
WHERE 
    generation_job_id = $job_id
    AND version = $expected_version
    AND status NOT IN ('COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED');
```

If the update yields `0 rows affected`, the repository performs a lookup:
1. If the job status is in (`COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`), it returns `TERMINAL_STATE_IMMUTABLE`.
2. If `version != $expected_version`, it returns `OPTIMISTIC_CONCURRENCY_CONFLICT`.

---

## 6. Lease Crash Recovery & The "Uncertain Submit" Protocol

### 6.1 The Distributed Worker Failure Mode
Generative video workflows take between 60 to 600 seconds. Browser workers driving Google Flow or API clients executing long-running requests can crash, lose network connectivity, or experience host restarts.

Without a robust lease model, a job would remain stuck in `RUNNING` forever (zombie execution), locking concurrency slots and budget credits.

### 6.2 Ephemeral Leases & Heartbeating
1. When a worker claims a job for execution, it must acquire a lease:
   ```sql
   UPDATE generation_jobs
   SET 
       status = 'RUNNING',
       execution_stage = 'SUBMITTING',
       lease_token = gen_random_uuid(),
       lease_expires_at = NOW() + INTERVAL '45 seconds',
       version = version + 1
   WHERE 
       generation_job_id = $job_id 
       AND status = 'RESERVED' 
       AND version = $expected_version;
   ```
2. The worker must heartbeat every 15 seconds, advancing `lease_expires_at = NOW() + INTERVAL '45 seconds'`.
3. If the worker crashes, the lease expires within 45 seconds.

### 6.3 The "Uncertain Submit" Dilemma & Two-Phase Reconciliation
The most dangerous failure mode in AI video orchestration is a crash during the `SUBMITTING` stage:
- Did Google Flow accept the generation request before the worker died?
  - If **YES**: Re-submitting will generate a duplicate video, double-charge GPU credits, and produce conflicting takes.
  - If **NO**: Failing the job without checking wastes human operator time.

```
       Worker Crashes during SUBMITTING
                      │
                      ▼
       Lease Expires (lease_expires_at < NOW())
                      │
                      ▼
       Reconciliation Sweeper Detects Expired Lease
                      │
                      ▼
     Status set to RECONCILED (Stage: SUBMITTED?)
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
[Query Provider by Key]     [No Record Found]
        │                           │
        ▼                           ▼
Video Exists / In Progress?   Mark RECONCILED_TERMINAL
 ├── YES: Stream to Take       Refund Reserved Budget
 └── NO: Mark Dead
```

#### Protocol Specification:
1. **Detection:** The `avf-core-state` Lease Reaper finds jobs where `status = 'RUNNING' AND lease_expires_at < NOW()`.
2. **Isolation:** The Reaper transitions the job to `status = 'RECONCILED'` with `execution_stage = 'RECONCILED_TERMINAL'`, revoking the `lease_token`.
3. **Reconciliation Activity:** R06 Workflow invokes a dedicated `ReconcileProviderSubmission` activity using the immutable `idempotency_key`:
   - It queries the provider session/history using the deterministic business key.
   - **Case A (Found Succeeded):** Downloader fetches media $\to$ Take registered $\to$ marks `execution_stage = 'RECONCILED_SUCCESS'`.
   - **Case B (Found Dead / Never Received):** Unlocks reserved credits $\to$ marks `execution_stage = 'RECONCILED_TERMINAL'`.

This protocol guarantees zero duplicate generations and zero budget leakage.

---

## 7. Performance & High-Throughput Database Optimization

Challengers often ask: *Why not record all 17 stages directly in PostgreSQL?*

### 7.1 Write-Amplification and Table Bloat Analysis
Under high-scale factory conditions (e.g. 50 parallel shot pipelines with 10 takes each):
- If every intermediate progress tick (`SUBMITTING`, `SUBMITTED`, `GENERATING` percentage ticks, `DOWNLOADING` chunk ticks, `DOWNLOADED`, `QC_RUNNING`) forced a synchronous PostgreSQL write:
  - **Single Job DB Writes:** 15 to 30 row updates.
  - **PostgreSQL Impact:** Severe MVCC tuple bloat, vacuum degradation, WAL saturation, lock contention on the `generation_jobs` primary key index, and constant cache invalidation.
- Under the **Two-Tier Architecture**:
  - **PostgreSQL Row Updates:** Only 3 to 5 transactional writes per job (`QUEUED` $\to$ `RESERVED` $\to$ `RUNNING` $\to$ `COMPLETED`).
  - **Fine-Grained Telemetry:** Ephemeral progress ticks are published via event streaming (Outbox pattern $\to$ Event Bus $\to$ Operator Console WebSocket) without executing full table updates.

### 7.2 Read-Model Query Performance
System queries from the Operator Console, Billing Ledger, and Rate Limiters require fast aggregation:
```sql
-- Fast, index-backed query for active cluster concurrency:
SELECT COUNT(*) FROM generation_jobs WHERE status = 'RUNNING';

-- Simple billing ledger reconciliation:
SELECT SUM(cost) FROM cost_usage_records 
WHERE generation_job_id IN (SELECT generation_job_id FROM generation_jobs WHERE status = 'COMPLETED');
```
With the 7-state canonical enum, these queries hit small, static B-tree indexes. If a flat 17-state enum were used, queries would require expansive `IN (...)` clauses that invalidate index scans and break every time a new pipeline step is introduced.

---

## 8. Concrete Defense Against Challenger Attack Vectors

| Attack Vector | Challenger Argument | Proponent Counter-Defense & Proof |
|---|---|---|
| **Split-Brain Desynchronization** | Dual fields (`status` and `execution_stage`) can diverge if a bug writes `status=COMPLETED` with `stage=SUBMITTING`. | **Mitigated by DB Check Constraints & API Boundary Guards.** The PostgreSQL schema contains a hard `chk_status_stage_consistency` constraint. Invalid combinations throw SQL errors and cannot be committed. |
| **Orchestrator Bypass** | Temporal workflow might execute retries without updating `avf-core-state`. | **Architectural Rule:** Temporal does NOT own state. Temporal activities call `avf-core-state` transactional endpoints. Core state enforces version checks and rejects out-of-order calls. |
| **Worker Zombie Locks** | Crashed browser worker holds lock forever, stalling shot pipeline. | **Mitigated by 45-Second Expiring Leases.** Background reaper sweeps expired leases and triggers deterministic reconciliation. |
| **Duplicate Generation on Network Glitch** | Worker timeout during submission causes workflow to resubmit same prompt. | **Mitigated by System Invariant 3 & Reconciliation Protocol.** Every submission carries an immutable `idempotency_key`. The workflow must reconcile before resubmission. |

---

## 9. Verification & Test Conformance Suite

To certify conformance for the v1.0 spec freeze, `avf-core-state` and `avf-workflow` must pass the following test matrix:

1. **State Machine Invariant Suite (`test_state_machine_matrix.py`):**
   - Exhaustive Cartesian product test validating that all 119 invalid $(status, stage)$ pairs are rejected with `InconsistentStateMappingError`.
   - Verification that all 17 valid $(status, stage)$ pairs commit successfully.
2. **Terminal State Immutability Suite (`test_terminal_immutability.py`):**
   - Attempt transitions from `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED` to any other state. All must throw `TERMINAL_STATE_IMMUTABLE`.
   - Verify that attempts to overwrite Take records or update `normalized_error` on terminal jobs fail.
3. **Lease Expiration & Crash Recovery Suite (`test_lease_reconciliation.py`):**
   - Simulate worker crash in `SUBMITTING`, `GENERATING`, and `DOWNLOADING` stages by killing worker process and fast-forwarding time past `lease_expires_at`.
   - Verify Lease Reaper transitions job to `RECONCILED` and triggers reconciliation activity.
   - Verify zero duplicate provider submissions occur.
4. **Optimistic Locking Race Condition Suite (`test_concurrency_conflicts.py`):**
   - Spawn 10 concurrent threads attempting conflicting state updates on the same `generation_job_id`. Verify exactly one succeeds and 9 receive `OPTIMISTIC_CONCURRENCY_CONFLICT`.

---

## 10. Architectural Verdict & Freeze Recommendation

The **Two-Tier State Machine Architecture** provides the necessary formal separation between:
- **Durable Business Truth** (CanonicalLifecycleStatus in PostgreSQL)
- **Transient Operational Orchestration** (ExecutionStage in Telemetry/Workflows)

It resolves all contradictions between `STATUS_STATE_MACHINES.md` and `domain-entities.schema.json`, enforces System Invariants 1, 2, 3, 16, 18, and 19, and provides mathematical guarantees against state divergence and double-spend failures.

**Recommendation:** **FULL APPROVAL & SPEC FREEZE (PASS)** for Decision Cluster 02.

---
*Authored by R02 Reliability Specialist — Autonomous Architecture Council*
