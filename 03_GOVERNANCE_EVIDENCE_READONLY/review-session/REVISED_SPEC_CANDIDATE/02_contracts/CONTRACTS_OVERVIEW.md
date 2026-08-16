# Contracts Overview

`avf-contracts` is the most important repository to freeze first.

## Contract families

1. Domain identity/reference schemas.
2. Commands and command results.
3. Events and event envelope.
4. Provider request/result/status.
5. Flow execution commands/results.
6. Error taxonomy.
7. Observability/correlation context.
8. Cost/usage records.

## Ownership

Contracts define exchanged data, not internal database table layouts.

## Common envelope

```json
{
  "schema_version": "1.0",
  "message_id": "uuid",
  "occurred_at": "RFC3339",
  "trace_id": "uuid-or-w3c-trace-id",
  "workflow_run_id": "uuid",
  "project_id": "uuid",
  "type": "GenerationRequested",
  "payload": {}
}
```

## Forward compatibility

- Consumers ignore unknown optional fields.
- Consumers reject unknown major schema versions.
- Enum growth is permitted only for fields explicitly marked extensible; otherwise use string codes and documented fallback.
- Producers never repurpose a field with new semantics.

## Error taxonomy

Top-level classes:

- `VALIDATION_ERROR`
- `CONFLICT`
- `NOT_FOUND`
- `TRANSIENT_TRANSPORT`
- `TRANSIENT_BROWSER`
- `PROVIDER_RATE_LIMIT`
- `PROVIDER_REJECTED`
- `AUTH_REQUIRED`
- `SECURITY_CHALLENGE`
- `UI_CHANGED`
- `BUDGET_EXHAUSTED`
- `QC_REJECTED`
- `UNSUPPORTED_CAPABILITY`
- `INTERNAL_ERROR`

Errors may contain provider-specific detail under `details.provider`, but retry logic keys off normalized error class.
