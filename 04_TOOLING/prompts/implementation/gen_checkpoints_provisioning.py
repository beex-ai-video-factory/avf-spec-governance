#!/usr/bin/env python3
"""
Generates 00_CHECKPOINTS and 01_REPO_PROVISIONING prompts for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"

# 1. CHK-01
CHK_01_MD = """# CHECKPOINT 01: PREFLIGHT & SECURITY AUDIT
## AI Video Factory — Pre-Implementation Baseline Verification

**PROMPT_ID:** `CHK-01`  
**PURPOSE:** Verify cryptographic baseline integrity against BASELINE.lock.json, confirm zero frozen mutation drift, verify workspace cleanliness, and ensure zero unredacted secrets exist before commencing implementation.  
**CURRENT_PHASE:** `00_CHECKPOINTS`  
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
- `PROJECT.md`
- `00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md`
- `01_FROZEN_RELEASE/v1.0.0/CONTENT_HASHES.json`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` (Phase 00 recorded as verified).  
**PASS_CRITERIA:**
- All 60/60 files in `01_FROZEN_RELEASE/v1.0.0/` match exact SHA-256 hashes.
- Frozen baseline mutation drift is exactly 0.
- Secrets scan reveals 0 unredacted tokens, API keys, or credentials.  
**FAIL_CRITERIA:**
- Hash mismatch in any frozen specification file or unredacted secret found.  
**GIT_EXPECTATION:** Clean working tree in frozen paths.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Do NOT proceed. Run `99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Baseline Hashes:**
   Run hash verification across `01_FROZEN_RELEASE/v1.0.0/` against `BASELINE.lock.json`. Confirm that the content tree hash matches `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846`.
2. **Perform Automated Secret Scan:**
   Scan workspace text files for accidental API keys, tokens, or private credentials. Confirm 0 violations.
3. **Initialize Runtime State:**
   Ensure `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` is active and record `CHK-01` as PASSED.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "CHK-01"
RESULT: PASS
REPO: "SYSTEM"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 2, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md"
RECOMMENDED_NEXT_TASK: "Execute development environment doctor check."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# 2. CHK-02
CHK_02_MD = """# CHECKPOINT 02: ENVIRONMENT DOCTOR AUDIT
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
"""

# 3. PROV-01
PROV_01_MD = """# PROVISIONING 01: REPOSITORY INSPECTION & LAYOUT PLAN
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
"""

# 4. PROV-02
PROV_02_MD = """# PROVISIONING 02: LOCAL POLYREPO INITIALIZATION
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
"""

# 5. PROV-03
PROV_03_MD = """# PROVISIONING 03: GITHUB REMOTES & BRANCH PROTECTION
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
"""

files = {
    "00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md": CHK_01_MD,
    "00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md": CHK_02_MD,
    "01_REPO_PROVISIONING/PROVISION_01_INSPECT_AND_PLAN.md": PROV_01_MD,
    "01_REPO_PROVISIONING/PROVISION_02_LOCAL_POLYREPO_INIT.md": PROV_02_MD,
    "01_REPO_PROVISIONING/PROVISION_03_GITHUB_REPOS_PROVISION.md": PROV_03_MD,
}

for rel_path, content in files.items():
    filepath = os.path.join(RUNBOOK_DIR, rel_path)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {rel_path}")

print("Checkpoints and provisioning prompts generated successfully.")
