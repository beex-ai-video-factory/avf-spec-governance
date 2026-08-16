# REPOSITORY DEPENDENCY GRAPH (DAG)
## AI Video Factory — Architectural Layering & Forbidden Dependency Matrix
**VERSION:** 1.0.0

---

## 1. Architectural Layers

```
Layer 0: R01 (Contracts)
Layer 1: R02 (Core State)
Layer 2: R03 (Creative), R04 (Assets/Continuity), R05 (Prompt Compiler), R11 (QC), R12 (Media)
Layer 3: R07 (Provider SDK), R08 (Google Flow Adapter)
Layer 4: R09 (Browser Worker), R10 (FlowKit Bridge)
Layer 5: R06 (Workflow), R13 (Operator Console)

Cross-Cutting:
- R14 (Platform Observability): Imported by all repos (R02–R15)
- R15 (Integration Harness): Consumes all repos for conformance testing
```

---

## 2. Dependency Matrix

| Repository | Allowed Dependencies | Forbidden Dependencies |
|---|---|---|
| **R01 Contracts** | *(None - Pure schemas/types)* | R02–R15 |
| **R02 Core State** | R01, R14 | R03–R13, R15 |
| **R03 Creative** | R01, R02 (API), R14 | R04–R13, R15, Direct DB |
| **R04 Assets/Continuity** | R01, R02 (API), R14 | R03, R05–R13, R15, Direct DB |
| **R05 Prompt Compiler** | R01, R02 (API), R04 (API), R14 | R06–R13, R15, Direct DB |
| **R06 Workflow** | R01, R02, R03, R04, R05, R07, R08, R11, R12, R14 | R09, R10, Direct DB |
| **R07 Provider SDK** | R01, R14 | R02–R06, R08–R13, R15, Direct DB |
| **R08 Google Flow Adapter** | R01, R07, R09 (Port), R10 (Port), R14 | R02–R06, Direct DB |
| **R09 Browser Worker** | R01, R14 | R02–R08, R10, R11–R13, Direct DB |
| **R10 FlowKit Bridge** | R01, R14 | R02–R09, R11–R13, Direct DB |
| **R11 QC** | R01, R14 | R02–R10, R12, R13, Direct DB |
| **R12 Media** | R01, R14 | R02–R11, R13, Direct DB |
| **R13 Operator Console** | R01, R02 (API), R06 (API), R14 | Direct DB, Internal Worker internals |
| **R14 Observability** | R01 | R02–R13, R15, Direct DB |
| **R15 Harness** | R01–R14 | Direct production DB mutation |

---

## 3. Invariants
- **Acyclic:** The dependency graph is mathematically acyclic (zero circular imports).
- **Database Encapsulation:** Only R02 Core State possesses credentials to access PostgreSQL.
- **Port Isolation:** R08 Google Flow Adapter interacts with R09/R10 strictly via the FlowExecutionPort.
