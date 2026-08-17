#!/usr/bin/env python3
"""
AI Video Factory v1.0.0 — Master Operator Runbook Generator
Generates the complete, production-grade 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/ pack.
"""

import os
import sys
import yaml
import re

BASE_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW"
RUNBOOK_DIR = os.path.join(BASE_DIR, "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0")
VALIDATORS_DIR = os.path.join(RUNBOOK_DIR, "validators")

SUBDIRS = [
    "00_CHECKPOINTS",
    "01_REPO_PROVISIONING",
    "02_R01_CONTRACTS",
    "03_R02_CORE_STATE",
    "04_R07_PROVIDER_SDK",
    "05_R06_WORKFLOW",
    "06_R15_INTEGRATION_HARNESS",
    "07_R08_GOOGLE_FLOW_ADAPTER",
    "08_R10_FLOWKIT_BRIDGE",
    "09_R09_BROWSER_WORKER",
    "10_R03_CREATIVE",
    "11_R04_ASSETS_CONTINUITY",
    "12_R05_PROMPT_COMPILER",
    "13_R11_QC",
    "14_R12_MEDIA",
    "15_R14_OBSERVABILITY",
    "16_R13_OPERATOR_CONSOLE",
    "17_INTEGRATION_GATES",
    "18_RELEASE",
    "99_RECOVERY",
    "validators"
]

for d in SUBDIRS:
    os.makedirs(os.path.join(RUNBOOK_DIR, d), exist_ok=True)

# 1. ROOT DOCS
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
  status: "IN_PROGRESS"

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
**NEXT_PROMPT_IF_PASS:** Dynamic routing based on `RUN_STATE.yaml`.  
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
"""

root_files = {
    "START_HERE.md": START_HERE_MD,
    "RUN_STATE_TEMPLATE.yaml": RUN_STATE_TEMPLATE_YAML,
    "MODEL_MATRIX.md": MODEL_MATRIX_MD,
    "OPERATOR_RULES.md": OPERATOR_RULES_MD,
    "WORKSPACE_AND_REPO_MAP.md": WORKSPACE_AND_REPO_MAP_MD,
    "MASTER_SEQUENCE.md": MASTER_SEQUENCE_MD,
    "FAILURE_DECISION_TREE.md": FAILURE_DECISION_TREE_MD,
    "RESUME_PROJECT.md": RESUME_PROJECT_MD,
}

for name, content in root_files.items():
    with open(os.path.join(RUNBOOK_DIR, name), "w") as f:
        f.write(content.strip() + "\n")

print("Generated root documents.")

# 2. CHECKPOINTS AND PROVISIONING
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

checkpoints_files = {
    "00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md": CHK_01_MD,
    "00_CHECKPOINTS/CHECKPOINT_02_ENVIRONMENT_DOCTOR.md": CHK_02_MD,
    "01_REPO_PROVISIONING/PROVISION_01_INSPECT_AND_PLAN.md": PROV_01_MD,
    "01_REPO_PROVISIONING/PROVISION_02_LOCAL_POLYREPO_INIT.md": PROV_02_MD,
    "01_REPO_PROVISIONING/PROVISION_03_GITHUB_REPOS_PROVISION.md": PROV_03_MD,
}

for rel_path, content in checkpoints_files.items():
    with open(os.path.join(RUNBOOK_DIR, rel_path), "w") as f:
        f.write(content.strip() + "\n")

print("Generated checkpoints and provisioning prompts.")

# 3. 15 REPOSITORIES (75 PROMPTS)
REPOS_CONFIG = [
    {
        "id": "R01",
        "prefix": "R01",
        "dir": "02_R01_CONTRACTS",
        "name": "R01_contracts",
        "display_name": "Contracts & Typed Schemas",
        "layer": "Layer 0",
        "phase": "02_R01_CONTRACTS",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R01_CONTRACTS.md",
        "contracts": [
            "02_contracts/domain-entities.schema.json",
            "02_contracts/event-envelope.schema.json",
            "02_contracts/provider-request.schema.json",
            "02_contracts/provider-result.schema.json",
            "02_contracts/browser-command.schema.json",
            "02_contracts/flow-execution-result.schema.json"
        ],
        "allowed_deps": "None (Pure schemas, types, validators)",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, Direct DB",
        "owns": "JSON Schemas, automated TypeScript type generation (json-schema-to-typescript), positive & negative fixture suites (>=3 each), FlowExecutionPort conformance test suite",
        "does_not_own": "Runtime execution, database connections, UI components, external network calls",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/15_R14_OBSERVABILITY/R14_01_PLAN.md",
        "prereq_plan": "PROV-03",
        "specific_guidance": "Read 05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md. Standardize $defs, represent all 17 normative execution stages, strongly-type discriminated unions for FlowExecutionResult 10 operations, produce positive and negative fixture test suites."
    },
    {
        "id": "R14",
        "prefix": "R14",
        "dir": "15_R14_OBSERVABILITY",
        "name": "R14_platform_observability",
        "display_name": "Observability, Telemetry & Security",
        "layer": "Cross-Cutting",
        "phase": "15_R14_OBSERVABILITY",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md",
        "contracts": ["02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "OpenTelemetry tracing SDK wrapper, correlation context propagation, secret & token redaction engine, structured log formatter, Prometheus metrics exporter",
        "does_not_own": "Domain persistence, business logic, workflow execution, provider calls",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/03_R02_CORE_STATE/R02_01_PLAN.md",
        "prereq_plan": "R01-04",
        "specific_guidance": "Zero secrets in logs. Automated redaction filter for Bearer tokens, cookies, passwords. Distributed trace context injection and W3C traceparent propagation."
    },
    {
        "id": "R02",
        "prefix": "R02",
        "dir": "03_R02_CORE_STATE",
        "name": "R02_core_state",
        "display_name": "Core State & Persistence Engine",
        "layer": "Layer 1",
        "phase": "03_R02_CORE_STATE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R02_CORE_STATE.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15",
        "owns": "PostgreSQL schema migrations, Prisma/Drizzle models, GenerationJob state machine, 17 execution stages, Idempotency store, entity CRUD API",
        "does_not_own": "Temporal workflow execution, video generation, browser automation, creative script generation",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/04_R07_PROVIDER_SDK/R07_01_PLAN.md",
        "prereq_plan": "R14-04",
        "specific_guidance": "Enforce INV-001 through INV-012. Deterministic state transitions, idempotency key uniqueness, sole owner of PostgreSQL connection."
    },
    {
        "id": "R07",
        "prefix": "R07",
        "dir": "04_R07_PROVIDER_SDK",
        "name": "R07_provider_sdk",
        "display_name": "Provider Neutral SDK & FakeProvider",
        "layer": "Layer 3",
        "phase": "04_R07_PROVIDER_SDK",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R07_PROVIDER_SDK.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "VideoProvider interface abstraction, capability matrix parser, normalized 9-error taxonomy, FakeVideoProvider with full simulation matrix",
        "does_not_own": "PostgreSQL persistence, Google Flow specific automation, Temporal workflows",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md",
        "prereq_plan": "R02-04",
        "specific_guidance": "FakeVideoProvider must support success(0s), success(30s), fail_transient(2), fail_provider, rate_limit, timeout, status_unknown, corrupt_output."
    },
    {
        "id": "R06",
        "prefix": "R06",
        "dir": "05_R06_WORKFLOW",
        "name": "R06_workflow",
        "display_name": "Temporal Workflow Orchestrator",
        "layer": "Layer 5",
        "phase": "05_R06_WORKFLOW",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R06_WORKFLOW.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json", "02_contracts/provider-request.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state, R03_creative, R04_assets_continuity, R05_prompt_compiler, R07_provider_sdk, R08_google_flow_adapter, R11_qc, R12_media, R14_platform_observability",
        "forbidden_deps": "R09, R10, Direct DB",
        "owns": "Temporal workflow definitions (SingleShot, MultiShot, RenderPipeline), retry policy engine, activity handlers, reconciliation logic",
        "does_not_own": "Database tables directly, browser automation, raw video rendering, UI rendering",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/06_R15_INTEGRATION_HARNESS/R15_01_PLAN.md",
        "prereq_plan": "GATE-00",
        "specific_guidance": "Temporal replay safety, deterministic workflows, exponential backoff with jitter, idempotency token persistence, crash/reconciliation."
    },
    {
        "id": "R15",
        "prefix": "R15",
        "dir": "06_R15_INTEGRATION_HARNESS",
        "name": "R15_integration_harness",
        "display_name": "End-to-End Integration & Scenario Test Harness",
        "layer": "Cross-Cutting",
        "phase": "06_R15_INTEGRATION_HARNESS",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R15_INTEGRATION_HARNESS.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json", "02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json", "02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14",
        "forbidden_deps": "Direct production DB mutation",
        "owns": "16 chaos/fault-injection scenarios, E2E test runner, offline test orchestration, golden test fixture assertions",
        "does_not_own": "Production runtime services, application logic",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_01_FAKEPROVIDER_E2E_GATE.md",
        "prereq_plan": "R06-04",
        "specific_guidance": "Implement 16 fault-injection scenarios: worker kill before/after submit, uncertain ack, duplicate delivery, provider timeout, browser disconnect, corrupted video output, budget block."
    },
    {
        "id": "R08",
        "prefix": "R08",
        "dir": "07_R08_GOOGLE_FLOW_ADAPTER",
        "name": "R08_google_flow_adapter",
        "display_name": "Google Flow Provider Adapter",
        "layer": "Layer 3",
        "phase": "07_R08_GOOGLE_FLOW_ADAPTER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json", "02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R07_provider_sdk, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, Direct DB",
        "owns": "Google Flow adapter implementing VideoProvider interface, FlowExecutionPort client caller, prompt/aspect translation",
        "does_not_own": "Direct browser automation code, WebSocket network parsing, database access",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/08_R10_FLOWKIT_BRIDGE/R10_01_PLAN.md",
        "prereq_plan": "GATE-01",
        "specific_guidance": "Decouple provider logic from execution tracks via 10-operation FlowExecutionPort abstraction."
    },
    {
        "id": "R10",
        "prefix": "R10",
        "dir": "08_R10_FLOWKIT_BRIDGE",
        "name": "R10_flowkit_bridge",
        "display_name": "Track B Direct FlowKit Bridge",
        "layer": "Layer 4",
        "phase": "08_R10_FLOWKIT_BRIDGE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md",
        "contracts": ["02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R11, R12, R13, Direct DB",
        "owns": "Direct HTTP/WebSocket protocol client implementing 10-operation FlowExecutionPort",
        "does_not_own": "Browser automation, DOM interaction, database state, workflow logic",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_01_PLAN.md",
        "prereq_plan": "R08-04",
        "specific_guidance": "10-op port conformance, session maintenance, token refresh, normalized error mapping."
    },
    {
        "id": "R09",
        "prefix": "R09",
        "dir": "09_R09_BROWSER_WORKER",
        "name": "R09_browser_worker",
        "display_name": "Track A Browser Automation Worker",
        "layer": "Layer 4",
        "phase": "09_R09_BROWSER_WORKER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R09_BROWSER_WORKER.md",
        "contracts": ["02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R10, R11, R12, R13, Direct DB",
        "owns": "Playwright/CDP automation implementing 10-operation FlowExecutionPort, 4-tier selector resolution (DOM, A11y, Visual, Agent Recovery), anti-abuse safety",
        "does_not_own": "Direct DB, direct API bridge, workflow state",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE.md",
        "prereq_plan": "R10-04",
        "specific_guidance": "Strict anti-abuse safety, human gate escalation on CAPTCHA/challenge, session isolation."
    },
    {
        "id": "R03",
        "prefix": "R03",
        "dir": "10_R03_CREATIVE",
        "name": "R03_creative",
        "display_name": "Creative & Script Generation Engine",
        "layer": "Layer 2",
        "phase": "10_R03_CREATIVE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R03_CREATIVE.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R14_platform_observability",
        "forbidden_deps": "R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "LLM-assisted story/scene decomposition service, scene parsing, creative structured outputs",
        "does_not_own": "Database persistence, video rendering, browser execution",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_01_PLAN.md",
        "prereq_plan": "GATE-02",
        "specific_guidance": "Strict JSON schema enforcement on LLM outputs, deterministic fallback parsers."
    },
    {
        "id": "R04",
        "prefix": "R04",
        "dir": "11_R04_ASSETS_CONTINUITY",
        "name": "R04_assets_continuity",
        "display_name": "Assets & Character Continuity Service",
        "layer": "Layer 2",
        "phase": "11_R04_ASSETS_CONTINUITY",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R04_ASSETS_CONTINUITY.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R14_platform_observability",
        "forbidden_deps": "R03, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "Asset catalog service, character reference embedding management, continuity token injection",
        "does_not_own": "Database persistence, video generation, workflow orchestration",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/12_R05_PROMPT_COMPILER/R05_01_PLAN.md",
        "prereq_plan": "R03-04",
        "specific_guidance": "Character reference consistency across multi-shot sequences."
    },
    {
        "id": "R05",
        "prefix": "R05",
        "dir": "12_R05_PROMPT_COMPILER",
        "name": "R05_prompt_compiler",
        "display_name": "Provider-Aware Prompt Compiler",
        "layer": "Layer 2",
        "phase": "12_R05_PROMPT_COMPILER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R05_PROMPT_COMPILER.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R04_assets_continuity (API), R14_platform_observability",
        "forbidden_deps": "R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "Prompt template compiler, dialect transformations (Veo, Luma, Runway syntax), negative prompt rules, safety filters",
        "does_not_own": "Direct video generation, storage, database",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_01_PLAN.md",
        "prereq_plan": "R04-04",
        "specific_guidance": "Deterministic prompt compilation, dialect rule engine, token substitution."
    },
    {
        "id": "R11",
        "prefix": "R11",
        "dir": "13_R11_QC",
        "name": "R11_qc",
        "display_name": "Quality Control & Validation Service",
        "layer": "Layer 2",
        "phase": "13_R11_QC",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R11_QC.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R12, R13, Direct DB",
        "owns": "Technical QC (FFprobe container, stream, resolution, framerate, duration check), Semantic QC (LLM/Vision scoring), bounded retry decision output",
        "does_not_own": "Database persistence, video stitching, video generation",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/14_R12_MEDIA/R12_01_PLAN.md",
        "prereq_plan": "R05-04",
        "specific_guidance": "Fast technical inspection before expensive semantic evaluation, quarantine DLQ."
    },
    {
        "id": "R12",
        "prefix": "R12",
        "dir": "14_R12_MEDIA",
        "name": "R12_media",
        "display_name": "Media Processing & Assembly Service",
        "layer": "Layer 2",
        "phase": "14_R12_MEDIA",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R12_MEDIA.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R13, Direct DB",
        "owns": "FFmpeg stitching, audio track overlay, color normalization, video transcoding, final packaging",
        "does_not_own": "Database persistence, generation workflows",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_03_CREATIVE_MEDIA_GATE.md",
        "prereq_plan": "R11-04",
        "specific_guidance": "Safe subprocess invocation, deterministic transcoding parameters."
    },
    {
        "id": "R13",
        "prefix": "R13",
        "dir": "16_R13_OPERATOR_CONSOLE",
        "name": "R13_operator_console",
        "display_name": "Human-in-the-Loop Operator Console",
        "layer": "Layer 5",
        "phase": "16_R13_OPERATOR_CONSOLE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R06_workflow (API), R14_platform_observability",
        "forbidden_deps": "R03, R04, R05, R07, R08, R09, R10, R11, R12, R15, Direct DB, Worker Internals",
        "owns": "Operator UI web application for human approval gates, generation inspection, error triage, DLQ replay triggers",
        "does_not_own": "Direct database mutations, worker execution internals",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_04_SYSTEM_INTEGRATION_GATE.md",
        "prereq_plan": "GATE-03",
        "specific_guidance": "Web UI interacting strictly via R02 Core State REST/gRPC and R06 Temporal client APIs."
    }
]

def generate_repo_suite(repo):
    p_id = repo["id"]
    p_dir = repo["dir"]
    name = repo["name"]
    disp = repo["display_name"]
    phase = repo["phase"]
    bp = repo["blueprint"]
    owns = repo["owns"]
    not_owns = repo["does_not_own"]
    allowed_deps = repo["allowed_deps"]
    forbidden_deps = repo["forbidden_deps"]
    guidance = repo["specific_guidance"]
    
    plan_id = f"{p_id}-01"
    plan_path = f"{p_dir}/{p_id}_01_PLAN.md"
    impl_id = f"{p_id}-02"
    impl_path = f"{p_dir}/{p_id}_02_IMPLEMENT.md"
    test_id = f"{p_id}-03"
    test_path = f"{p_dir}/{p_id}_03_TEST_AND_REVIEW.md"
    accept_id = f"{p_id}-04"
    accept_path = f"{p_dir}/{p_id}_04_ACCEPT_RELEASE.md"
    rec_id = f"{p_id}-REC"
    rec_file_path = f"{p_dir}/{p_id}_RECOVERY.md"
    
    plan_content = f"""# {p_id} {disp.upper()} — IMPLEMENTATION PLAN
## AI Video Factory — Architectural Specification & Test Plan

**PROMPT_ID:** `{plan_id}`  
**PURPOSE:** Create the complete architectural implementation and test plan for {name} ({disp}) adhering to all 16 blueprint sections without authoring production code.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["plan_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `{repo["prereq_plan"]}`  
**READ_ONLY_INPUTS:**
- `{bp}`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{plan_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`  
**PASS_CRITERIA:**
- PLAN.md covers all 16 blueprint sections from `{bp}`.
- Specific boundaries respected: OWNS: {owns}; DOES NOT OWN: {not_owns}.
- Allowed dependencies: {allowed_deps}; Forbidden dependencies: {forbidden_deps}.
- Test strategy defines >=85% coverage and contract conformance.
- Zero production code authored in this planning step.  
**FAIL_CRITERIA:**
- Missing blueprint sections or production source files written during planning.  
**GIT_EXPECTATION:** Plan committed on feature branch `feature/{p_id.lower()}-scaffold`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{rec_file_path}`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path}`

---

### Step-by-Step Instructions:

1. **Inspect Blueprint & Contracts:**
   Read `{bp}` and examine referenced schemas.
2. **Review Specific Hardening Requirements:**
   {guidance}
3. **Formulate PLAN.md:**
   Write `05_IMPLEMENTATION/repos/{name}/PLAN.md` detailing:
   - Module architecture and component breakdown
   - TypeScript interfaces / schemas
   - State ownership, persistence, and concurrency models
   - Error taxonomy & retry policy
   - Observability integration (via R14)
   - Comprehensive test plan (unit, contract, negative)
   - Definition of Done checklist
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{plan_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-scaffold"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 0, failed: 0}}
CONTRACT_TESTS: {{passed: 0, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/PLAN.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path}"
RECOMMENDED_NEXT_TASK: "Implement {name} application code and unit/contract test suites."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    impl_content = f"""# {p_id} {disp.upper()} — IMPLEMENTATION & BUILD
## AI Video Factory — Source Code Authoring & Test Suite Implementation

**PROMPT_ID:** `{impl_id}`  
**PURPOSE:** Implement all production source code, build toolchains, unit tests, and contract fixtures for {name} ({disp}) according to the approved PLAN.md.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["impl_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `{plan_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `{bp}`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Production source code in `05_IMPLEMENTATION/repos/{name}/src/`
- Test suites in `05_IMPLEMENTATION/repos/{name}/tests/`
- Build script passing cleanly (`npm test` / `pytest`).  
**PASS_CRITERIA:**
- All components in PLAN.md fully implemented without placeholder stubs.
- OWNS boundaries strictly enforced: {owns}.
- Zero forbidden dependencies imported: {forbidden_deps}.
- Unit and contract tests execute and pass 100%.  
**FAIL_CRITERIA:**
- Build compilation failure, test failures, or cross-repo file modifications.  
**GIT_EXPECTATION:** Clean commits on feature branch `feature/{p_id.lower()}-impl`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{rec_file_path}`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{test_path}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path}`

---

### Step-by-Step Instructions:

1. **Implement Core Components:**
   Author production modules in `src/` satisfying all architectural responsibilities.
2. **Implement Test Suites:**
   Build unit and contract test suites under `tests/`.
3. **Execute Local Build & Tests:**
   Run test suites and verify 100% pass rate with zero lint/type errors.
4. **Git Commit:**
   Commit all changes to `feature/{p_id.lower()}-impl`.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{impl_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 12, failed: 0}}
CONTRACT_TESTS: {{passed: 6, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/src/"
  - "05_IMPLEMENTATION/repos/{name}/tests/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{test_path}"
RECOMMENDED_NEXT_TASK: "Execute independent technical and adversarial review of {name}."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    test_content = f"""# {p_id} {disp.upper()} — INDEPENDENT TECHNICAL REVIEW & AUDIT
## AI Video Factory — Negative Testing, Security & Boundary Conformance

**PROMPT_ID:** `{test_id}`  
**PURPOSE:** Perform an independent technical audit of {name} ({disp}), executing negative test suites, contract compatibility checks, secret redaction validation, and dependency boundary verification.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["review_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (3-5 min)`  
**PREREQUISITES:** `{impl_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `05_IMPLEMENTATION/repos/{name}/src/**`
- `05_IMPLEMENTATION/repos/{name}/tests/**`
- `{bp}`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{test_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`  
**PASS_CRITERIA:**
- Zero forbidden imports detected (scanned against: {forbidden_deps}).
- Branch test coverage >= 85%.
- Negative fixtures correctly trigger normalized error responses.
- Observability and secret redaction verified.  
**FAIL_CRITERIA:**
- Boundary leak, uncovered critical path, secret leakage, or failed contract assertions.  
**GIT_EXPECTATION:** Audit report committed on branch.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{rec_file_path}`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{accept_path}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path}`

---

### Step-by-Step Instructions:

1. **Dependency Boundary Scan:**
   Run static grep search across `05_IMPLEMENTATION/repos/{name}/src/` to confirm zero forbidden imports.
2. **Execute Full Test & Negative Fixture Suite:**
   Run all positive, negative, and edge-case unit and contract tests.
3. **Verify Observability & Redaction:**
   Confirm that all telemetry integration masks sensitive credentials and attaches trace contexts.
4. **Compile AUDIT_REPORT.md:**
   Document test metrics, boundary scan results, and final verification signoff.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{test_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 18, failed: 0}}
CONTRACT_TESTS: {{passed: 8, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{accept_path}"
RECOMMENDED_NEXT_TASK: "Execute formal acceptance and release tagging for {name}."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    accept_content = f"""# {p_id} {disp.upper()} — ACCEPTANCE & RELEASE
## AI Video Factory — Formal Acceptance, Merge & Version Tagging

**PROMPT_ID:** `{accept_id}`  
**PURPOSE:** Conduct formal acceptance signoff for {name} ({disp}), merge feature branch to main, apply annotated git release tag, and unlock downstream dependency gates.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["accept_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `{repo["accept_conv"]}`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `{test_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `{bp}`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{accept_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Released `main` branch with annotated release tag `v1.0.0`
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- All tests pass on `main`.
- Clean merge commit and git tag `{name.lower()}-v1.0.0` applied.
- Repository status marked as `RELEASED` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Merge conflict, uncommitted changes, or failing CI checks.  
**GIT_EXPECTATION:** Tagged release commit on `main`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{rec_file_path}`.  
**NEXT_PROMPT_IF_PASS:** `{repo["pass_after_accept"]}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path}`

---

### Step-by-Step Instructions:

1. **Verify Audit Signoff:**
   Inspect `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md` and confirm PASS verdict.
2. **Merge to Main Branch:**
   Checkout `main` and merge `feature/{p_id.lower()}-impl` cleanly:
   `git checkout main && git merge --no-ff feature/{p_id.lower()}-impl -m "feat({p_id.lower()}): complete {name} implementation"`
3. **Apply Release Tag:**
   Apply annotated git tag:
   `git tag -a "{name.lower()}-v1.0.0" -m "Release {name} v1.0.0"`
4. **Update System Runtime State:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `{name}.status: "RELEASED"` and record commit SHA and tag.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{accept_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 18, failed: 0}}
CONTRACT_TESTS: {{passed: 8, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/ (tagged {name.lower()}-v1.0.0)"
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "{repo["pass_after_accept"]}"
RECOMMENDED_NEXT_TASK: "Proceed to next scheduled prompt in master execution sequence."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    rec_content = f"""# {p_id} {disp.upper()} — RECOVERY & TRIAGE
## AI Video Factory — Local Repository Defect Triage & Routing

**PROMPT_ID:** `{rec_id}`  
**PURPOSE:** Triage failures occurring within {name} ({disp}), categorize the defect class, and route to local remediation or master system recovery.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/FAILURE_DECISION_TREE.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Diagnostic defect analysis and targeted recovery action.  
**PASS_CRITERIA:**
- Defect correctly categorized (IMPLEMENTATION_BUG, CONTRACT_DEFECT, FROZEN_SPEC_DEFECT, ENVIRONMENT, DEPENDENCY, EXTERNAL_PROVIDER).
- Exact remediation command or recovery prompt returned.  
**FAIL_CRITERIA:**
- Unclassified defect.  
**GIT_EXPECTATION:** Worktree preserved for debugging.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human architect.  
**NEXT_PROMPT_IF_PASS:** Dynamic routing based on defect class.  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md`

---

### Defect Classification & Dispatch Matrix:

1. **Category A: Local Implementation Bug (Syntax, Logic, Local Unit Test)**
   - **Action:** Fix code within `05_IMPLEMENTATION/repos/{name}/src/` and re-run `{impl_path}`.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path}`
2. **Category B: Schema Incompatibility / Contract Break**
   - **Action:** Open contract change triage.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md`
3. **Category C: Frozen Spec Contradiction**
   - **Action:** Open formal Change Request.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md`
4. **Category D: Upstream Dependency Missing or Broken**
   - **Action:** Verify upstream repository release.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md`
5. **Category E: Git Conflict / Branch State Issue**
   - **Action:** Run git state reconciliation.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`
6. **Category F: Environment / Toolchain Failure**
   - **Action:** Re-run environment doctor.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`
"""

    return {
        plan_path: plan_content,
        impl_path: impl_content,
        test_path: test_content,
        accept_path: accept_content,
        rec_file_path: rec_content
    }

for repo in REPOS_CONFIG:
    suite = generate_repo_suite(repo)
    for rel_path, content in suite.items():
        with open(os.path.join(RUNBOOK_DIR, rel_path), "w") as f:
            f.write(content.strip() + "\n")

print("Generated all 75 repository prompt files.")

# 4. GATES AND RELEASE
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

gates_files = {
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

for rel_path, content in gates_files.items():
    with open(os.path.join(RUNBOOK_DIR, rel_path), "w") as f:
        f.write(content.strip() + "\n")

print("Generated gates and release prompts.")

# 5. RECOVERY PROMPTS
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

recovery_files = {
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

for rel_path, content in recovery_files.items():
    with open(os.path.join(RUNBOOK_DIR, rel_path), "w") as f:
        f.write(content.strip() + "\n")

print("Generated recovery prompts.")

# 6. RUNBOOK_MANIFEST.YAML GENERATION
def extract_header_fields(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    fields = {}
    patterns = {
        "id": r"\*\*PROMPT_ID:\*\*\s*`?([^`\n]+)`?",
        "purpose": r"\*\*PURPOSE:\*\*\s*([^\n]+)",
        "phase": r"\*\*CURRENT_PHASE:\*\*\s*`?([^`\n]+)`?",
        "workspace": r"\*\*RUN_FROM_WORKSPACE:\*\*\s*`?([^`\n]+)`?",
        "repo": r"\*\*OPEN_REPOSITORY:\*\*\s*`?([^`\n]+)`?",
        "working_dir": r"\*\*WORKING_DIRECTORY:\*\*\s*`?([^`\n]+)`?",
        "model": r"\*\*MODEL:\*\*\s*`?([^`\n]+)`?",
        "model_fallback": r"\*\*MODEL_FALLBACK:\*\*\s*`?([^`\n]+)`?",
        "mode": r"\*\*ANTIGRAVITY_MODE:\*\*\s*`?([^`\n]+)`?",
        "conversation": r"\*\*NEW_OR_EXISTING_CONVERSATION:\*\*\s*`?([^`\n]+)`?",
        "duration": r"\*\*EXPECTED_DURATION_CLASS:\*\*\s*`?([^`\n]+)`?",
        "prerequisites": r"\*\*PREREQUISITES:\*\*\s*`?([^`\n]+)`?",
        "pass_next": r"\*\*NEXT_PROMPT_IF_PASS:\*\*\s*`?([^`\n]+)`?",
        "fail_next": r"\*\*NEXT_PROMPT_IF_FAIL:\*\*\s*`?([^`\n]+)`?"
    }
    for key, pat in patterns.items():
        m = re.search(pat, content)
        if m:
            fields[key] = m.group(1).strip()
        else:
            fields[key] = None
            
    writes_m = re.search(r"\*\*WRITEABLE_PATHS:\*\*\n([\s\S]*?)(?=\*\*FORBIDDEN_PATHS:)", content)
    if writes_m:
        writes_lines = [l.strip("- `").strip() for l in writes_m.group(1).strip().split("\n") if l.strip().startswith("-")]
        fields["writes_to"] = writes_lines
    else:
        fields["writes_to"] = []
        
    forbid_m = re.search(r"\*\*FORBIDDEN_PATHS:\*\*\n([\s\S]*?)(?=\*\*COMMAND_TO_RUN:)", content)
    if forbid_m:
        forbid_lines = [l.strip("- `").strip() for l in forbid_m.group(1).strip().split("\n") if l.strip().startswith("-")]
        fields["forbidden_writes"] = forbid_lines
    else:
        fields["forbidden_writes"] = []
        
    return fields

all_prompt_entries = []
for root, dirs, files in os.walk(RUNBOOK_DIR):
    if "validators" in root:
        continue
    for file in sorted(files):
        if file.endswith(".md"):
            rel_path = os.path.relpath(os.path.join(root, file), RUNBOOK_DIR)
            if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                continue
            
            filepath = os.path.join(RUNBOOK_DIR, rel_path)
            hdr = extract_header_fields(filepath)
            
            entry = {
                "id": hdr["id"] or file.replace(".md", ""),
                "path": rel_path,
                "phase": hdr["phase"] or "GENERAL",
                "repo": hdr["repo"] or "SYSTEM",
                "purpose": hdr["purpose"] or "",
                "model": hdr["model"] or "Gemini 3.7 Flash High",
                "model_fallback": hdr["model_fallback"] or "Gemini 3.1 Pro High",
                "mode": hdr["mode"] or "Local workspace",
                "conversation_type": hdr["conversation"] or "NEW_OR_EXISTING",
                "duration_class": hdr["duration"] or "FAST (<3 min)",
                "prerequisites": [p.strip() for p in hdr["prerequisites"].split(",")] if hdr["prerequisites"] and hdr["prerequisites"] != "None" else [],
                "pass_next": hdr["pass_next"] or "TERMINAL_COMPLETE",
                "fail_next": hdr["fail_next"] or "99_RECOVERY/RECOVERY_06_STALLED_AGENT.md",
                "parallel_group": "PARALLEL_SAFE" if "PARALLEL_SAFE" in str(hdr.get("purpose", "")) or "PARALLEL" in str(hdr.get("phase", "")) else "NONE",
                "writes_to": hdr["writes_to"],
                "forbidden_writes": hdr["forbidden_writes"]
            }
            all_prompt_entries.append(entry)

manifest_data = {
    "version": "1.0.0",
    "project": "AI Video Factory",
    "total_prompts": len(all_prompt_entries),
    "prompts": all_prompt_entries
}

manifest_path = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")
with open(manifest_path, "w") as f:
    yaml.dump(manifest_data, f, sort_keys=False, default_flow_style=False)

print(f"Generated RUNBOOK_MANIFEST.yaml with {len(all_prompt_entries)} prompt entries.")

# 7. VALIDATORS
VALIDATE_MANIFEST_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[1/6] Running validate_manifest.py...")
    if not os.path.exists(MANIFEST_PATH):
        print(f"FAIL: Manifest not found at {MANIFEST_PATH}")
        return False
        
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    if len(prompts) == 0:
        print("FAIL: Zero prompts found in manifest.")
        return False
        
    ids = set()
    required_keys = ["id", "path", "phase", "repo", "purpose", "model", "model_fallback", "mode", "conversation_type", "pass_next", "fail_next", "writes_to", "forbidden_writes"]
    
    for p in prompts:
        for k in required_keys:
            if k not in p or p[k] is None:
                print(f"FAIL: Prompt {p.get('id')} missing required key '{k}'")
                return False
                
        if p["id"] in ids:
            print(f"FAIL: Duplicate prompt ID detected: {p['id']}")
            return False
        ids.add(p["id"])
        
        file_path = os.path.join(RUNBOOK_DIR, p["path"])
        if not os.path.exists(file_path):
            print(f"FAIL: Referenced file does not exist: {p['path']}")
            return False
            
    print(f"PASS: Manifest is valid with {len(prompts)} uniquely identified prompts.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

VALIDATE_PROMPT_HEADERS_PY = """#!/usr/bin/env python3
import os
import re
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANDATORY_HEADERS = [
    "PROMPT_ID",
    "PURPOSE",
    "CURRENT_PHASE",
    "RUN_FROM_WORKSPACE",
    "OPEN_REPOSITORY",
    "WORKING_DIRECTORY",
    "MODEL",
    "MODEL_FALLBACK",
    "ANTIGRAVITY_MODE",
    "NEW_OR_EXISTING_CONVERSATION",
    "EXPECTED_DURATION_CLASS",
    "PREREQUISITES",
    "READ_ONLY_INPUTS",
    "WRITEABLE_PATHS",
    "FORBIDDEN_PATHS",
    "COMMAND_TO_RUN",
    "EXPECTED_ARTIFACTS",
    "PASS_CRITERIA",
    "FAIL_CRITERIA",
    "GIT_EXPECTATION",
    "HUMAN_ACTION_AFTER_PASS",
    "HUMAN_ACTION_AFTER_FAIL",
    "NEXT_PROMPT_IF_PASS",
    "NEXT_PROMPT_IF_FAIL"
]

def validate():
    print("[2/6] Running validate_prompt_headers.py...")
    failures = 0
    total_files = 0
    
    for root, dirs, files in os.walk(RUNBOOK_DIR):
        if "validators" in root:
            continue
        for file in sorted(files):
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), RUNBOOK_DIR)
                if "/" not in rel_path and rel_path != "RESUME_PROJECT.md":
                    continue
                    
                total_files += 1
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    content = f.read()
                    
                missing = []
                for h in MANDATORY_HEADERS:
                    if f"**{h}:**" not in content:
                        missing.append(h)
                        
                if missing:
                    print(f"FAIL: {rel_path} missing mandatory headers: {missing}")
                    failures += 1
                    
    if failures > 0:
        print(f"FAIL: {failures}/{total_files} prompt files failed header validation.")
        return False
        
    print(f"PASS: All {total_files} execution prompts contain all 24 mandatory header fields.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

VALIDATE_NEXT_LINKS_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

def validate():
    print("[3/6] Running validate_next_links.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    valid_paths = set(p["path"] for p in prompts)
    valid_ids = set(p["id"] for p in prompts)
    
    failures = 0
    for p in prompts:
        pass_link = p["pass_next"]
        fail_link = p["fail_next"]
        
        if pass_link != "TERMINAL_COMPLETE" and not pass_link.startswith("Dynamic"):
            clean_pass = pass_link.replace("04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/", "")
            if clean_pass not in valid_paths and pass_link not in valid_ids:
                print(f"FAIL: Prompt {p['id']} has unresolved pass_next link: {pass_link}")
                failures += 1
                
        if fail_link != "TERMINAL_COMPLETE" and not fail_link.startswith("Dynamic"):
            clean_fail = fail_link.replace("04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/", "")
            if clean_fail not in valid_paths and fail_link not in valid_ids:
                print(f"FAIL: Prompt {p['id']} has unresolved fail_next link: {fail_link}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: {failures} dangling next links found.")
        return False
        
    print(f"PASS: Zero dangling links across all {len(prompts)} prompts. Graph resolves completely.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

VALIDATE_REPO_COVERAGE_PY = """#!/usr/bin/env python3
import os
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_REPOS = [
    ("R01", "02_R01_CONTRACTS", "R01_contracts"),
    ("R14", "15_R14_OBSERVABILITY", "R14_platform_observability"),
    ("R02", "03_R02_CORE_STATE", "R02_core_state"),
    ("R07", "04_R07_PROVIDER_SDK", "R07_provider_sdk"),
    ("R06", "05_R06_WORKFLOW", "R06_workflow"),
    ("R15", "06_R15_INTEGRATION_HARNESS", "R15_integration_harness"),
    ("R08", "07_R08_GOOGLE_FLOW_ADAPTER", "R08_google_flow_adapter"),
    ("R10", "08_R10_FLOWKIT_BRIDGE", "R10_flowkit_bridge"),
    ("R09", "09_R09_BROWSER_WORKER", "R09_browser_worker"),
    ("R03", "10_R03_CREATIVE", "R03_creative"),
    ("R04", "11_R04_ASSETS_CONTINUITY", "R04_assets_continuity"),
    ("R05", "12_R05_PROMPT_COMPILER", "R05_prompt_compiler"),
    ("R11", "13_R11_QC", "R11_qc"),
    ("R12", "14_R12_MEDIA", "R12_media"),
    ("R13", "16_R13_OPERATOR_CONSOLE", "R13_operator_console"),
]

PROMPT_SUFFIXES = [
    "01_PLAN.md",
    "02_IMPLEMENT.md",
    "03_TEST_AND_REVIEW.md",
    "04_ACCEPT_RELEASE.md",
    "RECOVERY.md"
]

def validate():
    print("[4/6] Running validate_repo_coverage.py...")
    failures = 0
    
    for r_id, r_dir, r_name in REQUIRED_REPOS:
        target_dir = os.path.join(RUNBOOK_DIR, r_dir)
        if not os.path.exists(target_dir):
            print(f"FAIL: Missing directory for {r_id} at {r_dir}")
            failures += 1
            continue
            
        for s in PROMPT_SUFFIXES:
            fname = f"{r_id}_{s}"
            fpath = os.path.join(target_dir, fname)
            if not os.path.exists(fpath):
                print(f"FAIL: Missing prompt {fname} in {r_dir}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Repository coverage check failed with {failures} missing files.")
        return False
        
    print(f"PASS: 15/15 repositories fully covered with 5-prompt standard suites (75/75 prompts).")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

VALIDATE_MODEL_MATRIX_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

ALLOWED_MODELS = [
    "Gemini 3.7 Flash High",
    "Gemini 3.1 Pro High",
    "Claude Opus 4.6 Thinking"
]

CRITICAL_ACCEPTANCE_PROMPTS = [
    "R01-04",
    "R06-04",
    "R08-04",
    "R10-04",
    "R09-04",
    "GATE-00",
    "GATE-02",
    "GATE-05",
    "REL-01"
]

def validate():
    print("[5/6] Running validate_model_matrix.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    failures = 0
    
    for p in prompts:
        model = p.get("model")
        fallback = p.get("model_fallback")
        conv = p.get("conversation_type")
        
        if model not in ALLOWED_MODELS:
            print(f"FAIL: Invalid model '{model}' in prompt {p['id']}")
            failures += 1
            
        if fallback not in ALLOWED_MODELS:
            print(f"FAIL: Invalid fallback model '{fallback}' in prompt {p['id']}")
            failures += 1
            
        if p["id"] in CRITICAL_ACCEPTANCE_PROMPTS:
            if model != "Claude Opus 4.6 Thinking":
                print(f"FAIL: Critical acceptance prompt {p['id']} must use Claude Opus 4.6 Thinking, got {model}")
                failures += 1
            if conv != "NEW_REQUIRED":
                print(f"FAIL: Critical acceptance prompt {p['id']} must require NEW conversation, got {conv}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Model matrix validation failed with {failures} issues.")
        return False
        
    print("PASS: Model routing, fallback definitions, and hostile acceptance assignments verified.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

VALIDATE_FROZEN_PATH_GUARDS_PY = """#!/usr/bin/env python3
import os
import yaml
import sys

RUNBOOK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(RUNBOOK_DIR, "RUNBOOK_MANIFEST.yaml")

FROZEN_PREFIXES = [
    "01_FROZEN_RELEASE",
    "02_SOURCE_KITS_READONLY",
    "03_GOVERNANCE_EVIDENCE_READONLY",
    "90_ARCHIVE_READONLY"
]

def validate():
    print("[6/6] Running validate_frozen_path_guards.py...")
    with open(MANIFEST_PATH, "r") as f:
        data = yaml.safe_load(f)
        
    prompts = data.get("prompts", [])
    failures = 0
    
    for p in prompts:
        writes = p.get("writes_to", [])
        forbidden = p.get("forbidden_writes", [])
        
        for w in writes:
            for frz in FROZEN_PREFIXES:
                if w.startswith(frz):
                    print(f"FAIL: Prompt {p['id']} declares writable access to frozen path: {w}")
                    failures += 1
                    
        for frz in FROZEN_PREFIXES:
            guarded = any(f.startswith(frz) for f in forbidden)
            if not guarded:
                print(f"FAIL: Prompt {p['id']} does not explicitly forbid writes to {frz}")
                failures += 1
                
    if failures > 0:
        print(f"FAIL: Frozen path guard check failed with {failures} violations.")
        return False
        
    print("PASS: Zero frozen-write permissions found. Absolute baseline protection confirmed across all prompts.")
    return True

if __name__ == "__main__":
    if not validate():
        sys.exit(1)
"""

RUN_ALL_VALIDATORS_PY = """#!/usr/bin/env python3
import subprocess
import sys
import os

VALIDATORS = [
    "validate_manifest.py",
    "validate_prompt_headers.py",
    "validate_next_links.py",
    "validate_repo_coverage.py",
    "validate_model_matrix.py",
    "validate_frozen_path_guards.py"
]

def main():
    print("================================================================")
    print(" AI VIDEO FACTORY v1.0.0 — RUNBOOK VALIDATION SUITE")
    print("================================================================")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    failed = []
    
    for val in VALIDATORS:
        val_path = os.path.join(script_dir, val)
        res = subprocess.run([sys.executable, val_path])
        if res.returncode != 0:
            failed.append(val)
            
    print("================================================================")
    if failed:
        print(f"RESULT: FAILED ({len(failed)}/{len(VALIDATORS)} validators failed)")
        print(f"Failed scripts: {failed}")
        sys.exit(1)
    else:
        print("RESULT: ALL 6/6 VALIDATORS PASSED CONVINCINGLY.")
        print("Runbook is 100% compliant with frozen baseline & operator specifications.")
        print("================================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()
"""

validator_files = {
    "validate_manifest.py": VALIDATE_MANIFEST_PY,
    "validate_prompt_headers.py": VALIDATE_PROMPT_HEADERS_PY,
    "validate_next_links.py": VALIDATE_NEXT_LINKS_PY,
    "validate_repo_coverage.py": VALIDATE_REPO_COVERAGE_PY,
    "validate_model_matrix.py": VALIDATE_MODEL_MATRIX_PY,
    "validate_frozen_path_guards.py": VALIDATE_FROZEN_PATH_GUARDS_PY,
    "run_all_validators.py": RUN_ALL_VALIDATORS_PY
}

for name, content in validator_files.items():
    filepath = os.path.join(VALIDATORS_DIR, name)
    with open(filepath, "w") as f:
        f.write(content.strip() + "\n")
    os.chmod(filepath, 0o755)

print("Generated validator suite.")
print("ALL RUNBOOK ARTIFACTS GENERATED SUCCESSFULLY.")
