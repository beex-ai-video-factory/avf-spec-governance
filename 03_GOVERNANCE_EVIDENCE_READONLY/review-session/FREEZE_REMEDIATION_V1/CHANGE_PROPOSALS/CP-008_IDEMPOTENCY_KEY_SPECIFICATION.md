# CHANGE PROPOSAL: CP-008 (RETAINED)
**CHANGE_ID:** CP-008
**TITLE:** Idempotency Key Specification & Deterministic Construction
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** RETAINED_UNCHANGED
**SOURCE_FINDINGS:** FINDING_009, FINDING_027, FINDING_065
**MATERIALLY_AFFECTED_ROLES:** R02 (Reliability), R05 (Data), R04 (Contracts)
**MANDATORY_SIGNOFF_ROLES:** R02 (Reliability), R05 (Data)

## 1. Rationale & Problem Description
Retains deterministic idempotency key derivation `SHA256(shot_version_id + prompt_version_id + provider_id + attempt_index + parameters_hash)` and DB unique constraint to guarantee zero duplicate submissions.

## 2. Exact Specification Changes
Integrated in `01_master/DATA_MODEL.md`, `02_contracts/domain-entities.schema.json`, and `03_repo_blueprints/R02_CORE_STATE.md`.
