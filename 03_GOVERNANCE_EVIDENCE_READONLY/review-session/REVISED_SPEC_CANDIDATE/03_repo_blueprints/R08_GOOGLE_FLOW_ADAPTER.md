# R08 — avf-google-flow-adapter Blueprint

**Repository type:** Provider adapter  
**Execution Type:** Deterministic adapter  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Implement VideoGenerationProvider for Google Flow by translating provider-neutral requests into FlowExecutionPort commands and normalizing results.

## RESPONSIBILITY / OWNS

- Google Flow capability mapping
- Flow-specific option mapping
- execution command sequencing
- Flow state interpretation
- normalized error translation

## DOES NOT OWN / NON-GOALS

- DOM selectors
- Chrome lifecycle
- FlowKit DB/models
- canonical business state
- creative retry decisions

## INPUTS

- ProviderGenerationRequest
- FlowExecutionPort implementation

## OUTPUTS

- ProviderGenerationResult/Status

## PUBLIC API / CONTRACT

- Implements VideoGenerationProvider
- bind_execution_port(track-a|track-b)

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Minimal provider session correlation only; persistent provider IDs recorded through caller/core.

## DEPENDENCIES

- avf-contracts
- avf-provider-sdk
- FlowExecutionPort

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- capability unsupported
- execution port unavailable
- ambiguous UI/external state
- download unavailable

## RETRY STRATEGY

Transport/read polling may retry within safe bounds; submit ambiguity must return reconciliation-required error rather than blindly resubmit.

## IDEMPOTENCY

Pass generation idempotency/correlation through execution metadata; adapter records provider/execution correlation.

## OBSERVABILITY

- track selected
- submit/status/download latency
- normalized Flow errors
- capability mismatch

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- Provider contract suite
- mock FlowExecutionPort tests
- same behavior against Track A and Track B fixtures

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Text/image/reference generation path needed by Phase 1/2 only.

## PRODUCTION VERSION

More Flow modes/capabilities added without changing upstream SDK major version.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Upstream workflow cannot distinguish Track A vs B except diagnostics
- no selector/internal endpoint appears in public adapter contract
- all errors normalized
- adapter passes provider conformance suite with both execution test doubles

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
