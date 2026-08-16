# CHANGE PROPOSAL: CP-019 (NEW - FA-003)
**CHANGE_ID:** CP-019
**TITLE:** Addition of attempt_index to provider-request.schema.json
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** GOV-003 (FA-003), TECH-008
**MATERIALLY_AFFECTED_ROLES:** R04 (Contracts), R07 (Provider SDK), R02 (Reliability)
**MANDATORY_SIGNOFF_ROLES:** R04 (Contracts), R07 (Provider SDK)

## 1. Rationale & Problem Description
Adds `attempt_index` (integer >= 1) to `provider-request.schema.json` to allow provider adapters to construct deterministic provider-side idempotency keys.

## 2. Exact Specification Changes
- `02_contracts/provider-request.schema.json`: Add `attempt_index` property.
