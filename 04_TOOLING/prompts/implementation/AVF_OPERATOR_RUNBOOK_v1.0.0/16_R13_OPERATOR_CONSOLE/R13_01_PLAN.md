# R13 HUMAN-IN-THE-LOOP OPERATOR CONSOLE — IMPLEMENTATION PLAN
## AI Video Factory — Architectural Specification & Test Plan

**PROMPT_ID:** `R13-01`  
**PURPOSE:** Create the complete architectural implementation and test plan for R13_operator_console (Human-in-the-Loop Operator Console) adhering to all 16 blueprint sections without authoring production code.  
**CURRENT_PHASE:** `16_R13_OPERATOR_CONSOLE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R13_operator_console`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R13_operator_console`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `GATE-03`  
**READ_ONLY_INPUTS:**
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R13_operator_console/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R13_operator_console/PLAN.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R13_operator_console )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_01_PLAN.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/R13_operator_console/PLAN.md`  
**PASS_CRITERIA:**
- PLAN.md covers all 16 blueprint sections from `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md`.
- Specific boundaries respected: OWNS: Operator UI web application for human approval gates, generation inspection, error triage, DLQ replay triggers; DOES NOT OWN: Direct database mutations, worker execution internals.
- Allowed dependencies: R01_contracts, R02_core_state (API), R06_workflow (API), R14_platform_observability; Forbidden dependencies: R03, R04, R05, R07, R08, R09, R10, R11, R12, R15, Direct DB, Worker Internals.
- Test strategy defines >=85% coverage and contract conformance.
- Zero production code authored in this planning step.  
**FAIL_CRITERIA:**
- Missing blueprint sections or production source files written during planning.  
**GIT_EXPECTATION:** Plan committed on feature branch `feature/r13-scaffold`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `16_R13_OPERATOR_CONSOLE/R13_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_02_IMPLEMENT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Inspect Blueprint & Contracts:**
   Read `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md` and examine referenced schemas.
2. **Review Specific Hardening Requirements:**
   Web UI interacting strictly via R02 Core State REST/gRPC and R06 Temporal client APIs.
3. **Formulate PLAN.md:**
   Write `05_IMPLEMENTATION/repos/R13_operator_console/PLAN.md` detailing:
   - Module architecture and component breakdown
   - TypeScript interfaces / schemas
   - State ownership, persistence, and concurrency models
   - Error taxonomy & retry policy
   - Observability integration (via R14)
   - Comprehensive test plan (unit, contract, negative)
   - Definition of Done checklist
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R13-01"
RESULT: PASS
REPO: "R13_operator_console"
BRANCH: "feature/r13-scaffold"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 0, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R13_operator_console/PLAN.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_02_IMPLEMENT.md"
RECOMMENDED_NEXT_TASK: "Implement R13_operator_console application code and unit/contract test suites."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
