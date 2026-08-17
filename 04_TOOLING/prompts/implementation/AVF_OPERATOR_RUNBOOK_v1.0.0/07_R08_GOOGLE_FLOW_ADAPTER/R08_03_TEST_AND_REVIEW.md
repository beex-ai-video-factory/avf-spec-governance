# R08 GOOGLE FLOW PROVIDER ADAPTER — INDEPENDENT TECHNICAL REVIEW & AUDIT
## AI Video Factory — Negative Testing, Security & Boundary Conformance

**PROMPT_ID:** `R08-03`  
**PURPOSE:** Perform an independent technical audit of R08_google_flow_adapter (Google Flow Provider Adapter), executing negative test suites, contract compatibility checks, secret redaction validation, and dependency boundary verification.  
**CURRENT_PHASE:** `07_R08_GOOGLE_FLOW_ADAPTER`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R08_google_flow_adapter`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R08_google_flow_adapter`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (3-5 min)`  
**PREREQUISITES:** `R08-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/PLAN.md`
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/src/**`
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/tests/**`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R08_google_flow_adapter/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R08_google_flow_adapter )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_03_TEST_AND_REVIEW.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/AUDIT_REPORT.md`  
**PASS_CRITERIA:**
- Zero forbidden imports detected (scanned against: R02, R03, R04, R05, R06, Direct DB).
- Branch test coverage >= 85%.
- Negative fixtures correctly trigger normalized error responses.
- Observability and secret redaction verified.  
**FAIL_CRITERIA:**
- Boundary leak, uncovered critical path, secret leakage, or failed contract assertions.  
**GIT_EXPECTATION:** Audit report committed on branch.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `07_R08_GOOGLE_FLOW_ADAPTER/R08_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_04_ACCEPT_RELEASE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Dependency Boundary Scan:**
   Run static grep search across `05_IMPLEMENTATION/repos/R08_google_flow_adapter/src/` to confirm zero forbidden imports.
2. **Execute Full Test & Negative Fixture Suite:**
   Run all positive, negative, and edge-case unit and contract tests.
3. **Verify Observability & Redaction:**
   Confirm that all telemetry integration masks sensitive credentials and attaches trace contexts.
4. **Compile AUDIT_REPORT.md:**
   Document test metrics, boundary scan results, and final verification signoff.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R08-03"
RESULT: PASS
REPO: "R08_google_flow_adapter"
BRANCH: "feature/r08-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 18, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R08_google_flow_adapter/AUDIT_REPORT.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_04_ACCEPT_RELEASE.md"
RECOMMENDED_NEXT_TASK: "Execute formal acceptance and release tagging for R08_google_flow_adapter."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
