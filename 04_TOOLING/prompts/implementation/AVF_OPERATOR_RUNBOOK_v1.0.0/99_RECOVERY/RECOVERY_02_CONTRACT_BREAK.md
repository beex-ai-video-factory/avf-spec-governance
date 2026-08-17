# RECOVERY 02: CONTRACT BREAK & SCHEMA INCOMPATIBILITY
## AI Video Factory — Contract Dispute Triage & Resolution

**PROMPT_ID:** `REC-02`  
**PURPOSE:** Resolve a contract schema discrepancy or typing incompatibility between two communicating repositories.  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/02_contracts/**`
- `05_IMPLEMENTATION/repos/R01_contracts/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R01_contracts/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/change-requests/**`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Contract analysis report and resolution path.  
**PASS_CRITERIA:**
- Root cause identified: Consumer typing error vs R01 contract defect.
- If consumer error: route back to consumer implementation prompt.
- If R01 defect: route to R01 update or formal Change Request.  
**FAIL_CRITERIA:**
- Direct modification of frozen baseline or bypass of contract schemas.  
**GIT_EXPECTATION:** Clean state tracking.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned prompt.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to system architect.  
**NEXT_PROMPT_IF_PASS:** Exact remediation prompt (Consumer defect -> `05_IMPLEMENTATION/repos/<consumer>/...`; R01 contract defect -> `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/02_R01_CONTRACTS/R01_02_IMPLEMENT.md`)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---


> [!IMPORTANT]
> **AUTONOMOUS RECOVERY MANDATE:**
> The recovery agent MUST compare schema vs payload, isolate consumer non-conformance vs R01 contract defect, and emit the EXACT remediation prompt in `RECOMMENDED_NEXT_PROMPT`.

### Step-by-Step Recovery Instructions:

1. **Compare Consumer Payload against R01 JSON Schemas:**
   Validate whether the issue is consumer non-conformance or an R01 schema bug.
2. **If Consumer Bug:**
   Route to consumer repo `<REPO>_02_IMPLEMENT.md`.
3. **If R01 Bug:**
   Route to `02_R01_CONTRACTS/R01_02_IMPLEMENT.md` to patch R01.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-02"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 1, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Execute targeted contract remediation prompt."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
