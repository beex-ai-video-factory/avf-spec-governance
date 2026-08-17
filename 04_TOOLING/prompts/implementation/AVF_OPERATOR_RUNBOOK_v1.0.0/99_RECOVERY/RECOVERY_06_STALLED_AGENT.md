# RECOVERY 06: STALLED OR LOOPING AGENT
## AI Video Factory — Session Reset & Context Restoration

**PROMPT_ID:** `REC-06`  
**PURPOSE:** Reset a stalled, looping, or hallucinating agent conversation, restoring execution from clean git checkpoints without data loss.  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `FAST (<2 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Cleaned state and clear resume instruction.  
**PASS_CRITERIA:**
- Uncorrupted git state verified.
- Exact prompt to restart returned for execution in a fresh conversation.  
**FAIL_CRITERIA:**
- Corrupt working directory.  
**GIT_EXPECTATION:** Clean checkout of last stable commit.  
**HUMAN_ACTION_AFTER_PASS:** Open a BRAND NEW conversation and run `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** Exact restart prompt path based on last uncompleted task in `RUN_STATE.yaml`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---


> [!IMPORTANT]
> **AUTONOMOUS RECOVERY MANDATE:**
> The recovery agent MUST inspect `RUN_STATE.yaml` and return the EXACT prompt command in `RECOMMENDED_NEXT_PROMPT` to restart in a fresh conversation.

### Step-by-Step Instructions:

1. **Inspect Working Tree:**
   Verify git status across all 15 repositories.
2. **Determine Last Stable Prompt:**
   Read `last_passed_prompt_id` from `RUN_STATE.yaml`.
3. **Instruct Fresh Conversation Launch:**
   Provide the single `/goal` command to run in a fresh chat window.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-06"
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
RECOMMENDED_NEXT_TASK: "Re-run the current prompt in a brand new conversation."
HUMAN_INSTRUCTION: "Open a NEW conversation window and run the command in RECOMMENDED_NEXT_PROMPT."
```
