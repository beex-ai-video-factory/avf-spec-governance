# GATE 00: FOUNDATION INTEGRATION GATE
## AI Video Factory — Contracts, State, SDK & Observability Validation

**PROMPT_ID:** `GATE-00`  
**PURPOSE:** Validate cross-repository integration between R01 Contracts, R14 Platform Observability, R02 Core State, and R07 Provider SDK in a clean environment before orchestrator implementation.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-8 min)`  
**PREREQUISITES:** `R07-04`, `R02-04`, `R14-04`, `R01-04`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R01_contracts/**`
- `05_IMPLEMENTATION/repos/R02_core_state/**`
- `05_IMPLEMENTATION/repos/R07_provider_sdk/**`
- `05_IMPLEMENTATION/repos/R14_platform_observability/**`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/04_integration/TEST_STRATEGY.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R01_contracts/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_00: PASSED.  
**PASS_CRITERIA:**
- PostgreSQL migrations apply cleanly.
- Domain entities validate against R01 JSON schemas.
- Idempotency store asserts unique constraint on idempotency keys.
- FakeVideoProvider generates simulated completions and error matrices.
- OpenTelemetry traces propagate correlation context without leaking secrets.  
**FAIL_CRITERIA:**
- Schema validation error, database connection failure, or secret leakage in logs.  
**GIT_EXPECTATION:** Clean working tree across R01, R02, R07, R14.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Verify Database Initialization:**
   Ensure PostgreSQL is running and apply R02 migrations.
2. **Execute Cross-Contract Test Suite:**
   Assert schema compliance between R02 domain events and R01 JSON schemas.
3. **Execute FakeVideoProvider Simulation:**
   Run simulated generation requests through R07 Provider SDK.
4. **Assert Telemetry Context & Secret Scrubbing:**
   Verify that OTel spans from R14 are attached and contain zero unredacted tokens.
5. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-00"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 24, failed: 0}
CONTRACT_TESTS: {passed: 12, failed: 0}
INTEGRATION_TESTS: {passed: 8, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R06 Temporal Workflow implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
