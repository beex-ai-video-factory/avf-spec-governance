# CHANGE PROPOSAL: CP-003 (AMENDED)
**CHANGE_ID:** CP-003
**TITLE:** FlowExecutionPort Strict Discriminated Operations & Result Schema
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** TECH-006, FINDING_003, FINDING_020
**MATERIALLY_AFFECTED_ROLES:** R06 (Flow Browser), R04 (Contracts), R02 (Reliability), R08 (QA), R10 (DX)
**MANDATORY_SIGNOFF_ROLES:** R06 (Flow Browser), R04 (Contracts), R02 (Reliability)

## 1. Rationale & Problem Description
Freezes the exact parameter, result, error, and timeout contracts for all 10 FlowExecutionPort operations, enabling Track A and Track B to be 100% interchangeable behind the adapter without code drift.

## 2. Exact Specification Changes
1. `02_contracts/browser-command.schema.json`: Strict typed `oneOf` with `command_type` for all 10 operations (ENSURE_SESSION, OPEN_FLOW, CREATE_OR_SELECT_PROJECT, ATTACH_ASSETS, SET_GENERATION_OPTIONS, SUBMIT_PROMPT, READ_GENERATION_STATE, DOWNLOAD_OUTPUT, CAPTURE_DIAGNOSTIC, CANCEL).
2. `02_contracts/flow-execution-result.schema.json` (NEW): Matching typed result schemas.
3. `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`, `R09_BROWSER_WORKER.md`, `R10_FLOWKIT_BRIDGE.md`: Update port interfaces.

## 3. Capability Preservation Proof
Preserves CAP-02 (Google Flow Adapter) and CAP-18 (Track A / Track B Port Equivalence).
