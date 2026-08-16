# Hostile Architecture & Contracts Audit (C05)

**AUDITOR_ID:** AUDITOR-A (Pro-Tier Architecture & Contracts Hostile Auditor)

## ATTACK_SURFACE_EVALUATION

### 1. Capability Preservation (C-01 to C-19)
At a superficial level, the capabilities map cleanly to schema enhancements (e.g., C-05 Two-phase budgeting is present in `CostUsageRecord.reservation_id`, C-10 is represented in `QCResult`, C-19 Operator Console is supported by `WorkflowRun` states). However, the implementation of **C-04 (Pluggable Provider Abstraction)** is compromised by upstream leakage (see Port Isolation below). 

### 2. Contract/Schema Rigor
Schemas validate against Draft 2020-12, but conceptually they are flawed. Core schemas intended to be "provider-neutral" contain implementation-specific enumerations. 

### 3. Port Isolation & Leakage (Google Flow Replaceability)
The architectural integrity claimed in the post-merge consistency report ("0 FlowKit / CDP Leakage") is a **lie**. 
The `avf-google-flow-adapter` (R08) was supposed to strictly isolate Google Flow execution models behind the `FlowExecutionPort`. CP-005 explicitly states: *"Zero FlowKit imports or browser DOM objects allowed outside R09/R10."*
However:
1. `02_contracts/provider-request.schema.json` explicitly defines `flow_track` with values `TRACK_A_BROWSER` and `TRACK_B_FLOWKIT`.
2. `02_contracts/domain-entities.schema.json` (inside `GenerationJob`) explicitly defines `track_mode` with values `TRACK_A_BROWSER` and `TRACK_B_FLOWKIT`.
This means the core domain and the supposedly "provider-neutral" request contract are hard-coupled to Google Flow's internal implementation dual-track details. A true hexagonal port would abstract this away, allowing the workflow to request a generation without knowing if a browser worker or a FlowKit bridge is executing it under the hood.

### 4. Unvoted Semantic Edits & Synthesis-Introduced Changes
The Post-Merge consistency report claims "0 Unvoted Semantic Edits". However, the injection of `track_mode` into `GenerationJob` in the canonical `domain-entities.schema.json` directly contradicts the mandate of CP-005, which forbids these types from leaking into the upstream core. This implies the synthesis script hallucinated or incorrectly hoisted these types to the global namespace.

### 5. Dependency Graph
The physical blueprint dependency graph is technically a unidirectional DAG. However, the logical dependency graph is circular: the core state (`R02`) depends on `avf-contracts` (`domain-entities.schema.json`), which now semantically depends on Google Flow's dual-track architecture (`TRACK_B_FLOWKIT`).

---

## AUDIT_FINDINGS

### FINDING 1: Hexagonal Port Leakage in Canonical Entities (AUDIT_BLOCKER)
- **Target:** `02_contracts/domain-entities.schema.json` (`GenerationJob.track_mode`) & `02_contracts/provider-request.schema.json` (`flow_track`)
- **Description:** The core canonical domain models and the provider execution requests explicitly contain `TRACK_A_BROWSER` and `TRACK_B_FLOWKIT` enumerations. This is a severe abstraction leak that destroys the hexagonal architecture (CP-005) and breaks the Pluggable Provider Abstraction capability (C-04). 
- **Remediation:** Remove `track_mode` and `flow_track` from core contracts. Execution track selection is an internal routing concern for `avf-google-flow-adapter` (R08) and should be managed via opaque options or adapter-level configuration, not global domain state.

### FINDING 2: Falsified Consistency Report (AUDIT_MAJOR)
- **Target:** `C04/POST_MERGE_CONSISTENCY_REPORT.md`
- **Description:** The report asserts "FlowKit / CDP Leakage: 0". This is factually incorrect as proven by Finding 1. Automated checks failed to semantically analyze string enums in JSON schemas.

---

## CONCLUSION & PRELIMINARY_GATE_OPINION

**PRELIMINARY_GATE_OPINION: FAIL_AUDIT_BLOCKER**

The specification candidate fails the architecture audit. The inclusion of `TRACK_A_BROWSER` and `TRACK_B_FLOWKIT` in the core domain entities and provider requests fundamentally violates the hexagonal architecture isolation mandated by CP-005. The core is currently hard-coupled to the internal implementation details of a single provider. The candidate must be rejected and the schema definitions must be cleansed of provider-specific execution modes before proceeding.
