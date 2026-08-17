# RECOVERY 04: TEST GATE FAILURE
## AI Video Factory — Unit, Conformance & Coverage Remediation

**PROMPT_ID:** `REC-04`  
**PURPOSE:** Diagnose and repair failing unit tests, broken negative fixtures, or insufficient code coverage in a repository.  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Test diagnostics and code fixes in affected repository.  
**PASS_CRITERIA:**
- Failing tests identified and resolved without lowering coverage thresholds or deleting assertions.  
**FAIL_CRITERIA:**
- Masking errors by skipping tests.  
**GIT_EXPECTATION:** Clean test fix commit.  
**HUMAN_ACTION_AFTER_PASS:** Re-run the review prompt for the affected repository.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human developer.  
**NEXT_PROMPT_IF_PASS:** Exact test and review prompt for affected repository (`04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/<REPO_DIR>/<REPO>_03_TEST_AND_REVIEW.md`)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---


> [!IMPORTANT]
> **AUTONOMOUS RECOVERY MANDATE:**
> The recovery agent MUST resolve test failures and emit the exact review prompt `<REPO>_03_TEST_AND_REVIEW.md` in `RECOMMENDED_NEXT_PROMPT`.

### Step-by-Step Instructions:

1. **Analyze Test Failure Logs:**
   Inspect test runner output to identify root cause.
2. **Apply Targeted Code Fix:**
   Repair implementation logic in `src/`.
3. **Re-run Test Suite:**
   Assert 100% pass rate.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-04"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 10, failed: 0}
CONTRACT_TESTS: {passed: 5, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Re-run review prompt for affected repository."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
