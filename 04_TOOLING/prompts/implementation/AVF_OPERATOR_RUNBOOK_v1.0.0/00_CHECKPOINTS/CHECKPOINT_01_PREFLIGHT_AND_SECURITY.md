# CHECKPOINT 01: PREFLIGHT & SECURITY AUDIT
## AI Video Factory — Pre-Implementation Baseline Verification

**PROMPT_ID:** `CHK-01`  
**PURPOSE:** Verify cryptographic baseline integrity against BASELINE.lock.json, confirm zero frozen mutation drift, verify workspace cleanliness, and ensure zero unredacted secrets exist before commencing implementation.  
**CURRENT_PHASE:** `00_CHECKPOINTS`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<2 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `BASELINE.lock.json`
- `PROJECT.md`
- `00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md`
- `01_FROZEN_RELEASE/v1.0.0/CONTENT_HASHES.json`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` (Phase 00 recorded as verified).  
**PASS_CRITERIA:**
- All 60/60 files in `01_FROZEN_RELEASE/v1.0.0/` match exact SHA-256 hashes.
- Frozen baseline mutation drift is exactly 0.
- Secrets scan reveals 0 unredacted tokens, API keys, or credentials.  
**FAIL_CRITERIA:**
- Hash mismatch in any frozen specification file or unredacted secret found.  
**GIT_EXPECTATION:** Clean working tree in frozen paths.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Do NOT proceed. Run `99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Baseline Hashes:**
   Run hash verification across `01_FROZEN_RELEASE/v1.0.0/` against `BASELINE.lock.json`. Confirm that the content tree hash matches `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846`.
2. **Perform Automated Secret Scan:**
   Scan workspace text files for accidental API keys, tokens, or private credentials. Confirm 0 violations.
3. **Initialize Runtime State:**
   Ensure `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` is active and record `CHK-01` as PASSED.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "CHK-01"
RESULT: PASS
REPO: "SYSTEM"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 2, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md"
RECOMMENDED_NEXT_TASK: "Execute development environment doctor check."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
