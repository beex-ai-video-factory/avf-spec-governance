# CHANGE PROPOSAL: CP-002 (AMENDED)
**CHANGE_ID:** CP-002
**TITLE:** Hierarchical Two-Tier GenerationJob Lifecycle State Machine & Stage Mapping
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** TECH-005, FINDING_002, FINDING_019
**MATERIALLY_AFFECTED_ROLES:** R02 (Reliability), R03 (Workflow), R04 (Contracts), R13 (Operator Console)
**MANDATORY_SIGNOFF_ROLES:** R02 (Reliability), R04 (Contracts), R03 (Workflow)

## 1. Rationale & Problem Description
Reconciles the contradiction between `STATUS_STATE_MACHINES.md` and `domain-entities.schema.json` by establishing a two-tier state model: 7 canonical DB lifecycle states (`status`) and 11 workflow execution stages (`execution_stage`).

## 2. Exact Specification Changes
1. `02_contracts/STATUS_STATE_MACHINES.md`:
   - Document the Parent Lifecycle States: `QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`.
   - Document the Execution Stages: `WAITING_FOR_ASSETS`, `PROMPT_READY`, `BUDGET_RESERVED`, `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`, `APPROVED`, `BLOCKED`, `ABORTED`.
   - Provide the strict Parent-to-Child Mapping Matrix and state transition table.
2. `02_contracts/domain-entities.schema.json`: Update `GenerationJob` schema with `status` (CanonicalLifecycleStatus enum) and `execution_stage` (ExecutionStage enum).
3. `03_repo_blueprints/R02_CORE_STATE.md`, `R06_WORKFLOW.md`, `R13_OPERATOR_CONSOLE.md`: Align state management.

## 3. Capability Preservation Proof
Preserves CAP-01 (Canonical Core State), CAP-03 (Provider SDK), and CAP-04 (Workflow Engine).
