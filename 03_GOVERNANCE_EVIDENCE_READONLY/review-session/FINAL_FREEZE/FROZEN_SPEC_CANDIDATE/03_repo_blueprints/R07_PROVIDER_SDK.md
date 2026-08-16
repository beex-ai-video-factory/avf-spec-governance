# R07 — avf-provider-sdk Blueprint

**Repository type:** Contract/library + gateway abstractions  
**Execution Type:** Deterministic library/reference worker  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Define provider-neutral video/image generation interface, capabilities, normalized statuses/errors, and FakeVideoProvider reference implementation.

## RESPONSIBILITY / OWNS

- VideoGenerationProvider interface
- ProviderCapabilities
- normalized error mapping interface
- FakeVideoProvider
- provider contract test suite

## DOES NOT OWN / NON-GOALS

- Google Flow DOM/extension details
- creative semantics
- canonical state

## INPUTS

- ProviderGenerationRequest

## OUTPUTS

- ProviderGenerationResult/Status
- output descriptors
- normalized errors

## PUBLIC API / CONTRACT

- create_session
- validate_request
- submit_generation
- get_status
- download_output
- attach_asset
- cancel

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

No canonical state. Provider implementations may maintain private ephemeral/session state.

## DEPENDENCIES

- avf-contracts

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- contract mismatch
- unsupported capability
- unmapped error

## RETRY STRATEGY

SDK does not make business retry decisions; provider implementations may perform transport retries only where safe.

## IDEMPOTENCY

submit requires caller-provided idempotency_key and implementation reconciliation semantics.

## OBSERVABILITY

- provider operation latency
- normalized error class
- capability mismatch

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- provider conformance suite
- FakeProvider success/failure/timeout/rate-limit scenarios
- idempotency conformance

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Interfaces + FakeVideoProvider + Google Flow capability profile contract.

## PRODUCTION VERSION

Additional provider adapters and capability negotiation.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- A new provider can be built without importing workflow/core internals
- FakeProvider supports all deterministic integration scenarios
- conformance suite is reusable by GoogleFlowProvider

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
