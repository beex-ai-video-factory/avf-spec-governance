# GATE 04: FULL SYSTEM INTEGRATION GATE
## AI Video Factory — Complete 15-Repository Offline System Simulation

**PROMPT_ID:** `GATE-04`  
**PURPOSE:** Execute full-system end-to-end integration across all 15 repositories (R01 through R15) in local docker environment with human-in-the-loop Operator Console review.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R13-04`, `GATE-03`, `GATE-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/environment/docker-compose.dev.yml`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_04_SYSTEM_INTEGRATION_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_04: PASSED.  
**PASS_CRITERIA:**
- All 15 repositories compile, link, and interact seamlessly.
- Complete multi-shot project generation workflow completes with simulated human approval in R13.
- Zero architectural boundary leaks and zero direct database access outside R02.  
**FAIL_CRITERIA:**
- System deadlock, missing cross-repo contract, or runtime failure.  
**GIT_EXPECTATION:** Clean working trees across all 15 repos.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Start System Stack:**
   Launch all backing services via Docker Compose.
2. **Execute Full E2E Scenario:**
   Run complete multi-shot generation simulation from narrative input to stitched video export.
3. **Simulate Operator Console Actions:**
   Approve generation checkpoints via R13 REST API.
4. **Assert End-to-End Metrics:**
   Verify trace spans and Prometheus metrics.
5. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-04"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 30, failed: 0}
CONTRACT_TESTS: {passed: 15, failed: 0}
INTEGRATION_TESTS: {passed: 15, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md"
RECOMMENDED_NEXT_TASK: "Execute controlled live Google Flow provider verification."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
