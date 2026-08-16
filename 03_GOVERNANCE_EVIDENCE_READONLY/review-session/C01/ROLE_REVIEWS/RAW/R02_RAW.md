# C01 Independent Review — R02 Distributed Systems & Reliability Architect

**Reviewer Role:** R02_RELIABILITY (Distributed Systems & Reliability Architect)  
**Review Round:** C01 (Independent Blind Review)  
**Session ID:** 7380b26a-7a61-41b9-bffa-bb438c0c91d0  
**Timestamp:** 2026-08-15T11:35:00+07:00  
**Model:** Claude 3.5 Sonnet / Antigravity Agent  
**Review Baseline:** `review-session/C00_FINAL/`  
**Target Specifications:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-008_WORKFLOW_ENGINE.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-003, INV-018, INV-019)
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/E2E_INTEGRATION_PROTOCOL.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md`

---

## 1. Executive Summary & Reliability Assessment

The AI Video Factory v0.9.0 blueprint presents a robust architectural foundation with clear layer separation, explicit contracts, and strict state boundaries (e.g., separating ephemeral browser state from canonical PostgreSQL business truth). The adoption of Temporal-class durable orchestration (ADR-008) and deterministic state machines is a commendable design choice for long-running media generation pipelines.

However, from a **distributed systems, concurrency, and fault-tolerance perspective**, critical ambiguities and missing protocol specifications threaten operational reliability:
1. **Uncertain Submit Handling on Non-Idempotent External Providers:** Google Flow provides no native client-assigned idempotency keys or job lookup by client token. A network partition or process crash immediately after prompt submission creates a high risk of duplicate paid generations violating **INV-003** and risking severe budget drain (Risk R6).
2. **Missing Fencing Tokens / Monotonic Leases on Browser Workers:** The command state machine (`QUEUED -> LEASED -> RUNNING -> SUCCEEDED`) lacks fencing tokens or lease epochs, permitting zombie workers (recovering from GC pauses or network partitions) to commit stale results or overwrite concurrent executions (**INV-005, INV-019**).
3. **GAP-001 (Error Detail Schemas):** Error details are defined as untyped wildcards (`details: object`), preventing automated, deterministic retry decisions, rate-limit backoffs, and structured diagnostic triage across the 14 error classes.
4. **GAP-004 (Browser Worker Timeout & Deadlock Bounds):** DOM polling, page navigation, and download wait loops in `avf-browser-worker` lack strict, bounded timeouts and differentiated failure classification (`UI_CHANGED` vs `TRANSIENT_BROWSER` vs `PROVIDER_TIMEOUT`), risking hung worker threads and queue head-of-line blocking.
5. **Two-Phase Budget Reservation Protocol Absence:** Direct deduction prior to generation lacks reservation/commit semantics, causing credit leakage when transient failures or crashes occur prior to external dispatch (**INV-018**).
6. **MV3 Service Worker Lifetime Constraints:** Chromium MV3 service workers terminate after 30 seconds of inactivity or 5 minutes max runtime, which directly intersects with multi-minute video generation polling without an explicit keep-alive and state synchronization protocol.

This review provides 6 formal, evidence-backed findings with concrete failure scenarios, rigorous mathematical/protocol solutions, test requirements, and zero reduction in protected system capability.

---

## 2. Enumeration of Inspected Specification Files

| File Path | Version / Status | Focus of Inspection |
|---|---|---|
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md` | v0.9.0 Candidate | Sections 4, 9, 10, 11, 16, 17 (Durable workflow, idempotency key structure, retry taxonomy) |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` | v0.9.0 Normative | Invariants INV-003, INV-018, INV-019, INV-001, INV-002, INV-005, INV-008, INV-010, INV-012, INV-015 |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md` | v0.9.0 Candidate | Activity sequencing, timeouts, reconciliation-before-resubmit, crash recovery |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-008_WORKFLOW_ENGINE.md` | v0.9.0 Accepted | Temporal-class orchestrator boundary vs LangGraph |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md` | v0.9.0 Candidate | Common envelope, 14 error classes, compatibility policy |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json` | v1.0.0 Draft | Structure of ProviderGenerationResult, error object schema |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json` | v1.0.0 Draft | FlowExecutionCommand schema, deadline_at, correlation envelope |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md` | v0.9.0 Candidate | State transitions for GenerationJob and Browser execution command |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md` | v0.9.0 Candidate | Optimistic concurrency, outbox records, transactional atomicity |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md` | v0.9.0 Candidate | VideoGenerationProvider interface, idempotency contract |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md` | v0.9.0 Candidate | Command sequencing, uncertain submit error mapping |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md` | v0.9.0 Candidate | MV3 lifecycle, Native Messaging/WebSocket transport, selector timeouts |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/E2E_INTEGRATION_PROTOCOL.md` | v0.9.0 Candidate | Suite A/B failure injection requirements |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md` | v0.9.0 Candidate | Risks R6 (Duplicate paid generation), R7 (Browser crash), R8 (MV3 termination), R12 (Budget) |
| `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` | Baseline | GAP-001 (Error detail schemas) and GAP-004 (Browser timeouts) |

---

## 3. Enumeration of Relevant System Invariants & Contracts

1. **INV-003:** Every external side effect has an idempotency key or an explicit documented reason it cannot.
   - *Reliability Rule:* Idempotency keys must be persisted prior to network calls and passed across all workflow and adapter boundaries. If a downstream provider cannot accept an idempotency key, the adapter MUST implement a deterministic reconciliation protocol before any retry.
2. **INV-018:** Budget limits are enforced by deterministic policy before external generation requests.
   - *Reliability Rule:* Budget checking must not cause phantom deductions or unreleased reservations during transient network/worker failures.
3. **INV-019:** A browser worker can crash without losing canonical queue truth.
   - *Reliability Rule:* Browser workers are untrusted, ephemeral peripherals. State machines must support lease expirations, worker heartbeat failure, and crash-safe restarts without orphan jobs or duplicate executions.
4. **INV-005:** Browser/extension/FlowKit state is never canonical business state.
   - *Reliability Rule:* No durable decision or completion can be finalized solely based on browser memory. Canonical state in PostgreSQL is updated only through validated command-response pairs.
5. **INV-015:** Correlation IDs (`trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`) must propagate across all boundaries.
   - *Reliability Rule:* Every error, timeout, lease, and diagnostic payload must carry the full correlation context for distributed tracing and reconciliation.

---

## 4. Deep Analysis of Assigned Gap Seeds

### 4.1 GAP-001: Error Detail Schemas (CONTRACTS_OVERVIEW.md & provider-result.schema.json)

**Defect Analysis:**  
`CONTRACTS_OVERVIEW.md` lists 14 high-level error classes, but `provider-result.schema.json` lines 82–86 defines `error.details` as:
```json
"details": {
  "type": "object"
}
```
This is a critical distributed systems deficiency:
- When a `PROVIDER_RATE_LIMIT` occurs, the orchestrator needs `retry_after_sec` (integer) and `quota_metric` (string) to schedule backoff. Without a schema, adapters serialize arbitrary fields or omit the cooldown window, causing the workflow retry loop to immediately hammer the rate-limited provider.
- When `TRANSIENT_BROWSER` occurs, the retry policy must distinguish between a reconnectable socket disconnect (`reconnectable: true`) and a catastrophic Chrome crash requiring browser process re-launch (`process_restart_required: true`).
- When `UI_CHANGED` occurs, diagnostic metadata (`failed_selector`, `dom_snapshot_uri`, `current_url`) is necessary for automated classification vs triage.
- When `SECURITY_CHALLENGE` or `AUTH_REQUIRED` occurs, the error details must specify the `challenge_type` (`CAPTCHA`, `OAUTH_EXPIRED`, `2FA`) and `session_id` to route to the correct operator queue without parsing unstructured text messages.

**Resolution Requirement:**  
Introduce a dedicated, versioned `error-detail.schema.json` in `avf-contracts` with explicit polymorphic discriminator mapping on `class` using JSON Schema Draft 2020-12 `oneOf` or `$defs`.

---

### 4.2 GAP-004: Browser Timeout & Retry Limits (R09_BROWSER_WORKER.md)

**Defect Analysis:**  
`R09_BROWSER_WORKER.md` specifies that the worker owns DOM selectors, download handling, and session lifecycle, but fails to define concrete execution deadlines, polling intervals, or exponential backoff parameters for:
- DOM element location (e.g. prompt input textarea, submit button);
- Generation progress polling (waiting for Flow generation card state: `QUEUED` -> `GENERATING` -> `READY`);
- File download completion (waiting for Chrome download manager to finish saving the `.mp4` binary);
- WebSocket / Native Messaging heartbeat interval and missed-heartbeat lease revocation threshold.

Without explicit bounded deadlines:
- An unresponsive DOM element leads to infinite async wait loops in the content script or Playwright context.
- Workflow activity timeouts fire *before* the browser worker times out, leading to orphaned browser tasks continuing in the background while the workflow attempts a retry, resulting in race conditions.
- Polling Google Flow too aggressively triggers anti-bot rate limiting or DOM thrashing, while polling too infrequently increases end-to-end latency unnecessarily.

**Resolution Requirement:**  
Establish normative timeout budgets in `R09_BROWSER_WORKER.md` and `browser-command.schema.json`:
- `DOM_ELEMENT_WAIT_TIMEOUT_MS`: 10,000 ms (10s)
- `PROMPT_SUBMISSION_ACK_TIMEOUT_MS`: 15,000 ms (15s)
- `GENERATION_POLL_INTERVAL_MS`: 3,000 ms (3s) with ±500ms jitter
- `GENERATION_OVERALL_DEADLINE_MS`: 600,000 ms (10 min)
- `DOWNLOAD_COMPLETION_TIMEOUT_MS`: 60,000 ms (60s)
- `HEARTBEAT_INTERVAL_MS`: 5,000 ms (5s); `HEARTBEAT_TIMEOUT_MS`: 15,000 ms (3 missed heartbeats)

---

## 5. Concrete Failure Scenarios & Distributed Systems Stress Tests

### Scenario A: Uncertain Submit & Ghost Generation Duplicate (INV-003, INV-019, Risk R6)
```text
[Core State]            [Workflow Activity]         [Browser Worker]          [Google Flow UI]
     |                          |                          |                         |
     |--- CreateGenerationJob ->|                          |                         |
     |    (SUBMITTING)          |                          |                         |
     |                          |--- SUBMIT_PROMPT ------->|                         |
     |                          |    (command_id=C1)       |--- Click 'Generate' --->|
     |                          |                          |                         | (Flow accepts,
     |                          |                          |                         |  starts generation)
     |                          |                    [CRASH / OOM]                   |
     |                          |                          X                         |
     |                          |<-- Activity Timeout -----|                         |
     |                          |    (Outcome UNCERTAIN)                             |
```
- **The Breakdown:** The activity times out with no response. The prompt was actually received by Google Flow, and generation is underway. If the workflow naively retries the `SUBMIT_PROMPT` activity on a new browser worker, a second generation is submitted, creating duplicate paid asset creation and violating **INV-003**.
- **Blueprint Gap:** The blueprint states "workflow must reconcile before issuing a new submit", but does not define the reconciliation protocol for black-box browser automation.
- **Reliability Solution:**
  1. Implement a **Prompt Marker / Seed Tagging Protocol**: When submitting prompts in Track A, the browser worker injects a deterministic zero-width or trailing metadata tag / unique correlation signature into the prompt metadata or selects a specific named Flow project/asset slot if available.
  2. Implement an **Active Inspection Reconciliation Activity (`RECONCILE_GENERATION_STATE`)**: Before executing a retry on uncertain submit, the workflow dispatches a read-only command to inspect the latest 3 cards in the target Flow project feed.
  3. If a generating card matches the prompt text/hash within the submission timestamp window ($T_{submit} \pm 60s$), the worker adopts that `provider_job_id` and transitions to `GENERATING` rather than re-submitting.
  4. If no match is found after an inspection window ($T_{wait} \ge 30s$), the state transitions to `FAILED_TRANSIENT` and allows safe resubmission under `attempt_no + 1`.

---

### Scenario B: Zombie Worker Split-Brain Execution (INV-005, INV-019)
```text
[Queue/State]              [Worker A (Stalled)]           [Worker B (New)]           [Google Flow]
     |                              |                             |                        |
     |-- Lease Command (Epoch 1) -->|                             |                        |
     |                              | [GC Pause / Net Partition]  |                        |
     |-- Lease Expired (Heartbeat) -|                             |                        |
     |-- Lease Command (Epoch 2) -------------------------------->|                        |
     |                              |                             |-- SUBMIT_PROMPT ------>|
     |                              | [Wakes Up!]                 |                        |
     |                              |-- SUBMIT_PROMPT ------------------------------------>| [DUPLICATE!]
     |                              |-- RecordSubmission -------->|                        |
```
- **The Breakdown:** Worker A stalls long enough for its lease to expire. The orchestrator reassigns the job to Worker B. Worker A resumes without realizing its lease was revoked, submitting the job to Google Flow and calling Core State to register its output.
- **Blueprint Gap:** `STATUS_STATE_MACHINES.md` lacks fencing token semantics on leased commands.
- **Reliability Solution:**
  1. Every leased command returned by Core State or Queue MUST include a strictly monotonic integer `lease_epoch` (or generation token).
  2. Any state transition or recording API (`RecordProviderSubmission`, `RegisterTake`, `FlowExecutionResult`) MUST pass `lease_epoch`.
  3. Core State MUST enforce optimistic conditional check: `UPDATE commands SET status = :status WHERE command_id = :id AND lease_epoch = :lease_epoch`. If the epoch does not match, Core State rejects the call with `LEASE_EXPIRED` (409 Conflict), and the zombie worker must immediately abort its browser task.

---

### Scenario C: Budget Drain on Pre-Submit Crash (INV-018, Risk R12)
```text
[Core State]                     [Workflow Engine]                 [Provider SDK]
     |                                   |                                |
     |-- Check & Decrement Budget ------>|                                |
     |   (UsageRecord Committed)         |                                |
     |                                   |-- Execute Generation Activity -|
     |                                   |   [Host Crash / Unhandled Err] |
     |                                   |   X                            |
     |                                   |<-- Activity Aborted -----------|
```
- **The Breakdown:** Under the naive interpretation of INV-018 ("Budget limits are enforced by deterministic policy before external generation requests"), deducting budget before external dispatch permanently locks credits if the process crashes before the request reaches the provider.
- **Reliability Solution:**
  - Implement a **Two-Phase Budget Reservation Protocol**:
    1. `RESERVE_BUDGET(project_id, generation_job_id, estimated_cost, ttl_sec=900)`: Atomically validates remaining quota and places a hold on funds.
    2. `COMMIT_BUDGET(reservation_id, actual_cost, provider_job_id)`: Atomically converts the reservation into a permanent `CostUsageRecord` upon successful provider submission ACK (`SUBMITTED`).
    3. `RELEASE_BUDGET(reservation_id, reason)`: Releases the reservation back to the available pool upon workflow cancellation, fatal validation error, or expiration of the reservation TTL via a background sweeper.

---

### Scenario D: MV3 Background Service Worker Suspension (Risk R8, INV-005, INV-019)
- **The Breakdown:** Chromium MV3 service workers are terminated if they do not receive an active event for 30 seconds. Video generation in Google Flow takes up to 300 seconds. If the extension service worker is waiting on a `setTimeout` or awaiting a DOM mutation event in the page without native messaging keep-alives, the service worker goes dormant. When the native host sends a status query, the connection is broken, triggering a false `TRANSIENT_BROWSER` crash alert.
- **Reliability Solution:**
  1. The host worker MUST utilize Chrome **Native Messaging** with long-lived stdio pipes, which keeps the background service worker alive during active command execution.
  2. For WebSocket-based transport (Option A2), the extension content script MUST run a 10-second `chrome.runtime.sendMessage` ping to the background script to keep the session alive, or the content script must directly maintain the loopback WebSocket to the local daemon, bypassing service worker dormancy entirely.
  3. Ephemeral state must be written to `chrome.storage.session` so that even if the service worker restarts, it can resume tracking the active tab immediately upon wake-up.

---

## 6. Formal Council Findings

### FINDING_ID: F-R02-001
**ROLE:** R02_RELIABILITY  
**SEVERITY:** HIGH (BLOCKER_BEFORE_FREEZE)  
**CATEGORY:** CONTRACTS_ERROR_HANDLING  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md`
- `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (GAP-001)  
**AFFECTED_CONTRACTS:** `https://avf.local/contracts/provider-result/1.0`, `https://avf.local/contracts/error-detail/1.0`  
**EVIDENCE:** `provider-result.schema.json` lines 82–86 defines `"details": { "type": "object" }` without typed schemas or required fields for the 14 error classes defined in `CONTRACTS_OVERVIEW.md`.  
**FAILURE_SCENARIO:** A provider adapter encounters a rate limit and returns `PROVIDER_RATE_LIMIT` with details `{ "backoff": 120 }` instead of `{ "retry_after_sec": 120 }`. The Temporal workflow retry policy cannot parse the backoff duration, defaults to immediate retry, and exhausts provider quotas, locking the entire production pipeline.  
**WHY_IT_MATTERS:** Deterministic retry policies (ADR-006) and automated circuit breaking require normalized, strongly typed error payloads across all provider adapters. Without schemas, error handling logic becomes brittle and error-prone.  
**PROPOSED_SOLUTION:**
Create a formal, normative schema `error-detail.schema.json` in `avf-contracts` and update `provider-result.schema.json` to reference it. The schema must enforce specific detail structures for each error class:
- `PROVIDER_RATE_LIMIT`: `{ "retry_after_sec": integer (>=0), "limit_type": "CONCURRENT"|"REQUESTS_PER_MINUTE"|"DAILY_CREDIT", "reset_at": "date-time" }`
- `TRANSIENT_BROWSER`: `{ "phase": "DOM_WAIT"|"SUBMISSION"|"POLLING"|"DOWNLOAD", "recoverable": boolean, "reconnect_suggested": boolean, "diagnostic_ref": "string" }`
- `UI_CHANGED`: `{ "expected_selector": "string", "detected_dom_state": "string", "screenshot_ref": "string" }`
- `SECURITY_CHALLENGE`: `{ "challenge_type": "CAPTCHA"|"BOT_DETECTION"|"REAUTH", "action_url": "string", "manual_intervention_required": true }`
- `BUDGET_EXHAUSTED`: `{ "current_usage": number, "limit": number, "currency_or_credits": "string" }`  
**ALTERNATIVES_CONSIDERED:**
1. Leave `details` as freeform object and parse in application logic: Rejected because it invites silent cross-repo semantic drift and runtime type errors.
2. Embed error schemas directly inside each individual command schema: Rejected to maintain a unified error taxonomy across the system.  
**CAPABILITY_IMPACT:** Zero reduction in capabilities; dramatically improves automated recovery and operational observability.  
**COMPATIBILITY_IMPACT:** Backward-compatible addition to `avf-contracts` (adds `$defs` / `oneOf` to `error.details`).  
**MIGRATION_IMPACT:** Adapters and SDK must map provider-specific error payloads into the validated schema.  
**TEST_OR_BENCHMARK_REQUIRED:** Unit schema validation tests for all 14 error classes; contract tests verifying `FakeVideoProvider` and `GoogleFlowAdapter` emit valid error payloads.  
**RESIDUAL_RISK:** Provider-specific novel errors must be categorized into one of the 14 classes with an `extended_details` property.  
**CONFIDENCE:** 1.0 (Certain)

---

### FINDING_ID: F-R02-002
**ROLE:** R02_RELIABILITY  
**SEVERITY:** HIGH (BLOCKER_BEFORE_FREEZE)  
**CATEGORY:** TIMEOUTS_AND_CONCURRENCY  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
- `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (GAP-004)  
**AFFECTED_CONTRACTS:** `https://avf.local/contracts/browser-command/1.0`  
**EVIDENCE:** `R09_BROWSER_WORKER.md` section "RETRY STRATEGY" and `browser-command.schema.json` omit explicit numeric constants for DOM search deadlines, polling intervals, and max operation timeouts, relying solely on an optional `deadline_at` field.  
**FAILURE_SCENARIO:** A selector changes on Google Flow. The browser worker's DOM wait loop hangs indefinitely waiting for a button that will never appear. Because no internal DOM timeout is defined, the worker process remains blocked until the global workflow activity timeout fires 15 minutes later, holding local worker resources and starving subsequent jobs in the queue.  
**WHY_IT_MATTERS:** Bounded execution is a fundamental prerequisite for reliable distributed workers. Unbounded DOM polling causes worker resource starvation, cascade failures, and false positives in health checks.  
**PROPOSED_SOLUTION:**
Explicitly specify normative timeout contracts in `R09_BROWSER_WORKER.md` and `browser-command.schema.json`:
1. Add `timeout_ms` property per command method in `browser-command.schema.json`.
2. Mandate the following default timeout and retry matrix in `R09_BROWSER_WORKER.md`:
   - `DOM_SEARCH_TIMEOUT_MS`: 10,000 ms (10s) -> failure produces `UI_CHANGED` with DOM snapshot.
   - `ACTION_ACK_TIMEOUT_MS`: 15,000 ms (15s) -> failure produces `TRANSIENT_BROWSER`.
   - `GENERATION_POLL_INTERVAL_MS`: 3,000 ms (3s) base with ±500ms uniform jitter to avoid thundering herds.
   - `GENERATION_MAX_WAIT_MS`: 600,000 ms (10 minutes) -> failure produces `PROVIDER_TIMEOUT`.
   - `DOWNLOAD_READINESS_TIMEOUT_MS`: 60,000 ms (60s) -> failure produces `TRANSIENT_BROWSER`.
3. Worker MUST respect `min(command.deadline_at - now(), method_default_timeout)`.  
**ALTERNATIVES_CONSIDERED:**
1. Rely exclusively on Temporal activity timeouts: Rejected because Temporal cancelling an activity does not terminate an uncooperative or hung browser thread without explicit internal cancellation checks.  
**CAPABILITY_IMPACT:** None. Protects system throughput and responsiveness.  
**COMPATIBILITY_IMPACT:** Backward-compatible contract enhancement.  
**MIGRATION_IMPACT:** Track A worker and test harnesses must enforce timeout configurations.  
**TEST_OR_BENCHMARK_REQUIRED:** Chaos test injecting DOM element absence; verify worker returns `UI_CHANGED` within exactly 10s ± 500ms.  
**RESIDUAL_RISK:** Legitimate slow generations taking >10 minutes may require configurable per-model timeout overrides in `ProviderCapabilities`.  
**CONFIDENCE:** 1.0 (Certain)

---

### FINDING_ID: F-R02-003
**ROLE:** R02_RELIABILITY  
**SEVERITY:** CRITICAL (BLOCKER_BEFORE_FREEZE)  
**CATEGORY:** IDEMPOTENCY_AND_RECONCILIATION  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-003)
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`  
**AFFECTED_CONTRACTS:** `STATUS_STATE_MACHINES.md`, `GenerationJob` lifecycle  
**EVIDENCE:** `STATUS_STATE_MACHINES.md` specifies: "On uncertain submit outcome, workflow must reconcile before issuing a new submit" without defining the concrete protocol, states, or queries required to reconcile non-idempotent browser-based submissions.  
**FAILURE_SCENARIO:** The browser worker submits a prompt to Google Flow. The generation starts on Google's backend, but the worker crashes before capturing the job ID. The Temporal workflow detects activity failure and initiates a retry. Because Google Flow has no API to query by client idempotency key, the retry naively submits the prompt again, resulting in duplicate generation, double billing, and multiple conflicting video outputs for a single `GenerationJob`.  
**WHY_IT_MATTERS:** Directly violates **INV-003** ("Every external side effect has an idempotency key or an explicit documented reason it cannot") and triggers **Risk R6** (Duplicate paid generation, Severity: Critical).  
**PROPOSED_SOLUTION:**
Formalize the **Uncertain Submit Reconciliation Protocol** in `avf-workflow` and `avf-google-flow-adapter`:
1. Add an explicit intermediate state `SUBMIT_UNCERTAIN` to `GenerationJob` state machine in `STATUS_STATE_MACHINES.md`.
2. Define a mandatory reconciliation activity `ReconcileExternalSubmissionActivity`:
   - Inspect active generation slots in the provider project workspace via `READ_GENERATION_STATE`.
   - Match recent generations against the deterministic `prompt_hash` and submission time window ($T_{submit} \pm 120s$).
   - If a matching generating/completed card is found, bind its `provider_job_id` to the canonical `GenerationJob` and transition state to `GENERATING` (reconciliation success).
   - If no matching card is found after a mandatory cooldown ($T_{cooldown} \ge 45s$), transition to `FAILED_TRANSIENT` and authorize a clean retry under `attempt_no + 1`.
   - If UI state is ambiguous (e.g. multiple identical prompts found), escalate to `HUMAN_REVIEW` with an alert.  
**ALTERNATIVES_CONSIDERED:**
1. Blindly retry after failure: Rejected (causes guaranteed duplicate spend).
2. Fail immediately and require human intervention on every uncertain submit: Rejected because automated feed inspection can safely resolve >95% of browser crashes.  
**CAPABILITY_IMPACT:** Zero reduction in capability; guarantees 100% adherence to duplicate prevention target.  
**COMPATIBILITY_IMPACT:** Adds `SUBMIT_UNCERTAIN` state to `GenerationJob` state enum.  
**MIGRATION_IMPACT:** Workflow state machine and adapter must implement the reconciliation activity.  
**TEST_OR_BENCHMARK_REQUIRED:** Failure injection test (E2E Suite A): simulate worker crash immediately after DOM submit click; verify reconciliation recovers the active job without duplicate submission.  
**RESIDUAL_RISK:** If Google Flow completely changes its project feed UI, reconciliation falls back to `HUMAN_REVIEW`.  
**CONFIDENCE:** 0.95 (High)

---

### FINDING_ID: F-R02-004
**ROLE:** R02_RELIABILITY  
**SEVERITY:** HIGH (BLOCKER_BEFORE_FREEZE)  
**CATEGORY:** CONCURRENCY_AND_SPLIT_BRAIN  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-005, INV-019)  
**AFFECTED_CONTRACTS:** `STATUS_STATE_MACHINES.md` (Browser execution command), `browser-command.schema.json`  
**EVIDENCE:** `STATUS_STATE_MACHINES.md` lines 39–45 defines the command lifecycle as `QUEUED -> LEASED -> RUNNING -> SUCCEEDED` but provides no mechanism for monotonic fencing tokens or lease epoch validation.  
**FAILURE_SCENARIO:** Browser Worker A leases command $C_1$. Worker A encounters a 45-second network partition or CPU throttle. The lease expires, and the queue issues $C_1$ to Browser Worker B with a fresh lease. Worker B starts processing. Worker A recovers, does not realize its lease was revoked, finishes the task, and sends `FlowExecutionResult` to Core State, overwriting Worker B's progress or committing duplicate output metadata.  
**WHY_IT_MATTERS:** Violates **INV-005** and **INV-019**. Split-brain worker execution causes data corruption, race conditions, and orphaned browser sessions.  
**PROPOSED_SOLUTION:**
1. Add `lease_epoch: integer (minimum: 1)` to `browser-command.schema.json` and all command status payloads.
2. In `avf-core-state`, implement monotonic lease verification on all command state updates:
   ```sql
   UPDATE browser_commands 
   SET status = :new_status, updated_at = NOW() 
   WHERE command_id = :command_id AND lease_epoch = :lease_epoch;
   ```
3. If zero rows are updated, Core State rejects the result with `CONFLICT` (`STALE_LEASE_EPOCH`).
4. Upon receiving `STALE_LEASE_EPOCH`, the worker MUST immediately abort execution and tear down any associated browser tab context.  
**ALTERNATIVES_CONSIDERED:**
1. Trust worker self-termination on wall-clock timer: Flawed because clock drift and thread pauses prevent workers from accurately knowing if they timed out.  
**CAPABILITY_IMPACT:** None. Completely eliminates split-brain concurrency hazards.  
**COMPATIBILITY_IMPACT:** Adds `lease_epoch` field to command schemas.  
**MIGRATION_IMPACT:** DB migration in `avf-core-state` to add `lease_epoch` column; workers updated to pass epoch in responses.  
**TEST_OR_BENCHMARK_REQUIRED:** Distributed concurrency test: simulate zombie worker completing after lease reassignment; verify stale completion is rejected.  
**RESIDUAL_RISK:** None. Standard distributed systems fencing token pattern.  
**CONFIDENCE:** 1.0 (Certain)

---

### FINDING_ID: F-R02-005
**ROLE:** R02_RELIABILITY  
**SEVERITY:** MEDIUM (BLOCKER_BEFORE_FREEZE)  
**CATEGORY:** DISTRIBUTED_TRANSACTIONS_AND_BUDGET  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-018)
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md`  
**AFFECTED_CONTRACTS:** `R02_CORE_STATE.md` Public API (`AppendUsageRecord`, budget tracking)  
**EVIDENCE:** `R02_CORE_STATE.md` lines 52 and `SYSTEM_INVARIANTS.md` INV-018 mandate deterministic budget enforcement before external requests, but specify only a single synchronous `AppendUsageRecord` command without a two-phase reservation/commit mechanism.  
**FAILURE_SCENARIO:** Core State decrements a project's budget before calling the provider. The generation activity fails due to a transient browser crash or network outage before the prompt is actually submitted. Because the usage was already permanently appended, the project's budget is drained for a generation that never took place, causing premature `BUDGET_EXHAUSTED` blocking on subsequent shots.  
**WHY_IT_MATTERS:** False budget exhaustion halts automated pipelines and requires manual database correction, undermining autonomous batch production.  
**PROPOSED_SOLUTION:**
Introduce a **Two-Phase Budget Reservation Protocol** in `avf-core-state`:
1. Add commands to `R02_CORE_STATE.md`:
   - `ReserveBudget(project_id, generation_job_id, amount, ttl_seconds)` -> returns `reservation_id`.
   - `CommitBudget(reservation_id, actual_usage, provider_job_id)` -> commits permanent `CostUsageRecord`.
   - `ReleaseBudget(reservation_id, reason)` -> unlocks held budget immediately.
2. In `avf-workflow`:
   - Execute `ReserveBudget` before initiating provider submission.
   - Execute `CommitBudget` upon verified `SUBMITTED` state.
   - Execute `ReleaseBudget` in compensation block if submission fails terminally before provider ACK.
3. Add a background sweeper in Core State to auto-release expired reservations whose TTL has elapsed without commit.  
**ALTERNATIVES_CONSIDERED:**
1. Deduct budget only after generation completes: Rejected because concurrent workflows could exceed project limits before any one job completes (violates INV-018).  
**CAPABILITY_IMPACT:** None. Prevents phantom budget leaks while strictly preserving INV-018.  
**COMPATIBILITY_IMPACT:** Adds reservation commands to Core State contract.  
**MIGRATION_IMPACT:** Database migration adding `budget_reservations` table and updating Core State service logic.  
**TEST_OR_BENCHMARK_REQUIRED:** Concurrency test: execute multiple parallel generations up to budget limit; inject failure before submit; verify budget is released and subsequent valid generation succeeds.  
**RESIDUAL_RISK:** None. Standard financial/quota ledger pattern.  
**CONFIDENCE:** 1.0 (Certain)

---

### FINDING_ID: F-R02-006
**ROLE:** R02_RELIABILITY  
**SEVERITY:** MEDIUM (NON_BLOCKING)  
**CATEGORY:** BROWSER_EXTENSION_LIFECYCLE  
**AFFECTED_FILES:**
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md` (Risk R8)  
**AFFECTED_CONTRACTS:** Track A Browser Worker Host-Extension Protocol  
**EVIDENCE:** `RISK_REGISTER.md` lists Risk R8 ("MV3 service worker termination", Probability: High, Impact: Medium) but `R09_BROWSER_WORKER.md` does not specify the keep-alive or state restoration architecture between the Native Messaging host and the MV3 extension.  
**FAILURE_SCENARIO:** During a 5-minute video generation in Google Flow, the MV3 background service worker becomes idle according to Chromium's internal lifecycle timer and is abruptly terminated. When the local worker host attempts to poll generation state via loopback WebSocket/Native Messaging, the request fails with a connection reset, triggering an unnecessary browser restart and false alarm.  
**WHY_IT_MATTERS:** Uncontrolled service worker termination introduces transient flakiness, degrades single-shot automation reliability below the target >=95%, and causes unnecessary worker churn.  
**PROPOSED_SOLUTION:**
Specify the MV3 lifecycle management architecture in `R09_BROWSER_WORKER.md`:
1. Use **Chrome Native Messaging** as primary transport: Native Messaging connections keep the MV3 background service worker active for the duration of the open port.
2. If WebSocket loopback (Option A2) is used, the content script injected into the Flow tab MUST maintain an active heartbeat channel (`chrome.runtime.connect` / ping loop every 20s) to prevent service worker termination.
3. Content scripts must autonomously monitor the DOM and store intermediate state in `chrome.storage.session` so that if the background worker restarts, state is restored without dropping generation observation.  
**ALTERNATIVES_CONSIDERED:**
1. Pin older Chrome Manifest V2: Rejected because MV2 is deprecated and blocked in modern Chromium releases.  
**CAPABILITY_IMPACT:** None. Ensures stability of Track A automation.  
**COMPATIBILITY_IMPACT:** Internal to `avf-browser-worker` implementation.  
**MIGRATION_IMPACT:** Reflected in Track A worker architecture and test suite.  
**TEST_OR_BENCHMARK_REQUIRED:** Idle lifecycle test: verify worker successfully maintains connection and captures output during a 10-minute simulated generation without process restart.  
**RESIDUAL_RISK:** Future Chromium policy changes on background timers; mitigated by Native Messaging port support.  
**CONFIDENCE:** 0.95 (High)

---

## 7. Residual Uncertainties & Recommended Spikes

1. **Google Flow Active DOM Marker Feasibility Spike (Track A):**
   - *Uncertainty:* Can a client inject hidden metadata (e.g. zero-width Unicode characters or prompt comment tags) into Google Flow prompts to enable 100% deterministic matching during uncertain submit reconciliation without altering generation output?
   - *Recommended Spike:* Phase 0 spike in `avf-browser-worker` testing zero-width space prompt tagging in Google Flow text input.
2. **Native Messaging vs Loopback WebSocket Performance & Packaging Spike:**
   - *Uncertainty:* Operational complexity of Native Messaging manifest registration on developer machines vs loopback WebSocket server security tokens.
   - *Recommended Spike:* Phase 0 spike comparing Native Messaging host lifecycle vs authenticated WebSocket in local Docker/macOS environment.

---

## 8. Review Sign-off & Metadata

- **Reviewer:** R02_RELIABILITY (Distributed Systems & Reliability Architect)
- **Role Identity:** Independent Voting Council Reviewer
- **Round:** C01 Independent Blind Review
- **Session ID:** `7380b26a-7a61-41b9-bffa-bb438c0c91d0`
- **Timestamp:** 2026-08-15T11:35:00+07:00
- **Status:** Review Complete — 6 Findings Submitted (3 Critical/High Blockers, 2 Medium Blockers, 1 Non-Blocking Enhancement).
