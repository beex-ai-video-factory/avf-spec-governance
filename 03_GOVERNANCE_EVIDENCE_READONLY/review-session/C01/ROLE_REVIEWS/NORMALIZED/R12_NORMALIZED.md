# Normalized Specialist Review — R12

**Reviewer Role:** `R12`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R12_RAW.md`  
**Raw SHA-256:** `962a47d1723fb044249e5ee2248cd3bf73e50334e449dd65a9c0c2f891582771`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R12-001: R12 Finding F-R12-001
- **Severity:** `HIGH`
- **Category:** `SPEC_GAP`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contr`
- **Affected Contracts:** `- domain-entities.schema.json - STATUS_STATE_MACHINES.md - COMMAND_EVENT_CATALOG.md`
- **Summary:** A generated video take has a minor 0.5-second freeze frame at the tail end but perfect character likeness and motion. Because the QC engine lacks a mu
- **Proposed Solution:** 1. Define a concrete `QCResult` schema in `avf-contracts` (`qc-result.schema.json`) with distinct objects for `technical_metrics` and `semantic_metric
- **Confidence:** `` (float [0..1]).    - `defect_annotations`: array of `{ metric: string, start_frame: int, end_frame: int, severity: "FATAL"|"WARNING"|"INFO", description: string }`. 2. Standardize baseline technical`

### F-R12-002: R12 Finding F-R12-002
- **Severity:** `HIGH`
- **Category:** `CONTRACT`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`
- **Affected Contracts:** `- CONTRACTS_OVERVIEW.md - domain-entities.schema.json - event-envelope.schema.json`
- **Summary:** An operator manually overrides a prompt on a high-visibility brand project and increases the project budget by $500 to push a deadline. Two days later
- **Proposed Solution:** 1. Create `operator-command.schema.json` in `avf-contracts` with standard fields:    - `schema_version`: "1.0"    - `command_id`: UUIDv4 (Idempotency 
- **Confidence:** `VERY HIGH (Proven defect; standard architectural pattern). ````

### F-R12-003: R12 Finding F-R12-003
- **Severity:** `HIGH`
- **Category:** `STATE_MACHINE`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo`
- **Affected Contracts:** `- STATUS_STATE_MACHINES.md - COMMAND_EVENT_CATALOG.md`
- **Summary:** A browser worker encounters a Google account re-authentication prompt. It detects the challenge and transitions `GenerationJob` to `BLOCKED_AUTH`. The
- **Proposed Solution:** Amend `STATUS_STATE_MACHINES.md` to include an explicit, authoritative State Transition Matrix for all blocked and recoverable states:
- **Confidence:** `VERY HIGH (Proven defect; explicit specification provided). ````

### F-R12-004: R12 Finding F-R12-004
- **Severity:** `HIGH`
- **Category:** `PROVENANCE`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0`
- **Affected Contracts:** `- domain-entities.schema.json - COMMAND_EVENT_CATALOG.md`
- **Summary:** During `HUMAN_REVIEW`, an operator notices that the prompt is missing a crucial lighting cue ("golden hour cinematic rim light"). The operator edits t
- **Proposed Solution:** 1. Extend `promptVersion` in `domain-entities.schema.json` to include:    - `origin`: enum (`"AI_COMPILED"`, `"HUMAN_OPERATOR"`, `"HYBRID"`) - default
- **Confidence:** `VERY HIGH (Proven defect; directly preserves System Invariants INV-002, INV-004, INV-011). ````

### F-R12-005: R12 Finding F-R12-005
- **Severity:** `MEDIUM`
- **Category:** `PRODUCT_POLICY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_bluep`
- **Affected Contracts:** `- domain-entities.schema.json - STATUS_STATE_MACHINES.md`
- **Summary:** A production studio creates a 60-shot social media video campaign. The system default requires human approval before prompt submission AND after QC fo
- **Proposed Solution:** 1. Introduce a formal `ApprovalPolicy` object into the Project and Shot entities in `domain-entities.schema.json`:    ```json    "approval_policy": { 
- **Confidence:** `assessments to `HUMAN_REVIEW`.    - `STRICT_HUMAN_GATE`: Halts at `HUMAN_REVIEW` before generation submit AND after take generation, regardless of QC scores.`

### F-R12-006: R12 Finding F-R12-006
- **Severity:** `HIGH`
- **Category:** `ROADMAP`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/PHASE_ROADMAP.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/BUILD_ORDER.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERA`
- **Affected Contracts:** `- API_COMPATIBILITY_POLICY.md`
- **Summary:** In Phase 1 and Phase 2, developers and QA engineers test multi-shot durable workflows with real browser workers. The browser hits an expired cookie or
- **Proposed Solution:** Restructure the Operator Control delivery across phases: 1. **Phase 1-2 (MVP Operator Control Surface & Admin CLI):**    - Ship a lightweight Operator
- **Confidence:** `VERY HIGH (Proven operational dependency). ````

### F-R12-007: R12 Finding F-R12-007
- **Severity:** `MEDIUM`
- **Category:** `UI_SPEC`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
- **Affected Contracts:** `- CONTRACTS_OVERVIEW.md`
- **Summary:** An operator reviews Take 1, which was flagged by QC for visual artifacting. The console only displays a small static thumbnail and an overall score of
- **Proposed Solution:** Specify core operator inspection view capabilities in `R13_OPERATOR_CONSOLE.md`: 1. **Frame-Accurate Video Player Component:**    - Transport controls
- **Confidence:** `HIGH (Standard best practice for video production tools). ````

### F-R12-008: R12 Finding F-R12-008
- **Severity:** `MEDIUM`
- **Category:** `COST_CONTROL`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_bluep`
- **Affected Contracts:** `- domain-entities.schema.json - STATUS_STATE_MACHINES.md`
- **Summary:** A 20-shot video generation workflow is running overnight. At shot 16, the project crosses its $50 budget limit by $0.50. The workflow immediately halt
- **Proposed Solution:** 1. Define a Multi-Tier Budget Control Model in `avf-core-state` and `avf-workflow`:    - `budget_limit_usd`: Absolute hard ceiling.    - `budget_warni
- **Confidence:** `VERY HIGH (Proven financial control pattern). ````
