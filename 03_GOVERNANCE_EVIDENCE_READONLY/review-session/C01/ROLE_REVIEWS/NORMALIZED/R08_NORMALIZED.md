# Normalized Specialist Review — R08

**Reviewer Role:** `R08`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R08_RAW.md`  
**Raw SHA-256:** `07ca5699e05ee051928f71dddd8439a6dff10b6562f9940d7f05e7806f7fcd50`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R08-001: R08 Finding F-R08-001
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `CONTRACT_DEFECT`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts`
- **Affected Contracts:** `- domain-entities   - CONTRACTS_OVERVIEW   - STATUS_STATE_MACHINES`
- **Summary:** An agent-built QC worker in Phase 5 emits an unvalidated JSON structure for a corrupted take. Because no schema exists in `avf-contracts`, the workflo
- **Proposed Solution:** 1. Add `qc-request.schema.json` and `qc-result.schema.json` to `02_contracts/` containing typed properties: `technical_metrics` (decode_valid, duratio
- **Confidence:** `` (float 0..1), and `recommendation` (APPROVE, RETRY_TECHNICAL, RETRY_CREATIVE, HUMAN_REVIEW, REJECT).   2. Update `domain-entities.schema.json` to include `take` and `qcResult` entity definitions.   `

### F-R08-002: R08 Finding F-R08-002
- **Severity:** `HIGH`
- **Category:** `TEST_HARNESS_DEFECT`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R15_INTEGRATION_HARNESS.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.`
- **Affected Contracts:** `- provider-request   - provider-result   - STATUS_STATE_MACHINES`
- **Summary:** In production, a browser worker loses WebSocket connectivity mid-render. Because FakeProvider lacked a `worker_heartbeat_lost` scenario in CI, the wor
- **Proposed Solution:** Expand the FakeProvider scenario specification in `TEST_STRATEGY.md`, `R07_PROVIDER_SDK.md`, and `R15_INTEGRATION_HARNESS.md` from 8 to 14 standardize
- **Confidence:** `HIGH ````

### F-R08-003: R08 Finding F-R08-003
- **Severity:** `HIGH`
- **Category:** `VERIFICATION_GAP`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R15_INTEGRATION_HARNESS.md`
- **Affected Contracts:** `- STATUS_STATE_MACHINES   - domain-entities`
- **Summary:** A chaos test kills a worker after prompt submission. The worker reboots and re-submits the prompt, creating two parallel jobs on the provider. The tes
- **Proposed Solution:** Define a formal **Invariant Verification Matrix** in `TEST_STRATEGY.md` and `R15_INTEGRATION_HARNESS.md` mapping each chaos scenario to mandatory asse
- **Confidence:** `. Release gates cannot certify system reliability without automated invariant verification.`

### F-R08-004: R08 Finding F-R08-004
- **Severity:** `MEDIUM`
- **Category:** `INTEGRATION_VERIFICATION_GAP`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/E2E_INTEGRATION_PROTOCOL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/0`
- **Affected Contracts:** `- browser-command   - provider-result`
- **Summary:** A change is made to Track A error normalization for DOM timeouts. Because Suite B cannot run in headless CI without live Google accounts, the change i
- **Proposed Solution:** Add a `Mock Flow Target` fixture in `R15_INTEGRATION_HARNESS` consisting of:   1. A static local HTTP server serving simulated Google Flow web applica
- **Confidence:** `HIGH ````

### F-R08-005: R08 Finding F-R08-005
- **Severity:** `MEDIUM`
- **Category:** `REGRESSION_TESTING_DEFECT`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R15_INTEGRATION_HARNESS.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.`
- **Affected Contracts:** `- domain-entities   - provider-result`
- **Summary:** A prompt compiler refactor in `R05` subtly alters whitespace formatting. Golden fixture tests are run with unversioned ad-hoc scripts. The change alte
- **Proposed Solution:** 1. Define a standardized Golden Fixture schema in `avf-contracts`:      `fixtures/{domain}/{fixture_id}/input.json`, `expected_output.json`, `manifest
- **Confidence:** `HIGH ````

### F-R08-006: R08 Finding F-R08-006
- **Severity:** `NON_BLOCKING`
- **Category:** `CI_STABILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R15_INTEGRATION_HARNESS.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** An integration test asserts a 30-second generation timeout using real `sleep(30)` in a GitHub Actions runner. Due to CPU throttling on the CI runner, 
- **Proposed Solution:** Update `TEST_STRATEGY.md` with explicit flake control rules:   1. **Virtual Time Requirement:** Mandate the use of Temporal's `TestWorkflowEnvironment
- **Confidence:** `HIGH ````
