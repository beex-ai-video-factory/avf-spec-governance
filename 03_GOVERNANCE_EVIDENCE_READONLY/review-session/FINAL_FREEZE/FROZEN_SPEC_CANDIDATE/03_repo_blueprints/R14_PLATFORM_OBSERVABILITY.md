# R14 — avf-platform-observability Blueprint

**Repository type:** Platform/infrastructure repository  
**Execution Type:** Deterministic platform  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Standardize telemetry, secrets/config conventions, local/production deployment primitives, backups, dashboards, and SLO measurement without owning business logic.

## RESPONSIBILITY / OWNS

- OpenTelemetry conventions
- log field schema
- metrics naming
- trace propagation helpers
- secret/config templates
- backup/runbook templates
- health/readiness conventions

## DOES NOT OWN / NON-GOALS

- project state
- workflow business logic
- provider implementation

## INPUTS

- telemetry from all components

## OUTPUTS

- logs/metrics/traces/dashboards/alerts/runbooks

## PUBLIC API / CONTRACT

- instrumentation packages/config
- health endpoint conventions

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Telemetry backend and deployment metadata only.

## DEPENDENCIES

- avf-contracts correlation context
- OTel-compatible stack

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- missing correlation IDs
- PII/token leakage
- telemetry outage
- cardinality explosion

## RETRY STRATEGY

Telemetry failure must not fail generation path; bounded buffering.

## IDEMPOTENCY

N/A.

## OBSERVABILITY

- self-monitor telemetry pipeline
- dropped spans/logs
- redaction violations

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- log schema validation
- trace propagation integration
- secret redaction tests
- backup restore drill scripts

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

structured logs + correlation context + basic metrics + local env templates.

## PRODUCTION VERSION

dashboards/alerts, backup verification, retention, security hardening.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- A GenerationJob trace crosses workflow/provider/execution/QC/media
- tokens/cookies redacted
- telemetry outage is non-fatal
- runbook identifies component/version/session from incident data

## HANDOFF ARTIFACTS

Implementation repo must contain:

```text
README.md
ARCHITECTURE.md
COMPATIBILITY.yaml
CHANGELOG.md
src/ or app/
tests/unit/
tests/contract/
tests/integration/
tests/failure/
docs/runbook.md
```

Where applicable it must also contain migrations, container definition, health/readiness endpoint, and generated API docs.
