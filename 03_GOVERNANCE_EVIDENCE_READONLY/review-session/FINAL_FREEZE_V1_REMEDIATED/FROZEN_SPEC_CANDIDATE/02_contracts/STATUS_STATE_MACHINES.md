# STATUS & STATE MACHINES SPECIFICATION
## AI Video Factory — Canonical Lifecycle & Execution Stage Reference
**VERSION:** 1.0.0

---

## 1. Two-Tier Hierarchical State Machine

AVF enforces a strict two-tier state machine to separate durable database business status from fine-grained workflow orchestrator progress:

### Tier 1: Canonical DB Lifecycle Status (`status`)
Durable entity status stored in PostgreSQL (`domain-entities.schema.json#//CanonicalLifecycleStatus`):
- `QUEUED`: Job created and awaiting budget reservation / worker pickup.
- `RESERVED`: Credits estimated and reserved; awaiting worker execution start.
- `RUNNING`: Worker has acquired lease; actively generating, downloading, or running QC.
- `COMPLETED`: Take successfully generated, QC passed, and final cost settled.
- `FAILED`: Unrecoverable execution error or QC failure; reservation released.
- `CANCELLED`: Aborted by operator or user; reservation released.
- `RECONCILED`: Recovered after lease expiration/crash; state reconciled with provider truth.

### Tier 2: Execution Stage (`execution_stage`)
Granular orchestrator stage emitted in telemetry and events (`domain-entities.schema.json#//ExecutionStage`):
- Under `QUEUED`: `WAITING_FOR_ASSETS`, `PROMPT_READY`
- Under `RESERVED`: `BUDGET_RESERVED`
- Under `RUNNING`: `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`
- Under `COMPLETED`: `APPROVED`
- Under `FAILED`: `EXECUTION_FAILED`, `QC_REJECTED`, `TIMEOUT`
- Under `CANCELLED`: `ABORTED_BY_USER`, `ABORTED_BY_SYSTEM`
- Under `RECONCILED`: `RECONCILED_SUCCESS`, `RECONCILED_TERMINAL`

---

## 2. Parent-to-Child Mapping Matrix

| Canonical Lifecycle Status | Valid Execution Stages | Allowed Next Lifecycle Status |
|---|---|---|
| `QUEUED` | `WAITING_FOR_ASSETS`, `PROMPT_READY` | `RESERVED`, `CANCELLED`, `FAILED` |
| `RESERVED` | `BUDGET_RESERVED` | `RUNNING`, `CANCELLED`, `FAILED` |
| `RUNNING` | `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING` | `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED` |
| `COMPLETED` | `APPROVED` | *(Terminal)* |
| `FAILED` | `EXECUTION_FAILED`, `QC_REJECTED`, `TIMEOUT` | *(Terminal)* |
| `CANCELLED` | `ABORTED_BY_USER`, `ABORTED_BY_SYSTEM` | *(Terminal)* |
| `RECONCILED` | `RECONCILED_SUCCESS`, `RECONCILED_TERMINAL` | *(Terminal)* |

---

## 3. State Invariants
1. **Durable Ownership:** R02 Core State is the sole authority for persisting lifecycle transitions.
2. **Terminal Immutability:** Once a job enters `COMPLETED`, `FAILED`, `CANCELLED`, or `RECONCILED`, its state is immutable.
3. **Lease Expiration:** If `status = RUNNING` and `lease_expires_at < NOW()`, the lease is considered broken. R02 Reconciliation Worker inspects provider state and transitions the job to `RECONCILED` or triggers a clean retry.
