# CHANGE PROPOSAL: CP-006 (AMENDED)
**CHANGE_ID:** CP-006
**TITLE:** Browser Execution Architecture & Multi-Tier Fallback Hierarchy
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** GOV-007, TECH-009, FINDING_008
**MATERIALLY_AFFECTED_ROLES:** R06 (Flow Browser), R11 (Platform), R02 (Reliability), R15 (Red Team)
**MANDATORY_SIGNOFF_ROLES:** R06 (Flow Browser), R02 (Reliability)

## 1. Rationale & Problem Description
Formally specifies the 3-tier browser execution model (A1/A2 MV3 extension -> A3 Playwright dedicated persistent profile -> Track B FlowKit bridge) and proves that SPK-001 empirical keepalive uncertainty is non-blocking for freeze.

## 2. Exact Specification Changes
1. `03_repo_blueprints/R09_BROWSER_WORKER.md`: Document A1, A2, and A3 Playwright dedicated profile fallback.
2. `03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`: Detail execution hierarchy.
3. `06_adrs/ADR-004_DUAL_FLOW_EXECUTION.md`: Update decision record.

## 3. Capability Preservation Proof
Preserves CAP-02 (Google Flow Adapter) and CAP-18 (Track A / Track B Interchangeability).
