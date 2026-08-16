# C02R GENUINE ADVERSARIAL CROSS-EXAMINATION: CLUSTER 04
## PROVIDER RESULT, LIFECYCLE & ERROR TAXONOMY
**ROLE:** R02 Reliability Specialist (CHALLENGER)  
**DECISION_CLUSTER:** CLUSTER-04 (Provider Result, Lifecycle & Error Taxonomy)  
**FINDINGS COVERED:** FINDING_005, FINDING_022, FINDING_051, TECH-008  
**DATE:** 2026-08-15  
**EVALUATION TYPE:** Genuine Technical Attack & Boundary Reliability Vulnerability Analysis  

---

### EXECUTIVE SUMMARY & CHALLENGER STANCE

As the R02 Reliability Specialist, I challenge the proposed Multi-Tier Provider Response and Error Taxonomy model (formulated in `SOL-05` and defended by Proponents R04 and R09). While separating transport-level RPC outcomes from asynchronous generation lifecycle states is conceptually sound, the current architecture introduces severe reliability vulnerabilities, cognitive friction for adapter authors, split-brain retry routing, polling deadlocks, and acute operational risks during authentication and security challenges.

Specifically, this attack demonstrates:
1. **The Four-Tier Combinatorial Hazard:** Decomposing provider outcomes into 4 orthogonal enum fields (`OperationStatus`, `ProviderGenerationStatus`, `NormalizedErrorCode`, `RetryCategory`) creates 720 possible state permutations without strict schema-level mutually exclusive invariants. This directly results in adapter implementation drift, contradictory retry classifications, and unhandled `null` dereferences in upstream orchestrators (`R06_WORKFLOW`).
2. **The Status Polling Ambiguity Paradox:** The specification lacks a formal distinction between an *RPC probe transport failure* and a *remote engine task abort*. During prolonged video generation (120–600s), transient network degradation risks either prematurely abandoning viable generation jobs (orphaning expensive GPU resources and exhausting account quotas) or entering infinite polling loops against crashed remote processes.
3. **The Security/Auth Challenge Cascading Failure Loop:** The interaction between `AUTH_REQUIRED` / `SECURITY_CHALLENGE`, worker lease lifecycles, and operator escalation violates System Invariant 12 and System Invariant 3. Automated retry policies lack circuit breakers to prevent account banning, and the worker-lease architecture forces an unresolvable tradeoff between holding expensive browser resources hostage during human intervention or dropping ephemeral session state entirely.

---

### 1. ATTACK 1: THE FOUR-TIER STATUS/ERROR MODEL — COGNITIVE OVERLOAD & SPLIT-BRAIN INVARIANTS

#### 1.1 Combinatorial Explosion & Invalid Matrix States
The proposed `SOL-05` specification establishes four distinct classification axes for a provider operation response:
1. `status` (OperationStatus): `SUCCESS`, `FAILED`, `PENDING`, `RUNNING`
2. `generation_status` (ProviderGenerationStatus): `QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`
3. `error.code` (NormalizedProviderErrorCode): `PROVIDER_RATE_LIMIT`, `AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`, `BUDGET_EXHAUSTED`, `UNSUPPORTED_CAPABILITY`, `NETWORK_TIMEOUT`, `BAD_REQUEST`, `PROVIDER_INTERNAL_ERROR`
4. `error.retry_category` (RetryCategory): `TRANSIENT`, `PERMANENT`, `POLICY_BLOCKED`, `RESOURCE_EXHAUSTED` (alongside a legacy `retryable: boolean` in `provider-result.schema.json`).

This four-dimensional matrix generates $4 \times 5 \times 9 \times 4 = 720$ theoretical state permutations. In reality, less than 5% of these permutations represent valid physical states. 

**Concrete Failure Modes in Adapter Development:**
* **Contradictory Success/Failure Payloads:** An adapter author implementing R08 (Google Flow) or a future Sora/Runway adapter can return:
  ```json
  {
    "status": "SUCCESS",
    "generation_status": "SUCCEEDED",
    "error": {
      "code": "AUTH_REQUIRED",
      "retry_category": "PERMANENT"
    }
  }
  ```
  Is this a successful generation or an authentication failure? Because `provider-result.schema.json` does not enforce conditional constraints tying `error` existence strictly to `status == "FAILED"` or `generation_status == "FAILED"`, upstream workflow consumers (`R06`) face parsing ambiguity.
* **The "Orphaned Failure" State:** An adapter encounters a CDP timeout communicating with Chrome and returns:
  ```json
  {
    "status": "FAILED",
    "generation_status": null,
    "error": null
  }
  ```
  When R06 attempts to evaluate `result.error.retry_category`, the worker crashes with an unhandled `TypeError: Cannot read properties of null (reading 'retry_category')`, escalating a minor probe blip into a catastrophic workflow worker crash.

#### 1.2 The Split-Brain Precedence Hazard (`code` vs `retry_category` vs `retryable`)
The schema contains duplicate semantic channels for driving retry decisions:
* `error.code` defines the domain cause (e.g., `PROVIDER_RATE_LIMIT`).
* `error.retry_category` defines the strategic bucket (e.g., `RESOURCE_EXHAUSTED` vs `TRANSIENT`).
* `error.retryable` (boolean) provides a direct binary flag.

**The Split-Brain Vulnerability:**
What happens when an adapter author maps a new provider error and outputs:
```json
{
  "code": "SECURITY_CHALLENGE",
  "retry_category": "TRANSIENT",
  "retryable": true
}
```
* If R06's deterministic retry policy engine evaluates `retry_category == 'TRANSIENT'`, it schedules an automated retry, hammering Google Flow with automated login requests and triggering a permanent security ban (violating Invariant 12).
* If R06 evaluates `code == 'SECURITY_CHALLENGE'`, it halts for operator review.
* If another microservice evaluates `retryable == true`, it re-queues the command.

Having three separate fields dictating retry behavior is a catastrophic anti-pattern. Retryability MUST be a deterministic, mathematical projection derived entirely from the normalized error code and central workflow policy (ADR-006: *"QC/LLMs provide scores/reasons; software policy owns retries and budgets"*), never an arbitrary choice made by individual adapter authors.

#### 1.3 Cognitive Overload in Polyrepo Adapter Construction
Under polyrepo governance (`R01_CONTRACTS`, `R07_PROVIDER_SDK`, `R08_GOOGLE_FLOW_ADAPTER`), independent developers will implement provider adapters. Requiring every adapter to correctly coordinate four disparate enum tiers without shared runtime assertion wrappers guarantees divergence:
* Adapter A will set `status: FAILED` on remote prompt rejection.
* Adapter B will set `status: SUCCESS, generation_status: FAILED` on remote prompt rejection.
* Adapter C will invent custom unmapped string codes under `details.provider`.

The contract specification fails to provide an unambiguous, closed discriminated union or a single canonical factory helper in `R07_PROVIDER_SDK`.

---

### 2. ATTACK 2: STATUS POLLING AMBIGUITIES — TRANSIENT DROPS VS PERMANENT ABORTS

#### 2.1 The Two-Dimensional Failure Space
In long-running generative video operations, status polling occurs over minutes (e.g., Google Flow Veo generation taking 180–420 seconds). During this window, two distinct failure types occur:
1. **Probe Transport Failure:** The HTTP RPC, WebSocket, or Chrome DevTools Protocol (CDP) connection between the AVF worker and the browser/API drops for 5 seconds (TCP reset, transient socket timeout, OS scheduling delay).
2. **Provider Remote Task Abort:** Google Flow silently drops the prompt, encounters a GPU out-of-memory error, displays a modal error toast ("Generation failed - Prompt violates safety guidelines"), or kills the generation job on the remote server.

The current schema (`provider-result.schema.json`) and state machine (`STATUS_STATE_MACHINES.md`) do not provide a structured protocol for polling reconciliation.

```
+------------------------------------------------------------------------------------+
|                               THE POLLING DILEMMA                                  |
|                                                                                    |
|                     +---------------------------------------+                      |
|                     | Polling Request: READ_GENERATION_STATE|                      |
|                     +-------------------+-------------------+                      |
|                                         |                                          |
|                         +---------------+---------------+                          |
|                         |                               |                          |
|                 [Transport Fails]               [Transport Succeeds]               |
|                 (Socket Timeout)                (HTTP 200 / CDP OK)                |
|                         |                               |                          |
|             +-----------+-----------+           +-------+-------+                  |
|             |                       |           |               |                  |
|       [Action A: Abort]       [Action B: Poll] [State: RUNNING][State: FAILED]     |
|             |                       |           |               |                  |
|      Orphans Remote Job        Infinite Loop    Continue Poll   Route Error        |
|      (Wastes $ / Quota)        on Dead Process                                     |
+------------------------------------------------------------------------------------+
```

#### 2.2 The "Silent Task Drop" vs "Network Flake" Race Condition
* **Scenario A (Premature Abandonment):** A worker issues `READ_GENERATION_STATE`. A transient WiFi/network blip occurs, causing a 15-second timeout. If the adapter maps this timeout to `status: FAILED, generation_status: FAILED, code: NETWORK_TIMEOUT`, R06 transitions the `GenerationJob` to `FAILED_TRANSIENT` or `FAILED_PROVIDER` and initiates a new submit attempt. Meanwhile, the original generation completes 60 seconds later on Google Flow. Result: Duplicate video generated, double quota consumed, wasted credit budget, and potential downstream continuity mismatch.
* **Scenario B (Zombie Polling Loop):** Google Flow encounters an internal UI error where the generation spinner freezes indefinitely due to an unhandled frontend JS exception. The adapter queries the DOM, sees the spinner element still present, and continuously returns `status: SUCCESS, generation_status: PROCESSING`. Without an explicit `max_poll_duration`, `staleness_threshold_ms`, or progress heartbeat contract, the worker remains stuck in `GENERATING` until global workflow timeout (e.g., 30 minutes), blocking the execution queue.

#### 2.3 Lease Expiry & Distributed Worker Collisions
Under `R02_CORE_STATE` and `R09_BROWSER_WORKER`, execution commands are protected by leases (e.g., 60-second TTL). 
1. Worker 1 is polling a 300-second video generation.
2. At second 120, Worker 1 suffers local network congestion or a process freeze for 65 seconds while attempting `READ_GENERATION_STATE`.
3. Worker 1's lease on `generation_job_id` expires in R02.
4. Worker 2 detects the expired lease, claims the `GenerationJob`, and sees the state is `SUBMITTED`. Worker 2 has no way to know if the generation is actually active in Worker 1's browser instance.
5. Worker 2 issues `SUBMIT_PROMPT` again, creating a duplicate concurrent generation task in Google Flow.
6. Worker 1 recovers, reads `SUCCEEDED` from its local browser session, and attempts to write `DOWNLOADED`. Worker 2 also finishes and writes `DOWNLOADED`.
7. Canonical state is corrupted with conflicting take artifacts, violating System Invariant 1 (*"A Take belongs to exactly one Shot and references exactly one GenerationJob"*).

---

### 3. ATTACK 3: SECURITY & AUTH CHALLENGES — INFINITE RETRIES & SAFE OPERATOR INTERVENTION

#### 3.1 Account Destruction via Automated Cascading Retries
Google Flow enforces stringent bot-detection and anti-scraping heuristics (reCAPTCHA Enterprise, Cloudflare Turnstile, behavioral mouse entropy, session cookie invalidation).

When an automated script encounters a bot detection challenge:
* The DOM displays a CAPTCHA modal or redirects to `accounts.google.com/signin/v2/challenge`.
* If R08 or R10 does not strictly recognize this pattern or misclassifies it as a generic `TRANSIENT_BROWSER` / `UI_CHANGED` error, the standard exponential backoff retry loop (e.g., 3 retries over 60 seconds) will repeatedly refresh the page and re-attempt DOM form injection.
* **The Failure Cascade:** Repeatedly hitting Google authentication challenge endpoints with automated CDP commands is the #1 trigger for permanent Google Workspace/Account termination. 
* System Invariant 12 explicitly dictates: *"Authentication/security challenges do not trigger automated bypass behavior."* Yet, the current blueprint kit contains **no architectural guarantee or circuit breaker** at the provider contract boundary to hard-kill retries immediately upon receiving `AUTH_REQUIRED` or `SECURITY_CHALLENGE`.

#### 3.2 The Worker Resource Starvation vs Session Context Eviction Paradox
When `SECURITY_CHALLENGE` or `AUTH_REQUIRED` is legitimately detected, the system must escalate to an operator via `R13_OPERATOR_CONSOLE`. However, this introduces an unresolvable architectural contradiction between `R02_CORE_STATE`, `R06_WORKFLOW`, and `R09_BROWSER_WORKER`:

```
                               THE OPERATOR INTERVENTION PARADOX
                               
  Option 1: Hold Browser Lock                     Option 2: Release Browser Lock
  ---------------------------                     ------------------------------
  - Worker holds browser profile open             - Worker releases lease and closes browser
  - Operator opens browser & solves CAPTCHA       - Operator alerted to log in
  - CON: Expensive worker process blocked         - CON: Chrome profile session / ephemeral
    for hours; blocks queue concurrency;                 state destroyed; ongoing render context
    violates lease TTL invariants                        lost; operator cannot solve in-situ
```

* **If Option 1 is chosen (Hold Lock):** The browser worker holds the active Chrome instance open, waiting for the human operator to solve the challenge. But operators may take 30 minutes to 8 hours to respond. Holding the worker lease blocks the worker slot, starves the entire generation pipeline, and breaks distributed lease renewal models.
* **If Option 2 is chosen (Evict Context):** The worker releases the lease and terminates the process. When the operator eventually logs in via R13, the in-situ generation state, tab session, and prompt context are completely lost. The operator cannot "resume" the specific failed job; they must manually rebuild the entire pipeline state.

#### 3.3 Missing Operator Intervention Contracts & Resume Protocols
The blueprint kit defines no explicit contract for operator intervention lifecycle. Specifically:
1. `STATUS_STATE_MACHINES.md` lists `BLOCKED_AUTH` and `BLOCKED_SECURITY` as recoverable/error states for `GenerationJob`, but does not define:
   - What command or event transitions `BLOCKED_AUTH -> READY` or `BLOCKED_SECURITY -> SUBMITTING`?
   - How does the system verify that the human has actually solved the challenge before releasing the job back into automated execution?
   - If an automated retry fires immediately after operator "unblock" without credential verification, and the challenge was NOT solved, the account is instantly banned.
2. `browser-command.schema.json` has `HUMAN_REQUIRED`, but lacks an operation like `PAUSE_FOR_OPERATOR`, `AWAIT_OPERATOR_RESOLUTION`, or `RESUME_AFTER_AUTH`.

---

### 4. SUMMARY OF SPECIFICATION DEFECTS

| Defect ID | Severity | Root Cause | Impact |
|---|---|---|---|
| **DEF-C04-01** | CRITICAL | 4 orthogonal, non-constrained status/error enums | 720 state permutations; split-brain retry decisions between `code` and `retry_category`; null-dereference crashes in workflow. |
| **DEF-C04-02** | HIGH | Conflation of probe transport failure with engine task abort | Network jitter causes premature abandonment of active renders (wasted credits/quota) or infinite polling loops on frozen browser tabs. |
| **DEF-C04-03** | CRITICAL | Absence of strict circuit-breaking on `SECURITY_CHALLENGE` / `AUTH_REQUIRED` | Automated retries hammer Google challenge endpoints, violating INV-012 and causing permanent provider account bans. |
| **DEF-C04-04** | HIGH | Unresolved worker lease vs human intervention lifecycle | Holding browser workers hostage during CAPTCHAs starves queues; terminating workers destroys ephemeral session context needed to solve the challenge. |
| **DEF-C04-05** | MEDIUM | Lack of formal Operator Resume / Handshake Contract | No verified state machine transition from `BLOCKED_AUTH`/`BLOCKED_SECURITY` back to execution; risk of immediate re-triggering against unresolved challenges. |

---

### 5. REQUIRED STRICT REMEDIATION CONSTRAINTS (FOR C03R / C04R)

To remediate these critical reliability vulnerabilities prior to specification freeze, the Council must mandate the following changes in C03R/C04R:

1. **Eliminate Redundant Error Classification Fields:**
   - Remove `retry_category` and `retryable` boolean from `provider-result.schema.json`.
   - Maintain a single, strictly typed `error.code` enum.
   - Establish a 100% deterministic lookup table in `R07_PROVIDER_SDK` / `R06_WORKFLOW` that maps `error.code` $\to$ `RetryPolicy` (Backoff interval, Max Retries, Escalation Route). Individual adapters must NEVER declare retryability.

2. **Enforce Discriminated Union / Conditional JSON Schema on Provider Result:**
   - If `status == "SUCCESS"`, `generation_status` MUST be present; `error` MUST be `null`.
   - If `status == "FAILED"`, `error` MUST be present with a valid `code` and human-readable `message`.
   - If `generation_status == "FAILED"`, `error` MUST be present.

3. **Explicit Probe vs Task Error Separation in Status Polling:**
   - Introduce `probe_status` (HTTP/CDP transport outcome: `PROBE_OK`, `PROBE_FAILED`) separate from `task_status` (`QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`).
   - Mandate a `consecutive_probe_failures_limit` (e.g., 5 probes over 60s) before marking a job `FAILED_TRANSIENT`.
   - Mandate monotonic task progress tracking or maximum non-progress duration (`max_poll_idle_ms`) to detect frozen browser DOMs.

4. **Zero-Retry Hard Circuit Breakers for Auth & Security Challenges:**
   - On `AUTH_REQUIRED` or `SECURITY_CHALLENGE`, the adapter and workflow must IMMEDIATELY execute an atomic circuit breaker: 0 automated retries permitted.
   - Transition `GenerationJob` to `BLOCKED_AUTH` / `BLOCKED_SECURITY`.
   - Emit `ProviderAuthChallengeEncountered` event to alert operator via `R13_OPERATOR_CONSOLE`.

5. **Formalized Operator Intervention & Session Parking Protocol:**
   - When transitioning to `BLOCKED_AUTH`, decouple the heavy browser worker lease.
   - Park the execution state with a dedicated correlation token (`auth_challenge_id`).
   - Require explicit operator action `RESUME_WITH_VERIFIED_AUTH` from R13, which runs a non-destructive session validation probe (`ENSURE_SESSION`) before any generation submission is re-attempted.

---
**CHALLENGER SIGN-OFF:** R02 (Reliability Specialist) — *Vulnerabilities submitted for council disposition.*
