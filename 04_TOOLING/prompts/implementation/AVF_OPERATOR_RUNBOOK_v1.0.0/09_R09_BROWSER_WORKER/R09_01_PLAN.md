# R09 TRACK A BROWSER AUTOMATION WORKER — IMPLEMENTATION PLAN
## AI Video Factory — Architectural Specification & Test Plan

**PROMPT_ID:** `R09-01`  
**PURPOSE:** Create the complete architectural implementation and test plan for R09_browser_worker (Track A Browser Automation Worker) adhering to all 16 blueprint sections without authoring production code.  
**CURRENT_PHASE:** `09_R09_BROWSER_WORKER`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R09_browser_worker`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R09_browser_worker`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `R10-04`  
**READ_ONLY_INPUTS:**
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R09_BROWSER_WORKER.md`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R09_browser_worker/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R09_browser_worker/PLAN.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R09_browser_worker )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_01_PLAN.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/R09_browser_worker/PLAN.md`  
**PASS_CRITERIA:**
- PLAN.md covers all 16 blueprint sections from `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R09_BROWSER_WORKER.md`.
- Specific boundaries respected: OWNS: Playwright/CDP automation implementing 10-operation FlowExecutionPort, 4-tier selector resolution (DOM, A11y, Visual, Agent Recovery), anti-abuse safety; DOES NOT OWN: Direct DB, direct API bridge, workflow state.
- Allowed dependencies: R01_contracts, R14_platform_observability; Forbidden dependencies: R02, R03, R04, R05, R06, R07, R08, R10, R11, R12, R13, Direct DB.
- Test strategy defines >=85% coverage and contract conformance.
- Zero production code authored in this planning step.  
**FAIL_CRITERIA:**
- Missing blueprint sections or production source files written during planning.  
**GIT_EXPECTATION:** Plan committed on feature branch `feature/r09-scaffold`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `09_R09_BROWSER_WORKER/R09_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_02_IMPLEMENT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Inspect Blueprint & Contracts:**
   Read `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R09_BROWSER_WORKER.md` and examine referenced schemas.
2. **Review Specific Hardening Requirements:**
   Strict anti-abuse safety, human gate escalation on CAPTCHA/challenge, session isolation.
3. **Formulate PLAN.md:**
   Write `05_IMPLEMENTATION/repos/R09_browser_worker/PLAN.md` detailing:
   - Module architecture and component breakdown
   - TypeScript interfaces / schemas
   - State ownership, persistence, and concurrency models
   - Error taxonomy & retry policy
   - Observability integration (via R14)
   - Comprehensive test plan (unit, contract, negative)
   - Definition of Done checklist
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R09-01"
RESULT: PASS
REPO: "R09_browser_worker"
BRANCH: "feature/r09-scaffold"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 0, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R09_browser_worker/PLAN.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_02_IMPLEMENT.md"
RECOMMENDED_NEXT_TASK: "Implement R09_browser_worker application code and unit/contract test suites."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
