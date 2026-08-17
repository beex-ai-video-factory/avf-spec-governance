# RELEASE 01: FINAL PRE-RELEASE AUDIT
## AI Video Factory — Full System Forensic & Quality Signoff

**PROMPT_ID:** `REL-01`  
**PURPOSE:** Perform comprehensive forensic audit across all 15 repositories, all 6 integration gates, frozen baseline drift, and documentation before release tagging.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `GATE-05`  
**READ_ONLY_INPUTS:**
- `BASELINE.lock.json`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/repos/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`  
**PASS_CRITERIA:**
- 15/15 repositories released with passing test suites.
- 6/6 system gates passed.
- 0 bytes frozen baseline drift against lockfile.
- 0 security vulnerabilities or exposed secrets.  
**FAIL_CRITERIA:**
- Any failing test, missing gate, uncommitted change, or frozen baseline mutation.  
**GIT_EXPECTATION:** Clean working trees across all repos.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Baseline Integrity:**
   Assert 0 bytes drift against `BASELINE.lock.json`.
2. **Verify All 15 Repository Test Suites:**
   Execute full test suites across all 15 repositories.
3. **Verify All 6 Integration Gates:**
   Confirm that GATE-00 through GATE-05 are marked PASSED in `RUN_STATE.yaml`.
4. **Compile FINAL_RELEASE_AUDIT.md:**
   Document the pre-release audit verdict.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-01"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 150, failed: 0}
CONTRACT_TESTS: {passed: 50, failed: 0}
INTEGRATION_TESTS: {passed: 40, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md"
RECOMMENDED_NEXT_TASK: "Apply system release tags and publish packages."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
