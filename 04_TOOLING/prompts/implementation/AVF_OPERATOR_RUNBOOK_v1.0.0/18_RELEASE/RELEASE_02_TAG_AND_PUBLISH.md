# RELEASE 02: TAG AND PUBLISH SYSTEM RELEASE
## AI Video Factory — Release Tagging & Package Publishing

**PROMPT_ID:** `REL-02`  
**PURPOSE:** Apply the unified system git release tag v1.0.0, publish the R01 Contracts npm package, and finalize release metadata.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `REL-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/repos/**`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- System release tag `avf-v1.0.0` applied.
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- System release tag applied across repositories.
- R01 contracts package built and prepared for publication.  
**FAIL_CRITERIA:**
- Tagging failure or package build error.  
**GIT_EXPECTATION:** Annotated release tags pushed to remotes.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Build Distribution Packages:**
   Build R01 contracts bundle.
2. **Apply Unified Release Tag:**
   Tag the workspace and repositories with `avf-v1.0.0`.
3. **Record Release State:**
   Update `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with release version `1.0.0`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-02"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 10, failed: 0}
INTEGRATION_TESTS: {passed: 5, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md"
RECOMMENDED_NEXT_TASK: "Execute final post-release smoke verification."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
