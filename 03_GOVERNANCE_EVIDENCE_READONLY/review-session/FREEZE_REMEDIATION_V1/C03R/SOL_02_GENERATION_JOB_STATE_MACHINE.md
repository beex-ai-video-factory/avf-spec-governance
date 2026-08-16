# C03R SOLUTION PACKAGE 02: GENERATION JOB LIFECYCLE & STATE MACHINE
**SOLUTION_ID:** SOL-02
**FINDINGS_ADDRESSED:** TECH-005, FINDING_002, FINDING_019
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
`STATUS_STATE_MACHINES.md` defined 12 granular workflow stages while `domain-entities.schema.json` defined a 6-state enum. When workflow activities run, developers lacked a formal contract mapping execution stages to database lifecycle states, risking state machine divergence.

---

## 2. Options Analysis

### Option A: Formal Two-Tier Hierarchical State Machine (Recommended)
- **Architecture:**
  - Tier 1: Canonical Lifecycle Status (`status` field in DB):
    `QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`.
  - Tier 2: Execution Stage (`execution_stage` field):
    - When `QUEUED`: `WAITING_FOR_ASSETS`, `PROMPT_READY`
    - When `RESERVED`: `BUDGET_RESERVED`
    - When `RUNNING`: `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`
    - When `COMPLETED`: `APPROVED`
    - When `FAILED`: `EXECUTION_FAILED`, `QC_REJECTED`, `TIMEOUT`
    - When `CANCELLED`: `ABORTED_BY_USER`, `ABORTED_BY_SYSTEM`
    - When `RECONCILED`: `RECONCILED_SUCCESS`, `RECONCILED_TERMINAL`
  - Deterministic Transition Matrix: R02 State Engine enforces valid transitions. Terminal states (`COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`) are immutable once written.
- **Exact Normative Files to Change:**
  - `02_contracts/STATUS_STATE_MACHINES.md`
  - `02_contracts/domain-entities.schema.json`
  - `03_repo_blueprints/R02_CORE_STATE.md`
  - `03_repo_blueprints/R06_WORKFLOW.md`
  - `03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
- **Tests & Conformance:** State machine unit tests verifying valid transitions and rejecting invalid transitions (e.g. `QUEUED -> COMPLETED` without `RUNNING`).

### Option B: Single 18-State Flat Enum
- **Drawbacks:** Makes high-level SQL queries (e.g. "count running jobs") complex and brittle, and exposes ephemeral worker states to external billing systems.

---

## 3. Decision
**Selected: Option A.** Provides clean separation between durable business state and fine-grained orchestrator telemetry.
