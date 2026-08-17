# PROVISIONING 02: LOCAL POLYREPO INITIALIZATION
## AI Video Factory — Initialize Local Git Repositories

**PROMPT_ID:** `PROV-02`  
**PURPOSE:** Create local directory trees and initialize clean git repositories with standard .gitignore, README.md, and configuration skeletons for all 15 independent repositories under 05_IMPLEMENTATION/repos/.  
**CURRENT_PHASE:** `01_REPO_PROVISIONING`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (3-5 min)`  
**PREREQUISITES:** `PROV-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repo-registry.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R01_contracts/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_02_LOCAL_POLYREPO_INIT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- 15 initialized local git repos under `05_IMPLEMENTATION/repos/`.  
**PASS_CRITERIA:**
- All 15 repositories possess initialized `.git` repositories on branch `main`.
- Each repo contains a tailored `.gitignore` and `README.md` identifying its OWNS and DOES NOT OWN boundaries.  
**FAIL_CRITERIA:**
- Directory creation failure or git init error in any repo.  
**GIT_EXPECTATION:** Initial commit in each of the 15 repositories.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_03_GITHUB_REPOS_PROVISION.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Create Repo Directories:**
   Create directories under `05_IMPLEMENTATION/repos/`:
   `R01_contracts`, `R02_core_state`, `R03_creative`, `R04_assets_continuity`, `R05_prompt_compiler`,
   `R06_workflow`, `R07_provider_sdk`, `R08_google_flow_adapter`, `R09_browser_worker`, `R10_flowkit_bridge`,
   `R11_qc`, `R12_media`, `R13_operator_console`, `R14_platform_observability`, `R15_integration_harness`.
2. **Initialize Git Repositories:**
   Inside each repo directory:
   - Initialize git repository: `git init -b main`
   - Add `.gitignore` (ignoring node_modules, .env, dist, coverage, *.log)
   - Add `README.md` documenting repository responsibility, primary contracts, and boundaries
   - Commit initial scaffold: `git add . && git commit -m "chore: initialize polyrepo scaffold"`
3. **Update Runtime State:**
   Update `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with repo initialization statuses.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "PROV-02"
RESULT: PASS
REPO: "SYSTEM"
BRANCH: "main"
COMMIT_SHA: "INITIAL_COMMITS"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R01_contracts/"
  - "05_IMPLEMENTATION/repos/R02_core_state/"
  - "05_IMPLEMENTATION/repos/R03_creative/"
  - "05_IMPLEMENTATION/repos/R04_assets_continuity/"
  - "05_IMPLEMENTATION/repos/R05_prompt_compiler/"
  - "05_IMPLEMENTATION/repos/R06_workflow/"
  - "05_IMPLEMENTATION/repos/R07_provider_sdk/"
  - "05_IMPLEMENTATION/repos/R08_google_flow_adapter/"
  - "05_IMPLEMENTATION/repos/R09_browser_worker/"
  - "05_IMPLEMENTATION/repos/R10_flowkit_bridge/"
  - "05_IMPLEMENTATION/repos/R11_qc/"
  - "05_IMPLEMENTATION/repos/R12_media/"
  - "05_IMPLEMENTATION/repos/R13_operator_console/"
  - "05_IMPLEMENTATION/repos/R14_platform_observability/"
  - "05_IMPLEMENTATION/repos/R15_integration_harness/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_03_GITHUB_REPOS_PROVISION.md"
RECOMMENDED_NEXT_TASK: "Configure GitHub remotes and branch protection policies."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
