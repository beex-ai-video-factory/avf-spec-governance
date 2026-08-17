# RELEASE 03: POST-RELEASE VERIFICATION
## AI Video Factory — Final System Acceptance & Operations Handoff

**PROMPT_ID:** `REL-03`  
**PURPOSE:** Execute post-release smoke tests, verify production health checks, and finalize the operator implementation journey.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `REL-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Final updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` (Status: COMPLETE).  
**PASS_CRITERIA:**
- All health check endpoints responsive.
- All 15 repositories verified at release tag v1.0.0.
- System operational handoff complete.  
**FAIL_CRITERIA:**
- Health check failure.  
**GIT_EXPECTATION:** Clean working trees.  
**HUMAN_ACTION_AFTER_PASS:** Implementation is 100% complete! Proceed to production operations.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `TERMINAL_COMPLETE`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Health Endpoints:**
   Ping Core State, Workflow worker, and Operator Console health endpoints.
2. **Mark Run State as Complete:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `current_execution.status: "COMPLETE"`.
3. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-03"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 10, failed: 0}
CONTRACT_TESTS: {passed: 5, failed: 0}
INTEGRATION_TESTS: {passed: 5, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "TERMINAL_COMPLETE"
RECOMMENDED_NEXT_TASK: "AI Video Factory v1.0.0 implementation is 100% complete."
HUMAN_INSTRUCTION: "All 15 repositories and 6 gates have passed. System is ready for production."
```
