# CHECKPOINT 02: ENVIRONMENT DOCTOR AUDIT
## AI Video Factory — Toolchain & Runtime Environment Verification

**PROMPT_ID:** `CHK-02`  
**PURPOSE:** Execute the implementation environment doctor script, validating that Node.js, Python, Docker, Temporal CLI, FFmpeg, and Git toolchains satisfy all baseline requirements.  
**CURRENT_PHASE:** `00_CHECKPOINTS`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `CHK-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/environment/doctor.sh`
- `05_IMPLEMENTATION/environment/docker-compose.dev.yml`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Environment verification report in `RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- `doctor.sh` executes with 0 critical errors.
- Node.js (>= 20.x), Python (>= 3.10), Docker engine, FFmpeg, and Git are available.  
**FAIL_CRITERIA:**
- Missing required runtimes or doctor script returns exit code != 0.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md` to resolve missing dependencies.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_01_INSPECT_AND_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Execute Environment Doctor:**
   Run `bash 05_IMPLEMENTATION/environment/doctor.sh`.
2. **Verify Toolchain Versions:**
   Assert:
   - Node.js version >= 20.0.0
   - Python version >= 3.10.0
   - Git version >= 2.30.0
   - Docker / Container engine responsive
   - FFprobe / FFmpeg binary installed
3. **Record Result in State:**
   Update `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "CHK-02"
RESULT: PASS
REPO: "SYSTEM"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 5, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_01_INSPECT_AND_PLAN.md"
RECOMMENDED_NEXT_TASK: "Inspect repository registry and plan polyrepo layout."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
