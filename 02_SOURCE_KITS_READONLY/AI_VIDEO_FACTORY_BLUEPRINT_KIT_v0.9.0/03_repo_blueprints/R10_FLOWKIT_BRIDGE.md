# R10 — avf-flowkit-bridge Blueprint

**Repository type:** Compatibility adapter to external OSS engine (Track B)  
**Execution Type:** Deterministic compatibility bridge around FlowKit  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Use FlowKit to accelerate Google Flow integration while preserving AVF contracts and preventing FlowKit architecture/models from contaminating the core system.

## RESPONSIBILITY / OWNS

- FlowExecutionPort <-> FlowKit mapping
- FlowKit process health adapter
- FlowKit version compatibility matrix
- normalized error mapping
- translation fixtures

## DOES NOT OWN / NON-GOALS

- forking AVF core into FlowKit
- exposing FlowKit SQLite as canonical state
- copying provider-security bypass logic into AVF
- creative/project ownership

## INPUTS

- FlowExecutionCommand
- configured FlowKit instance/version

## OUTPUTS

- FlowExecutionResult
- FlowKit diagnostics under namespaced metadata

## PUBLIC API / CONTRACT

- Same FlowExecutionPort as Track A
- health/version probe
- compatibility report

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Bridge correlation only; FlowKit private state is treated as cache/execution-engine state and never authoritative.

## DEPENDENCIES

- avf-contracts
- FlowKit pinned release/commit
- local process/HTTP/WS integration as supported by selected FlowKit version

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- FlowKit API/protocol change
- extension disconnected
- FlowKit DB inconsistency
- unsupported Flow capability
- security challenge
- version mismatch

## RETRY STRATEGY

Bridge retries transport reads only; relies on AVF workflow for business retries; challenge/error maps to normalized blocked states.

## IDEMPOTENCY

Translate command_id and generation correlation; never assume FlowKit queue identity is AVF canonical identity.

## OBSERVABILITY

- FlowKit version/commit
- bridge version
- health
- translation errors
- normalized vs raw status
- request correlation

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- Golden translation fixtures
- FlowExecutionPort conformance
- version mismatch tests
- FlowKit unavailable/restart tests
- same upstream E2E as Track A

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Wrap the smallest FlowKit operations required for one-shot generation/status/download; no source fork if public/local interfaces suffice.

## PRODUCTION VERSION

Pin tested versions; optional maintained fork only behind bridge; migration tests for FlowKit upgrades.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Removing FlowKit requires changes only in Track B deployment, not core contracts
- FlowKit-specific identifiers stay namespaced
- bridge passes same execution conformance suite as Track A
- unsupported/policy-sensitive behavior is not promoted into AVF requirements

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
