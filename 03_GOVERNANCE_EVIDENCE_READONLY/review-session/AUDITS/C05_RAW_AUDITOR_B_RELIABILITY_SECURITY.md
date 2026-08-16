# C05 Auditor B Report: Reliability & Security (Hostile Evaluation)

**AUDITOR_ID:** AUDITOR-B (Pro-Tier Reliability & Security Hostile Auditor)
**DATE:** 2026-08-15
**TARGET:** Candidate v1.0.0

## ATTACK_SURFACE_EVALUATION

### 1. Idempotency & Budgeting (CP-004)
The two-phase budgeting protocol defines a reservation daemon that releases stale reservations older than 30 minutes. However, CP-006 explicitly states that video synthesis can take up to 60 minutes. This creates a severe race condition: a legitimate 60-minute job will have its budget reservation released halfway through execution. Another job can then claim the budget. When the first job completes, the system will overdraw, violating the two-phase budgeting guarantees. 
Additionally, the idempotency key formula `sha256(project_id + shot_id + prompt_version_id + seed + provider_params)` lacks a nonce or `attempt_id`. If a user wants to deliberately re-roll a generation (or if a local state inconsistency requires a manual retry), it is impossible without mutating a parameter, breaking deterministic reproducible workflows.

### 2. Recovery & Leases (CP-003, R02)
Distributed worker leases with a 120s TTL and periodic heartbeats are proposed. If a worker experiences thread starvation, GC pauses, or blocks on synchronous I/O (like an FFmpeg probe), it will miss its heartbeat. The lease will expire, and another worker will acquire the job. Both workers will issue provider API calls. While optimistic concurrency (`entity_version`) prevents database corruption on the final write, it does NOT prevent the double-billing side-effect at the provider layer.

### 3. MV3 Keepalive (CP-006, SPK-001, R09)
The dual-layer keepalive (Offscreen Document + Native Messaging Host) introduces a single point of failure: the Native Messaging Host daemon. If the daemon crashes, the browser extension cannot spontaneously restart it (Chrome limits how native hosts are launched). Furthermore, employing fake active audio channels to evade MV3 lifecycle policies heavily risks Chrome Web Store suspension or behavioral blocking by future Chrome updates.

### 4. Security & Enclave (CP-007, SECURITY_MODEL)
The SecretEnclave proposes using `sodium.memzero` for memory-wiping. In JavaScript/V8 (which the browser worker and Node.js use), strings and buffers are often immutable and heavily garbage-collected. Copies of secrets will inevitably leak into the heap before they reach the enclave. Furthermore, relying on HMAC-SHA256 for IPC requires a shared secret. If this secret is passed via environment variables, any local process (including vulnerable FlowKit dependencies) can read it, completely undermining the zero-trust architecture.

### 5. Observability & Provenance (CP-010)
W3C Trace Context propagation across asynchronous queues is sound, but extending it across the Chrome MV3 boundary to the isolated Native Messaging pipe is highly brittle. Additionally, the `TakeProvenance` immutable ledger mandates a `provider_job_id`. If an execution fails *before* a provider job ID is returned (e.g., local rate limit, network failure, validation error), the system cannot create a valid provenance record, leading to untraceable ghost failures.

### 6. Testability & Mocks (CP-012)
Hermetic mock providers enable fast integration tests, but they introduce a "mock drift" vulnerability. When providers silently update their API schemas, rate limit headers, or error formats (which happens frequently), the static mocks will pass locally while production breaks.

### 7. AQC & Remediation (CP-009)
The AQC remediation engine automatically retries if a score is below a threshold (up to 3 times). If a prompt triggers a provider's safety filter, the provider might return a corrupted video or blank output, which AQC will score as `visual_score = 0.0`. The engine will blindly retry 3 times, burning budget on a deterministic policy failure.

## AUDIT_FINDINGS

* **FINDING-B-01 (AUDIT_BLOCKER):** Budget Reservation Timeout Mismatch. 30-minute stale release daemon (CP-004) conflicts with 60-minute video generation times (CP-006), leading to guaranteed budget overdraws.
* **FINDING-B-02 (AUDIT_BLOCKER):** Lack of Attempt Nonce in Idempotency Key. Prevents legitimate retries of identical configurations without arbitrary mutation.
* **FINDING-B-03 (AUDIT_MAJOR):** Double-Billing via Lease Expiration. Lease TTL expiration under thread starvation leads to duplicate provider execution despite DB-level optimistic concurrency.
* **FINDING-B-04 (AUDIT_MAJOR):** V8 Memory Wiping Unsoundness. `sodium.memzero` is ineffective for securing secrets in JS/V8 heap, leaving credentials vulnerable in memory dumps.
* **FINDING-B-05 (AUDIT_MAJOR):** Automated Retry Budget Burn. AQC remediation does not distinguish between transient failures and deterministic policy/safety rejections, causing unbounded budget burn on blocked prompts.
* **FINDING-B-06 (RESIDUAL_RISK):** MV3 Keepalive Suspension Risk. Abusing offscreen audio for keepalive risks CWS suspension.
* **FINDING-B-07 (RESIDUAL_RISK):** Mock Provider Drift. Containerized mocks will diverge from live undocumented provider API changes.

## CONCLUSION & PRELIMINARY_GATE_OPINION

**FAIL_AUDIT_BLOCKER**

The specification introduces severe race conditions between budgeting and long-running job lifecycles. The two-phase commit protocol is structurally flawed due to mismatched timeouts, guaranteeing financial leaks. Optimistic concurrency prevents DB corruption but fails to prevent duplicate provider execution. The architecture must address these fundamental reliability and idempotency flaws before proceeding.
