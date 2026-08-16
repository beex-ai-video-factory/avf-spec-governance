# R13 — avf-operator-console Blueprint

**Repository type:** Human-control application  
**Execution Type:** Human + deterministic UI/API client  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Give operators transparent project/job/session/QC visibility and controlled manual actions without provider-specific hidden state.

## RESPONSIBILITY / OWNS

- operator views
- action UX
- approval/retry/edit flows
- browser session health presentation

## DOES NOT OWN / NON-GOALS

- business state persistence
- provider/browser implementation
- retry algorithms
- direct DB access

## INPUTS

- Core query APIs
- workflow status
- observability read APIs

## OUTPUTS

- validated operator commands/signals

## PUBLIC API / CONTRACT

- UI only; consumes public Core/Workflow endpoints

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

UI preferences/session only; business state remains server-side.

## DEPENDENCIES

- avf-contracts client models
- avf-core-state API
- avf-workflow API
- observability backend

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- stale view
- action conflict
- workflow unavailable
- authorization failure

## RETRY STRATEGY

Read retries safe; write actions carry command IDs and show conflict/result.

## IDEMPOTENCY

Every operator mutation includes command_id; double-click safe.

## OBSERVABILITY

- operator action audit
- blocked-job age
- manual intervention counts

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- UI unit
- API contract mocks
- double-submit
- stale version conflict
- role/authorization

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Projects, Shots, GenerationJobs, blocked states, approve/retry/resume, browser session health.

## PRODUCTION VERSION

Cost/QC dashboards, prompt/asset diff, bulk actions, RBAC.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- No direct DB/provider calls
- all mutations auditable
- blocked auth/UI/security states visible with actionable reason
- stale data cannot silently overwrite newer versions

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
