# PROVISIONING 01: REPOSITORY INSPECTION & LAYOUT PLAN
## AI Video Factory — Polyrepo Provisioning Architecture

**PROMPT_ID:** `PROV-01`  
**PURPOSE:** Inspect repo-registry.yaml and formulate the exact directory structure, package manifests, and licensing/git configurations for all 15 independent repositories.  
**CURRENT_PHASE:** `01_REPO_PROVISIONING`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `CHK-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_01_INSPECT_AND_PLAN.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Provisioning plan validated in `RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- Exactly 15 repositories registered with unique names, distinct paths, and valid dependency constraints.
- Polyrepo directory layout fully specified without overlapping folders.  
**FAIL_CRITERIA:**
- Missing repo in registry or circular dependency detected in registry DAG.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_02_LOCAL_POLYREPO_INIT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Inspect Repo Registry:**
   Read `05_IMPLEMENTATION/repo-registry.yaml` and verify all 15 repos:
   `R01_contracts`, `R02_core_state`, `R03_creative`, `R04_assets_continuity`, `R05_prompt_compiler`,
   `R06_workflow`, `R07_provider_sdk`, `R08_google_flow_adapter`, `R09_browser_worker`, `R10_flowkit_bridge`,
   `R11_qc`, `R12_media`, `R13_operator_console`, `R14_platform_observability`, `R15_integration_harness`.
2. **Verify Dependency DAG:**
   Confirm zero circular dependencies across the 15 repositories.
3. **Plan Local Directory Targets:**
   Map each repo to its target path under `05_IMPLEMENTATION/repos/<repo_name>/`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "PROV-01"
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
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/01_REPO_PROVISIONING/PROVISION_02_LOCAL_POLYREPO_INIT.md"
RECOMMENDED_NEXT_TASK: "Initialize local polyrepo directory structures and git repos."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
