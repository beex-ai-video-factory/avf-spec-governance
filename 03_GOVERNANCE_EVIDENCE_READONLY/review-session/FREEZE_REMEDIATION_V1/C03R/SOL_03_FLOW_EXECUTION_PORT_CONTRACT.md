# C03R SOLUTION PACKAGE 03: FLOW EXECUTION PORT & 10 OPERATION CONTRACTS
**SOLUTION_ID:** SOL-03
**FINDINGS_ADDRESSED:** TECH-006, FINDING_003, FINDING_020
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
`browser-command.schema.json` had unconstrained `params` and lacked a corresponding result schema, making independent implementation of Track A (Browser Worker) and Track B (FlowKit Bridge) against the same port impossible.

---

## 2. Options Analysis

### Option A: Fully Typed Discriminated JSON Schemas for All 10 Operations (Recommended)
- **Architecture:**
  - Update `browser-command.schema.json` to use strict `oneOf` with `command_type` discriminator and `additionalProperties: false` for all 10 operations:
    1. `ENSURE_SESSION`: params `{session_id, account_alias, headless}`
    2. `OPEN_FLOW`: params `{session_id, flow_url, timeout_ms}`
    3. `CREATE_OR_SELECT_PROJECT`: params `{session_id, project_name, project_id}`
    4. `ATTACH_ASSETS`: params `{session_id, assets: [{asset_id, storage_uri, mime_type, role}]}`
    5. `SET_GENERATION_OPTIONS`: params `{session_id, aspect_ratio, resolution, duration_seconds, seed, model_version}`
    6. `SUBMIT_PROMPT`: params `{session_id, prompt_text, negative_prompt, idempotency_key}`
    7. `READ_GENERATION_STATE`: params `{session_id, provider_job_id}`
    8. `DOWNLOAD_OUTPUT`: params `{session_id, provider_job_id, destination_storage_uri}`
    9. `CAPTURE_DIAGNOSTIC`: params `{session_id, include_har, include_screenshot, include_console_logs}`
    10. `CANCEL`: params `{session_id, provider_job_id}`
  - Create normative `flow-execution-result.schema.json` with matching discriminated results returning typed payloads (e.g. `provider_job_id`, `generation_status`, `output_asset_metadata`, `diagnostic_bundle_uri`, `normalized_error`).
  - Strict URI-based payload passing (no base64 binary bloat in JSON).
- **Exact Normative Files to Change:**
  - `02_contracts/browser-command.schema.json`
  - `02_contracts/flow-execution-result.schema.json` (NEW)
  - `02_contracts/CONTRACTS_OVERVIEW.md`
  - `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
  - `03_repo_blueprints/R09_BROWSER_WORKER.md`
  - `03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
  - `03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`

### Option B: Generic Map Contract with Client-Side Type Assertions
- **Drawbacks:** Fails contract gate G02; permits Track A and Track B to drift in parameter naming, defeating hot-swappability.

---

## 3. Decision
**Selected: Option A.** Enables 100% automated conformance testing of Track A and Track B against identical schemas.
