# AI VIDEO FACTORY v1.0.0 — SESSION RESUMPTION TOOL
## Automatic State Reconciliation & Next Action Resolver

**PROMPT_ID:** `RESUME-01`  
**PURPOSE:** Inspect current implementation runtime state, verify cryptographic baseline integrity, and compute the exact next prompt command without modifying application code.  
**CURRENT_PHASE:** `SYSTEM_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<2 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `BASELINE.lock.json`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RUNBOOK_MANIFEST.yaml`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with verified timestamp.  
**PASS_CRITERIA:**
- Baseline integrity verified (0 bytes drift).
- Exact next prompt, workspace, model, and command identified and returned in standard YAML output.  
**FAIL_CRITERIA:**
- Frozen baseline drift detected or corrupt state file.  
**GIT_EXPECTATION:** No uncommitted changes in frozen paths.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md` or investigate drift.  
**NEXT_PROMPT_IF_PASS:** Exact first unpassed prompt computed from `RUN_STATE.yaml` (e.g. `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md`)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`

---

### Resumption Agent Instructions:

1. **Verify Baseline Integrity:** Check `BASELINE.lock.json` against `01_FROZEN_RELEASE/`. Assert 0 bytes drift.
2. **Read Runtime State:** Inspect `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`. If not present, initialize it from `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RUN_STATE_TEMPLATE.yaml`.
3. **Inspect Git Status:** Check which repos under `05_IMPLEMENTATION/repos/` have been initialized, committed, or tagged.
4. **Determine Exact Next Step:** Match the current progress against `RUNBOOK_MANIFEST.yaml` to identify the first unpassed prompt.
5. **Output Standard Contract:** Return standard YAML block indicating the exact command to run.

```yaml
PROMPT_ID: "RESUME-01"
RESULT: PASS
REPO: "SYSTEM"
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
RECOMMENDED_NEXT_TASK: "Execute the next scheduled implementation prompt."
HUMAN_INSTRUCTION: "Run the command specified in RECOMMENDED_NEXT_PROMPT."
```
