# C02R HEARING TRANSCRIPT: CLUSTER 08 — IDEMPOTENCY, LEASE FENCING & TWO-PHASE SETTLEMENT
**CLUSTER_ID:** CLUSTER-08
**FINDINGS_COVERED:** FINDING_009, FINDING_027, FINDING_065, GOV-003
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R02 (Reliability Specialist) & R05 (Data Specialist)
- **Position:** In paid AI video generation, network failures or crash-restarts during prompt submission can lead to double-charging credits or submitting duplicate render jobs. We must enforce end-to-end idempotency:
  1. *Deterministic Idempotency Key:* Constructed from immutable inputs: `SHA256(shot_version_id + prompt_version_id + provider_id + attempt_index + parameters_hash)`.
  2. *Lease Fencing & TTL:* When a worker takes a job, it acquires a lease with an explicit `lease_token` (UUID) and `lease_expires_at` (TTL 90 minutes for video generation). If a worker crashes, the lease expires and a new worker can safely take over.
  3. *Two-Phase Credit Settlement:* Phase 1 reserves estimated credits in `RESERVED` state. Phase 2 settles exact used credits upon `COMPLETED` or releases reservation upon `FAILED` / `CANCELLED`.
- **Evidence:** `R02_CORE_STATE.md`, `DATA_MODEL.md`, `ADR-006`.
- **Failure Scenario:** A generation takes 45 minutes. With a 30-minute lease TTL, the lease expires while the job is still rendering, causing a second worker to acquire the lease and submit a duplicate paid generation.

## 2. Challenger Attack
- **Challenger:** R14 (Perf/Cost Specialist) & R03 (Workflow Specialist)
- **Attack Vector:**
  1. *Stale Lock Deadlocks:* If TTL is 90 minutes and a worker crashes 2 minutes in, does the job sit locked and stalled for 88 minutes before retry?
  2. *Reconciliation Race:* If a worker tries to renew its lease while another node is running health checks, can split-brain execution occur?

## 3. Domain Owner Review
- **Domain Owner:** R02 (Reliability Specialist)
- **Evaluation:**
  - The 90-minute TTL is a maximum safety ceiling for untracked crashes. Active workers must send periodic heartbeats (every 30 seconds) to extend their lease (`lease_expires_at = NOW() + 5 minutes`). If heartbeats cease, R02 allows operator intervention or health-check recovery after a short grace period (e.g. 3 minutes).
  - Idempotency keys must be enforced at the database level via a unique index: `UNIQUE (provider_id, idempotency_key)`.
  - The provider adapter must query existing jobs using the idempotency key before sending new submission requests.

## 4. Proponent Response
- **Response:**
  - We formalize heartbeat lease extension alongside the 90-minute absolute TTL.
  - We add strict unique constraints in `DATA_MODEL.md` and `domain-entities.schema.json`.
  - We specify the exact two-phase credit settlement state transitions.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Rely solely on Temporal workflow execution locks without database-level lease fencing.
- **Why Rejected:** If Temporal history is cleared or a direct API submission occurs, database-level invariants are the last line of defense against double-spending and duplicate generation.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-008 & CP-009 amended (and CP-018 for TTL/attempt semantics) to:
  1. Normatively freeze the 90-minute TTL, heartbeat protocol, and idempotency key derivation.
  2. Update `R02_CORE_STATE.md`, `DATA_MODEL.md`, and `domain-entities.schema.json`.
