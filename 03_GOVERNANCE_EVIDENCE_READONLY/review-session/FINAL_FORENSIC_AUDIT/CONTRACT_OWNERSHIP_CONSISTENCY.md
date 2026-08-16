# CONTRACT AND OWNERSHIP CONSISTENCY AUDIT
## Final Freeze Forensic Audit — AI Video Factory v1.0.0
**AUDITOR_ROLE:** Independent Post-Freeze Forensic Auditor  
**AUDIT_DATE:** 2026-08-15  
**SOURCE:** review-session/FINAL_FREEZE/FROZEN_SPEC_CANDIDATE/  

---

## 1. OWNERSHIP INVARIANTS TO VERIFY

Per governance requirement (Section 13), verify:
1. avf-core-state is canonical business state owner
2. Workflow history is not canonical domain truth
3. Browser/extension/FlowKit state is non-canonical
4. Provider adapter cannot mutate Project/Shot directly
5. FlowExecutionPort remains isolated
6. Track A and Track B share upstream semantics
7. FlowKit does not leak upstream
8. Repo private DB access is prohibited
9. External side effects have idempotency/reconciliation semantics

---

## 2. VERIFICATION RESULTS

### 2.1 avf-core-state as Canonical Owner
**Evidence:** R02_CORE_STATE.md line 9: "This is the authoritative source of truth for project, shot, prompt, generation, take, QC references, provenance, and workflow linkage."
**OWNS:** PostgreSQL schema, Project/Shot/Take lifecycle, version creation, optimistic concurrency, outbox records, audit log references, budget/usage ledger.
**VERDICT:** ✓ CONFIRMED

### 2.2 Workflow History Non-Canonical
**Evidence:** R06_WORKFLOW.md owns "WorkflowRun execution records" but R02 owns canonical GenerationJob/Take state. R06 DOES NOT OWN per blueprint: canonical domain state, QC scoring, budget management.
**VERDICT:** ✓ CONFIRMED — R06 tracks execution orchestration, R02 owns canonical business facts.

### 2.3 Browser/Extension/FlowKit State Non-Canonical
**Evidence:** R09_BROWSER_WORKER.md line 56-57: "Disposable session/command state only. Persistent Chrome profile is secret local infrastructure, not business state."
R09 DOES NOT OWN: "canonical project state, generation budget, creative retry, QC policy, FlowKit internals"
**VERDICT:** ✓ CONFIRMED

### 2.4 Provider Adapter Cannot Mutate Project/Shot
**Evidence:** R08_GOOGLE_FLOW_ADAPTER.md DOES NOT OWN: "DOM selectors, Chrome lifecycle, FlowKit DB/models, canonical business state, creative retry decisions"
R08 OUTPUTS: "ProviderGenerationResult/Status" only — return results, no direct state mutation.
R08 implements `VideoGenerationProvider` and `bind_execution_port(track-a|track-b)` — adapter pattern only.
**VERDICT:** ✓ CONFIRMED

### 2.5 FlowExecutionPort Isolation
**Evidence (from grep):** No `track_mode`, `flow_track`, `TRACK_A_BROWSER`, `TRACK_B_FLOWKIT` appear in the FROZEN_SPEC_CANDIDATE/02_contracts/ directory (grep returned 0 results).
The `attempt_index` field exists in `domain-entities.schema.json` (line 431, 474) — this is an idempotency field, not a FlowKit field.
**VERDICT:** ✓ CONFIRMED — FlowKit-specific execution model is contained within R08/R09/R10 adapters.

### 2.6 Track A and Track B Share Upstream Semantics
**Evidence:** Both Track A (R09 Browser Worker) and Track B (R10 FlowKit Bridge) implement the same `FlowExecutionPort` interface. Upstream (R06 Workflow) uses `FlowExecutionPort` without knowing which track executes.
CP-005 explicitly mandates: "Pure FlowExecutionPort contract. Zero FlowKit/CDP types in upstream core."
**VERDICT:** ✓ CONFIRMED

### 2.7 FlowKit Does Not Leak Upstream
**Evidence (grep result):** Zero matches for FlowKit-specific types in `/02_contracts/` directory of FROZEN_SPEC_CANDIDATE. 
R10_FLOWKIT_BRIDGE.md is confined to implementing the FlowExecutionPort.
**VERDICT:** ✓ CONFIRMED

### 2.8 Repo Private DB Access Prohibited
**Evidence:** R02_CORE_STATE.md line 65: "Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only."
This rule is stated in R02's blueprint. It's a specification rule, not an enforced technical constraint — implementation conformance depends on the coding agent following the rule.
**VERDICT:** ✓ SPECIFIED (implementation-phase enforcement required)

### 2.9 External Side Effects Have Idempotency Semantics
**Evidence:** 
- Provider requests: `provider-request.schema.json` includes mandatory `idempotency_key` (sha256) and `attempt_index`
- Worker operations: Lease fencing with `entity_version` and `lease_expires_at` on GenerationJob
- Event processing: Event envelope includes `event_id` for idempotent consumer middleware (CP-015)
**VERDICT:** ✓ CONFIRMED

---

## 3. SCHEMA CONSISTENCY SPOT CHECK

### 3.1 GenerationJob Schema (post-remediation)
Verified fields in domain-entities.schema.json:
- `attempt_index`: present (added by C05 remediation script, unvoted — see SEMANTIC_CHANGE_TRACEABILITY.md)
- `track_mode`: ABSENT (removed by C05 remediation script — FlowKit isolation restored) ✓
- `entity_version`: present (optimistic concurrency) ✓
- `lease_worker_id`, `lease_expires_at`: referenced in C05 Auditor-C report as present — enables lease fencing ✓

### 3.2 Provider Request Schema
Verified fields in provider-request.schema.json:
- `flow_track`: ABSENT (removed by C05 remediation) ✓
- `attempt_index`: present (idempotency) ✓

### 3.3 Provider Result Schema
- `error.category` with TRANSIENT/PERMANENT/POLICY/RESOURCE enum: per CP-002 and verified in C05 Auditor-C ✓
- `error.retryable`: present ✓

---

## 4. CONTRADICTIONS DETECTED

None material. The following notes are observations:

**NOTE-001:** The `attempt_index` field on `GenerationJob` in `domain-entities.schema.json` was added by the C05 remediation script, making it an unvoted semantic change (documented in SEMANTIC_CHANGE_TRACEABILITY.md). However, this field is architecturally correct and consistent with CP-004's intent.

**NOTE-002:** The R02 private DB access prohibition is a specification rule without automated enforcement. An implementing agent must enforce it by discipline. This is not a contradiction but an implementation-phase risk.

---

## 5. CONTRACT CONSISTENCY METRICS

| INVARIANT | STATUS |
|---|---|
| avf-core-state canonical owner | ✓ VERIFIED |
| Workflow non-canonical | ✓ VERIFIED |
| Browser state non-canonical | ✓ VERIFIED |
| Provider adapter read-only to domain | ✓ VERIFIED |
| FlowExecutionPort isolated | ✓ VERIFIED |
| Track A/B upstream semantic equivalence | ✓ VERIFIED |
| FlowKit does not leak upstream | ✓ VERIFIED |
| Private DB prohibition specified | ✓ SPECIFIED |
| External side effects idempotent | ✓ VERIFIED |

**CONTRACT CONSISTENCY VERDICT: PASS** — All 9 ownership invariants are correctly specified in the frozen specification. No contradictions between schemas and repo blueprints were detected.
