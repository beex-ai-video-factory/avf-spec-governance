# RECOVERY 01: BLOCKED UPSTREAM DEPENDENCY
## AI Video Factory — Upstream Dependency Resolution

**PROMPT_ID:** `REC-01`  
**PURPOSE:** Diagnose and resolve a situation where a downstream repository is blocked by an unreleased or unbuilt upstream dependency without violating polyrepo isolation.  
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
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Recovery diagnosis and routing instructions.  
**PASS_CRITERIA:**
- Upstream missing repository identified.
- Downstream task cleanly paused in `RUN_STATE.yaml`.
- Exact prompt to build upstream dependency returned.  
**FAIL_CRITERIA:**
- Permitting downstream agent to edit upstream repository source code.  
**GIT_EXPECTATION:** Downstream worktree preserved cleanly.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned upstream implementation prompt.  
**HUMAN_ACTION_AFTER_FAIL:** Contact system architect.  
**NEXT_PROMPT_IF_PASS:** Exact upstream prompt path determined by inspecting missing dependency in `RUN_STATE.yaml` (e.g. `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/02_R01_CONTRACTS/R01_01_PLAN.md`)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---


> [!IMPORTANT]
> **AUTONOMOUS RECOVERY MANDATE:**
> The recovery agent MUST inspect `RUN_STATE.yaml`, identify the specific unreleased upstream dependency, and output the EXACT prompt path in `RECOMMENDED_NEXT_PROMPT`. Do not leave branch selection to the operator.

### Step-by-Step Recovery Instructions:

1. **Identify Missing Upstream Dependency:**
   Check `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` to identify which required predecessor repo is unreleased.
2. **Apply Polyrepo Rule:**
   Never allow the current repository agent to edit upstream code.
3. **Route Operator to Upstream Repo:**
   Instruct operator to switch to the upstream repository prompt pack.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-01"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: ["Upstream dependency unreleased"]
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Complete upstream repository release before resuming downstream task."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT to build the required upstream dependency."
```
