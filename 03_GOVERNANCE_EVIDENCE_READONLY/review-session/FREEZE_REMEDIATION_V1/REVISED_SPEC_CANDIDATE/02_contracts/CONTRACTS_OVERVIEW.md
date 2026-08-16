# CONTRACTS OVERVIEW
## AI Video Factory — Inter-Repository Contract Standards
**VERSION:** 1.0.0

---

## 1. Contract Inventory
All inter-repository contracts in AVF are defined as JSON Schema draft-07 packages and exported as strongly-typed TypeScript definitions from `R01_CONTRACTS`.

1. `domain-entities.schema.json`: Canonical data model entities (`Project`, `Shot`, `ShotVersion`, `PromptVersion`, `GenerationJob`, `Take`, `AssetVersion`, `CharacterVersion`, `StyleVersion`).
2. `browser-command.schema.json`: FlowExecutionPort discriminated commands for all 10 operations.
3. `flow-execution-result.schema.json`: FlowExecutionPort discriminated results and errors.
4. `provider-request.schema.json`: Generic video generation request payload.
5. `provider-result.schema.json`: Multi-tier provider response with normalized error taxonomy.
6. `event-envelope.schema.json`: Common distributed event envelope with OpenTelemetry tracing headers.

---

## 2. Schema Packaging & Fragment Entrypoint Conventions
`domain-entities.schema.json` is a modular schema library containing entity definitions under ``. Consumers reference specific entity schemas using fragment entrypoints:
- `domain-entities.schema.json#//Project`
- `domain-entities.schema.json#//ShotVersion`
- `domain-entities.schema.json#//PromptVersion`
- `domain-entities.schema.json#//GenerationJob`
- `domain-entities.schema.json#//Take`
- `domain-entities.schema.json#//AssetVersion`

---

## 3. Normalized Error Taxonomy
Provider and browser worker errors must be mapped to one of the 9 standard error codes:
- `PROVIDER_RATE_LIMIT` (Retry: `TRANSIENT`, backoff required)
- `AUTH_REQUIRED` (Retry: `POLICY_BLOCKED`, human operator login required)
- `SECURITY_CHALLENGE` (Retry: `POLICY_BLOCKED`, CAPTCHA challenge pause)
- `UI_CHANGED` (Retry: `PERMANENT`, DOM automation selector failure)
- `BUDGET_EXHAUSTED` (Retry: `RESOURCE_EXHAUSTED`, credit quota exceeded)
- `UNSUPPORTED_CAPABILITY` (Retry: `PERMANENT`, requested resolution/aspect ratio not supported)
- `NETWORK_TIMEOUT` (Retry: `TRANSIENT`, socket/HTTP timeout)
- `BAD_REQUEST` (Retry: `PERMANENT`, validation failure on submitted prompt/parameters)
- `PROVIDER_INTERNAL_ERROR` (Retry: `TRANSIENT`, 500 error from AI engine)

---

## 4. Distributed Event Envelope Standards
All events published to message buses must conform to `event-envelope.schema.json`:
- `event_type`: Must match `^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$` (e.g. `avf.generation.job_created`).
- `trace_id` & `span_id`: Propagate OpenTelemetry distributed trace context.
- `correlation_id`: Root request UUID.
- `aggregate_id` & `aggregate_version`: Concurrency fencing for event sourcing.
