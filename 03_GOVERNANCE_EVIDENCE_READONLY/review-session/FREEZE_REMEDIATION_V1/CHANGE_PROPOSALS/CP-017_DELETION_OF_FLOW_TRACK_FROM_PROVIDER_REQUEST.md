# CHANGE PROPOSAL: CP-017 (NEW - FA-003)
**CHANGE_ID:** CP-017
**TITLE:** Deletion of flow_track from provider-request.schema.json
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** GOV-003 (FA-003), TECH-008
**MATERIALLY_AFFECTED_ROLES:** R04 (Contracts), R07 (Provider SDK), R08 (Google Flow Adapter)
**MANDATORY_SIGNOFF_ROLES:** R04 (Contracts), R07 (Provider SDK)

## 1. Rationale & Problem Description
In the prior run, `flow_track` was removed from `provider-request.schema.json` post-vote. This proposal formally ratifies removing provider-level track selection from generic provider requests, encapsulating track routing inside R08 adapter configuration.

## 2. Exact Specification Changes
- `02_contracts/provider-request.schema.json`: Remove `flow_track` from `ProviderRequest` schema.
