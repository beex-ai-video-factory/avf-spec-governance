# R11 QUALITY CONTROL & VALIDATION SERVICE — IMPLEMENTATION & BUILD
## AI Video Factory — Source Code Authoring & Test Suite Implementation

**PROMPT_ID:** `R11-02`  
**PURPOSE:** Implement all production source code, build toolchains, unit tests, and contract fixtures for R11_qc (Quality Control & Validation Service) according to the approved PLAN.md.  
**CURRENT_PHASE:** `13_R11_QC`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R11_qc`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R11_qc`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R11-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R11_qc/PLAN.md`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R11_QC.md`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R11_qc/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R11_qc/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R11_qc )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_02_IMPLEMENT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Production source code in `05_IMPLEMENTATION/repos/R11_qc/src/`
- Test suites in `05_IMPLEMENTATION/repos/R11_qc/tests/`
- Build script passing cleanly (`npm test` / `pytest`).  
**PASS_CRITERIA:**
- All components in PLAN.md fully implemented without placeholder stubs.
- OWNS boundaries strictly enforced: Technical QC (FFprobe container, stream, resolution, framerate, duration check), Semantic QC (LLM/Vision scoring), bounded retry decision output.
- Zero forbidden dependencies imported: R02, R03, R04, R05, R06, R07, R08, R09, R10, R12, R13, Direct DB.
- Unit and contract tests execute and pass 100%.  
**FAIL_CRITERIA:**
- Build compilation failure, test failures, or cross-repo file modifications.  
**GIT_EXPECTATION:** Clean commits on feature branch `feature/r11-impl`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `13_R11_QC/R11_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_03_TEST_AND_REVIEW.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Implement Core Components:**
   Author production modules in `src/` satisfying all architectural responsibilities.
2. **Implement Test Suites:**
   Build unit and contract test suites under `tests/`.
3. **Execute Local Build & Tests:**
   Run test suites and verify 100% pass rate with zero lint/type errors.
4. **Git Commit:**
   Commit all changes to `feature/r11-impl`.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R11-02"
RESULT: PASS
REPO: "R11_qc"
BRANCH: "feature/r11-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 12, failed: 0}
CONTRACT_TESTS: {passed: 6, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R11_qc/src/"
  - "05_IMPLEMENTATION/repos/R11_qc/tests/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_03_TEST_AND_REVIEW.md"
RECOMMENDED_NEXT_TASK: "Execute independent technical and adversarial review of R11_qc."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
