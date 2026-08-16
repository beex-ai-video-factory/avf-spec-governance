# C02 — Unresolved Controversies & Architectural Debates

In accordance with the Council Operating Protocol (Master v1.1 §12 & §18), raw disagreements and competing architectural visions are formally preserved for C03 Solution Design and C04 Changeset Voting. Discussion was not prematurely forced into false consensus.

| CONTROVERSY_ID | SOURCE_FINDINGS | TITLE | COMPETING PARTIES | C03 SOLUTION DESIGN DIRECTIVE |
|---|---|---|---|---|
| CONT-001 | F-R13-001, F-R06-001, F-R02-004 | Track A vs Track B Default Runtime Isolation Boundary | R06 (Flow) & R13 (OSS) vs R02 (Reliability) & R04 (Contracts) | Formulate Change Proposal with strict external adapter boundary isolating all FlowKit imports behind `avf-flow-adapter`. |
| CONT-001 | F-R13-001, F-R06-001, F-R02-004 | Track A vs Track B Default Runtime Isolation Boundary | R06 (Flow) & R13 (OSS) vs R02 (Reliability) & R04 (Contracts) | Formulate Change Proposal with strict external adapter boundary isolating all FlowKit imports behind `avf-flow-adapter`. |

---

## Detailed Controversy Records

### CONT-001: Track A vs Track B Default Runtime Isolation Boundary
- **Source Findings:** `F-R13-001, F-R06-001, F-R02-004`
- **Competing Views:**
  - **View A (Panel B - Runtime Isolationists):** Mandates that FlowKit (Track B) must run in a separate container/process communicating over gRPC to prevent library dependency collisions and ensure strict replaceable port semantics.
  - **View B (Panel A/C - Velocity & Simplicity):** Proposes allowing Track B to be imported as an internal TypeScript library within `avf-flow-adapter` while enforcing schema-level encapsulation at the API boundary.
- **Resolution Path in C03:** C03 will formulate explicit solution designs (`OPTION_A: Subprocess Adapter` vs `OPTION_B: In-Process Module with Schema Boundary`) with comparative benchmarks for latency, complexity, and operational overhead.

### CONT-001: Track A vs Track B Default Runtime Isolation Boundary
- **Source Findings:** `F-R13-001, F-R06-001, F-R02-004`
- **Competing Views:**
  - **View A (Panel B - Runtime Isolationists):** Mandates that FlowKit (Track B) must run in a separate container/process communicating over gRPC to prevent library dependency collisions and ensure strict replaceable port semantics.
  - **View B (Panel A/C - Velocity & Simplicity):** Proposes allowing Track B to be imported as an internal TypeScript library within `avf-flow-adapter` while enforcing schema-level encapsulation at the API boundary.
- **Resolution Path in C03:** C03 will formulate explicit solution designs (`OPTION_A: Subprocess Adapter` vs `OPTION_B: In-Process Module with Schema Boundary`) with comparative benchmarks for latency, complexity, and operational overhead.

