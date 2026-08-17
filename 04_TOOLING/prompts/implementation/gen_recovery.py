#!/usr/bin/env python3
"""
Generates 99_RECOVERY prompts for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"

# REC-01
REC_01_MD = """# RECOVERY 01: BLOCKED UPSTREAM DEPENDENCY
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
**NEXT_PROMPT_IF_PASS:** Dynamic upstream prompt (e.g. `R01-01`, `R02-01`, etc.)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

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
"""

# REC-02
REC_02_MD = """# RECOVERY 02: CONTRACT BREAK & SCHEMA INCOMPATIBILITY
## AI Video Factory — Contract Dispute Triage & Resolution

**PROMPT_ID:** `REC-02`  
**PURPOSE:** Resolve a contract schema discrepancy or typing incompatibility between two communicating repositories.  
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
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/02_contracts/**`
- `05_IMPLEMENTATION/repos/R01_contracts/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/change-requests/**`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Contract analysis report and resolution path.  
**PASS_CRITERIA:**
- Root cause identified: Consumer typing error vs R01 contract defect.
- If consumer error: route back to consumer implementation prompt.
- If R01 defect: route to R01 update or formal Change Request.  
**FAIL_CRITERIA:**
- Direct modification of frozen baseline or bypass of contract schemas.  
**GIT_EXPECTATION:** Clean state tracking.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned prompt.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to system architect.  
**NEXT_PROMPT_IF_PASS:** Dynamic routing based on contract analysis.  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Recovery Instructions:

1. **Compare Consumer Payload against R01 JSON Schemas:**
   Validate whether the issue is consumer non-conformance or an R01 schema bug.
2. **If Consumer Bug:**
   Route to consumer repo `<REPO>_02_IMPLEMENT.md`.
3. **If R01 Bug:**
   Route to `02_R01_CONTRACTS/R01_02_IMPLEMENT.md` to patch R01.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-02"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 1, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Execute targeted contract remediation prompt."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REC-03
REC_03_MD = """# RECOVERY 03: FROZEN SPEC DEFECT & CHANGE REQUEST
## AI Video Factory — Formal Specification Change Control

**PROMPT_ID:** `REC-03`  
**PURPOSE:** Open and document a formal Change Request (CR) when an irreconcilable defect, impossibility, or contradiction is discovered in the frozen v1.0.0 specification.  
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
- `01_FROZEN_RELEASE/v1.0.0/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/change-requests/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-XX.md`  
**PASS_CRITERIA:**
- Formal CR created with impact analysis, alternative solutions, and affected repository lists.
- Zero modification to frozen baseline files.
- Affected repository marked as `PAUSED_FOR_CR` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Direct edits to `01_FROZEN_RELEASE/`.  
**GIT_EXPECTATION:** CR document committed.  
**HUMAN_ACTION_AFTER_PASS:** Human sponsor must review and approve/reject CR.  
**HUMAN_ACTION_AFTER_FAIL:** Revert any unauthorized edits to frozen files.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Draft Change Request Document:**
   Create `05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-01.md`.
2. **Detail Specification Conflict:**
   Document exact file, line, and contradiction in frozen spec.
3. **Record Blocker in State:**
   Add CR to `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-03"
RESULT: HUMAN_ACTION_REQUIRED
REPO: "SYSTEM_GOVERNANCE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: ["CR pending human sponsor approval"]
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-01.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md"
RECOMMENDED_NEXT_TASK: "Human sponsor review of Change Request."
HUMAN_INSTRUCTION: "Review the Change Request and approve before resuming implementation."
```
"""

# REC-04
REC_04_MD = """# RECOVERY 04: TEST GATE FAILURE
## AI Video Factory — Unit, Conformance & Coverage Remediation

**PROMPT_ID:** `REC-04`  
**PURPOSE:** Diagnose and repair failing unit tests, broken negative fixtures, or insufficient code coverage in a repository.  
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
- `05_IMPLEMENTATION/repos/**`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Test diagnostics and code fixes in affected repository.  
**PASS_CRITERIA:**
- Failing tests identified and resolved without lowering coverage thresholds or deleting assertions.  
**FAIL_CRITERIA:**
- Masking errors by skipping tests.  
**GIT_EXPECTATION:** Clean test fix commit.  
**HUMAN_ACTION_AFTER_PASS:** Re-run the review prompt for the affected repository.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human developer.  
**NEXT_PROMPT_IF_PASS:** Dynamic repo review prompt (`<REPO>_03_TEST_AND_REVIEW.md`).  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Analyze Test Failure Logs:**
   Inspect test runner output to identify root cause.
2. **Apply Targeted Code Fix:**
   Repair implementation logic in `src/`.
3. **Re-run Test Suite:**
   Assert 100% pass rate.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-04"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 10, failed: 0}
CONTRACT_TESTS: {passed: 5, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/..."
RECOMMENDED_NEXT_TASK: "Re-run review prompt for affected repository."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REC-05
REC_05_MD = """# RECOVERY 05: INTEGRATION GATE FAILURE
## AI Video Factory — Cross-Repository Integration Triage

**PROMPT_ID:** `REC-05`  
**PURPOSE:** Triage and isolate failures occurring during cross-repository system integration gates (GATE-00 through GATE-05).  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<5 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Integration gate diagnostic report.  
**PASS_CRITERIA:**
- Responsible component isolated and remediation prompt identified.  
**FAIL_CRITERIA:**
- Unclear root cause.  
**GIT_EXPECTATION:** State preserved cleanly.  
**HUMAN_ACTION_AFTER_PASS:** Execute the targeted remediation prompt.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human lead.  
**NEXT_PROMPT_IF_PASS:** Dynamic remediation prompt.  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Inspect Integration Traces:**
   Read error logs from the failed integration gate.
2. **Isolate Faulty Component:**
   Determine whether the fault is state persistence (R02), workflow retry logic (R06), provider adapter (R08), or QC (R11).
3. **Route to Component Fix:**
   Return the implementation fix prompt for the faulty component.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-05"
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
RECOMMENDED_NEXT_TASK: "Remediate isolated component defect."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REC-06
REC_06_MD = """# RECOVERY 06: STALLED OR LOOPING AGENT
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
**NEXT_PROMPT_IF_PASS:** Dynamic prompt based on last uncompleted task.  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

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
"""

# REC-07
REC_07_MD = """# RECOVERY 07: GIT & SOURCE CONTROL RECOVERY
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
"""

# REC-08
REC_08_MD = """# RECOVERY 08: ENVIRONMENT & DOCKER OUTAGE
## AI Video Factory — Infrastructure & Toolchain Repair

**PROMPT_ID:** `REC-08`  
**PURPOSE:** Diagnose and recover from Docker container failures, PostgreSQL connection outages, or missing runtime dependencies.  
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
- `05_IMPLEMENTATION/environment/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Restored docker services and verified doctor report.  
**PASS_CRITERIA:**
- Docker compose restart succeeds and `doctor.sh` passes 100%.  
**FAIL_CRITERIA:**
- Docker engine unresponsive.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Re-run `CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`.  
**HUMAN_ACTION_AFTER_FAIL:** Ensure Docker Desktop / engine is running.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md`

---

### Step-by-Step Instructions:

1. **Restart Docker Compose Stack:**
   Run `docker compose -f 05_IMPLEMENTATION/environment/docker-compose.dev.yml down && docker compose -f 05_IMPLEMENTATION/environment/docker-compose.dev.yml up -d`.
2. **Re-run Doctor Check:**
   Execute `bash 05_IMPLEMENTATION/environment/doctor.sh`.
3. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-08"
RESULT: PASS
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 5, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md"
RECOMMENDED_NEXT_TASK: "Re-run environment doctor checkpoint."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REC-09
REC_09_MD = """# RECOVERY 09: EXTERNAL PROVIDER BLOCKER & CAPTCHA ESCALATION
## AI Video Factory — Anti-Abuse Safety & Human Operator Escalation

**PROMPT_ID:** `REC-09`  
**PURPOSE:** Handle Google Flow security challenges, bot detections, CAPTCHAs, or rate limit blocks strictly through human operator escalation without unauthorized automation bypass.  
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
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/**`
- `05_IMPLEMENTATION/repos/R09_browser_worker/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Escalation record in `RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- Anti-abuse zero-bypass rule strictly enforced.
- Operator escalation notification generated.
- State mapped to `BLOCKED_PROVIDER` until human completes manual session challenge.  
**FAIL_CRITERIA:**
- Attempting automated CAPTCHA solver or credential brute-forcing.  
**GIT_EXPECTATION:** State preserved cleanly.  
**HUMAN_ACTION_AFTER_PASS:** Human operator opens browser, resolves challenge manually, then runs `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Stop all automated provider requests.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Verify Security Challenge:**
   Record challenge type (`CAPTCHA`, `AUTH_EXPIRED`, `RATE_LIMIT_EXCEEDED`).
2. **Enforce Zero-Bypass Invariant:**
   Do not attempt automated solver scripts.
3. **Escalate to Human Operator:**
   Provide manual resolution instructions.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-09"
RESULT: HUMAN_ACTION_REQUIRED
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: ["Provider security challenge requiring manual operator resolution"]
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md"
RECOMMENDED_NEXT_TASK: "Resume live Flow gate after human completes security verification."
HUMAN_INSTRUCTION: "Open browser session, solve challenge manually, and re-run GATE_05."
```
"""

files = {
    "99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md": REC_01_MD,
    "99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md": REC_02_MD,
    "99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md": REC_03_MD,
    "99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md": REC_04_MD,
    "99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md": REC_05_MD,
    "99_RECOVERY/RECOVERY_06_STALLED_AGENT.md": REC_06_MD,
    "99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md": REC_07_MD,
    "99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md": REC_08_MD,
    "99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md": REC_09_MD,
}

for rel_path, content in files.items():
    filepath = os.path.join(RUNBOOK_DIR, rel_path)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {rel_path}")

print("Recovery prompts generated successfully.")
