# CHANGE PROPOSAL: CP-018 (NEW - FA-003)
**CHANGE_ID:** CP-018
**TITLE:** Formal Addition of GenerationJob.attempt_index and 90-Minute Safety Lease TTL
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** GOV-003 (FA-003), TECH-004
**MATERIALLY_AFFECTED_ROLES:** R02 (Reliability), R04 (Contracts), R05 (Data), R06 (Workflow)
**MANDATORY_SIGNOFF_ROLES:** R02 (Reliability), R04 (Contracts)

## 1. Rationale & Problem Description
Formally ratifies the addition of `attempt_index` (integer >= 1) to `GenerationJob` and sets the safety lease TTL to 90 minutes with 30-second worker heartbeats.

## 2. Exact Specification Changes
- `02_contracts/domain-entities.schema.json`: Add `attempt_index` to `GenerationJob`.
- `03_repo_blueprints/R02_CORE_STATE.md`: Specify 90-minute TTL and 30-second heartbeat.
