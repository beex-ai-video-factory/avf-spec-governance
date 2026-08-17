# RECOVERY 08: ENVIRONMENT & DOCKER OUTAGE
## AI Video Factory — Infrastructure & Toolchain Repair

**PROMPT_ID:** `REC-08`  
**PURPOSE:** Diagnose and recover from Docker container failures, PostgreSQL connection outages, or missing runtime dependencies.  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/environment/**`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Restored docker services and verified doctor report.  
**PASS_CRITERIA:**
- Docker compose restart succeeds and `doctor.sh` passes 100%.  
**FAIL_CRITERIA:**
- Docker engine unresponsive.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Re-run `CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`.  
**HUMAN_ACTION_AFTER_FAIL:** Ensure Docker Desktop / engine is running.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`

---

### Step-by-Step Instructions:

1. **Restart Docker Compose Stack:**
   Run `docker compose -f 05_IMPLEMENTATION/environment/docker-compose.dev.yml down && docker compose -f 05_IMPLEMENTATION/environment/docker-compose.dev.yml up -d`.
2. **Re-run Doctor Check:**
   Execute `bash 05_IMPLEMENTATION/environment/doctor.sh`.
3. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-08"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 5, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md"
RECOMMENDED_NEXT_TASK: "Re-run environment doctor checkpoint."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
