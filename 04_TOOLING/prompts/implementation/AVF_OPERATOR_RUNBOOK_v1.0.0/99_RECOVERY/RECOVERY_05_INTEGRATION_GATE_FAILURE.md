# RECOVERY 05: INTEGRATION GATE FAILURE
## AI Video Factory — Cross-Repository Integration Triage

**PROMPT_ID:** `REC-05`  
**PURPOSE:** Triage and isolate failures occurring during cross-repository system integration gates (GATE-00 through GATE-05).  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<5 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Integration gate diagnostic report.  
**PASS_CRITERIA:**
- Responsible component isolated and remediation prompt identified.  
**FAIL_CRITERIA:**
- Unclear root cause.  
**GIT_EXPECTATION:** State preserved cleanly.  
**HUMAN_ACTION_AFTER_PASS:** Execute the targeted remediation prompt.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human lead.  
**NEXT_PROMPT_IF_PASS:** Exact remediation prompt for isolated faulty component (e.g. `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/03_R02_CORE_STATE/R02_02_IMPLEMENT.md`)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---


> [!IMPORTANT]
> **AUTONOMOUS RECOVERY MANDATE:**
> The recovery agent MUST analyze integration traces, isolate the failing component, and output its EXACT implementation prompt path in `RECOMMENDED_NEXT_PROMPT`.

### Step-by-Step Instructions:

1. **Inspect Integration Traces:**
   Read error logs from the failed integration gate.
2. **Isolate Faulty Component:**
   Determine whether the fault is state persistence (R02), workflow retry logic (R06), provider adapter (R08), or QC (R11).
3. **Route to Component Fix:**
   Return the implementation fix prompt for the faulty component.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-05"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Remediate isolated component defect."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
