# R06 TEMPORAL WORKFLOW ORCHESTRATOR — ACCEPTANCE & RELEASE
## AI Video Factory — Formal Acceptance, Merge & Version Tagging

**PROMPT_ID:** `R06-04`  
**PURPOSE:** Conduct formal acceptance signoff for R06_workflow (Temporal Workflow Orchestrator), merge feature branch to main, apply annotated git release tag, and unlock downstream dependency gates.  
**CURRENT_PHASE:** `05_R06_WORKFLOW`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R06_workflow`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R06_workflow`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `R06-03`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R06_workflow/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/repos/R06_workflow/PLAN.md`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R06_WORKFLOW.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R06_workflow/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R06_workflow/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R06_workflow )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_04_ACCEPT_RELEASE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Released `main` branch with annotated release tag `v1.0.0`
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- All tests pass on `main`.
- Clean merge commit and git tag `r06_workflow-v1.0.0` applied.
- Repository status marked as `RELEASED` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Merge conflict, uncommitted changes, or failing CI checks.  
**GIT_EXPECTATION:** Tagged release commit on `main`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `05_R06_WORKFLOW/R06_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/06_R15_INTEGRATION_HARNESS/R15_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Verify Audit Signoff:**
   Inspect `05_IMPLEMENTATION/repos/R06_workflow/AUDIT_REPORT.md` and confirm PASS verdict.
2. **Merge to Main Branch:**
   Checkout `main` and merge `feature/r06-impl` cleanly:
   `git checkout main && git merge --no-ff feature/r06-impl -m "feat(r06): complete R06_workflow implementation"`
3. **Apply Release Tag:**
   Apply annotated git tag:
   `git tag -a "r06_workflow-v1.0.0" -m "Release R06_workflow v1.0.0"`
4. **Update System Runtime State:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `R06_workflow.status: "RELEASED"` and record commit SHA and tag.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R06-04"
RESULT: PASS
REPO: "R06_workflow"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 18, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R06_workflow/ (tagged r06_workflow-v1.0.0)"
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/06_R15_INTEGRATION_HARNESS/R15_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Proceed to next scheduled prompt in master execution sequence."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
