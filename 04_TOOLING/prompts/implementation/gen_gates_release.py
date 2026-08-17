#!/usr/bin/env python3
"""
Generates 17_INTEGRATION_GATES and 18_RELEASE prompts for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"

# GATE-00
GATE_00_MD = """# GATE 00: FOUNDATION INTEGRATION GATE
## AI Video Factory — Contracts, State, SDK & Observability Validation

**PROMPT_ID:** `GATE-00`  
**PURPOSE:** Validate cross-repository integration between R01 Contracts, R14 Platform Observability, R02 Core State, and R07 Provider SDK in a clean environment before orchestrator implementation.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-8 min)`  
**PREREQUISITES:** `R07-04`, `R02-04`, `R14-04`, `R01-04`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R01_contracts/**`
- `05_IMPLEMENTATION/repos/R02_core_state/**`
- `05_IMPLEMENTATION/repos/R07_provider_sdk/**`
- `05_IMPLEMENTATION/repos/R14_platform_observability/**`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/04_integration/TEST_STRATEGY.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_00: PASSED.  
**PASS_CRITERIA:**
- PostgreSQL migrations apply cleanly.
- Domain entities validate against R01 JSON schemas.
- Idempotency store asserts unique constraint on idempotency keys.
- FakeVideoProvider generates simulated completions and error matrices.
- OpenTelemetry traces propagate correlation context without leaking secrets.  
**FAIL_CRITERIA:**
- Schema validation error, database connection failure, or secret leakage in logs.  
**GIT_EXPECTATION:** Clean working tree across R01, R02, R07, R14.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Verify Database Initialization:**
   Ensure PostgreSQL is running and apply R02 migrations.
2. **Execute Cross-Contract Test Suite:**
   Assert schema compliance between R02 domain events and R01 JSON schemas.
3. **Execute FakeVideoProvider Simulation:**
   Run simulated generation requests through R07 Provider SDK.
4. **Assert Telemetry Context & Secret Scrubbing:**
   Verify that OTel spans from R14 are attached and contain zero unredacted tokens.
5. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-00"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 24, failed: 0}
CONTRACT_TESTS: {passed: 12, failed: 0}
INTEGRATION_TESTS: {passed: 8, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/05_R06_WORKFLOW/R06_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R06 Temporal Workflow implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# GATE-01
GATE_01_MD = """# GATE 01: FAKEPROVIDER E2E WORKFLOW GATE
## AI Video Factory — Deterministic Single-Shot & Chaos Fault-Injection Gate

**PROMPT_ID:** `GATE-01`  
**PURPOSE:** Verify deterministic single-shot video generation workflow execution, Temporal replay safety, retry policies, and fault injection scenarios using FakeVideoProvider and R15 Integration Harness.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R15-04`, `R06-04`, `GATE-00`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R06_workflow/**`
- `05_IMPLEMENTATION/repos/R15_integration_harness/**`
- `05_IMPLEMENTATION/repos/R07_provider_sdk/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_01_FAKEPROVIDER_E2E_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_01: PASSED.  
**PASS_CRITERIA:**
- Deterministic single-shot workflow completes end-to-end against FakeVideoProvider.
- All 16 fault-injection scenarios execute and recover correctly (worker crash, uncertain submit, timeout, rate limit).
- Temporal workflow history asserts replay determinism.  
**FAIL_CRITERIA:**
- Temporal non-deterministic error, deadlock, unhandled exception, or failed chaos assertion.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute Deterministic Single-Shot Test:**
   Run the standard single-shot pipeline with FakeVideoProvider delay=0 and delay=30s.
2. **Execute 16 Fault-Injection Scenarios:**
   Run `R15_integration_harness` chaos test suite. Assert:
   - Worker kill before submit: Workflow resumes and submits cleanly.
   - Worker kill after submit: Reconciles remote generation status without double submission.
   - Corrupt video payload: Quarantine DLQ triggered.
3. **Assert Temporal Replay Safety:**
   Verify workflow execution history against replay runner.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-01"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 16, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 16, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/07_R08_GOOGLE_FLOW_ADAPTER/R08_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R08 Google Flow Adapter implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# GATE-02
GATE_02_MD = """# GATE 02: FLOW EXECUTION PORT CONFORMANCE GATE
## AI Video Factory — Track A (Browser) vs Track B (Direct Protocol) Conformance

**PROMPT_ID:** `GATE-02`  
**PURPOSE:** Run comparative 10-operation FlowExecutionPort benchmark testing Track A (R09 Browser Worker) and Track B (R10 FlowKit Bridge) via R08 Google Flow Adapter to verify semantic equivalence.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R09-04`, `R10-04`, `R08-04`, `GATE-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/**`
- `05_IMPLEMENTATION/repos/R09_browser_worker/**`
- `05_IMPLEMENTATION/repos/R10_flowkit_bridge/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_02: PASSED.  
**PASS_CRITERIA:**
- Both Track A and Track B implement all 10 operations of `FlowExecutionPort`.
- Conformance suite yields identical semantic outputs for identical inputs.
- Normalized error taxonomy correctly maps HTTP 429, auth expiration, and UI changes.  
**FAIL_CRITERIA:**
- Missing operation, output contract discrepancy, or leaky abstractions between tracks.  
**GIT_EXPECTATION:** Clean working tree across R08, R09, R10.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/10_R03_CREATIVE/R03_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute FlowExecutionPort Conformance Suite against Track B (FlowKit Bridge):**
   Verify all 10 operations against mocked protocol endpoint.
2. **Execute FlowExecutionPort Conformance Suite against Track A (Browser Worker):**
   Verify Playwright/CDP automation with 4-tier selector resolution.
3. **Compare Equivalence:**
   Assert that `FlowExecutionResult` discriminated unions match 100%.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-02"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 20, failed: 0}
CONTRACT_TESTS: {passed: 10, failed: 0}
INTEGRATION_TESTS: {passed: 10, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/10_R03_CREATIVE/R03_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R03 Creative & Script Generation implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# GATE-03
GATE_03_MD = """# GATE 03: CREATIVE & MEDIA PIPELINE GATE
## AI Video Factory — Scripting, Continuity, Prompting, QC & Assembly Integration

**PROMPT_ID:** `GATE-03`  
**PURPOSE:** Verify the integration of the creative automation pipeline: R03 Creative -> R04 Assets Continuity -> R05 Prompt Compiler -> R11 QC -> R12 Media Processing.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-8 min)`  
**PREREQUISITES:** `R12-04`, `R11-04`, `R05-04`, `R04-04`, `R03-04`, `GATE-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R03_creative/**`
- `05_IMPLEMENTATION/repos/R04_assets_continuity/**`
- `05_IMPLEMENTATION/repos/R05_prompt_compiler/**`
- `05_IMPLEMENTATION/repos/R11_qc/**`
- `05_IMPLEMENTATION/repos/R12_media/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_03_CREATIVE_MEDIA_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_03: PASSED.  
**PASS_CRITERIA:**
- Multi-shot script decompiles into structured scene/shot descriptors.
- Continuity tokens are injected consistently.
- Provider dialect compilation generates valid prompt payloads.
- Technical QC (FFprobe) and Semantic QC evaluate test video clips.
- FFmpeg media worker stitches shots and attaches audio track without errors.  
**FAIL_CRITERIA:**
- Schema validation error, broken continuity tokens, FFprobe failure, or FFmpeg crash.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute End-to-End Creative Compilation:**
   Transform raw narrative into compiled provider prompt sequences.
2. **Execute Video QC Inspection:**
   Run sample video assets through R11 technical container analyzer and semantic evaluator.
3. **Execute FFmpeg Assembly Pipeline:**
   Stitch multiple shots into final master video asset using R12 Media Service.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-03"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 8, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R13 Operator Console implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# GATE-04
GATE_04_MD = """# GATE 04: FULL SYSTEM INTEGRATION GATE
## AI Video Factory — Complete 15-Repository Offline System Simulation

**PROMPT_ID:** `GATE-04`  
**PURPOSE:** Execute full-system end-to-end integration across all 15 repositories (R01 through R15) in local docker environment with human-in-the-loop Operator Console review.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `R13-04`, `GATE-03`, `GATE-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/**`
- `05_IMPLEMENTATION/environment/docker-compose.dev.yml`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_04_SYSTEM_INTEGRATION_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_04: PASSED.  
**PASS_CRITERIA:**
- All 15 repositories compile, link, and interact seamlessly.
- Complete multi-shot project generation workflow completes with simulated human approval in R13.
- Zero architectural boundary leaks and zero direct database access outside R02.  
**FAIL_CRITERIA:**
- System deadlock, missing cross-repo contract, or runtime failure.  
**GIT_EXPECTATION:** Clean working trees across all 15 repos.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Start System Stack:**
   Launch all backing services via Docker Compose.
2. **Execute Full E2E Scenario:**
   Run complete multi-shot generation simulation from narrative input to stitched video export.
3. **Simulate Operator Console Actions:**
   Approve generation checkpoints via R13 REST API.
4. **Assert End-to-End Metrics:**
   Verify trace spans and Prometheus metrics.
5. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-04"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 30, failed: 0}
CONTRACT_TESTS: {passed: 15, failed: 0}
INTEGRATION_TESTS: {passed: 15, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md"
RECOMMENDED_NEXT_TASK: "Execute controlled live Google Flow provider verification."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# GATE-05
GATE_05_MD = """# GATE 05: CONTROLLED LIVE FLOW GATE
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
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
"""

# REL-01
REL_01_MD = """# RELEASE 01: FINAL PRE-RELEASE AUDIT
## AI Video Factory — Full System Forensic & Quality Signoff

**PROMPT_ID:** `REL-01`  
**PURPOSE:** Perform comprehensive forensic audit across all 15 repositories, all 6 integration gates, frozen baseline drift, and documentation before release tagging.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Claude Opus 4.6 Thinking`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_REQUIRED`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `GATE-05`  
**READ_ONLY_INPUTS:**
- `BASELINE.lock.json`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/repos/**`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`  
**PASS_CRITERIA:**
- 15/15 repositories released with passing test suites.
- 6/6 system gates passed.
- 0 bytes frozen baseline drift against lockfile.
- 0 security vulnerabilities or exposed secrets.  
**FAIL_CRITERIA:**
- Any failing test, missing gate, uncommitted change, or frozen baseline mutation.  
**GIT_EXPECTATION:** Clean working trees across all repos.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Baseline Integrity:**
   Assert 0 bytes drift against `BASELINE.lock.json`.
2. **Verify All 15 Repository Test Suites:**
   Execute full test suites across all 15 repositories.
3. **Verify All 6 Integration Gates:**
   Confirm that GATE-00 through GATE-05 are marked PASSED in `RUN_STATE.yaml`.
4. **Compile FINAL_RELEASE_AUDIT.md:**
   Document the pre-release audit verdict.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-01"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 150, failed: 0}
CONTRACT_TESTS: {passed: 50, failed: 0}
INTEGRATION_TESTS: {passed: 40, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md"
RECOMMENDED_NEXT_TASK: "Apply system release tags and publish packages."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REL-02
REL_02_MD = """# RELEASE 02: TAG AND PUBLISH SYSTEM RELEASE
## AI Video Factory — Release Tagging & Package Publishing

**PROMPT_ID:** `REL-02`  
**PURPOSE:** Apply the unified system git release tag v1.0.0, publish the R01 Contracts npm package, and finalize release metadata.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.7 Flash High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `REL-01`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/operator-state/FINAL_RELEASE_AUDIT.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`
- `05_IMPLEMENTATION/repos/**`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- System release tag `avf-v1.0.0` applied.
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- System release tag applied across repositories.
- R01 contracts package built and prepared for publication.  
**FAIL_CRITERIA:**
- Tagging failure or package build error.  
**GIT_EXPECTATION:** Annotated release tags pushed to remotes.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Build Distribution Packages:**
   Build R01 contracts bundle.
2. **Apply Unified Release Tag:**
   Tag the workspace and repositories with `avf-v1.0.0`.
3. **Record Release State:**
   Update `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with release version `1.0.0`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-02"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 10, failed: 0}
INTEGRATION_TESTS: {passed: 5, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md"
RECOMMENDED_NEXT_TASK: "Execute final post-release smoke verification."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

# REL-03
REL_03_MD = """# RELEASE 03: POST-RELEASE VERIFICATION
## AI Video Factory — Final System Acceptance & Operations Handoff

**PROMPT_ID:** `REL-03`  
**PURPOSE:** Execute post-release smoke tests, verify production health checks, and finalize the operator implementation journey.  
**CURRENT_PHASE:** `18_RELEASE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `REL-02`  
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
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Final updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` (Status: COMPLETE).  
**PASS_CRITERIA:**
- All health check endpoints responsive.
- All 15 repositories verified at release tag v1.0.0.
- System operational handoff complete.  
**FAIL_CRITERIA:**
- Health check failure.  
**GIT_EXPECTATION:** Clean working trees.  
**HUMAN_ACTION_AFTER_PASS:** Implementation is 100% complete! Proceed to production operations.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `TERMINAL_COMPLETE`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md`

---

### Step-by-Step Instructions:

1. **Verify Health Endpoints:**
   Ping Core State, Workflow worker, and Operator Console health endpoints.
2. **Mark Run State as Complete:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `current_execution.status: "COMPLETE"`.
3. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REL-03"
RESULT: PASS
REPO: "SYSTEM_RELEASE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 10, failed: 0}
CONTRACT_TESTS: {passed: 5, failed: 0}
INTEGRATION_TESTS: {passed: 5, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "TERMINAL_COMPLETE"
RECOMMENDED_NEXT_TASK: "AI Video Factory v1.0.0 implementation is 100% complete."
HUMAN_INSTRUCTION: "All 15 repositories and 6 gates have passed. System is ready for production."
```
"""

files = {
    "17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md": GATE_00_MD,
    "17_INTEGRATION_GATES/GATE_01_FAKEPROVIDER_E2E_GATE.md": GATE_01_MD,
    "17_INTEGRATION_GATES/GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE.md": GATE_02_MD,
    "17_INTEGRATION_GATES/GATE_03_CREATIVE_MEDIA_GATE.md": GATE_03_MD,
    "17_INTEGRATION_GATES/GATE_04_SYSTEM_INTEGRATION_GATE.md": GATE_04_MD,
    "17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md": GATE_05_MD,
    "18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md": REL_01_MD,
    "18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md": REL_02_MD,
    "18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md": REL_03_MD,
}

for rel_path, content in files.items():
    filepath = os.path.join(RUNBOOK_DIR, rel_path)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {rel_path}")

print("Gates and release prompts generated successfully.")
