# R04 ASSETS & CHARACTER CONTINUITY SERVICE — IMPLEMENTATION & BUILD
## AI Video Factory — Source Code Authoring & Test Suite Implementation

**PROMPT_ID:** `R04-02`  
**PURPOSE:** Implement all production source code, build toolchains, unit tests, and contract fixtures for R04_assets_continuity (Assets & Character Continuity Service) according to the approved PLAN.md.  
**CURRENT_PHASE:** `11_R04_ASSETS_CONTINUITY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R04_assets_continuity`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R04_assets_continuity`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R04-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R04_assets_continuity/PLAN.md`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R04_ASSETS_CONTINUITY.md`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R04_assets_continuity/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R04_assets_continuity/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R04_assets_continuity )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_02_IMPLEMENT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Production source code in `05_IMPLEMENTATION/repos/R04_assets_continuity/src/`
- Test suites in `05_IMPLEMENTATION/repos/R04_assets_continuity/tests/`
- Build script passing cleanly (`npm test` / `pytest`).  
**PASS_CRITERIA:**
- All components in PLAN.md fully implemented without placeholder stubs.
- OWNS boundaries strictly enforced: Asset catalog service, character reference embedding management, continuity token injection.
- Zero forbidden dependencies imported: R03, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB.
- Unit and contract tests execute and pass 100%.  
**FAIL_CRITERIA:**
- Build compilation failure, test failures, or cross-repo file modifications.  
**GIT_EXPECTATION:** Clean commits on feature branch `feature/r04-impl`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `11_R04_ASSETS_CONTINUITY/R04_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_03_TEST_AND_REVIEW.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Implement Core Components:**
   Author production modules in `src/` satisfying all architectural responsibilities.
2. **Implement Test Suites:**
   Build unit and contract test suites under `tests/`.
3. **Execute Local Build & Tests:**
   Run test suites and verify 100% pass rate with zero lint/type errors.
4. **Git Commit:**
   Commit all changes to `feature/r04-impl`.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R04-02"
RESULT: PASS
REPO: "R04_assets_continuity"
BRANCH: "feature/r04-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 12, failed: 0}
CONTRACT_TESTS: {passed: 6, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R04_assets_continuity/src/"
  - "05_IMPLEMENTATION/repos/R04_assets_continuity/tests/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_03_TEST_AND_REVIEW.md"
RECOMMENDED_NEXT_TASK: "Execute independent technical and adversarial review of R04_assets_continuity."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
