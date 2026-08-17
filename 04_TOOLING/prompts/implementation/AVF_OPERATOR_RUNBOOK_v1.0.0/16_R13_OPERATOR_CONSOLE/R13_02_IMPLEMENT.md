# R13 HUMAN-IN-THE-LOOP OPERATOR CONSOLE — IMPLEMENTATION & BUILD
## AI Video Factory — Source Code Authoring & Test Suite Implementation

**PROMPT_ID:** `R13-02`  
**PURPOSE:** Implement all production source code, build toolchains, unit tests, and contract fixtures for R13_operator_console (Human-in-the-Loop Operator Console) according to the approved PLAN.md.  
**CURRENT_PHASE:** `16_R13_OPERATOR_CONSOLE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R13_operator_console`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R13_operator_console`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R13-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R13_operator_console/PLAN.md`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R13_operator_console/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R13_operator_console/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R13_operator_console )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_02_IMPLEMENT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Production source code in `05_IMPLEMENTATION/repos/R13_operator_console/src/`
- Test suites in `05_IMPLEMENTATION/repos/R13_operator_console/tests/`
- Build script passing cleanly (`npm test` / `pytest`).  
**PASS_CRITERIA:**
- All components in PLAN.md fully implemented without placeholder stubs.
- OWNS boundaries strictly enforced: Operator UI web application for human approval gates, generation inspection, error triage, DLQ replay triggers.
- Zero forbidden dependencies imported: R03, R04, R05, R07, R08, R09, R10, R11, R12, R15, Direct DB, Worker Internals.
- Unit and contract tests execute and pass 100%.  
**FAIL_CRITERIA:**
- Build compilation failure, test failures, or cross-repo file modifications.  
**GIT_EXPECTATION:** Clean commits on feature branch `feature/r13-impl`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `16_R13_OPERATOR_CONSOLE/R13_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_03_TEST_AND_REVIEW.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Implement Core Components:**
   Author production modules in `src/` satisfying all architectural responsibilities.
2. **Implement Test Suites:**
   Build unit and contract test suites under `tests/`.
3. **Execute Local Build & Tests:**
   Run test suites and verify 100% pass rate with zero lint/type errors.
4. **Git Commit:**
   Commit all changes to `feature/r13-impl`.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R13-02"
RESULT: PASS
REPO: "R13_operator_console"
BRANCH: "feature/r13-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 12, failed: 0}
CONTRACT_TESTS: {passed: 6, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R13_operator_console/src/"
  - "05_IMPLEMENTATION/repos/R13_operator_console/tests/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_03_TEST_AND_REVIEW.md"
RECOMMENDED_NEXT_TASK: "Execute independent technical and adversarial review of R13_operator_console."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
