# CHANGE PROPOSAL: CP-016 (NEW - FA-003)
**CHANGE_ID:** CP-016
**TITLE:** Deletion of GenerationJob.track_mode from Canonical Domain Schema
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** GOV-003 (FA-003), TECH-004
**MATERIALLY_AFFECTED_ROLES:** R01 (Domain DDD), R04 (Contracts), R05 (Data), R06 (Flow Browser)
**MANDATORY_SIGNOFF_ROLES:** R01 (Domain DDD), R04 (Contracts)

## 1. Rationale & Problem Description
In the prior run, `GenerationJob.track_mode` was removed by a script without formal vote. This proposal formally approves removing `track_mode` from the canonical domain entity schema, as worker execution track is an operational execution detail, not a core domain entity attribute.

## 2. Exact Specification Changes
- `02_contracts/domain-entities.schema.json`: Remove `track_mode` property and required field from `GenerationJob` definition.
