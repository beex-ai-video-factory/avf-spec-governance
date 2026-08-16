# C02R HEARING TRANSCRIPT: CLUSTER 05 — EVENT ENVELOPE & CATALOG NAMING STANDARDS
**CLUSTER_ID:** CLUSTER-05
**FINDINGS_COVERED:** FINDING_006, FINDING_023, FINDING_054, TECH-007
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R04 (Contracts Specialist) & R11 (Platform Specialist)
- **Position:** There is an active conflict between `CONTRACTS_OVERVIEW.md` (which documented envelope fields like `message_id`, `occurred_at`, `trace_id`, `project_id`), `event-envelope.schema.json` (which required `event_id`, `aggregate_id`, `aggregate_version`, `correlation_id`, `timestamp_utc`), and `COMMAND_EVENT_CATALOG.md` (which used PascalCase event names like `ProjectCreated`, `GenerationJobCreated` that failed the schema's dotted lowercase regex `^[a-z0-9_]+(\.[a-z0-9_]+)+$`). We must establish one canonical event envelope schema and consistent event naming across all documents and code blueprints.
- **Evidence:** `CONTRACTS_OVERVIEW.md` vs `event-envelope.schema.json` vs `COMMAND_EVENT_CATALOG.md`.
- **Failure Scenario:** Event producers publish `GenerationJobCreated` matching the catalog. The event bus validator validates against `event-envelope.schema.json` and rejects all events because `GenerationJobCreated` fails the lowercase dot-separated regex, halting the entire event pipeline.

## 2. Challenger Attack
- **Challenger:** R14 (Observability Specialist) & R15 (Red Team Specialist)
- **Attack Vector:**
  1. *Distributed Tracing Context:* Does the schema support OpenTelemetry trace headers (`trace_id`, `span_id`, `baggage`)? If not, cross-service distributed tracing across 15 repos is broken.
  2. *Event Naming Convention:* Dotted lowercase (e.g. `avf.generation.job_created`) is standard in Kafka/RabbitMQ topic routing, whereas PascalCase (e.g. `GenerationJobCreated`) is standard in TypeScript domain models. Which is canonical?

## 3. Domain Owner Review
- **Domain Owner:** R11 (Platform Specialist)
- **Evaluation:**
  - Topic/Routing event type MUST be lowercase dotted with domain prefix: `avf.<domain>.<entity>_<action>` (e.g. `avf.core.project_created`, `avf.generation.job_submitted`, `avf.qc.completed`).
  - The envelope must explicitly support OpenTelemetry distributed tracing: `trace_id` (UUID or 32-hex string) and `span_id` alongside `correlation_id`, `workflow_run_id`, `aggregate_id`, `aggregate_version`, `event_id`, and `timestamp_utc`.
  - In TypeScript code, PascalCase class names map directly to the canonical dotted event string constant: `export class GenerationJobCreatedEvent { static readonly EVENT_TYPE = "avf.generation.job_created"; }`.

## 4. Proponent Response
- **Response:**
  - We update `event-envelope.schema.json` to include `trace_id`, `span_id`, `correlation_id`, `workflow_run_id`, `aggregate_id`, `aggregate_version`, `timestamp_utc`, `event_id`, `event_type`, `schema_version`, and `payload`.
  - We update `COMMAND_EVENT_CATALOG.md` and `CONTRACTS_OVERVIEW.md` to list both the canonical dotted string and the TypeScript event class name.
  - The regex in `event-envelope.schema.json` will strictly match `^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$`.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Allow arbitrary unconstrained string for `event_type`.
- **Why Rejected:** Unconstrained event types lead to event bus routing chaos, unmonitored dead-letter queues, and inability to automate event schema registry checks.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-005 amended to:
  1. Update `event-envelope.schema.json` with OTel tracing fields and canonical regex.
  2. Synchronize `COMMAND_EVENT_CATALOG.md` and `CONTRACTS_OVERVIEW.md`.
  3. Add event schema conformance test with valid and invalid event fixtures.
