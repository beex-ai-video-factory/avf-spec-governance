# R06 — avf-workflow Blueprint

**Repository type:** Durable orchestration worker  
**Execution Type:** Deterministic durable workflows  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Coordinate long-running project/shot workflows, timers, waits, activities, human gates, and recovery without owning canonical business truth.

## RESPONSIBILITY / OWNS

- workflow definitions
- activity sequencing
- timeouts/backoff
- child workflow structure
- reconciliation steps
- workflow version migration policy

## DOES NOT OWN / NON-GOALS

- project database tables
- LLM prompt semantics
- browser selectors
- provider private protocol
- QC model scoring

## INPUTS

- StartProject/StartShot commands
- canonical IDs
- activity results

## OUTPUTS

- commands to core/services
- workflow status/progress
- escalations

## PUBLIC API / CONTRACT

- StartShotWorkflow
- StartProjectWorkflow
- SignalApprove
- SignalResume
- CancelWorkflow
- QueryWorkflowProgress

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Durable workflow history in workflow engine; canonical business state remains core.

## DEPENDENCIES

- avf-contracts
- avf-core-state
- avf-provider-sdk
- creative/assets/prompt/qc/media activity interfaces
- Temporal-class runtime

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- activity timeout
- worker crash
- workflow nondeterminism
- uncertain provider submit
- stuck human gate

## RETRY STRATEGY

Activity-specific retry; external submit uses reconciliation-before-resubmit; no global catch-and-retry-all.

## IDEMPOTENCY

Workflow IDs deterministic by business operation; activities require idempotency keys.

## OBSERVABILITY

- workflow duration
- activity retry counts
- stuck workflows
- human wait duration
- replay/nondeterminism alerts

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- workflow unit/replay tests
- fake activities
- crash/restart integration
- uncertain-submit scenario
- human signal tests

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

SingleShotWorkflow and sequential MultiShotWorkflow using FakeProvider.

## PRODUCTION VERSION

Versioned workflows, child workflows, provider queues, richer human gates.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Worker restart resumes from durable history
- replay tests pass
- provider submit cannot duplicate in injected-crash scenarios
- workflow can run with FakeProvider and either Flow execution track unchanged

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
