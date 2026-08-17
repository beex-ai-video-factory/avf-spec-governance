# GATE 05: CONTROLLED LIVE FLOW GATE
## AI Video Factory — Live Google Flow Generation Smoke Verification

**PROMPT_ID:** `GATE-05`  
**PURPOSE:** Execute a controlled, bounded live video generation smoke test against the live Google Flow provider, verifying session management, anti-abuse safety, and download pipelines.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `FAST (<5 min)`  
**PREREQUISITES:** `GATE-04`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_05: PASSED.  
**PASS_CRITERIA:**
- Live single-shot request submits, polls status, and downloads generated video without error.
- If a security challenge / CAPTCHA occurs, system safely halts and escalates to operator (mapped to valid test pass).
- No unhandled exceptions or anti-abuse bypass attempts.  
**FAIL_CRITERIA:**
- Unhandled network crash or unauthorized attempt to bypass provider security controls.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md`

---

### Step-by-Step Verification Instructions:

1. **Verify Credentials:**
   Check availability of Google Flow testing credentials.
2. **Execute Single-Shot Smoke Test:**
   Submit a minimal test prompt to Google Flow.
3. **Assert Video Download & QC:**
   Verify that output MP4 is downloaded and technical QC inspects valid container stream.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-05"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 1, failed: 0}
INTEGRATION_TESTS: {passed: 1, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md"
RECOMMENDED_NEXT_TASK: "Execute final full-system pre-release audit."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
