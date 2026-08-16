# R01 — avf-contracts Blueprint

**Repository type:** Contract/SDK repository  
**Execution Type:** Deterministic library/tooling  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Own language-neutral schemas, shared identifiers, error taxonomy, compatibility rules, and generated client/model packages used by every other repository.

## RESPONSIBILITY / OWNS

- JSON Schema sources
- message envelopes
- normalized error codes
- schema version metadata
- contract test fixtures
- generated type packages

## DOES NOT OWN / NON-GOALS

- business state
- database migrations for services
- provider implementation details
- browser selectors

## INPUTS

- architecture freeze decisions
- consumer contract requirements

## OUTPUTS

- versioned schemas
- generated Python/TypeScript models
- contract fixtures
- compatibility report

## PUBLIC API / CONTRACT

- No runtime API required
- publish package artifacts and schema bundle
- CLI: avf-contract validate <payload>

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Git history + release artifacts only.

## DEPENDENCIES

- JSON Schema tooling
- Semantic Versioning

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- breaking change published as minor
- generated types drift from schema
- ambiguous enum extension

## RETRY STRATEGY

N/A; CI blocks invalid release.

## IDEMPOTENCY

N/A.

## OBSERVABILITY

- CI contract compatibility report
- release checksum

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- schema validation tests
- backward-compatibility diff tests
- golden payload fixtures
- generated-model round-trip tests

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Provider request/result, browser command, event envelope, domain refs, error taxonomy.

## PRODUCTION VERSION

Code generation, consumer-driven fixtures, deprecation linter.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- All schemas validate against draft 2020-12
- Python/TS generated models pass round-trip fixtures
- breaking-change detector blocks incompatible v1 changes
- every downstream repo can pin a released artifact without Git source dependency

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
