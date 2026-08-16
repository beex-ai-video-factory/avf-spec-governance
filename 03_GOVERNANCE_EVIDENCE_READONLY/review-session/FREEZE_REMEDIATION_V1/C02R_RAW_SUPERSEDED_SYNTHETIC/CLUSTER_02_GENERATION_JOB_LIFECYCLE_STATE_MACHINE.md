# C02R HEARING TRANSCRIPT: CLUSTER 02 — GENERATION JOB LIFECYCLE & STATE MACHINES
**CLUSTER_ID:** CLUSTER-02
**FINDINGS_COVERED:** FINDING_002, FINDING_019, FINDING_044, TECH-005
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R02 (Reliability Specialist)
- **Position:** The repository previously suffered from a severe contradiction between `domain-entities.schema.json` (which allowed only `QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `RECONCILED`) and `STATUS_STATE_MACHINES.md` (which defined granular stages like `WAITING_FOR_ASSETS`, `SUBMITTING`, `GENERATING`, `DOWNLOADING`, `QC_RUNNING`, `APPROVED`). We propose a hierarchical two-tier state model:
  1. *Canonical Core State (Database & Top-Level Entity):* Coarse-grained, durable lifecycle status (`QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`).
  2. *Workflow Execution Sub-State (Temporal Activity & Telemetry):* Fine-grained stage enum (`WAITING_FOR_ASSETS`, `PROMPT_READY`, `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`, `APPROVED`, `BLOCKED`, `ABORTED`) stored in `execution_stage` and emitted in events.
- **Evidence:** `STATUS_STATE_MACHINES.md` lines 12-48 vs `domain-entities.schema.json` line 395.
- **Failure Scenario:** If Temporal workflow tries to write `SUBMITTING` to PostgreSQL and the schema only accepts `RUNNING`, either the DB write throws a validation error, or developers hack custom bypass strings, breaking state query consistency for the Operator UI.

## 2. Challenger Attack
- **Challenger:** R03 (Workflow Specialist)
- **Attack Vector:**
  1. *Two Sources of Truth:* Maintaining both a top-level `status` and an `execution_stage` introduces the risk of split-brain states (e.g. `status = COMPLETED` while `execution_stage = SUBMITTING`).
  2. *Terminal State Synchronization:* If a job fails during `DOWNLOADING`, who decides whether the state is `FAILED` or `RECONCILED`? Does Temporal decide, or does R02 Core State state-transition logic enforce it?

## 3. Domain Owner Review
- **Domain Owner:** R02 (Reliability Specialist) & R04 (Contracts Specialist)
- **Evaluation:**
  - R02 Core State is the sole owner of canonical PostgreSQL records. Temporal executes orchestrations but persists state by calling R02 State APIs.
  - To eliminate split-brain risk, R02 must enforce a strict parent-child state mapping matrix. For instance, when `execution_stage = SUBMITTING`, `status` MUST be `RUNNING`. A transition to `COMPLETED` is only valid when `execution_stage = APPROVED` (or `QC_PASSED`).
  - Terminal transitions to `FAILED` must record a `normalized_error` object containing error code, retry category, and failure timestamp.

## 4. Proponent Response
- **Response:**
  - We formalize the exact Parent-Child State Mapping Matrix in both `STATUS_STATE_MACHINES.md` and `domain-entities.schema.json`.
  - `domain-entities.schema.json` will include `status` (CanonicalLifecycleStatus enum) and `execution_stage` (ExecutionStage enum), with JSON Schema `allOf` conditionals or contract documentation explicitly constraining valid combinations.
  - R02 API rejects any transition where the child stage does not map to the parent lifecycle state.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Collapse everything into a single 15-state flat enum in both DB and schemas.
- **Why Rejected:** High-level state queries (e.g. "show all active running jobs for cost metering") would require complex `status IN ('SUBMITTING', 'SUBMITTED', 'GENERATING', 'DOWNLOADING', 'QC_RUNNING')` queries that change every time an intermediate pipeline step is added.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-002 amended to:
  1. Synchronize `STATUS_STATE_MACHINES.md`, `domain-entities.schema.json`, `R02_CORE_STATE.md`, `R06_WORKFLOW.md`, and `R13_OPERATOR_CONSOLE.md`.
  2. Define the explicit 7-state CanonicalLifecycleStatus and 11-stage ExecutionStage.
  3. Provide exact deterministic state transition rules, terminal failure semantics, and cancellation transitions.
