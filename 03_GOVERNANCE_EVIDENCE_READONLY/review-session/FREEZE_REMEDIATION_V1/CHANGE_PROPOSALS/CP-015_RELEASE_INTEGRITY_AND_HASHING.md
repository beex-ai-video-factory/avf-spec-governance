# CHANGE PROPOSAL: CP-015 (AMENDED)
**CHANGE_ID:** CP-015
**TITLE:** Release Identity Alignment & Deterministic 4-Stage Hashing Pipeline
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** GOV-001, GOV-006, TECH-001, TECH-002, TECH-011, TECH-012
**MATERIALLY_AFFECTED_ROLES:** R11 (Platform), R08 (QA), R15 (Red Team)
**MANDATORY_SIGNOFF_ROLES:** R11 (Platform)

## 1. Rationale & Problem Description
Establishes release identity v1.0.0, deterministic non-self-referential package hashing, and evidence-derived certification linking to raw ballot SHA-256 digests.

## 2. Exact Specification Changes
Integrated in candidate manifests and release builder tooling.
