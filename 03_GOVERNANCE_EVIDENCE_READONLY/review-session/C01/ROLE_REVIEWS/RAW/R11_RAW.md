# C01 Independent Specialist Review — R11_PLATFORM

**Role:** Platform / Observability / Operations Architect (R11_PLATFORM)  
**Evaluation Round:** Round C01 — Independent Blind Specialist Review  
**Authority:** `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0`  
**Timestamp:** 2026-08-15T11:30:00+07:00  
**Session ID:** `f8d7a075-c083-4eb0-ae7c-7c4ac2473faa`  
**Review Mode:** Blind Independent Evaluation (Zero cross-reviewer collusion)

---

## 1. Executive Summary & Review Scope

As the Platform, Observability, and Operations Architect (R11), my primary mandate is ensuring that every distributed execution step, state transition, background activity, and failure event in the AI Video Factory is fully observable, deterministic, recoverable, and diagnosable from persisted evidence without human guesswork.

### 1.1 Specification Files Inspected
1. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` (Primary blueprint)
2. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md` (Primary catalog)
3. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md` (Primary graph)
4. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json`
5. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
6. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json`
7. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json`
8. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json`
9. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md`
10. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
11. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/LOCAL_DEVELOPMENT.md`
12. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md`
13. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/FREEZE_CHECKLIST.md`
14. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
15. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md`
16. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
17. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
18. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
19. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
20. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R15_INTEGRATION_HARNESS.md`
21. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md`
22. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md`
23. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-001_MODULAR_POLYREPO.md` through `ADR-008_WORKFLOW_ENGINE.md`
24. `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md`
25. `review-session/C00_FINAL/REQUIREMENT_TRACEABILITY_MATRIX.md`
26. `review-session/C00_FINAL/PROTECTED_CAPABILITY_REGISTER.md`
27. `review-session/C00_FINAL/SYSTEM_INVARIANT_INVENTORY.md`
28. `review-session/C00_FINAL/CONTRACT_INVENTORY.md`
29. `review-session/C00_FINAL/EVIDENCE_LEDGER.md`

### 1.2 Assigned Gap Seeds Handled
- **GAP-006**: Diagnostic screenshot storage format, encryption at rest, and retention lifecycle policy.
- **GAP-009**: OpenTelemetry metric naming standards, Prometheus exposition format, histogram bucket definitions, and SLI/SLO catalog.

---

## 2. Invariants & Contracts Relevant to R11 Platform Lens

1. **`INV-015` (Correlation Propagation)**: Correlation IDs (`trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`) must propagate across workflow, provider, browser execution, QC, and media processing.
2. **`INV-001` (Take Ownership & Reference Integrity)**: A Take belongs to exactly one Shot and references exactly one GenerationJob.
3. **`INV-003` (Idempotency of External Side Effects)**: Every external side effect has an idempotency key or an explicit documented reason it cannot.
4. **`INV-005` (Non-Canonical Worker State)**: Browser/extension/FlowKit state is never canonical business state; local worker memory is disposable.
5. **`INV-012` (No Automated Security Bypass)**: Authentication/security challenges do not trigger automated bypass behavior; must be safely surfaced to operators.
6. **`INV-013` (Private Database Isolation)**: A repository cannot read another repository's private database schema directly.
7. **`INV-016` (Immutability of Completed Takes)**: A completed Take cannot be overwritten; replacement produces another Take/AssetVersion.
8. **`INV-019` (Worker Crash Resilience)**: A browser worker can crash without losing canonical queue truth.
9. **`REQ-014` (R14 Ownership)**: R14 owns OpenTelemetry conventions, log field schemas, metric naming standards, correlation propagation helpers, and tracing dashboards.
10. **`REQ-027` (Standard Event Envelope)**: All published events must adhere to the standardized event envelope contract.
11. **`REQ-050` (Privileged Local Execution Security)**: Browser profiles, cookies, and tokens are secrets; logs and diagnostic screenshots must redact tokens/cookies.
12. **`REQ-055` (Transactional Outbox Semantics)**: Core transactions write canonical state + outbox row atomically; dispatcher delivers idempotently.

---

## 3. Concrete Failure Scenarios Evaluated

### Scenario 1: Broken Trace Graph Across Asynchronous Outbox & Worker Boundaries
An operator reports that generation jobs in a multi-shot project intermittently take over 10 minutes or fail silently. The platform engineer queries Jaeger/Tempo for the `trace_id` generated during the initial API command. The trace ends abruptly after 15ms inside `avf-core-state`'s HTTP handler. Because `event-envelope.schema.json` only carries a bare `trace_id` string without W3C `traceparent` (`version-trace_id-parent_span_id-trace_flags`), `tracestate`, or OpenTelemetry span context injection, the subsequent Outbox publisher, Temporal workflow orchestrator, browser worker commands, and media transcoding steps execute as disconnected root traces. SREs cannot trace causality across the system, rendering distributed flame charts and automated latency bottleneck attribution useless.

### Scenario 2: Outbox Dispatcher Contention & Poison Pill Lockup in High-Availability Deployments
In a multi-replica deployment of `avf-core-state` (or multiple outbox dispatcher instances), both dispatchers execute `SELECT * FROM outbox_events WHERE status = 'PENDING' LIMIT 50` without explicit row locking (`FOR UPDATE SKIP LOCKED`). Both instances fetch identical pending events, attempt concurrent delivery, trigger duplicate event storms to downstream message handlers, and collide on status updates. Furthermore, when an outbox message contains an unroutable destination or unparseable payload, the dispatcher continuously retries every 500ms without exponential backoff or dead-letter queue (DLQ) isolation, halting the delivery pipeline for all subsequent video generation events.

### Scenario 3: Unencrypted Diagnostic Dumps Leaking User Credentials & Google Flow Session Material
A Track A Browser Worker encounters an unexpected UI state in Google Flow (e.g., an account verification modal or layout shift) and triggers `CAPTURE_DIAGNOSTIC`. The worker captures an unredacted full-viewport screenshot containing the user's logged-in Google email address, account switcher profile avatar, and active prompt draft. The diagnostic screenshot and raw DOM dump are written unencrypted to local storage. When diagnostic logs are ingested into central storage or shared in a bug report, sensitive personal data and Google session identifiers are exposed to unauthorized personnel in violation of `REQ-050` and `INV-012`.

### Scenario 4: Worker Process Hang & Missing Heartbeat Lease Expiration
During a long-running video generation polling loop, a Chrome MV3 service worker terminates or enters an unresponsive state due to internal browser memory exhaustion. Because there is no active liveness heartbeat probe or lease timeout between `avf-google-flow-adapter` and `avf-browser-worker`, the adapter process blocks indefinitely until the global Temporal activity timeout of 15 minutes is reached. The operator console shows "Generating..." with no feedback, and no automatic worker recycling or failover occurs.

### Scenario 5: Disaster Recovery Failure & Data Loss Due to Undefined WAL Archiving & Backup RTO/RPO
The PostgreSQL database disk hosting `avf-core-state` suffers an unrecoverable hardware failure. The operations team attempts disaster recovery, only to discover that backups were limited to an unverified nightly `pg_dump` that ran 16 hours prior. Because continuous PostgreSQL WAL (Write-Ahead Logging) archiving to object storage was not specified or automated, all `Project`, `ShotVersion`, `PromptVersion`, `Take`, and audit ledger entries recorded over the preceding 16 hours are permanently lost, violating data provenance (`INV-006`) and state immutability (`INV-016`).

---

## 4. Evidence-Backed Council Findings

```markdown
### FINDING_ID: F-R11-001
- **ROLE**: R11_PLATFORM
- **SEVERITY**: HIGH
- **CATEGORY**: CONTRACTS / OBSERVABILITY
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
- **AFFECTED_CONTRACTS**: 
  - `event-envelope.schema.json`
  - `browser-command.schema.json`
  - `provider-request.schema.json`
- **EVIDENCE**: 
  In `event-envelope.schema.json` (lines 26-40), the envelope defines `"trace_id": { "type": "string" }`, `"workflow_run_id"`, and `"project_id"`, but completely omits `"span_id"`, `"parent_span_id"`, `"trace_flags"`, `"tracestate"`, and OpenTelemetry W3C `traceparent` formatting. Similarly, `browser-command.schema.json` (lines 45-65) defines an ad-hoc `correlation` object with only `trace_id`, `generation_job_id`, and `attempt_id`. `provider-request.schema.json` (lines 107-121) requires only `trace_id` and `workflow_run_id`.
- **FAILURE_SCENARIO**: 
  When a command flows from the API gateway -> core-state -> transactional outbox -> message broker -> workflow worker -> provider adapter -> browser worker -> media worker -> QC service, OpenTelemetry SDKs cannot extract parent span IDs across asynchronous message boundaries. Every async consumer creates a detached root trace or assigns a random new span without linking to the initiating parent span. Distributed tracing UIs (Jaeger/Tempo) display fragmented, single-span traces, making it impossible to calculate end-to-end latency waterfalls or pinpoint which activity caused a generation stall.
- **WHY_IT_MATTERS**: 
  Invariant 15 (`INV-015`) explicitly states: "Correlation IDs must propagate across workflow, provider, browser execution, QC, and media processing." Without standard W3C TraceContext headers (`traceparent`, `tracestate`), standards-compliant distributed tracing is broken across the entire polyglot architecture.
- **PROPOSED_SOLUTION**: 
  1. Standardize distributed tracing on the W3C TraceContext specification (`traceparent` header string formatted as `00-${trace_id}-${span_id}-${trace_flags}`).
  2. Update `event-envelope.schema.json`, `browser-command.schema.json`, and `provider-request.schema.json` to include:
     ```json
     "traceparent": {
       "type": "string",
       "pattern": "^00-[0-9a-fA-F]{32}-[0-9a-fA-F]{16}-[0-9a-fA-F]{2}$",
       "description": "W3C TraceContext traceparent string: 00-traceid-spanid-traceflags"
     },
     "tracestate": {
       "type": ["string", "null"],
       "description": "W3C TraceContext tracestate string"
     },
     "baggage": {
       "type": "object",
       "additionalProperties": { "type": "string" },
       "description": "OpenTelemetry baggage containing domain keys: project_id, shot_id, generation_job_id, attempt_id"
     }
     ```
  3. Mandate in `R14_PLATFORM_OBSERVABILITY.md` that all service SDKs and interceptors automatically inject and extract `traceparent` and domain baggage across HTTP, gRPC, WebSocket, Native Messaging, and Outbox event boundaries.
- **ALTERNATIVES_CONSIDERED**: 
  - *Keep custom string IDs only*: Rejected because standard OpenTelemetry collectors and APM tooling cannot reconstruct trace parent-child hierarchies without manual custom span stitching.
  - *Rely exclusively on Temporal's built-in workflow tracing*: Rejected because browser workers, media workers, outbox publishers, and direct HTTP/gRPC services operate outside of Temporal's internal workflow execution context.
- **CAPABILITY_IMPACT**: Enables true end-to-end distributed APM visualization, automated distributed latency profiling, and seamless cross-service root-cause analysis without sacrificing system modularity.
- **COMPATIBILITY_IMPACT**: Non-breaking additive schema enhancement to contracts; existing `trace_id` fields can be retained as convenience aliases.
- **MIGRATION_IMPACT**: Update JSON schema definitions in `avf-contracts` and update the correlation helper library in `avf-platform-observability`.
- **TEST_OR_BENCHMARK_REQUIRED**: Contract test validating W3C regex conformance in schema fixtures; integration test verifying parent-child span linkage across an asynchronous Outbox -> Workflow -> Browser Worker execution flow.
- **RESIDUAL_RISK**: Low. W3C TraceContext is an industry-standard specification natively supported by all major OpenTelemetry language SDKs.
- **CONFIDENCE**: HIGH (100% based on direct contract schema inspection and W3C OTel standard specifications).
```

```markdown
### FINDING_ID: F-R11-002
- **ROLE**: R11_PLATFORM
- **SEVERITY**: HIGH
- **CATEGORY**: SECURITY / PLATFORM / STORAGE
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
  - `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (GAP-006)
- **AFFECTED_CONTRACTS**: 
  - `SECURITY_MODEL.md`
  - `R14_PLATFORM_OBSERVABILITY.md`
- **EVIDENCE**: 
  `SECURITY_MODEL.md` (line 38) states: "diagnostics screenshot retention is configurable and access-controlled," but defines no concrete storage path hierarchy, encryption standard, retention window, or automated lifecycle pruning rules. In `C00_GAP_TO_C01_SEED_REGISTER.md`, GAP-006 identifies this exact ambiguity as a `BLOCKER_BEFORE_FREEZE`.
- **FAILURE_SCENARIO**: 
  A Track A Browser Worker captures failure diagnostics during a Google Flow generation failure. The resulting full-screen PNG contains the operator's private Google account email, profile picture, billing workspace information, and active prompt draft. Because no retention or encryption policy is enforced:
  1. The files sit unencrypted on a shared filesystem or S3 bucket indefinitely, accumulating hundreds of gigabytes of unmanaged storage.
  2. Anyone with read access to the general media bucket can inspect sensitive personal account data.
  3. Diagnostic dumps shared in open issue trackers or ingested into central log stores violate privacy regulations (GDPR/SOC2) and compromise operator security (`REQ-050`).
- **WHY_IT_MATTERS**: 
  Diagnostic captures are vital for debugging complex browser automation and UI drift failures, but unencrypted, unbounded storage of screenshots containing Google session data represents a critical security vulnerability and operational storage leak.
- **PROPOSED_SOLUTION**: 
  Formally specify the diagnostic artifact storage and lifecycle standard in `R14_PLATFORM_OBSERVABILITY.md` and `SECURITY_MODEL.md`:
  1. **Storage Bucket & Key Hierarchy**:
     - Dedicated isolated bucket: `s3://${AVF_DIAGNOSTICS_BUCKET}/` (strictly separate from public media output buckets).
     - Standard key layout: `diagnostics/projects/{project_id}/jobs/{generation_job_id}/{command_id}_{timestamp}_{error_class}.png` and accompanying metadata `..._{error_class}.meta.json`.
  2. **Encryption Standard**:
     - Enforce Server-Side Encryption with KMS or AES-256-GCM (`SSE-S3` / `SSE-KMS`) at rest.
  3. **Automated Retention & Pruning Lifecycle**:
     - *Successful executions*: Ephemeral screenshots deleted immediately upon successful command completion.
     - *Transient errors (retried)*: 24-hour expiration via S3 Lifecycle Rule (`Expiration: Days: 1`).
     - *Hard errors / Human review required / Security challenges*: 7-day retention (`Expiration: Days: 7`), after which objects are permanently purged unless explicitly flagged as `pinned_for_incident` in the incident database.
  4. **PII Masking at Capture Source**:
     - Browser worker capture scripts must apply visual bounding-box redaction (black fill) over known Google header coordinates (email, avatar, account selector) before serializing PNGs, or restrict screenshot capture to the generation canvas viewport element.
  5. **Access Control**:
     - Read access restricted to authenticated `OPERATOR` and `ADMIN` roles via short-lived pre-signed URLs (TTL <= 15 minutes).
- **ALTERNATIVES_CONSIDERED**: 
  - *Store screenshots in the primary PostgreSQL database as BLOBs*: Rejected due to database bloat, WAL write amplifications, and backup degradation.
  - *Disable screenshots entirely*: Rejected because visual inspection is indispensable for diagnosing headless browser selector drift and Google Flow anti-bot challenge states.
- **CAPABILITY_IMPACT**: Resolves GAP-006 completely, guarantees automated storage cleanup, prevents PII exposure, and provides robust diagnostic evidence for operations.
- **COMPATIBILITY_IMPACT**: Backward compatible; standardizes diagnostic storage across Track A (Browser Worker) and Track B (FlowKit Bridge).
- **MIGRATION_IMPACT**: Implementation of S3 lifecycle bucket policies and client-side masking in `avf-browser-worker` and `avf-platform-observability`.
- **TEST_OR_BENCHMARK_REQUIRED**: Automated integration test verifying that uploaded diagnostic screenshots have KMS headers, match the key hierarchy, auto-expire after TTL, and contain masked headers.
- **RESIDUAL_RISK**: Low. Standard AWS S3 / MinIO lifecycle features handle automated object expiration natively.
- **CONFIDENCE**: HIGH (Complete, concrete resolution for GAP-006).
```

```markdown
### FINDING_ID: F-R11-003
- **ROLE**: R11_PLATFORM
- **SEVERITY**: MEDIUM
- **CATEGORY**: PLATFORM / METRICS
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (GAP-009)
- **AFFECTED_CONTRACTS**: 
  - `R14_PLATFORM_OBSERVABILITY.md`
- **EVIDENCE**: 
  `R14_PLATFORM_OBSERVABILITY.md` (line 15) lists "metrics naming" under its responsibilities, but does not define canonical metric names, metric types (Counter, Gauge, Histogram), standard unit dimensions, Prometheus/OTel semantic conventions, or target SLIs/SLOs. `C00_GAP_TO_C01_SEED_REGISTER.md` flags GAP-009 as an unresolved metrics standardization seed.
- **FAILURE_SCENARIO**: 
  Independent repository development agents invent divergent metric names and types:
  - `avf-workflow` instruments `workflow_timer_seconds` (Summary);
  - `avf-provider-sdk` instruments `provider.latency.ms` (Gauge);
  - `avf-browser-worker` instruments `chrome_cmd_duration` (Histogram in milliseconds);
  - `avf-core-state` instruments `db_query_time` (plain Counter).
  When exported to Prometheus/Grafana, standardized alerting rules, SLO error budget calculations, and out-of-the-box dashboards fail because metric names, dimensions, and unit conversions are mismatched across components.
- **WHY_IT_MATTERS**: 
  Observability without a rigid metric specification creates operational chaos, prevents automated SLO tracking (e.g., Generation Latency SLO <= 90s for 95% of shots), and causes high cardinality metric explosions if agents attach raw prompt strings or unique UUIDs as metric labels.
- **PROPOSED_SOLUTION**: 
  Establish the normative OpenTelemetry Metric Catalog and Prometheus Exposition Specification in `R14_PLATFORM_OBSERVABILITY.md`:
  
  #### 1. Metric Naming & Namespace Rules
  - OpenTelemetry namespace: `avf.<subsystem>.<entity>.<action/property>_<unit>`
  - Prometheus export translation: `avf_<subsystem>_<entity>_<action/property>_<unit>`
  
  #### 2. Canonical Core Metric Catalog
  | Metric Name | Instrument | Unit | Attributes / Labels | Description |
  |---|---|---|---|---|
  | `avf.generation.job.duration_seconds` | Histogram | seconds | `provider`, `capability`, `status`, `resolution`, `model` | End-to-end generation job execution latency |
  | `avf.generation.job.queue_duration_seconds` | Histogram | seconds | `provider`, `priority` | Time job spent queued before execution started |
  | `avf.generation.job.active_count` | UpDownCounter | 1 | `provider`, `track` | Currently active generation jobs |
  | `avf.generation.job.total` | Counter | 1 | `provider`, `status`, `error_class` | Total generation jobs processed |
  | `avf.workflow.execution.duration_seconds` | Histogram | seconds | `workflow_type`, `status` | Total workflow execution duration |
  | `avf.workflow.activity.duration_seconds` | Histogram | seconds | `activity_name`, `status`, `retry_count` | Individual activity execution latency |
  | `avf.provider.request.total` | Counter | 1 | `provider`, `operation`, `http_status`, `error_class` | Provider API / Adapter call count |
  | `avf.provider.request.duration_seconds` | Histogram | seconds | `provider`, `operation`, `status` | Provider API / Adapter call latency |
  | `avf.browser_worker.session.status` | Gauge | 1 | `worker_id`, `track`, `profile_id` | Worker health status (1=Healthy, 0=Unhealthy) |
  | `avf.browser_worker.command.duration_seconds` | Histogram | seconds | `method`, `status` | Browser worker method execution latency |
  | `avf.outbox.events.published_total` | Counter | 1 | `event_type`, `status` | Outbox event delivery counter |
  | `avf.outbox.lag_seconds` | Gauge | seconds | `queue_name` | Age of oldest unpublished outbox event |
  | `avf.outbox.unprocessed_count` | Gauge | 1 | `queue_name` | Total pending outbox events count |
  | `avf.qc.evaluation.duration_seconds` | Histogram | seconds | `evaluator_type`, `verdict` | Technical QC evaluation duration |
  | `avf.media.transcode.duration_seconds` | Histogram | seconds | `codec`, `preset`, `status` | Media normalization & transcode duration |

  #### 3. Standard Histogram Buckets
  - Explicit latency buckets for video generation (`avf.generation.job.duration_seconds`):  
    `[0.5, 1.0, 2.5, 5.0, 10.0, 15.0, 30.0, 60.0, 90.0, 120.0, 180.0, 300.0, 600.0]`
  - Explicit latency buckets for internal API/DB/Activity operations:  
    `[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]`

  #### 4. Cardinality Constraint Rules
  - **FORBIDDEN Labels**: High-cardinality values (`trace_id`, `generation_job_id`, `shot_id`, `project_id`, `prompt_hash`, `prompt_text`, `error_message`) MUST NEVER be used as metric labels. They must be recorded only in Spans and Structured Logs. OpenTelemetry Exemplars should link metric bucket samples to exact `trace_id`s.
- **ALTERNATIVES_CONSIDERED**: 
  - *Leave metric naming to each repo implementer*: Rejected because distributed dashboards and alerts require a strictly unified naming schema.
  - *Use StatsD format*: Rejected because OpenTelemetry and Prometheus have superseded StatsD as modern cloud-native observability standards.
- **CAPABILITY_IMPACT**: Fully resolves GAP-009, enabling automated Prometheus scraping, unified Grafana dashboards, standard alerting rules, and automated SLO calculation.
- **COMPATIBILITY_IMPACT**: Non-breaking; establishes standard metrics for MVP and Production.
- **MIGRATION_IMPACT**: Include metric helper constants and pre-configured registries in `avf-platform-observability`.
- **TEST_OR_BENCHMARK_REQUIRED**: Metric validation test suite in `R14` asserting that emitted metrics match the defined naming pattern and forbidden labels are blocked.
- **RESIDUAL_RISK**: Low. Standard OTel SDK conventions are well established.
- **CONFIDENCE**: HIGH (Definitive resolution for GAP-009).
```

```markdown
### FINDING_ID: F-R11-004
- **ROLE**: R11_PLATFORM
- **SEVERITY**: HIGH
- **CATEGORY**: RELIABILITY / PLATFORM / STATE
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
- **AFFECTED_CONTRACTS**: 
  - `COMMAND_EVENT_CATALOG.md`
  - `event-envelope.schema.json`
- **EVIDENCE**: 
  `COMMAND_EVENT_CATALOG.md` (lines 44-50) and `R02_CORE_STATE.md` (lines 17, 39, 88, 131) specify that canonical state mutations and outbox rows are committed atomically, and a dispatcher publishes/forwards events. However, the specification completely omits:
  1. The relational table schema for `outbox_events`;
  2. The polling/dispatch locking mechanism to prevent race conditions across concurrent workers;
  3. The error recovery, backoff, and Dead-Letter Queue (DLQ) policy for unroutable or malformed events;
  4. The retention and pruning lifecycle for published outbox records.
- **FAILURE_SCENARIO**: 
  In production, two instances of `avf-core-state` run for high availability. Both execute a polling query `SELECT * FROM outbox_events WHERE status = 'PENDING'` simultaneously. Without row-level exclusion (`FOR UPDATE SKIP LOCKED`), both instances pick up the same batch of events and publish duplicate `TakeApproved` and `GenerationCompleted` messages to downstream consumers. Furthermore, if an event serialization fails due to an unexpected schema mismatch, the dispatcher retries infinitely every 200ms, creating a head-of-line blocking bottleneck where no other events can be published.
- **WHY_IT_MATTERS**: 
  Requirement `REQ-055` mandates reliable outbox event semantics. An underspecified outbox implementation leads to event duplication storms, head-of-line dispatch deadlocks, and infinite database table growth.
- **PROPOSED_SOLUTION**: 
  Specify the exact Transactional Outbox operational contract in `COMMAND_EVENT_CATALOG.md` and `R02_CORE_STATE.md`:
  
  #### 1. Normative `outbox_events` Table Schema
  ```sql
  CREATE TABLE outbox_events (
      id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      message_id UUID NOT NULL UNIQUE,
      aggregate_type VARCHAR(64) NOT NULL,
      aggregate_id VARCHAR(128) NOT NULL,
      event_type VARCHAR(128) NOT NULL,
      payload JSONB NOT NULL,
      traceparent VARCHAR(64) NOT NULL,
      tracestate VARCHAR(256),
      baggage JSONB,
      status VARCHAR(32) NOT NULL DEFAULT 'PENDING', -- PENDING, PUBLISHED, FAILED_DLQ
      retry_count INT NOT NULL DEFAULT 0,
      max_retries INT NOT NULL DEFAULT 5,
      last_error TEXT,
      next_retry_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      published_at TIMESTAMPTZ
  );
  CREATE INDEX idx_outbox_pending ON outbox_events (status, next_retry_at) WHERE status = 'PENDING';
  CREATE INDEX idx_outbox_created_at ON outbox_events (created_at);
  ```

  #### 2. Concurrency-Safe Dispatch Query
  Dispatchers MUST poll using row-level locking with skipped locks:
  ```sql
  SELECT * FROM outbox_events
  WHERE status = 'PENDING' AND next_retry_at <= NOW()
  ORDER BY created_at ASC
  LIMIT 50
  FOR UPDATE SKIP LOCKED;
  ```
  *(Optional optimization: Use PostgreSQL `LISTEN/NOTIFY` for instant low-latency wakeup, falling back to polling every 1 second).*

  #### 3. Error Handling, Exponential Backoff & Dead-Letter Queue (DLQ)
  - On publish failure: increment `retry_count`, record `last_error`, set `next_retry_at = NOW() + (POWER(2, retry_count) * INTERVAL '1 second')`.
  - If `retry_count >= max_retries`: update `status = 'FAILED_DLQ'`, emit alert `avf.outbox.dlq_event_count`, and continue processing remaining events to prevent head-of-line blocking.

  #### 4. Outbox Archival & Pruning Policy
  - Successfully published events (`status = 'PUBLISHED'`) are retained for 7 days for audit/replay, then purged by an automated daily maintenance job (`DELETE FROM outbox_events WHERE status = 'PUBLISHED' AND published_at < NOW() - INTERVAL '7 days'`).
- **ALTERNATIVES_CONSIDERED**: 
  - *Direct in-memory event publishing in HTTP request thread*: Rejected because if the application crashes or the broker is temporarily down, the event is lost forever while the database commit succeeded (dual-write problem).
  - *Rely on Debezium / Kafka CDC*: Rejected for MVP to avoid heavy infrastructure dependencies, while keeping the database outbox schema 100% compatible with future CDC adoption.
- **CAPABILITY_IMPACT**: Guarantees atomic, at-least-once, non-blocking event publishing with strict duplicate prevention and automated dead-letter safety.
- **COMPATIBILITY_IMPACT**: Zero breaking changes to public domain contracts; standardizes internal database persistence for `avf-core-state`.
- **MIGRATION_IMPACT**: Include migration script in `avf-core-state` and outbox dispatcher logic in the platform blueprint.
- **TEST_OR_BENCHMARK_REQUIRED**: Concurrency integration test with 4 parallel dispatcher instances asserting that 1,000 generated events are published exactly once with zero deadlocks and zero duplicates.
- **RESIDUAL_RISK**: Low. `FOR UPDATE SKIP LOCKED` is standard PostgreSQL concurrency architecture.
- **CONFIDENCE**: HIGH (Proven database pattern resolving critical distributed reliability gap).
```

```markdown
### FINDING_ID: F-R11-005
- **ROLE**: R11_PLATFORM
- **SEVERITY**: MEDIUM
- **CATEGORY**: OBSERVABILITY / LOGGING
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
- **AFFECTED_CONTRACTS**: 
  - `R14_PLATFORM_OBSERVABILITY.md`
  - `CONTRACTS_OVERVIEW.md`
- **EVIDENCE**: 
  `R14_PLATFORM_OBSERVABILITY.md` (line 14) lists "log field schema" as owned, but no formal JSON schema, standard field names, severity levels, or automated PII/credential scrubbing filters are specified. `SECURITY_MODEL.md` (line 37) requires that "logs redact cookies, bearer tokens, reCAPTCHA/security artifacts, API keys," but provides no technical implementation standard or redaction pattern specification.
- **FAILURE_SCENARIO**: 
  Services write unstructured text logs or mismatched JSON properties (`msg` vs `message`, `ts` vs `timestamp`, `level` vs `severity`, `err` vs `exception`). During an incident, querying logs across `avf-core-state`, `avf-workflow`, and `avf-browser-worker` requires five distinct query syntaxes. More critically, an uncaught HTTP exception in `avf-google-flow-adapter` dumps the raw HTTP Authorization header and Google session cookie into standard output, where central log shippers store and index it in plaintext.
- **WHY_IT_MATTERS**: 
  Incident diagnosis requires consistent log queryability. Unstructured or unscrubbed logs cause severe compliance failures and drastically increase MTTR during production outages.
- **PROPOSED_SOLUTION**: 
  1. Define the normative `log-record.schema.json` in `avf-contracts` and `R14_PLATFORM_OBSERVABILITY.md`:
     ```json
     {
       "$schema": "https://json-schema.org/draft/2020-12/schema",
       "$id": "https://avf.local/contracts/log-record/1.0",
       "title": "AVFStructuredLogRecord",
       "type": "object",
       "required": [
         "timestamp",
         "severity",
         "service_name",
         "service_version",
         "message",
         "trace_id"
       ],
       "properties": {
         "timestamp": { "type": "string", "format": "date-time" },
         "severity": { "type": "string", "enum": ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] },
         "service_name": { "type": "string" },
         "service_version": { "type": "string" },
         "environment": { "type": "string" },
         "trace_id": { "type": "string" },
         "span_id": { "type": "string" },
         "workflow_run_id": { "type": ["string", "null"] },
         "project_id": { "type": ["string", "null"] },
         "shot_id": { "type": ["string", "null"] },
         "generation_job_id": { "type": ["string", "null"] },
         "attempt_id": { "type": ["string", "null"] },
         "message": { "type": "string" },
         "error": {
           "type": "object",
           "properties": {
             "type": { "type": "string" },
             "message": { "type": "string" },
             "stack_trace": { "type": "string" },
             "code": { "type": "string" }
           }
         },
         "context": { "type": "object", "additionalProperties": true }
       },
       "additionalProperties": false
     }
     ```
  2. **Mandatory Redaction Middleware**: Implement a core logging interceptor in `R14` that executes before any log line is emitted. The interceptor must recursively sanitize all dictionary keys matching:
     - `(?i)(token|cookie|secret|password|auth|authorization|bearer|api[_-]?key|session[_-]?id|credit_card)`
     and mask string values with `"[REDACTED]"`.
  3. **Pattern-based String Scrubber**: Regex scrub all log message strings for:
     - Bearer tokens: `Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*`
     - Google session cookies: `SID=[^;\s]+|SSID=[^;\s]+|HSID=[^;\s]+`
- **ALTERNATIVES_CONSIDERED**: 
  - *Rely on developer discipline to not log secrets*: Discarded as unsafe and prone to human error.
  - *Use log shipper regex masking*: Adopted as defense-in-depth, but in-process scrubbing at source is mandatory to prevent secrets from ever hitting container stdout or disk.
- **CAPABILITY_IMPACT**: Eliminates secret leakage in logs and enables unified log aggregation, filtering, and cross-service correlation in OpenSearch/Grafana Loki.
- **COMPATIBILITY_IMPACT**: Non-breaking; standardizes logging formats across all services and workers.
- **MIGRATION_IMPACT**: Integrate the logging utility package from `avf-platform-observability` into all repository templates.
- **TEST_OR_BENCHMARK_REQUIRED**: Unit tests asserting that strings and dictionaries with secrets, cookies, and tokens are 100% replaced by `[REDACTED]` before output.
- **RESIDUAL_RISK**: Low. Standard regex and key-matching log formatters have negligible CPU overhead (<1ms per batch).
- **CONFIDENCE**: HIGH (Addresses critical security requirement `REQ-050` and logging ownership in `REQ-014`).
```

```markdown
### FINDING_ID: F-R11-006
- **ROLE**: R11_PLATFORM
- **SEVERITY**: HIGH
- **CATEGORY**: OPERATIONS / RELIABILITY
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
  - `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (GAP-008)
- **AFFECTED_CONTRACTS**: 
  - `browser-command.schema.json`
  - `R14_PLATFORM_OBSERVABILITY.md`
- **EVIDENCE**: 
  `R14_PLATFORM_OBSERVABILITY.md` (line 19) states ownership of "health/readiness conventions", `R09_BROWSER_WORKER.md` (line 18) mentions "browser heartbeat/lease", and `R10_FLOWKIT_BRIDGE.md` (line 14) mentions "FlowKit process health adapter". However, no concrete health probe protocol (Liveness, Readiness, Startup), heartbeat interval, lease acquisition/renewal TTL, or supervisor process watchdog contract is defined.
- **FAILURE_SCENARIO**: 
  1. A containerized service starts up and takes 25 seconds to establish its database connection. Kubernetes/Docker sends traffic immediately because no `/ready` endpoint is configured, resulting in 502/503 errors during deployments.
  2. In Track A, the Chrome MV3 background extension crashes silently while handling a long video generation wait. The upstream adapter continues waiting for 10 minutes without realizing the connection died.
  3. In Track B, FlowKit runs as a background process; when it experiences an uncaught Python exception or unhandled promise rejection, the process enters a zombie state (PID alive, port unreachable). The bridge does not detect the freeze and commands time out indefinitely.
- **WHY_IT_MATTERS**: 
  Container orchestrators and workflow engines depend on reliable health probes and heartbeat leases to detect deadlocks, restart crashed workers, and safely route traffic.
- **PROPOSED_SOLUTION**: 
  Establish the Operational Health, Lease, and Process Supervision Protocol:
  
  #### 1. Standard HTTP Service Health Probes
  Every HTTP service (`avf-core-state`, `avf-operator-console`, etc.) MUST expose:
  - `GET /health/live`: Returns `200 {"status":"UP"}` if the process event loop is responsive.
  - `GET /health/ready`: Returns `200 {"status":"READY"}` if dependent resources (PostgreSQL, object store, Temporal broker) are reachable and migrations are complete; returns `503 {"status":"NOT_READY", "reason":"..."}` otherwise.
  - `GET /health/startup`: Returns `200` once initial bootstrap and warmup are completed.

  #### 2. Worker Heartbeat & Execution Lease Protocol (Track A Browser Worker)
  - **Heartbeat Interval**: Worker sends a heartbeat ping every `5 seconds` over WebSocket/Native Messaging.
  - **Missed Heartbeat Threshold**: If `3 consecutive heartbeats (15s)` are missed, the adapter marks the worker as `DISCONNECTED` and aborts active pending commands with error class `WORKER_DISCONNECTED`.
  - **Execution Lease**:
    - When a command is dispatched, the worker acquires an execution lease with a `30-second TTL`.
    - The worker MUST renew the lease every `10 seconds` while the command is actively executing (e.g. during prompt submission or file upload).
    - If the lease expires without renewal, the supervisor immediately marks the task failed and initiates process recycling.

  #### 3. Subprocess Supervisor Watchdog Protocol (Track B FlowKit Bridge / Local Daemons)
  - The bridge supervisor manages FlowKit as a supervised child process:
    - Periodically pings FlowKit's local IPC/HTTP endpoint every `5 seconds` with a `2-second deadline`.
    - Captures stdout/stderr into circular in-memory buffer (last 500 lines) for crash diagnosis.
    - If FlowKit is non-responsive for `15 seconds`: Send `SIGTERM`, wait `5 seconds` grace period, escalate to `SIGKILL`, clean up orphaned temporary profile locks, and restart the process.
- **ALTERNATIVES_CONSIDERED**: 
  - *Rely solely on global workflow timeouts (e.g. 15 minutes)*: Rejected because waiting 15 minutes for a crashed worker destroys operational throughput and user experience.
  - *Run FlowKit unmanaged on host*: Rejected because unmanaged external processes cannot guarantee auto-recovery or deterministic state clearing.
- **CAPABILITY_IMPACT**: Fully resolves worker crash detection and recovery (`INV-019`), prevents zombie process hangs, and enables zero-downtime container rollouts.
- **COMPATIBILITY_IMPACT**: Non-breaking; defines runtime operational endpoints and internal heartbeat mechanics.
- **MIGRATION_IMPACT**: Implement health routes in HTTP services and watchdog classes in `avf-browser-worker` and `avf-flowkit-bridge`.
- **TEST_OR_BENCHMARK_REQUIRED**: Chaos integration test that terminates the Chrome MV3 process mid-generation and verifies that the adapter detects the disconnect within 15 seconds and fails gracefully without database corruption.
- **RESIDUAL_RISK**: Low. Standard watchdog and heartbeat algorithms.
- **CONFIDENCE**: HIGH (Essential operational reliability requirement).
```

```markdown
### FINDING_ID: F-R11-007
- **ROLE**: R11_PLATFORM
- **SEVERITY**: HIGH
- **CATEGORY**: PLATFORM / DATA INTEGRITY
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/TEST_STRATEGY.md`
- **AFFECTED_CONTRACTS**: 
  - `R14_PLATFORM_OBSERVABILITY.md`
  - `R02_CORE_STATE.md`
- **EVIDENCE**: 
  `R14_PLATFORM_OBSERVABILITY.md` (lines 18, 81, 98) references "backup/runbook templates" and "backup restore drill scripts", but does not specify Recovery Point Objective (RPO), Recovery Time Objective (RTO), backup mechanisms (WAL archiving vs snapshots), or automated restore validation procedures for the canonical PostgreSQL database and object storage.
- **FAILURE_SCENARIO**: 
  A production database storage volume is corrupted or accidentally dropped. The operations team attempts to restore from an ad-hoc daily `pg_dump` backup file. The restore takes 3.5 hours (exceeding operational tolerance), and when completed, all project metadata, shot versions, prompt revisions, take approvals, and audit records generated during the previous 14 hours are unrecoverable. Furthermore, references in the restored database point to media asset checksums in object storage that were deleted or modified, breaking system invariant `INV-001` and `INV-006`.
- **WHY_IT_MATTERS**: 
  Canonical project and shot history is the core asset of the video factory. Without a verified continuous backup and disaster recovery specification, data loss during infrastructure outages is inevitable.
- **PROPOSED_SOLUTION**: 
  Formally define the Backup, Recovery, and Disaster Recovery Standard in `R14_PLATFORM_OBSERVABILITY.md`:
  
  #### 1. Target Objectives
  - **Recovery Point Objective (RPO)**: `<= 15 minutes` (Maximum allowable data loss).
  - **Recovery Time Objective (RTO)**: `<= 60 minutes` (Maximum allowable downtime for full state restoration).

  #### 2. PostgreSQL Database Backup Architecture
  - **Continuous WAL Archiving**: Enable PostgreSQL Write-Ahead Log (WAL) archiving to S3/MinIO using `pgBackRest` or `WAL-G` with `archive_timeout = 300` (5 minutes). This ensures point-in-time recovery (PITR) up to the last 5 minutes.
  - **Full Base Backups**: Automated daily full base backup taken during off-peak hours, retained for `30 days`.
  - **Retention Policy**:
    - Full backups: 30 days.
    - WAL archives: 7 days continuous PITR window.
    - Monthly archive snapshots: Retained for 1 year.

  #### 3. Object Storage Asset Backup
  - Source assets, references, and approved takes in S3/MinIO must have **Object Versioning** enabled.
  - Lifecycle rules set to transition non-current asset versions to cold/archive storage after 30 days.

  #### 4. Automated Disaster Recovery Drills (CI / Integration Harness)
  - Define an automated restore verification script in `R15_INTEGRATION_HARNESS` (`scripts/dr-drill.sh`):
    1. Spin up an isolated ephemeral PostgreSQL container.
    2. Download the latest base backup and WAL archives from test storage.
    3. Perform PITR recovery to a specific timestamp.
    4. Run `avf-core-state` verification suite asserting table integrity, foreign keys, and constraint validity.
    5. Terminate the drill and publish an automated drill report (`backup_verification_status`).
- **ALTERNATIVES_CONSIDERED**: 
  - *Nightly `pg_dump` only*: Rejected because a 24-hour RPO causes unacceptable production data loss.
  - *Synchronous multi-region database replication*: Overkill and cost-prohibitive for MVP; continuous WAL archiving to S3 achieves <=15m RPO at minimal operational complexity.
- **CAPABILITY_IMPACT**: Guarantees non-destructive data recovery, achieves <=15 min RPO and <=60 min RTO, and ensures verifiable continuity for all canonical video assets.
- **COMPATIBILITY_IMPACT**: Zero breaking changes to application code or contracts.
- **MIGRATION_IMPACT**: Add PostgreSQL backup configuration templates and restore drill scripts to `avf-platform-observability` and `avf-integration-harness`.
- **TEST_OR_BENCHMARK_REQUIRED**: Automated DR restore drill script executing successfully in CI / staging environment.
- **RESIDUAL_RISK**: Low. Standard enterprise database operations architecture.
- **CONFIDENCE**: HIGH (Essential operational standard protecting business data assets).
```

```markdown
### FINDING_ID: F-R11-008
- **ROLE**: R11_PLATFORM
- **SEVERITY**: MEDIUM
- **CATEGORY**: PLATFORM / CONFIGURATION
- **AFFECTED_FILES**: 
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`
  - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/LOCAL_DEVELOPMENT.md`
- **AFFECTED_CONTRACTS**: 
  - `R14_PLATFORM_OBSERVABILITY.md`
  - `SECURITY_MODEL.md`
- **EVIDENCE**: 
  `R14_PLATFORM_OBSERVABILITY.md` (line 17) owns "secret/config templates", `SECURITY_MODEL.md` (lines 62-65) describes development vs production secret handling, and `LOCAL_DEVELOPMENT.md` lists compose profiles. However, there is no standardized environment variable naming convention, configuration validation schema, or release manifest credential guardrail.
- **FAILURE_SCENARIO**: 
  A developer or AI coding agent configures database connection strings using `DB_URL` in `avf-core-state`, `DATABASE_URL` in `avf-workflow`, and `POSTGRES_CONNECTION_STRING` in `avf-media`. In production deployment, configuration drift occurs, services fail to read credentials, or worse, an agent commits a hardcoded default API token into `release-manifest.json` or a local `.env.example` file that is deployed to a staging environment.
- **WHY_IT_MATTERS**: 
  Configuration fragmentation and secret mishandling are leading causes of deployment failures and security breaches across multi-repository architectures.
- **PROPOSED_SOLUTION**: 
  Standardize the Configuration, Secrets, and Manifest Validation Framework in `R14_PLATFORM_OBSERVABILITY.md`:
  
  #### 1. Unified Environment Variable Namespace (`AVF_*`)
  All configuration keys MUST follow the unified uppercase snake_case prefix `AVF_<SUBSYSTEM>_<KEY>`:
  - Database: `AVF_CORE_DB_HOST`, `AVF_CORE_DB_PORT`, `AVF_CORE_DB_NAME`, `AVF_CORE_DB_USER`, `AVF_CORE_DB_PASSWORD` (or `AVF_CORE_DATABASE_URL`).
  - Object Storage: `AVF_STORAGE_ENDPOINT`, `AVF_STORAGE_BUCKET_MEDIA`, `AVF_STORAGE_BUCKET_DIAGNOSTICS`, `AVF_STORAGE_ACCESS_KEY`, `AVF_STORAGE_SECRET_KEY`.
  - Workflow: `AVF_WORKFLOW_TEMPORAL_HOST`, `AVF_WORKFLOW_TEMPORAL_NAMESPACE`.
  - Telemetry: `AVF_OTEL_EXPORTER_OTLP_ENDPOINT`, `AVF_OTEL_SERVICE_NAME`, `AVF_LOG_LEVEL`.
  - Browser Worker: `AVF_BROWSER_WS_PORT`, `AVF_BROWSER_WS_SECRET`, `AVF_BROWSER_HEADLESS`.

  #### 2. Strict Configuration Schema Validation on Startup
  Every service repository must implement strict startup environment validation using Pydantic Settings (Python) or Zod / Envalid (Node.js/TypeScript). If any required variable is missing or malformed, the process MUST exit immediately with exit code `1` and log a structured fatal error detailing the invalid property (without printing secret values).

  #### 3. Release Manifest Secret Scanner CI Gate
  Add an automated static analysis check to `avf-integration-harness` (`tests/security/test_manifest_secrets.py`) that scans `release-manifest.json`, docker-compose files, and commit diffs using regex rules (e.g. `gitleaks` / `trufflehog`) to block any unredacted tokens, private keys, or passwords from ever being merged.
- **ALTERNATIVES_CONSIDERED**: 
  - *Allow arbitrary environment variable names*: Rejected because cross-service Docker Compose profiles and Helm charts become unmaintainable.
  - *Use a centralized dynamic config server (e.g. Consul/ZooKeeper)*: Overkill for MVP; standard 12-factor environment variables with strict local schema validation provide optimal simplicity and reliability.
- **CAPABILITY_IMPACT**: Eliminates configuration drift, standardizes local and production deployments, and prevents accidental credential leakage.
- **COMPATIBILITY_IMPACT**: Non-breaking standard across all repositories.
- **MIGRATION_IMPACT**: Provide standard `.env.template` files and configuration schema classes in `avf-platform-observability`.
- **TEST_OR_BENCHMARK_REQUIRED**: Startup unit tests asserting that missing required `AVF_*` variables fail fast with clear validation diagnostics.
- **RESIDUAL_RISK**: Low. Standard 12-factor app architecture.
- **CONFIDENCE**: HIGH (Essential software engineering and operational hygiene).
```

---

## 5. Detailed Resolution of Assigned Gap Seeds

### 5.1 GAP-006: Diagnostic Screenshot Storage, Format, Encryption, and Retention Lifecycle Policy
- **Inspected Sources**: `04_integration/SECURITY_MODEL.md` (lines 11, 38), `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` (lines 80, 87), `03_repo_blueprints/R09_BROWSER_WORKER.md` (lines 17, 37, 93).
- **Core Defect**: The specification states that diagnostic screenshot retention is "configurable and access-controlled" but defines no concrete storage path, encryption standard, retention period, or redaction rules, leading to unbounded storage consumption and risk of Google account PII leakage.
- **Formal Resolution**:
  1. **Storage Location**: Dedicated S3 bucket `s3://${AVF_DIAGNOSTICS_BUCKET}/diagnostics/projects/{project_id}/jobs/{generation_job_id}/{command_id}_{timestamp}_{error_class}.png` with companion JSON metadata file.
  2. **Encryption**: Mandatory Server-Side Encryption (`SSE-S3` or `SSE-KMS` AES-256-GCM).
  3. **Retention Policy**:
     - Success commands: Purged immediately (0-day retention).
     - Transient failure retries: 24-hour retention via automated S3 lifecycle rule.
     - Hard failure / Security challenge / Human escalation: 7-day retention (`Expiration: Days: 7`), automatically deleted thereafter unless flagged as `pinned_for_incident`.
  4. **Source Redaction**: Browser extension/worker captures must apply coordinate bounding-box black-fill masking over Google account header elements (email, avatar) or capture only the generation canvas element.
  5. **Access Control**: Signed URLs only, restricted to `OPERATOR` role with a maximum TTL of 15 minutes.
- **Status**: **RESOLVED** (Incorporated into Finding `F-R11-002`).

### 5.2 GAP-009: OpenTelemetry Metric Naming Standards, Prometheus Exposition, and SLI/SLO Catalog
- **Inspected Sources**: `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` (lines 13-16, 68-75), `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (line 13).
- **Core Defect**: `R14_PLATFORM_OBSERVABILITY.md` asserts ownership over metrics naming but specifies zero canonical metric names, metric types, units, histogram buckets, or label constraints.
- **Formal Resolution**:
  1. **Namespace**: Standardized `avf.<subsystem>.<entity>.<property>_<unit>` for OpenTelemetry, exporting as `avf_<subsystem>_<entity>_<property>_<unit>` for Prometheus.
  2. **Canonical Metric Catalog**: Published full normative table (see Finding `F-R11-003`) covering generation duration, queue wait time, active jobs, provider requests, browser worker status, outbox lag/events, media transcoding, and QC evaluation.
  3. **Histogram Boundaries**: Explicit bucket distributions for long-running video operations (`[0.5, 1, 2.5, 5, 10, 15, 30, 60, 90, 120, 180, 300, 600]` seconds) and sub-second internal services.
  4. **Cardinality Constraints**: Strictly prohibited UUIDs and dynamic prompt/error text from metric labels; mandated the use of OpenTelemetry Exemplars to attach `trace_id`s to histogram samples.
  5. **Target SLIs/SLOs**:
     - *Generation Availability SLO*: 99.0% of valid generation requests complete without system/platform errors.
     - *Generation Latency SLI*: 95% of single-shot text-to-video generations complete within 90 seconds (measured via `avf.generation.job.duration_seconds`).
     - *Outbox Freshness SLI*: 99.9% of outbox events published within 1.0 second (`avf.outbox.lag_seconds <= 1.0`).
- **Status**: **RESOLVED** (Incorporated into Finding `F-R11-003`).

---

## 6. Residual Uncertainties & Recommended Spikes

While the platform and observability architecture is fundamentally sound, two technical areas require experimental spikes during Phase 0 to confirm runtime performance characteristics:

1. **Spike 1: Chrome MV3 TraceContext Propagation Overhead**:
   - *Question*: Does injecting and extracting W3C `traceparent` headers across Chrome MV3 Native Messaging / WebSocket frames introduce any measurable latency or serialization issues in high-frequency DOM polling loops?
   - *Classification*: Uncertainty needing a spike (Non-blocking for specification freeze).
   - *Recommended Spike*: Build a lightweight prototype in `avf-browser-worker` sending 1,000 W3C-instrumented commands over loopback WebSocket to verify latency overhead is <0.5ms.

2. **Spike 2: High-Throughput PostgreSQL Outbox Polling vs LISTEN/NOTIFY Benchmark**:
   - *Question*: Under 100 concurrent shot generation workflows, what is the CPU and lock contention difference between polling `outbox_events` with `FOR UPDATE SKIP LOCKED` at 500ms intervals versus using PostgreSQL `LISTEN/NOTIFY` triggers?
   - *Classification*: Performance optimization spike (Non-blocking; `FOR UPDATE SKIP LOCKED` is guaranteed correct).
   - *Recommended Spike*: Execute a 10,000-event benchmark in `R15_INTEGRATION_HARNESS` comparing throughput and database connection pool utilization.

---

## 7. Reviewer Sign-Off & Attestation

- **Reviewer Role**: R11_PLATFORM (Platform / Observability / Operations Architect)
- **Model / Reasoning Mode**: Advanced Agentic Reasoning Mode
- **Skill Versions / Hashes**:
  - `modern-web-guidance`: v1.0.0
  - `a11y-debugging`: v1.0.0
  - `chrome-devtools`: v1.0.0
- **Session ID**: `f8d7a075-c083-4eb0-ae7c-7c4ac2473faa`
- **Timestamp**: 2026-08-15T11:30:00+07:00
- **Independent Attestation**: I attest that this review was conducted completely independently without inspecting other reviewers' raw submissions. All findings are backed by direct source inspection, rigorous architectural failure scenarios, concrete schema proposals, and full resolution of assigned gap seeds.

*(Signed)* **R11_PLATFORM**
