# R02 — avf-core-state Blueprint

**Repository type:** Stateful service  
**Execution Type:** Deterministic service  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Own canonical project/business state and transactional commands/queries. This is the authoritative source of truth for project, shot, prompt, generation, take, QC references, provenance, and workflow linkage.

## RESPONSIBILITY / OWNS

- PostgreSQL schema
- Project/Shot/Take lifecycle persistence
- version creation rules
- optimistic concurrency
- outbox records
- audit log references
- budget/usage ledger

## DOES NOT OWN / NON-GOALS

- creative reasoning
- browser automation
- provider polling
- media transformation
- semantic QC scoring

## INPUTS

- validated commands from API/workflow/operator
- events/results from bounded workers

## OUTPUTS

- canonical records
- command results
- read models
- outbox events

## PUBLIC API / CONTRACT

- CreateProject
- CreateShotVersion
- RegisterPromptVersion
- CreateGenerationJob
- RecordProviderSubmission
- RegisterTake
- RecordQCResult
- ApproveTake
- BlockGeneration
- AppendUsageRecord

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

PostgreSQL only; object content stored externally via Asset refs.

## DEPENDENCIES

- avf-contracts
- PostgreSQL

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- transaction conflict
- duplicate idempotency command
- migration failure
- orphaned references

## RETRY STRATEGY

Clients may retry commands with command_id/idempotency key; service returns prior result for completed duplicate commands.

## IDEMPOTENCY

Command idempotency table; unique business constraints.

## OBSERVABILITY

- audit log
- DB latency
- conflict rate
- command idempotency hits
- outbox lag

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- domain invariant unit tests
- migration tests
- transaction/concurrency tests
- idempotency tests
- repository integration tests with Postgres

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Project, ShotVersion, PromptVersion, GenerationJob, Take, basic Asset refs, WorkflowRun.

## PRODUCTION VERSION

Fine-grained audit, retention/tombstone, richer budget/read models.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- No downstream repo needs direct DB access
- all System Invariants expressible/enforced
- duplicate command tests are deterministic
- restart preserves all canonical state
- outbox and state commit atomically

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
