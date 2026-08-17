# GATE 01: FAKEPROVIDER E2E WORKFLOW GATE
## AI Video Factory — Deterministic Single-Shot & Chaos Fault-Injection Gate

**PROMPT_ID:** `GATE-01`  
**PURPOSE:** Verify deterministic single-shot video generation workflow execution, Temporal replay safety, retry policies, and fault injection scenarios using FakeVideoProvider and R15 Integration Harness.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R15-04`, `R06-04`, `GATE-00`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R06_workflow/**`
- `05_IMPLEMENTATION/repos/R15_integration_harness/**`
- `05_IMPLEMENTATION/repos/R07_provider_sdk/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R06_workflow/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_01_FAKEPROVIDER_E2E_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_01: PASSED.  
**PASS_CRITERIA:**
- Deterministic single-shot workflow completes end-to-end against FakeVideoProvider.
- All 16 fault-injection scenarios execute and recover correctly (worker crash, uncertain submit, timeout, rate limit).
- Temporal workflow history asserts replay determinism.  
**FAIL_CRITERIA:**
- Temporal non-deterministic error, deadlock, unhandled exception, or failed chaos assertion.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute Deterministic Single-Shot Test:**
   Run the standard single-shot pipeline with FakeVideoProvider delay=0 and delay=30s.
2. **Execute 16 Fault-Injection Scenarios:**
   Run `R15_integration_harness` chaos test suite. Assert:
   - Worker kill before submit: Workflow resumes and submits cleanly.
   - Worker kill after submit: Reconciles remote generation status without double submission.
   - Corrupt video payload: Quarantine DLQ triggered.
3. **Assert Temporal Replay Safety:**
   Verify workflow execution history against replay runner.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-01"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 16, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 16, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R08 Google Flow Adapter implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
