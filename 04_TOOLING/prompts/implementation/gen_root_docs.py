#!/usr/bin/env python3
"""
Generates the core control and navigation documents for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"

# 1. START_HERE.md
START_HERE_MD = """# AI VIDEO FACTORY v1.0.0 — OPERATOR IMPLEMENTATION RUNBOOK
## Start Here — Human Operator Master Entrypoint

**Document Version:** 1.0.0  
**Baseline Lock:** `BASELINE.lock.json` (SHA-256: `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846`)  
**Forensic Status:** `FORENSIC_STATUS = VERIFIED_IMPLEMENTATION_BASELINE`  
**Current System State:** `READY_FOR_IMPLEMENTATION`  
**Workspace Root:** `AVF_SPEC_REVIEW/`

---

## 1. The Golden Operator Rule

> [!IMPORTANT]
> **DO NOT CHOOSE THE NEXT STEP YOURSELF.**
> After each prompt completes, read the standard YAML output block:
> - If `RESULT: PASS`, copy and run the exact path and command given in `RECOMMENDED_NEXT_PROMPT`.
> - If `RESULT: FAIL` or `RESULT: BLOCKED`, run the specific recovery prompt returned in the output block.
> - Never guess or alter the sequence manually.

---

## 2. Absolute Immutability Boundary

The frozen baseline directories are **STRICTLY READ-ONLY**:
- `01_FROZEN_RELEASE/`
- `02_SOURCE_KITS_READONLY/`
- `03_GOVERNANCE_EVIDENCE_READONLY/`
- `90_ARCHIVE_READONLY/`

Any prompt or agent attempting to modify, delete, or write inside these directories violates system security invariants. All production code must be written strictly within `05_IMPLEMENTATION/repos/<repo_name>/`.

---

## 3. Quick Reference Map

| Document | Purpose |
|---|---|
| [MASTER_SEQUENCE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/MASTER_SEQUENCE.md) | End-to-end linear & parallel execution graph |
| [MODEL_MATRIX.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/MODEL_MATRIX.md) | Mandatory model assignments per prompt class |
| [OPERATOR_RULES.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md) | 10 Non-negotiable implementation invariants |
| [WORKSPACE_AND_REPO_MAP.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md) | Polyrepo boundaries, paths, OWNS / DOES NOT OWN |
| [FAILURE_DECISION_TREE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/FAILURE_DECISION_TREE.md) | Error taxonomy and recovery dispatch matrix |
| [RESUME_PROJECT.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md) | Read-only resumption tool when restarting sessions |

---

## 4. First Operator Action

To begin implementation of AI Video Factory v1.0.0, execute Step 1:

### Step 1: Preflight & Security Checkpoint
- **Workspace:** Open `AVF_SPEC_REVIEW/`
- **Model:** **Gemini 3.7 Flash High** (Mode: Local workspace)
- **Prompt File:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md`
- **Command to Run:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```

---

## 5. Session Resumption Procedure

If your session is interrupted, restarted, or you open a fresh terminal/conversation:
1. Open workspace `AVF_SPEC_REVIEW/`.
2. Select model **Gemini 3.7 Flash High**.
3. Run the resumption command:
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md and execute it completely.
```
4. Follow the single `RECOMMENDED_NEXT_PROMPT` returned by the resumption tool.
"""

# 2. RUN_STATE_TEMPLATE.yaml
RUN_STATE_TEMPLATE_YAML = """# AI Video Factory v1.0.0 — Implementation Run State
# Copy this template to 05_IMPLEMENTATION/operator-state/RUN_STATE.yaml

version: "1.0.0"
project: "AI Video Factory"
baseline_version: "1.0.0"
baseline_content_hash: "7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846"
created_at: "2026-08-16T00:00:00Z"
updated_at: "2026-08-16T00:00:00Z"

current_execution:
  phase: "00_CHECKPOINTS"
  current_prompt_id: "CHK-01"
  last_passed_prompt_id: null
  status: "IN_PROGRESS" # IN_PROGRESS | PAUSED | BLOCKED | COMPLETE

system_gates:
  GATE_00_FOUNDATION_GATE: { status: "PENDING", passed_at: null, commit_sha: null }
  GATE_01_FAKEPROVIDER_E2E_GATE: { status: "PENDING", passed_at: null, commit_sha: null }
  GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE: { status: "PENDING", passed_at: null, commit_sha: null }
  GATE_03_CREATIVE_MEDIA_GATE: { status: "PENDING", passed_at: null, commit_sha: null }
  GATE_04_SYSTEM_INTEGRATION_GATE: { status: "PENDING", passed_at: null, commit_sha: null }
  GATE_05_CONTROLLED_LIVE_FLOW_GATE: { status: "PENDING", passed_at: null, commit_sha: null }

repositories:
  R01_contracts: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R14_platform_observability: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R02_core_state: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R07_provider_sdk: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R06_workflow: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R15_integration_harness: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R08_google_flow_adapter: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R10_flowkit_bridge: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R09_browser_worker: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R03_creative: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R04_assets_continuity: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R05_prompt_compiler: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R11_qc: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R12_media: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }
  R13_operator_console: { status: "NOT_STARTED", current_step: "01_PLAN", version: "0.0.0", branch: "main", commit_sha: null, tag: null }

active_blockers: []
change_requests: []
"""

# 3. MODEL_MATRIX.md
MODEL_MATRIX_MD = """# AI VIDEO FACTORY v1.0.0 — MODEL ROUTING MATRIX
## Authoritative Model Routing & Verification Policy

**Version:** 1.0.0  
**Authority:** Technical Architecture Board

---

## 1. Model Roles & Hierarchy

To achieve maximum engineering rigor while preventing hallucination and superficial test approvals, AI Video Factory mandates a three-tier model hierarchy:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PRIMARY BUILDER: Gemini 3.7 Flash High                  │
│    - Implementation planning (PLAN.md)                      │
│    - Code implementation & refactoring (IMPLEMENT.md)       │
│    - Unit test authoring & local debugging                  │
│    - Documentation & Git state operations                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 2. CRITICAL TECHNICAL REVIEWER: Gemini 3.1 Pro High         │
│    - Deep architectural review (TEST_AND_REVIEW.md)         │
│    - R01, R02, R06, R07, R08, R09, R10, R15 verification   │
│    - Concurrency, replay safety, contract dispute triage    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ 3. CROSS-FAMILY HOSTILE ACCEPTANCE: Claude Opus 4.6 Thinking │
│    - Independent hostile audit (ACCEPT_RELEASE.md / GATES)  │
│    - R01 Contracts final signoff                            │
│    - Foundation Gate (GATE_00) & Durability Gate (R06)      │
│    - Flow Execution Port Boundary Gate (GATE_02)            │
│    - Final Pre-Release Release Audit (RELEASE_01)           │
│    - MUST RUN IN A BRAND NEW CONVERSATION                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Model Routing by Prompt Category

| Category / Repo ID | Implementation Phase | Primary Model | Fallback Model | Conversation Mode |
|---|---|---|---|---|
| **00_CHECKPOINTS** | Preflight / Doctor | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **01_PROVISIONING** | Polyrepo / GitHub | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **R01 Contracts** | Plan & Implement | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **R01 Contracts** | Test & Review | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R01 Contracts** | Acceptance & Release | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **R02 Core State** | Test & Review | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R02 Core State** | Acceptance & Release | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R07 Provider SDK** | Test & Review / Accept | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R06 Workflow** | Test & Review | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R06 Workflow** | Acceptance & Release | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **R15 Harness** | Test & Review / Accept | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **R08 Flow Adapter** | Test & Review / Accept | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **R10 FlowKit Bridge** | Test & Review / Accept | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **R09 Browser Worker**| Test & Review / Accept | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **R03, R04, R05** | Plan, Impl, Review, Accept | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **R11, R12, R13, R14**| Plan, Impl, Review, Accept | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **GATE_00 (Foundation)**| Cross-Repo Gate | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **GATE_01 (Fake E2E)** | Cross-Repo Gate | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **GATE_02 (Flow Port)** | Cross-Repo Gate | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **GATE_03 (Creative)** | Cross-Repo Gate | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **GATE_04 (System E2E)**| Cross-Repo Gate | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |
| **GATE_05 (Live Flow)** | Cross-Repo Gate | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **RELEASE_01 (Audit)** | Final Release Audit | **Claude Opus 4.6 Thinking** | Gemini 3.1 Pro High | **NEW CONVERSATION** |
| **RELEASE_02, 03** | Publish & Verify | Gemini 3.7 Flash High | Gemini 3.1 Pro High | Existing/New |
| **99_RECOVERY** | Recovery Diagnostics | Gemini 3.1 Pro High | Gemini 3.7 Flash High | Existing/New |

---

## 3. Truthfulness & Fallback Policy

1. **Explicit Recording:** If a designated model (e.g. Claude Opus 4.6 Thinking) is unavailable, the fallback model must be selected, and the operator output block must explicitly declare:
   ```yaml
   ACTUAL_MODEL_USED: "Gemini 3.1 Pro High (FALLBACK)"
   HOSTILE_CROSS_FAMILY_REVIEW_COMPLETED: false
   ```
2. **Zero False Claims:** Never claim a cross-family hostile review occurred when a same-family model was used.
"""

# 4. OPERATOR_RULES.md
OPERATOR_RULES_MD = """# AI VIDEO FACTORY v1.0.0 — OPERATOR RULES
## 10 Non-Negotiable System Invariants & Operational Rules

**Version:** 1.0.0  
**Authority:** Technical Architecture Board & Security Custodian

---

### Rule 1: The Golden Routing Rule
Never guess or manually pick the next execution step. After every prompt execution, strictly follow the `RECOMMENDED_NEXT_PROMPT` provided in the standardized YAML output block.

### Rule 2: Immutability of the Frozen Baseline
The directories `01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, and `90_ARCHIVE_READONLY/` are permanently frozen. Any modification, deletion, or addition inside these paths is strictly forbidden.

### Rule 3: Strict Polyrepo Domain Boundary Isolation
One coding task owns exactly one repository. When working in `05_IMPLEMENTATION/repos/RXX/`, the agent must never edit files belonging to another repository. Upstream changes require completing and releasing the upstream repo first.

### Rule 4: Single-Ownership Database Principle
Only `R02_core_state` owns database access and credentials. No other service, worker, workflow, or UI may connect directly to PostgreSQL. All persistence occurs through R02's strongly typed REST/gRPC interfaces.

### Rule 5: FlowExecutionPort Isolation Principle
`R08_google_flow_adapter` must interact with Track A (`R09_browser_worker`) and Track B (`R10_flowkit_bridge`) strictly through the 10-operation `FlowExecutionPort` contract. Track A and Track B must remain mutually independent with zero cross-imports.

### Rule 6: FakeProvider-First Verification
At least 80% of all workflow, failure, and edge-case behavior must be proven deterministically against `FakeVideoProvider` in `R07_provider_sdk` before incurring paid external generation credits.

### Rule 7: Anti-Abuse & Zero-Bypass Policy
No automated agent, test, or worker may attempt to bypass CAPTCHAs, bot detections, or rate limits. When a security challenge occurs, the system must immediately escalate to a `HUMAN_REQUIRED` / `BLOCKED_PROVIDER` state.

### Rule 8: Temporal Determinism & Replay Safety
All workflow definitions in `R06_workflow` must be strictly deterministic. No direct I/O, random number generation, system clocks, or unversioned state mutations inside workflow functions.

### Rule 9: Observability & Automated Secret Redaction
All logs, metrics, and trace spans emitted via `R14_platform_observability` must pass through automated secret redaction filters. Zero plain-text tokens, passwords, or cookies in telemetry.

### Rule 10: Strict Standardized Output Contract
Every execution prompt must conclude with the exact YAML output contract block containing `RESULT`, `REPO`, `TESTS`, `BLOCKERS`, and `RECOMMENDED_NEXT_PROMPT`. Prose-only conclusions are invalid.
"""

# 5. WORKSPACE_AND_REPO_MAP.md
WORKSPACE_AND_REPO_MAP_MD = """# AI VIDEO FACTORY v1.0.0 — WORKSPACE AND REPO MAP
## Polyrepo Layout, Boundaries, and Dependency Envelopes

**Version:** 1.0.0  
**Authority:** Technical Architecture Board

---

## 1. Local Filesystem Layout

```text
AVF_SPEC_REVIEW/
├── 00_PROJECT_ADMIN/              # Project governance & certificates
├── 01_FROZEN_RELEASE/             # READ-ONLY Frozen v1.0.0 Specification
├── 02_SOURCE_KITS_READONLY/       # READ-ONLY Reference source kits
├── 03_GOVERNANCE_EVIDENCE_READONLY# READ-ONLY Historical audit evidence
├── 04_TOOLING/                    # Operational tooling, validators, runbook
│   └── prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/
├── 05_IMPLEMENTATION/             # ALL PRODUCT CODE LIVES HERE
│   ├── operator-state/            # Runtime execution state & history
│   ├── change-requests/           # Formal Change Requests (CR)
│   ├── decisions/                 # Implementation Decision Records (IDR)
│   ├── environment/               # Docker composition & doctor scripts
│   └── repos/                     # 15 Independent Polyrepos
│       ├── R01_contracts/
│       ├── R02_core_state/
│       ├── R03_creative/
│       ├── R04_assets_continuity/
│       ├── R05_prompt_compiler/
│       ├── R06_workflow/
│       ├── R07_provider_sdk/
│       ├── R08_google_flow_adapter/
│       ├── R09_browser_worker/
│       ├── R10_flowkit_bridge/
│       ├── R11_qc/
│       ├── R12_media/
│       ├── R13_operator_console/
│       ├── R14_platform_observability/
│       └── R15_integration_harness/
└── 90_ARCHIVE_READONLY/           # READ-ONLY Archived packages
```

---

## 2. Repository Mapping & Boundary Table

| Code | Repo Name | Layer | Primary Path | Allowed Inbound Deps | Forbidden Dependencies |
|---|---|---|---|---|---|
| **R01** | `R01_contracts` | Layer 0 | `05_IMPLEMENTATION/repos/R01_contracts/` | All repos (R02–R15) | R02–R15 |
| **R02** | `R02_core_state` | Layer 1 | `05_IMPLEMENTATION/repos/R02_core_state/` | R03, R04, R05, R06, R13, R15 | R03–R13, R15 |
| **R03** | `R03_creative` | Layer 2 | `05_IMPLEMENTATION/repos/R03_creative/` | R06, R15 | R04–R13, R15, Direct DB |
| **R04** | `R04_assets_continuity` | Layer 2 | `05_IMPLEMENTATION/repos/R04_assets_continuity/` | R05, R06, R15 | R03, R05–R13, R15, Direct DB |
| **R05** | `R05_prompt_compiler` | Layer 2 | `05_IMPLEMENTATION/repos/R05_prompt_compiler/` | R06, R15 | R06–R13, R15, Direct DB |
| **R06** | `R06_workflow` | Layer 5 | `05_IMPLEMENTATION/repos/R06_workflow/` | R13, R15 | R09, R10, Direct DB |
| **R07** | `R07_provider_sdk` | Layer 3 | `05_IMPLEMENTATION/repos/R07_provider_sdk/` | R06, R08, R15 | R02–R06, R08–R13, R15, Direct DB |
| **R08** | `R08_google_flow_adapter` | Layer 3 | `05_IMPLEMENTATION/repos/R08_google_flow_adapter/`| R06, R15 | R02–R06, Direct DB |
| **R09** | `R09_browser_worker` | Layer 4 | `05_IMPLEMENTATION/repos/R09_browser_worker/` | R08 (via Port), R15 | R02–R08, R10, R11–R13, Direct DB |
| **R10** | `R10_flowkit_bridge` | Layer 4 | `05_IMPLEMENTATION/repos/R10_flowkit_bridge/` | R08 (via Port), R15 | R02–R09, R11–R13, Direct DB |
| **R11** | `R11_qc` | Layer 2 | `05_IMPLEMENTATION/repos/R11_qc/` | R06, R15 | R02–R10, R12, R13, Direct DB |
| **R12** | `R12_media` | Layer 2 | `05_IMPLEMENTATION/repos/R12_media/` | R06, R15 | R02–R11, R13, Direct DB |
| **R13** | `R13_operator_console` | Layer 5 | `05_IMPLEMENTATION/repos/R13_operator_console/` | Human Operator | R03, R04, R05, R07–R12, R15, Direct DB |
| **R14** | `R14_platform_observability`| Cross | `05_IMPLEMENTATION/repos/R14_platform_observability/`| All repos (R02–R15) | R02–R13, R15, Direct DB |
| **R15** | `R15_integration_harness` | Cross | `05_IMPLEMENTATION/repos/R15_integration_harness/`| Test Runners | Direct production DB mutation |
"""

# 6. MASTER_SEQUENCE.md
MASTER_SEQUENCE_MD = """# AI VIDEO FACTORY v1.0.0 — MASTER EXECUTION SEQUENCE
## Critical Path, Gates, and Parallel Sprints

**Version:** 1.0.0  
**Authority:** Technical Architecture Board

---

## 1. Master Critical Path Diagram

```mermaid
graph TD
    CHK01[CHK-01: Preflight & Security] --> CHK02[CHK-02: Env Doctor]
    CHK02 --> PROV01[PROV-01: Polyrepo Plan]
    PROV01 --> PROV02[PROV-02: Polyrepo Init]
    PROV02 --> PROV03[PROV-03: GitHub Provision]
    PROV03 --> R01[R01 Contracts: Plan -> Impl -> Test -> Accept]
    R01 --> R14[R14 Observability: Plan -> Impl -> Test -> Accept]
    R14 --> R02[R02 Core State: Plan -> Impl -> Test -> Accept]
    R02 --> R07[R07 Provider SDK: Plan -> Impl -> Test -> Accept]
    R07 --> GATE00[GATE-00: Foundation Gate]
    
    GATE00 --> R06[R06 Workflow: Plan -> Impl -> Test -> Accept]
    R06 --> R15[R15 Integration Harness: Plan -> Impl -> Test -> Accept]
    R15 --> GATE01[GATE-01: FakeProvider E2E Gate]
    
    GATE01 --> R08[R08 Google Flow Adapter]
    R08 --> R10[R10 FlowKit Bridge - Track B]
    R10 --> R09[R09 Browser Worker - Track A]
    R09 --> GATE02[GATE-02: Flow Port Conformance Gate]
    
    GATE02 --> R03[R03 Creative]
    R03 --> R04[R04 Assets Continuity]
    R04 --> R05[R05 Prompt Compiler]
    R05 --> R11[R11 QC Service]
    R11 --> R12[R12 Media Service]
    R12 --> GATE03[GATE-03: Creative & Media Gate]
    
    GATE03 --> R13[R13 Operator Console]
    R13 --> GATE04[GATE-04: Full System Integration Gate]
    GATE04 --> GATE05[GATE-05: Controlled Live Flow Gate]
    GATE05 --> REL01[REL-01: Pre-Release Audit]
    REL01 --> REL02[REL-02: Tag & Publish Release]
    REL02 --> REL03[REL-03: Post-Release Verification]
```

---

## 2. Phase-by-Phase Execution Schedule

| Phase ID | Phase Name | Execution Mode | Unlocking Gate | Primary Output |
|---|---|---|---|---|
| **Phase 00** | Checkpoints & Preflight | SEQUENTIAL_REQUIRED | Doctor PASS | Clean dev environment |
| **Phase 01** | Repository Provisioning | SEQUENTIAL_REQUIRED | Repo Init PASS | 15 initialized git repos |
| **Phase 02** | R01 Contracts | SEQUENTIAL_REQUIRED | R01 Released | Schemas, types, fixture suite |
| **Phase 03** | R14 Observability | SEQUENTIAL_REQUIRED | R14 Released | OTel SDK, Secret Redaction |
| **Phase 04** | R02 Core State | SEQUENTIAL_REQUIRED | R02 Released | PostgreSQL schema, entities, state machine |
| **Phase 05** | R07 Provider SDK | SEQUENTIAL_REQUIRED | R07 Released | VideoProvider, FakeVideoProvider |
| **Gate 00** | Foundation Gate | SEQUENTIAL_REQUIRED | GATE_00 Passed | Contracts, State, SDK validated |
| **Phase 06** | R06 Workflow | SEQUENTIAL_REQUIRED | R06 Released | Temporal workflows & activities |
| **Phase 07** | R15 Integration Harness | SEQUENTIAL_REQUIRED | R15 Released | 16 Fault injection scenarios |
| **Gate 01** | FakeProvider E2E Gate | SEQUENTIAL_REQUIRED | GATE_01 Passed | Deterministic single-shot proven |
| **Phase 08** | R08 Google Flow Adapter | SEQUENTIAL_REQUIRED | R08 Released | FlowExecutionPort interface |
| **Phase 09** | R10 FlowKit Bridge | PARALLEL_SAFE_AFTER_GATE_01 | R10 Released | Direct Protocol Bridge (Track B) |
| **Phase 10** | R09 Browser Worker | PARALLEL_SAFE_AFTER_GATE_01 | R09 Released | Playwright CDP Worker (Track A) |
| **Gate 02** | Flow Port Conformance Gate | SEQUENTIAL_REQUIRED | GATE_02 Passed | 10-op benchmark equivalence |
| **Phase 11** | R03 Creative | PARALLEL_SAFE_AFTER_GATE_00 | R03 Released | LLM scene decomposition |
| **Phase 12** | R04 Assets Continuity | PARALLEL_SAFE_AFTER_GATE_00 | R04 Released | Character continuity manager |
| **Phase 13** | R05 Prompt Compiler | PARALLEL_SAFE_AFTER_R04 | R05 Released | Dialect template compiler |
| **Phase 14** | R11 QC Service | PARALLEL_SAFE_AFTER_GATE_00 | R11 Released | Technical & Semantic QC |
| **Phase 15** | R12 Media Service | PARALLEL_SAFE_AFTER_GATE_00 | R12 Released | FFmpeg video stitching |
| **Gate 03** | Creative & Media Gate | SEQUENTIAL_REQUIRED | GATE_03 Passed | End-to-end creative pipeline |
| **Phase 16** | R13 Operator Console | SEQUENTIAL_REQUIRED | R13 Released | Web UI for human review & DLQ |
| **Gate 04** | System Integration Gate | SEQUENTIAL_REQUIRED | GATE_04 Passed | Offline 15-repo complete system |
| **Gate 05** | Controlled Live Flow Gate | SEQUENTIAL_REQUIRED | GATE_05 Passed | Real Google Flow verification |
| **Phase 18** | Release Engineering | SEQUENTIAL_REQUIRED | v1.0.0 Released | Tagged & published system |
"""

# 7. FAILURE_DECISION_TREE.md
FAILURE_DECISION_TREE_MD = """# AI VIDEO FACTORY v1.0.0 — FAILURE DECISION TREE
## Systematic Error Triage & Recovery Routing Matrix

**Version:** 1.0.0  
**Authority:** Technical Architecture Board

---

## 1. Triage Decision Tree

```
Failure Detected during Prompt Execution
│
├── 1. Is the error a localized implementation bug (syntax error, failed unit test in current repo)?
│   └── YES ──> Run Local Repo Recovery: <REPO>_RECOVERY.md
│
├── 2. Is the error caused by a broken schema, missing field, or incompatible type definition?
│   └── YES ──> Run Contract Break Recovery: 99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md
│
├── 3. Does the error reveal a contradiction or flaw in the frozen specification (01_FROZEN_RELEASE/)?
│   └── YES ──> Open Formal Change Request: 99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md
│
├── 4. Is the failure due to an unbuilt or unreleased upstream dependency?
│   └── YES ──> Run Blocked Dependency Recovery: 99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md
│
├── 5. Did a system integration gate or scenario harness fail?
│   └── YES ──> Run Integration Gate Recovery: 99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md
│
├── 6. Did the coding agent stall, loop endlessly, or produce truncated code?
│   └── YES ──> Run Stalled Agent Recovery: 99_RECOVERY/RECOVERY_06_STALLED_AGENT.md
│
├── 7. Is the failure a Git conflict, dirty worktree, or branch drift?
│   └── YES ──> Run Git Recovery: 99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md
│
├── 8. Is Docker, PostgreSQL, Temporal, MinIO, or the dev environment unhealthy?
│   └── YES ──> Run Environment Recovery: 99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md
│
└── 9. Did Google Flow present a CAPTCHA, bot detection challenge, or rate limit?
    └── YES ──> Run External Provider Recovery: 99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md
```

---

## 2. Recovery Prompt Dispatch Catalog

| Category Code | Recovery Scenario | Dispatch Recovery Prompt |
|---|---|---|
| `REC-01` | Blocked Upstream Dependency | [RECOVERY_01_BLOCKED_DEPENDENCY.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md) |
| `REC-02` | Contract Incompatibility / Schema Break | [RECOVERY_02_CONTRACT_BREAK.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md) |
| `REC-03` | Frozen Spec Defect / Formal CR Required | [RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md) |
| `REC-04` | Unit / Conformance Test Gate Failure | [RECOVERY_04_TEST_GATE_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md) |
| `REC-05` | System Integration Gate Failure | [RECOVERY_05_INTEGRATION_GATE_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md) |
| `REC-06` | Stalled or Hallucinating Agent | [RECOVERY_06_STALLED_AGENT.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md) |
| `REC-07` | Git Conflicts & Branch State Inconsistencies| [RECOVERY_07_GIT_RECOVERY.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md) |
| `REC-08` | Docker / Local Dev Environment Outage | [RECOVERY_08_ENVIRONMENT_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md) |
| `REC-09` | External Provider Security Challenge / CAPTCHA| [RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md) |
"""

# 8. RESUME_PROJECT.md
RESUME_PROJECT_MD = """# AI VIDEO FACTORY v1.0.0 — SESSION RESUMPTION TOOL
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
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
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
**NEXT_PROMPT_IF_PASS:** Computed dynamically based on `RUN_STATE.yaml`.  
**NEXT_PROMPT_IF_FAIL:** `REC-08`

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
"""

files = {
    "START_HERE.md": START_HERE_MD,
    "RUN_STATE_TEMPLATE.yaml": RUN_STATE_TEMPLATE_YAML,
    "MODEL_MATRIX.md": MODEL_MATRIX_MD,
    "OPERATOR_RULES.md": OPERATOR_RULES_MD,
    "WORKSPACE_AND_REPO_MAP.md": WORKSPACE_AND_REPO_MAP_MD,
    "MASTER_SEQUENCE.md": MASTER_SEQUENCE_MD,
    "FAILURE_DECISION_TREE.md": FAILURE_DECISION_TREE_MD,
    "RESUME_PROJECT.md": RESUME_PROJECT_MD,
}

for name, content in files.items():
    filepath = os.path.join(RUNBOOK_DIR, name)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {name}")

print("Root documents generated successfully.")
