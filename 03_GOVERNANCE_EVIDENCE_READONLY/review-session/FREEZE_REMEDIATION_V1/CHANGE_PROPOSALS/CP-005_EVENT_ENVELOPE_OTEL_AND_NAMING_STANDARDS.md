# CHANGE PROPOSAL: CP-005 (AMENDED)
**CHANGE_ID:** CP-005
**TITLE:** Event Envelope Standardization with OpenTelemetry Distributed Tracing & Topic Naming
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** TECH-007, FINDING_006, FINDING_023
**MATERIALLY_AFFECTED_ROLES:** R04 (Contracts), R11 (Platform), R14 (Observability), R02 (Reliability)
**MANDATORY_SIGNOFF_ROLES:** R04 (Contracts), R11 (Platform)

## 1. Rationale & Problem Description
Unifies event envelope fields across documentation and JSON schema, adds OpenTelemetry tracing headers (`trace_id`, `span_id`), and aligns event naming to lowercase dotted convention (`^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$`).

## 2. Exact Specification Changes
1. `02_contracts/event-envelope.schema.json`: Include `trace_id`, `span_id`, `correlation_id`, `workflow_run_id`, `aggregate_id`, `aggregate_version`, `timestamp_utc`, `event_id`, `event_type`, `schema_version`, `payload`.
2. `04_integration/COMMAND_EVENT_CATALOG.md`: Document dotted event names.
3. `02_contracts/CONTRACTS_OVERVIEW.md`: Update event envelope contract.

## 3. Capability Preservation Proof
Preserves CAP-04 (Event-Driven Integration) and CAP-14 (Platform Observability).
