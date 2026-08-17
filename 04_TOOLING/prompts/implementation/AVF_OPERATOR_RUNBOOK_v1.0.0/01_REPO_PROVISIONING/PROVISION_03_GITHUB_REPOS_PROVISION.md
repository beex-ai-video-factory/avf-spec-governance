# PROVISIONING 03: GITHUB REMOTES & BRANCH PROTECTION
## AI Video Factory — Source Control Remotes & CI Safeguards

**PROMPT_ID:** `PROV-03`  
**PURPOSE:** Inspect GitHub CLI authentication and configure remote GitHub repositories (avf-contracts, avf-core-state, etc.) with branch protection rules, or establish local git remotes if operating in offline mode.  
**CURRENT_PHASE:** `01_REPO_PROVISIONING`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `PROV-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repo-registry.yaml`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/`
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_03_GITHUB_REPOS_PROVISION.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Git remotes and branch protection configured for all 15 repos.  
**PASS_CRITERIA:**
- All 15 repositories configured with valid remote URLs or local upstream tracking.
- Branch protection policies defined: releasable `main`, short-lived feature branches, no force push.  
**FAIL_CRITERIA:**
- Unhandled Git error or permission failure.  
**GIT_EXPECTATION:** Clean working trees with upstream tracking.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT` to begin Gate 0 (R01 Contracts).  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/02_R01_CONTRACTS/R01_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Check GitHub Auth & Environment Mode:**
   Check if `gh auth status` is authenticated.
   - If authenticated and remote creation is authorized, create GitHub repositories:
     `avf-spec-governance`, `avf-contracts`, `avf-core-state`, `avf-creative`, `avf-assets-continuity`,
     `avf-prompt-compiler`, `avf-workflow`, `avf-provider-sdk`, `avf-google-flow-adapter`, `avf-browser-worker`,
     `avf-flowkit-bridge`, `avf-qc`, `avf-media`, `avf-operator-console`, `avf-observability`, `avf-integration-harness`.
   - If offline or unauthenticated, configure local git tracking.
2. **Apply Branch Protection Configuration:**
   Enforce:
   - Default branch: `main`
   - No direct force pushes
   - PR / review requirement before merge
3. **Record Completion in State:**
   Update `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "PROV-03"
RESULT: PASS
REPO: "SYSTEM"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/02_R01_CONTRACTS/R01_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R01 Contracts implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
