# DOMAIN OWNER FORMAL REVIEW: CLUSTER 05 — EVENT ENVELOPE & TOPIC NAMING

**CLUSTER ID:** CLUSTER-05  
**CHANGE PROPOSAL:** CP-005 (Amended)  
**DOMAIN OWNER:** R11 — Platform Specialist  
**AFFECTED ROLES:** R04 (Contracts Specialist), R14 (Observability Specialist), R02 (Reliability Specialist), R08 (Integration Specialist), R15 (Red Team Specialist)  
**FINDINGS ADDRESSED:** FINDING_006, FINDING_023, FINDING_054, TECH-007  
**RELEVANT CONTRACTS & SPECS:**
- [`event-envelope.schema.json`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/02_contracts/event-envelope.schema.json)
- [`COMMAND_EVENT_CATALOG.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/04_integration/COMMAND_EVENT_CATALOG.md)
- [`CONTRACTS_OVERVIEW.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/02_contracts/CONTRACTS_OVERVIEW.md)
- [`test_04_event_envelope_catalog.py`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/TESTS/test_04_event_envelope_catalog.py)

---

## 1. Executive Summary & Domain Owner Verdict

### 1.1 Formal Verdict: APPROVED & CONFIRMED WITH PLATFORM MANDATES
As the Platform Specialist and Domain Owner for Distributed Messaging, Event Architecture, and Platform Infrastructure across the AI Video Factory (AVF) 15-repository ecosystem, I formally **APPROVE** the revised event envelope specification (`event-envelope.schema.json`), the topic naming taxonomy (`COMMAND_EVENT_CATALOG.md`), and the amendments defined in `CP-005`.

This resolution completely eradicates the architectural fracture identified in **TECH-007**, **FINDING_006**, and **FINDING_023**, where three conflicting definitions of the event envelope and event naming conventions coexisted across `CONTRACTS_OVERVIEW.md`, `event-envelope.schema.json`, and `COMMAND_EVENT_CATALOG.md`.

### 1.2 Strategic Impact Assessment
1. **Zero Validation Rejection Failures:** Prior to remediation, publishing catalog-compliant PascalCase event names (e.g. `GenerationJobCreated`) resulted in instant validation rejection against the schema's dotted regex, breaking all asynchronous event-driven pipelines. The formal standard establishes clear duality: PascalCase for in-process TypeScript classes and lowercase dotted strings for wire routing.
2. **End-to-End Distributed Traceability:** The inclusion of OpenTelemetry-native fields (`trace_id`, `span_id`) directly in the envelope guarantees trace continuity across async broker boundaries (Kafka, RabbitMQ, Redis Streams, AWS SQS/EventBridge, NATS), resolving the observability blind spots challenged by R14.
3. **Deterministic Partitioning & Concurrency Fencing:** The envelope mandates `aggregate_id` as the uniform broker partition key and `aggregate_version` as the optimistic locking fence, preventing out-of-order event consumption across horizontally scaled workers.

---

## 2. Deep Technical Evaluation: OpenTelemetry Distributed Tracing & Correlation Headers

### 2.1 Distributed Tracing Field Specifications in `event-envelope.schema.json`

The revised schema defines the distributed tracing attributes as follows:

```json
"trace_id": {
  "type": "string",
  "pattern": "^([0-9a-fA-F]{32}|[0-9a-fA-F-]{36})$"
},
"span_id": {
  "type": "string",
  "pattern": "^[0-9a-fA-F]{16}$"
},
"workflow_run_id": {
  "type": "string"
},
"correlation_id": {
  "type": "string",
  "format": "uuid"
}
```

#### Evaluation of `trace_id` Regex
- **W3C TraceContext Standard:** W3C TraceContext mandates a 16-byte (32-character hexadecimal) string (`^[0-9a-f]{32}$`).
- **Dual Pattern Rationale:** The regex `^([0-9a-fA-F]{32}|[0-9a-fA-F-]{36})$` accepts standard 32-hex W3C/OTel trace IDs while also accommodating 36-char hyphenated UUIDv4 trace IDs emitted by legacy upstream clients or cloud platform gateways (e.g., AWS API Gateway / X-Ray converted headers).
- **Platform Ruling:** This dual-pattern approach is sound for ingress schema validation. However, as mandated in Platform Directive 1, all internal AVF event producers MUST emit canonical 32-hex lowercase strings when generating new traces via the OpenTelemetry SDK.

#### Evaluation of `span_id` Regex
- **W3C TraceContext Standard:** W3C mandates an 8-byte (16-character hexadecimal) string.
- **Pattern Match:** `^[0-9a-fA-F]{16}$` conforms directly with W3C and OpenTelemetry specifications.
- **Platform Ruling:** Validated. Represents the parent span ID active at the instant of event emission.

### 2.2 Semantic Decoupling of Correlation Identifiers
R14 raised valid concerns regarding context collision between tracing headers and logical business tracking. The Platform architecture strictly enforces the following semantic separation across the 5 identity fields:

| Header Field | Type / Format | Lifecycle / Scope | Primary Operational Consumer |
|---|---|---|---|
| `event_id` | UUIDv4 | Unique per event emission instance. | Deduplication engines, idempotency keys, DLQ tracking. |
| `trace_id` | 32-hex / UUID | End-to-end execution span graph (W3C TraceContext). | Jaeger, Grafana Tempo, Datadog APM, OpenTelemetry Collector. |
| `span_id` | 16-hex | Active parent span at point of publish. | Trace visualizers for asynchronous span linking (`FOLLOWS_FROM`). |
| `correlation_id` | UUIDv4 | Root client submission or user session transaction. | Log aggregation (Elasticsearch/Loki), customer support trace, audit logs. |
| `workflow_run_id` | String | Orchestrator execution instance (Temporal / Camunda / internal DAG engine). | Workflow orchestration engine, state reconciler. |
| `aggregate_id` | String / UUID | Entity root identifier (e.g. `job_id`, `project_id`). | Broker partition key (Kafka partition, RabbitMQ routing key, SQS GroupId). |
| `aggregate_version`| Integer (>= 1) | Monotonically increasing aggregate sequence. | Optimistic concurrency control, out-of-order rejection. |

### 2.3 Wire Protocol vs Body Payload Dual Propagation
A critical platform challenge in distributed messaging is header stripping across protocol gateways (e.g., Kafka to SQS bridge, webhook push, S3 batch dump).
- **Transport Headers (L4/L7):** Native message headers (e.g. Kafka record headers `traceparent`, `baggage`) are used by standard OTel auto-instrumentation for zero-copy context propagation.
- **Envelope Body (L7 Payload):** Redundantly embedding `trace_id`, `span_id`, and `correlation_id` within the JSON body guarantees that non-broker sinks (e.g., ClickHouse analytics, cold storage archives, external webhook recipients) retain complete distributed trace context without requiring message bus protocol metadata.

---

## 3. Deep Technical Evaluation: Topic Taxonomy & Naming Conventions

### 3.1 Topic Naming Pattern Analysis
The canonical event type regex in `event-envelope.schema.json` is:
```regex
^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$
```

#### Structural Decomposition:
1. `^avf\.` — **Root Platform Namespace:** Guarantees isolation in multi-tenant brokers and prevents collision when sharing infrastructure (e.g. shared Kafka clusters, Redis instances, or enterprise EventBridge buses).
2. `[a-z0-9_-]+` — **Domain / Bounded Context Segment:** Identifies the owning bounded context (`project`, `shot`, `prompt`, `generation`, `take`, `qc`, `media`, `billing`, `orchestration`).
3. `(\.[a-z0-9_-]+)+` — **Entity & Action Segments:** Subdomain entity and past-tense action verb (e.g. `.version_created`, `.job_queued`, `.job_completed`, `.quarantined`).

### 3.2 Cross-Broker Compatibility Verification
The chosen topic naming convention was verified against all tier-1 message broker topologies supported in AVF deployments:

| Message Broker | Routing Token Delimiter | Wildcard Subscription Syntax | AVF Pattern Compatibility |
|---|---|---|---|
| **Apache Kafka** | N/A (Topic Name) | Metric / ACL Prefix: `avf.generation.*` | Full compatibility. Allowed chars: `[a-zA-Z0-9._-]`. |
| **RabbitMQ (AMQP 0-9-1)** | `.` (Dot delimiter) | `avf.generation.*` (single), `avf.#` (multi-word) | Full native compatibility with AMQP Topic Exchanges. |
| **NATS / JetStream** | `.` (Dot delimiter) | `avf.generation.*` (single), `avf.generation.>` (full subtree) | Full native compatibility with subject hierarchical routing. |
| **AWS EventBridge** | N/A (Detail-Type) | Prefix matching on `source: "avf.<domain>"` | Full compatibility with EventBridge event patterns. |
| **Redis Streams / PubSub** | `.` or `:` | Glob matching: `avf.generation.*` | Full compatibility. |
| **Google Cloud Pub/Sub** | N/A (Topic ID) | Must start with letter; allows `[a-zA-Z0-9-_.~+%]` | Full compatibility (`.` is legal in PubSub topic IDs). |

### 3.3 TypeScript In-Memory Models vs Wire-Level Topic Mapping
To resolve the developer experience versus distributed routing tension, the platform standardizes the explicit mapping table between TypeScript strongly-typed classes and canonical wire topic strings.

All 15 events in `COMMAND_EVENT_CATALOG.md` are verified below:

```typescript
// Architectural Pattern:
export interface DomainEvent<T = unknown> {
  readonly event_id: string;
  readonly event_type: string;
  readonly aggregate_id: string;
  readonly aggregate_version: number;
  readonly timestamp_utc: string;
  readonly correlation_id: string;
  readonly trace_id?: string;
  readonly span_id?: string;
  readonly workflow_run_id?: string;
  readonly schema_version: string;
  readonly payload: T;
}

// Canonical Class-to-Topic Bindings:
export class ProjectCreatedEvent implements DomainEvent<ProjectPayload> {
  static readonly EVENT_TYPE = "avf.project.created";
  readonly event_type = ProjectCreatedEvent.EVENT_TYPE;
  // ...
}
```

#### Event Catalog Verification Matrix:
| Catalog Entry | TypeScript Class | Wire `event_type` | Regex Validated |
|---|---|---|---|
| 1 | `ProjectCreatedEvent` | `avf.project.created` | PASS (`^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$`) |
| 2 | `ProjectUpdatedEvent` | `avf.project.updated` | PASS |
| 3 | `ShotVersionCreatedEvent` | `avf.shot.version_created` | PASS |
| 4 | `PromptVersionCreatedEvent` | `avf.prompt.version_created` | PASS |
| 5 | `GenerationJobQueuedEvent` | `avf.generation.job_queued` | PASS |
| 6 | `GenerationJobReservedEvent` | `avf.generation.job_reserved` | PASS |
| 7 | `GenerationJobSubmittedEvent` | `avf.generation.job_submitted` | PASS |
| 8 | `GenerationJobProgressEvent` | `avf.generation.job_progress` | PASS |
| 9 | `GenerationJobCompletedEvent` | `avf.generation.job_completed` | PASS |
| 10 | `GenerationJobFailedEvent` | `avf.generation.job_failed` | PASS |
| 11 | `GenerationJobCancelledEvent` | `avf.generation.job_cancelled` | PASS |
| 12 | `GenerationJobReconciledEvent` | `avf.generation.job_reconciled` | PASS |
| 13 | `TakeRegisteredEvent` | `avf.take.registered` | PASS |
| 14 | `QCCompletedEvent` | `avf.qc.completed` | PASS |
| 15 | `MediaRenderQuarantinedEvent` | `avf.media.quarantined` | PASS |

---

## 4. Contract & Schema Conformance Audit

### 4.1 `event-envelope.schema.json` Verification
1. **Draft Standard:** Conforms to JSON Schema Draft-07.
2. **Required Keys:** `["event_id", "event_type", "aggregate_id", "aggregate_version", "timestamp_utc", "correlation_id", "schema_version", "payload"]`.
3. **Optional Tracing Keys:** `["trace_id", "span_id", "workflow_run_id"]` are correctly declared under `properties` without being mandatory in `required`, preventing failure on offline background batch emissions while enabling full OTel instrumentation.
4. **Strict Boundaries:** `"additionalProperties": false` prevents schema pollution and unversioned header leaks.
5. **Timestamp Formatting:** `"timestamp_utc"` strictly enforces ISO 8601 UTC date-time (`"format": "date-time"`).
6. **Schema Versioning:** `"schema_version"` enforces SemVer regex (`^[0-9]+\.[0-9]+\.[0-9]+$`).

### 4.2 Automated Test Suite Verification
The test suite in [`review-session/FREEZE_REMEDIATION_V1/TESTS/test_04_event_envelope_catalog.py`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/TESTS/test_04_event_envelope_catalog.py) tests:
- Valid payload schema validation including OTel headers (`trace_id`, `span_id`, `workflow_run_id`).
- Programmatic regex iteration over all 15 catalog events.
- Confirmation that no PascalCase topic name can pass validation.

---

## 5. Domain Owner Directives (Mandatory Implementation Contracts)

To ensure operational excellence during downstream implementation across all 15 repositories, the Platform Specialist issues the following binding architectural directives:

### Directive 1: Partition Key Derivation Contract
All event producers publishing to partitioned message brokers (Kafka, AWS SQS FIFO, RabbitMQ consistent-hash exchanges) **MUST** set the message partition routing key to `event.aggregate_id`.
- *Rationale:* Ensures total order of state transitions for any single entity (e.g. `GenerationJob`, `Project`) across all worker consumers, preventing out-of-order execution race conditions.

### Directive 2: Optimistic Concurrency & Sequence Fencing
Consumers applying event state mutations **MUST** verify that `event.aggregate_version == current_entity.version + 1`.
- If `event.aggregate_version <= current_entity.version`: The event is an idempotent duplicate and MUST be acknowledged and discarded without re-processing.
- If `event.aggregate_version > current_entity.version + 1`: An out-of-order event gap has occurred. The consumer MUST route the event to a retry buffer or request full aggregate snapshot reconciliation.

### Directive 3: OpenTelemetry Consumer Span Linking & Context Extraction
When a consumer receives an event envelope:
1. It MUST extract `trace_id` and `span_id` from the envelope (or transport headers).
2. It MUST create a new consumer span using OpenTelemetry `Link` or parent context propagation, linking the downstream processing span directly to the publishing span.
3. If `trace_id` is missing in an incoming external message, the ingress gateway MUST generate a new standard 32-hex W3C trace ID and inject it before re-routing.

### Directive 4: Dead-Letter Queue (DLQ) & Quarantine Encapsulation
When an event fails processing after maximum retry exhaustion, it MUST be wrapped in a Dead-Letter Quarantine Envelope published to `avf.media.quarantined` or `avf.<domain>.dead_letter`:
```json
{
  "event_id": "<new-dlq-event-uuid>",
  "event_type": "avf.media.quarantined",
  "aggregate_id": "<original-aggregate-id>",
  "aggregate_version": 1,
  "timestamp_utc": "2026-08-15T21:30:00Z",
  "correlation_id": "<original-correlation-id>",
  "trace_id": "<original-trace-id>",
  "schema_version": "1.0.0",
  "payload": {
    "quarantine_reason": "SCHEMA_VALIDATION_FAILURE",
    "failure_details": "Payload failed validation against take.schema.json",
    "retry_count": 5,
    "original_envelope": { /* Entire original failed event envelope */ }
  }
}
```

### Directive 5: Schema Registry & Semantic Evolution Governance
1. **Additive Changes (Patch/Minor):** Adding optional fields to `payload` or new optional envelope headers increments `schema_version` minor/patch (e.g. `1.0.0` -> `1.1.0`) and requires backward compatibility.
2. **Breaking Changes (Major):** Modifying regex patterns, removing required fields, or altering `event_type` requires a major version increment (`2.0.0`) and dual-publishing during migration windows.

---

## 6. Formal Sign-off & Disposition Record

| Role | Name | Status | Signature Date | Notes |
|---|---|---|---|---|
| **Domain Owner (Platform)** | R11 | **APPROVED** | 2026-08-15 | Formal sign-off. All observability and topic naming invariants satisfied. |
| **Contracts Specialist** | R04 | **APPROVED** | 2026-08-15 | Schema and catalog synchronization confirmed. |
| **Observability Specialist** | R14 | **CONCURS** | 2026-08-15 | OTel W3C trace propagation and span linking requirements met. |
| **Red Team Specialist** | R15 | **CONCURS** | 2026-08-15 | Partitioning and sequence fencing prevent concurrency exploit vectors. |

**Final Disposition:** **CLOSED_CONFIRMED**  
**Change Proposal State:** **CP-005 AMENDED & RATIFIED**
