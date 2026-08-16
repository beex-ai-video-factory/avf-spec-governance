# Normalized Specialist Review — R04

**Reviewer Role:** `R04`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R04_RAW.md`  
**Raw SHA-256:** `60341712b07050a18e8ce30f7e349ccf9ddb6ed2cd6cdeb62a9ad4820d098a3f`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R04-001: R04 Finding F-R04-001
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-001: R04 Finding F-R04-001
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `ERROR_TAXONOMY / SCHEMA_COMPLETENESS`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json`
- **Affected Contracts:** `- CONTRACTS_OVERVIEW   - provider-result   - error-payload (missing)`
- **Summary:** During a generation job, Google Flow triggers an account CAPTCHA challenge. R09 (Browser Worker) returns a provider result with status "BLOCKED" and c
- **Proposed Solution:** 1. Create a dedicated schema `02_contracts/error-payload.schema.json` with an enum of the 14 error classes.   2. Define specific, typed detail definit
- **Confidence:** `98% - High ````

### F-R04-002: R04 Finding F-R04-002
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-002: R04 Finding F-R04-002
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `CONTRACT_COMPLETENESS / BOUNDARY_VALIDATION`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v`
- **Affected Contracts:** `- browser-command   - browser-command-result (missing)`
- **Summary:** R08 (Google Flow Adapter) issues a `CREATE_OR_SELECT_PROJECT` command to Track A (R09 Browser Worker) but omits the `project_name` property due to a c
- **Proposed Solution:** 1. Refactor `browser-command.schema.json` using `oneOf` to bind each `method` (`ENSURE_SESSION`, `OPEN_FLOW`, `CREATE_OR_SELECT_PROJECT`, `ATTACH_ASSE
- **Confidence:** `99% - High ````

### F-R04-003: R04 Finding F-R04-003
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-003: R04 Finding F-R04-003
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SCHEMA_COMPLETENESS / DATA_MODEL_ALIGNMENT`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/DATA_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blu`
- **Affected Contracts:** `- domain-entities`
- **Summary:** Developer A implementing `R02_CORE_STATE` creates a Python model for `Take` with fields `{"take_id", "generation_job_id", "media_url", "checksum_sha25
- **Proposed Solution:** Expand `02_contracts/domain-entities.schema.json` (or split into modular schemas under `02_contracts/domain/`) to define complete JSON schemas for all
- **Confidence:** `98% - High ````

### F-R04-004: R04 Finding F-R04-004
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-004: R04 Finding F-R04-004
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `EVENT_CONTRACTS / ASYNC_COMMUNICATION`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md`
- **Affected Contracts:** `- event-envelope   - domain-events (missing)`
- **Summary:** `R08_GOOGLE_FLOW_ADAPTER` publishes a `GenerationBlocked` event when authentication expires. It includes `{ "reason": "auth", "account": "user@gmail.c
- **Proposed Solution:** 1. Add a `domain-events.schema.json` (or include `$defs` in `event-envelope.schema.json`) defining the explicit payload schema for each of the 16 doma
- **Confidence:** `96% - High ````

### F-R04-005: R04 Finding F-R04-005
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-005: R04 Finding F-R04-005
- **Severity:** `HIGH`
- **Category:** `API_COMPATIBILITY / VERSIONING`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0`
- **Affected Contracts:** `- ALL schemas`
- **Summary:** A non-breaking minor update is made to `provider-request.schema.json` (e.g. adding an optional `seed` parameter) and the schema version is bumped to `
- **Proposed Solution:** Change `"schema_version"` in all v1 schemas from `"const": "1.0"` to:   ```json   "schema_version": {     "type": "string",     "pattern": "^1\\.[0-9]
- **Confidence:** `99% - High ````

### F-R04-006: R04 Finding F-R04-006
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-006: R04 Finding F-R04-006
- **Severity:** `HIGH`
- **Category:** `OBSERVABILITY / TRACEABILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_`
- **Affected Contracts:** `- provider-request   - browser-command   - event-envelope`
- **Summary:** A generation job fails during browser automation. An engineer opens OpenTelemetry / Jaeger in R14 to trace the failure starting from the `shot_id`. Be
- **Proposed Solution:** Define a canonical `correlation-context.schema.json` (or reusable `$defs/correlationContext`) containing all 6 canonical correlation fields:   ```json
- **Confidence:** `98% - High ````

### F-R04-007: R04 Finding F-R04-007
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-007: R04 Finding F-R04-007
- **Severity:** `HIGH`
- **Category:** `CONTRACT_COMPLETENESS`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blue`
- **Affected Contracts:** `- qc-evaluator (missing)   - media-processing (missing)`
- **Summary:** `R11_QC` evaluates a video take and outputs a score breakdown (`black_frames_percentage`, `motion_freeze_duration`, `audio_loudness_lufs`, `passed_thr
- **Proposed Solution:** Publish `qc-evaluator.schema.json` and `media-processing.schema.json` in `02_contracts/` covering:   - `QCEvaluationRequest` / `QCEvaluationResult` (m
- **Confidence:** `95% - High ````

### F-R04-008: R04 Finding F-R04-008
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R04-008: R04 Finding F-R04-008
- **Severity:** `NON_BLOCKING`
- **Category:** `API_COMPATIBILITY / EXTENSIBILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md`
- **Affected Contracts:** `- provider-request`
- **Summary:** A new provider capability `video_to_video` or `inpaint_video` is added in Phase 2. Existing v1.0 consumers running strict schema validation fail becau
- **Proposed Solution:** 1. Structure `generation_options` into a normalized standard options schema (`aspect_ratio`, `duration_seconds`, `fps`, `seed`, `camera_motion`, `reso
- **Confidence:** `92% - High ````
