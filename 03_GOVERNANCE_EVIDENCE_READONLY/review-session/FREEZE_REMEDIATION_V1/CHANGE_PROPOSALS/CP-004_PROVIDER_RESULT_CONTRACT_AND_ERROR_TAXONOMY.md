# CHANGE PROPOSAL: CP-004 (AMENDED)
**CHANGE_ID:** CP-004
**TITLE:** Provider Result Contract Separation & Normalized Error Taxonomy
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** TECH-008, FINDING_005, FINDING_022
**MATERIALLY_AFFECTED_ROLES:** R04 (Contracts), R02 (Reliability), R09 (AI), R07 (Security)
**MANDATORY_SIGNOFF_ROLES:** R04 (Contracts), R02 (Reliability)

## 1. Rationale & Problem Description
Separates synchronous transport status (`SUCCESS`, `FAILED`, `PENDING`, `RUNNING`), asynchronous provider generation status (`QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`), normalized error codes (`PROVIDER_RATE_LIMIT`, `AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`, `BUDGET_EXHAUSTED`, `UNSUPPORTED_CAPABILITY`, `NETWORK_TIMEOUT`, `BAD_REQUEST`, `PROVIDER_INTERNAL_ERROR`), and retry classifications (`TRANSIENT`, `PERMANENT`, `POLICY_BLOCKED`, `RESOURCE_EXHAUSTED`).

## 2. Exact Specification Changes
1. `02_contracts/provider-result.schema.json`: Restructure with separated status, generation_status, and normalized error.
2. `02_contracts/CONTRACTS_OVERVIEW.md`: Update provider contract section.
3. `03_repo_blueprints/R07_PROVIDER_SDK.md`, `R08_GOOGLE_FLOW_ADAPTER.md`: Update error handling.

## 3. Capability Preservation Proof
Preserves CAP-03 (Provider Abstraction) and CAP-12 (Autonomous Error Recovery).
