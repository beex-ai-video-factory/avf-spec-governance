# Final Contract Compatibility Matrix (v1.0.0)

| CONTRACT_NAME | SCHEMA_FILE | PRODUCER_REPO | CONSUMER_REPOS | COMPATIBILITY_RULE | ERROR_TAXONOMY | IDEMPOTENCY |
|---|---|---|---|---|---|---|
| Domain Entities | `domain-entities.schema.json` | R01 / R02 | R02, R03, R04, R05, R06, R11, R12, R13 | Additive v1.0 (Draft 2020-12) | Standard Status Codes | Version Fencing |
| Provider Request | `provider-request.schema.json` | R06 / R08 | R07, R08, R09, R10, R15 | Strict Schema v1.0 | Standard Provider Errors | SHA-256 Idempotency Key |
| Provider Result | `provider-result.schema.json` | R07 / R08 / R09 / R10 | R06, R02, R11, R14 | Strict Schema v1.0 | 4 Error Categories | Deduplication Token |
| Event Envelope | `event-envelope.schema.json` | All Repos | R02, R06, R13, R14 | Standard v1.0 Envelope | DLQ Error Envelope | UUIDv4 Deduplication |
| Browser Command | `browser-command.schema.json` | R08 | R09, R15 | Strict Schema v1.0 | CDP Transport Errors | Command Sequence ID |
