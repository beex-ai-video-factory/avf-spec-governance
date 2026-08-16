# R15 — avf-integration-harness Blueprint

**Repository type:** Composition/release/test repository  
**Execution Type:** Deterministic test/release tooling  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Assemble pinned component releases, run contract/integration/E2E/failure suites, provide FakeProvider scenarios, and act as the release gate for the whole system.

## RESPONSIBILITY / OWNS

- Docker Compose profiles
- release manifest
- cross-repo compatibility matrix
- system test fixtures
- fault injection
- live smoke orchestration

## DOES NOT OWN / NON-GOALS

- production domain logic
- provider private logic
- schema redefinition

## INPUTS

- released component artifacts/images
- contract package
- test environment credentials when live

## OUTPUTS

- compatibility report
- E2E report
- release candidate manifest
- Phase 0 benchmark results

## PUBLIC API / CONTRACT

- CLI/scripts for compose, contract test, e2e, benchmark

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Test reports and release manifests only.

## DEPENDENCIES

- all component artifacts
- avf-contracts
- FakeProvider
- optional Track A/Track B live setups

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- version incompatibility
- flaky live test
- environment mismatch
- missing migration

## RETRY STRATEGY

Deterministic suites must not rely on retry to hide failures; live smoke may classify environmental/transient separately.

## IDEMPOTENCY

Test environment reset scripts and unique run IDs.

## OBSERVABILITY

- suite duration
- pass/fail by component version
- flake classification
- benchmark distributions

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- The repository is the test harness; its own utilities have unit tests.

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Core compose + FakeProvider E2E + FlowExecutionPort conformance runner.

## PRODUCTION VERSION

Fault injection matrix, release promotion automation, Track A/B comparison benchmark.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- A release can be reproduced from manifest only
- Track A and B can be swapped by profile/config
- contract mismatch blocks promotion
- failure injection proves resume/idempotency invariants

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
