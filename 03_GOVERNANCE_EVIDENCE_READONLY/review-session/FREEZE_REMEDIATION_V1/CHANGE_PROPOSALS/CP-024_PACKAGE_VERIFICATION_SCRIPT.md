# CHANGE PROPOSAL: CP-024 (NEW - GOV-006 / TECH-011)
**CHANGE_ID:** CP-024
**TITLE:** Deterministic Package Verification Tooling
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** GOV-006, TECH-011
**MATERIALLY_AFFECTED_ROLES:** R11 (Platform), R08 (QA), R15 (Red Team)
**MANDATORY_SIGNOFF_ROLES:** R11 (Platform), R08 (QA)

## 1. Rationale & Problem Description
Provides an automated standalone verification script (`verify_package.py`) allowing any verifier to independently check individual file hashes, tree hash, and archive hash without external dependencies.

## 2. Exact Specification Changes
- Create `verify_package.py` in the candidate root and final freeze package.
