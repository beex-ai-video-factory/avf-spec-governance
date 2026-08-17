# RECOVERY 07: GIT & SOURCE CONTROL RECOVERY
## AI Video Factory — Branch Reconciliation & Worktree Reset

**PROMPT_ID:** `REC-07`  
**PURPOSE:** Resolve git merge conflicts, detached HEAD states, dirty worktrees, or corrupted repository indexes across polyrepos.  
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
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/operator-state/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Restored git repositories on valid branches.  
**PASS_CRITERIA:**
- All 15 repositories on clean `main` or active feature branches with no uncommitted merge conflicts.  
**FAIL_CRITERIA:**
- Unresolvable git corruption.  
**GIT_EXPECTATION:** Clean working trees.  
**HUMAN_ACTION_AFTER_PASS:** Resume implementation with `RESUME_PROJECT.md`.  
**HUMAN_ACTION_AFTER_FAIL:** Manually inspect git status.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Inspect Git Status across Repos:**
   Run `git status` in each repo under `05_IMPLEMENTATION/repos/`.
2. **Resolve Conflicts & Clean Worktrees:**
   Abort broken merges, stash uncommitted work, and restore valid branch state.
3. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-07"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md"
RECOMMENDED_NEXT_TASK: "Resume project execution."
HUMAN_INSTRUCTION: "Run RESUME_PROJECT.md to continue."
```
