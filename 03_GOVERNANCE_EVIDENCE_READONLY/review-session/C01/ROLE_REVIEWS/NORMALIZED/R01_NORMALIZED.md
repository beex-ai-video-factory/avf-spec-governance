# Normalized Specialist Review — R01

**Reviewer Role:** `R01`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R01_RAW.md`  
**Raw SHA-256:** `3d8f55f9e46ff648041007697095d0764ca9bbb5247aa6612e20be0bedfa528c`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R01-001: R01 Finding F-R01-001
- **Severity:** `HIGH`
- **Category:** `CONTRACT_DEFICIENCY`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/DATA_MODEL.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_bl`
- **Affected Contracts:** `- `domain-entities.schema.json` - `CONTRACTS_OVERVIEW.md``
- **Summary:** When a developer implements `avf-core-state`, `avf-assets-continuity`, or `avf-qc`, there is no machine-verifiable JSON Schema contract for `Project`,
- **Proposed Solution:** Expand `domain-entities.schema.json` to include comprehensive JSON Schema definitions for all 14 canonical entities, explicitly declaring required fie
- **Confidence:** `1.0 (Defect proven by inspecting `domain-entities.schema.json`).`

### F-R01-002: R01 Finding F-R01-002
- **Severity:** `HIGH`
- **Category:** `BOUNDED_CONTEXT / OWNERSHIP_AMBIGUITY`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R04_ASSETS_CONTINUITY.md` (line 54) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md` (lines 13-20, 43-53) - `A`
- **Affected Contracts:** `- `R02_CORE_STATE` Public API - `R04_ASSETS_CONTINUITY` Public API - `COMMAND_EVENT_CATALOG.md``
- **Summary:** If `avf-assets-continuity` implements its own isolated database tables for `CharacterVersion` and `AssetVersion`, `avf-core-state` cannot enforce rela
- **Proposed Solution:** 1. Explicitly designate `avf-core-state` as the sole PostgreSQL schema owner for all canonical domain tables (`project`, `scene`, `shot`, `shot_versio
- **Confidence:** `1.0 (Defect proven by contradicting text in R04 line 54 vs R02 lines 13-20).`

### F-R01-003: R01 Finding F-R01-003
- **Severity:** `HIGH`
- **Category:** `DOMAIN_STATE_MACHINE / COMMAND_CONTRACT`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md` (lines 43-53) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md` (lines 3-28) - `AI_VIDEO_FA`
- **Affected Contracts:** `- `R02_CORE_STATE` Public API - `STATUS_STATE_MACHINES.md` - `COMMAND_EVENT_CATALOG.md``
- **Summary:** When `avf-workflow` orchestrator transitions a job from `SUBMITTED` to `GENERATING` upon receiving a progress webhook/poll, or advances to `DOWNLOADIN
- **Proposed Solution:** 1. Add explicit state transition commands to `R02_CORE_STATE.md` Public API:    - `TransitionJobStatus(generation_job_id, expected_status, new_status,
- **Confidence:** `1.0 (Defect proven by comparing R02 Public API with STATUS_STATE_MACHINES.md).`

### F-R01-004: R01 Finding F-R01-004
- **Severity:** `MEDIUM`
- **Category:** `ARCHITECTURAL_GOVERNANCE / ADR_METADATA`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-001_MODULAR_POLYREPO.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-002_CANONICAL_STATE.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_a`
- **Affected Contracts:** `- Baseline ADRs ADR-001 through ADR-008 - GAP-003 Seed`
- **Summary:** During Phase 1 implementation, an external contributor or autonomous agent inspects `ADR-002` or `ADR-004` and, finding no formal `ACCEPTED` status he
- **Proposed Solution:** 1. Insert explicit `## Status: ACCEPTED (v0.9.0 Baseline — Ratified in C01)` metadata into ADR-001 through ADR-008. 2. Customize `## Revisit Trigger` 
- **Confidence:** `1.0 (Defect proven by inspecting all 8 ADR files).`

### F-R01-005: R01 Finding F-R01-005
- **Severity:** `MEDIUM`
- **Category:** `DOMAIN_MODEL / ENTITY_RELATIONSHIPS`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/DATA_MODEL.md` (lines 8-23, 99-109) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-006, INV-016) - `AI_VIDEO_FACTORY_B`
- **Affected Contracts:** `- `DATA_MODEL.md` ERD - `domain-entities.schema.json``
- **Summary:** When `avf-workflow` completes downloading a video take from Google Flow, it needs to pass the media reference to `avf-qc` and `avf-media`. If `Take` s
- **Proposed Solution:** 1. Update `DATA_MODEL.md` ERD to add the explicit relationship:    `Take ||--|| AssetVersion : references_binary` 2. Specify that every `Take` entity 
- **Confidence:** `1.0 (Defect proven by inspecting ERD in `DATA_MODEL.md`).`

### F-R01-006: R01 Finding F-R01-006
- **Severity:** `MEDIUM`
- **Category:** `DOMAIN_INVARIANTS / DETERMINISM`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/DATA_MODEL.md` (lines 73-74) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md` (lines 16, 37, 72) - `AI_VIDEO_FACTO`
- **Affected Contracts:** `- `domain-entities.schema.json` - `R05_PROMPT_COMPILER` contract`
- **Summary:** `avf-prompt-compiler` is implemented in Python and calculates `input_hash` using `json.dumps(obj, sort_keys=True)`. `avf-core-state` is implemented in
- **Proposed Solution:** Mandate RFC 8785 (JSON Canonicalization Scheme - JCS) with SHA-256 for all domain hash calculations (`input_hash`, `content_checksum`, `idempotency_ke
- **Confidence:** `1.0 (Defect proven by omission of canonical serialization standard in R05 and DATA_MODEL).`

### F-R01-007: R01 Finding F-R01-007
- **Severity:** `NON_BLOCKING`
- **Category:** `DOMAIN_MODEL / AGGREGATE_NAVIGATION`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/DATA_MODEL.md` (lines 45-58) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json` (lines 24-88) - `AI_VIDEO_FACTORY_BLU`
- **Affected Contracts:** `- `domain-entities.schema.json` - `R02_CORE_STATE` read models`
- **Summary:** An operator creates `ShotVersion` v1, then edits the action to create `ShotVersion` v2. When `avf-workflow` triggers `StartProjectWorkflow` to generat
- **Proposed Solution:** Define `Shot` entity in `domain-entities.schema.json` with fields: - `shot_id UUID` - `scene_id UUID` - `project_id UUID` - `shot_number integer` - `s
- **Confidence:** `0.95 (Logical gap in aggregate navigation).`
