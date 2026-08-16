# R03 — avf-creative Blueprint

**Repository type:** Bounded AI worker/service  
**Execution Type:** LLM tasks; agent only for explicitly approved multi-step research  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Transform Brief -> CreativeSpec -> ScriptVersion -> ScenePlan -> proposed ShotVersions using structured LLM outputs.

## RESPONSIBILITY / OWNS

- creative transformation prompts/templates
- structured output validation/repair
- creative model routing policy
- creative provenance

## DOES NOT OWN / NON-GOALS

- canonical project writes
- generation provider calls
- retry budgets
- browser actions
- asset binary storage

## INPUTS

- Brief
- approved constraints
- Character/Style refs when available

## OUTPUTS

- CreativeSpec proposal
- ScriptVersion proposal
- ScenePlan proposal
- ShotVersion proposals

## PUBLIC API / CONTRACT

- GenerateCreativeSpec
- GenerateScript
- GenerateScenePlan
- GenerateShotPlan
- ReviseCreativeArtifact

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

No canonical state; optional ephemeral job cache. Outputs include model/template provenance.

## DEPENDENCIES

- avf-contracts
- LLM provider SDKs

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- invalid structured output
- model refusal/unavailability
- creative inconsistency
- token/context overflow

## RETRY STRATEGY

Schema repair then max bounded model retry; never infinite creative loop.

## IDEMPOTENCY

Request hash can cache deterministic-equivalent proposal but canonical commit is handled by core.

## OBSERVABILITY

- model name/version
- template version
- tokens/latency
- repair count
- validation failures

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- JSON fixture validation
- prompt golden tests where useful
- fake LLM tests
- bounded retry tests
- no-direct-state-mutation contract test

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Brief -> structured ShotVersion proposals; script/storyboard can be manual.

## PRODUCTION VERSION

Separate transforms, optional research agent, human approval checkpoints, eval suite.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Every output validates against frozen contracts
- model prose is never required by downstream services
- all LLM calls emit provenance
- invalid output reaches explicit failure after bounded repair

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
