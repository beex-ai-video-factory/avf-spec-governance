# R09 — avf-browser-worker Blueprint

**Repository type:** Privileged local worker + Chrome MV3 extension (Track A)  
**Execution Type:** Deterministic-first browser automation; constrained recovery fallback  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Provide controlled, replaceable Google Flow browser execution using documented Chrome extension/browser mechanisms and deterministic-first UI automation.

## RESPONSIBILITY / OWNS

- Chrome session lifecycle
- extension content scripts
- DOM/accessibility selectors
- upload/download handling
- screenshots/diagnostics
- browser heartbeat/lease
- FlowExecutionPort server/host

## DOES NOT OWN / NON-GOALS

- canonical project state
- generation budget
- creative retry
- QC policy
- FlowKit internals
- security-challenge bypass

## INPUTS

- FlowExecutionCommand

## OUTPUTS

- FlowExecutionResult
- diagnostics
- session health

## PUBLIC API / CONTRACT

- ENSURE_SESSION
- OPEN_FLOW
- CREATE_OR_SELECT_PROJECT
- ATTACH_ASSETS
- SET_GENERATION_OPTIONS
- SUBMIT_PROMPT
- READ_GENERATION_STATE
- DOWNLOAD_OUTPUT
- CAPTURE_DIAGNOSTIC
- CANCEL

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Disposable session/command state only. Persistent Chrome profile is secret local infrastructure, not business state.

## DEPENDENCIES

- avf-contracts
- Chrome MV3
- option A1 Native Messaging host or A2 authenticated loopback WebSocket
- optional Playwright dedicated persistent context for lifecycle/test harness

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- browser crash
- MV3 service worker termination
- selector drift
- download interruption
- auth expired
- security challenge
- Flow page state unknown

## RETRY STRATEGY

Reconnect/reload/read-state within bounded policy; security challenge => HUMAN_REQUIRED; submit ambiguity => reconciliation result.

## IDEMPOTENCY

command_id de-duplicates worker commands where observable; submit relies on adapter/workflow business idempotency and state reconciliation.

## OBSERVABILITY

- worker/session ID
- extension version
- selector bundle version
- heartbeat
- command latency
- screenshots on failure
- auth/blocked states

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- DOM fixture tests
- extension unit tests
- FlowExecutionPort conformance
- service worker restart
- browser crash
- download failure
- selector drift simulation
- live smoke suite

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

One dedicated Chrome profile, one active Flow tab/session, loopback authenticated transport, text-to-video + download.

## PRODUCTION VERSION

Native Messaging preferred where packaging permits; worker leases; multiple isolated sessions; visual fallback; signed extension build.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Extension can restart without losing canonical work
- no global service-worker variable is required for correctness
- security challenges surface HUMAN_REQUIRED
- all Flow-specific selectors are isolated/versioned
- passes FlowExecutionPort contract suite

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
