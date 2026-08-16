# CHANGE PROPOSAL: CP-023 (NEW - TECH-001)
**CHANGE_ID:** CP-023
**TITLE:** Release Version 1.0.0 Synchronization Across All Candidate Files
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** TECH-001 (B01)
**MATERIALLY_AFFECTED_ROLES:** R10 (DX), R11 (Platform)
**MANDATORY_SIGNOFF_ROLES:** R10 (DX), R11 (Platform)

## 1. Rationale & Problem Description
Synchronizes release identity across `VERSION`, `README.md`, `KIT_MANIFEST.yaml`, and `COMMITTEE_REVIEW_EDITION.md` to state `1.0.0-remediated-rc1` (promoted to `1.0.0` upon freeze certification).

## 2. Exact Specification Changes
- `VERSION`: Set to `1.0.0-remediated-rc1`
- `README.md`: Update candidate version to `v1.0.0-remediated-rc1`
- `KIT_MANIFEST.yaml`: Update version to `1.0.0-remediated-rc1`
- `COMMITTEE_REVIEW_EDITION.md`: Update edition to `v1.0.0`.
