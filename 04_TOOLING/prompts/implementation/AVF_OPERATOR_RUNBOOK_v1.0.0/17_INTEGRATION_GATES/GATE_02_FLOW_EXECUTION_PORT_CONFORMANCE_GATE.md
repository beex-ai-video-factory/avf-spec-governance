# GATE 02: FLOW EXECUTION PORT CONFORMANCE GATE
## AI Video Factory — Track A (Browser) vs Track B (Direct Protocol) Conformance

**PROMPT_ID:** `GATE-02`  
**PURPOSE:** Run comparative 10-operation FlowExecutionPort benchmark testing Track A (R09 Browser Worker) and Track B (R10 FlowKit Bridge) via R08 Google Flow Adapter to verify semantic equivalence.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R09-04`, `R10-04`, `R08-04`, `GATE-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/**`
- `05_IMPLEMENTATION/repos/R09_browser_worker/**`
- `05_IMPLEMENTATION/repos/R10_flowkit_bridge/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R08_google_flow_adapter/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_02: PASSED.  
**PASS_CRITERIA:**
- Both Track A and Track B implement all 10 operations of `FlowExecutionPort`.
- Conformance suite yields identical semantic outputs for identical inputs.
- Normalized error taxonomy correctly maps HTTP 429, auth expiration, and UI changes.  
**FAIL_CRITERIA:**
- Missing operation, output contract discrepancy, or leaky abstractions between tracks.  
**GIT_EXPECTATION:** Clean working tree across R08, R09, R10.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/10_R03_CREATIVE/R03_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute FlowExecutionPort Conformance Suite against Track B (FlowKit Bridge):**
   Verify all 10 operations against mocked protocol endpoint.
2. **Execute FlowExecutionPort Conformance Suite against Track A (Browser Worker):**
   Verify Playwright/CDP automation with 4-tier selector resolution.
3. **Compare Equivalence:**
   Assert that `FlowExecutionResult` discriminated unions match 100%.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-02"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 20, failed: 0}
CONTRACT_TESTS: {passed: 10, failed: 0}
INTEGRATION_TESTS: {passed: 10, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/10_R03_CREATIVE/R03_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R03 Creative & Script Generation implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
