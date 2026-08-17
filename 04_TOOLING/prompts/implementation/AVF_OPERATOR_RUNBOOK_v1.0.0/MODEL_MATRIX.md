# AI VIDEO FACTORY v1.0.0 — MODEL ROUTING MATRIX
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
