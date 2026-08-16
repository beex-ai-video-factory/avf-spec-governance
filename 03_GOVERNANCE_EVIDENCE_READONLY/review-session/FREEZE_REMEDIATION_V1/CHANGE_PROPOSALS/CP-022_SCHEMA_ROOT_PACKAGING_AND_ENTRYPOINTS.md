# CHANGE PROPOSAL: CP-022 (NEW - TECH-017)
**CHANGE_ID:** CP-022
**TITLE:** JSON Schema Root Packaging & Fragment Entrypoint Documentation
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** NEW_PROPOSAL
**SOURCE_FINDINGS:** TECH-017
**MATERIALLY_AFFECTED_ROLES:** R04 (Contracts), R10 (DX), R08 (QA)
**MANDATORY_SIGNOFF_ROLES:** R04 (Contracts), R10 (DX)

## 1. Rationale & Problem Description
Clarifies that `domain-entities.schema.json` is a schema definitions package whose canonical types are referenced via fragments (`#//Project`, `#//ShotVersion`, etc.) and documents root schema validation behavior in `CONTRACTS_OVERVIEW.md`.

## 2. Exact Specification Changes
- `02_contracts/CONTRACTS_OVERVIEW.md`: Add Fragment Entrypoints section.
