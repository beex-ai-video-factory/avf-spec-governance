# R05 — avf-prompt-compiler Blueprint

**Repository type:** Stateless service/library  
**Execution Type:** Deterministic-first with optional bounded LLM enrichment  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Compile normalized semantic Shot + continuity + provider capability profile into immutable provider-targeted PromptVersion proposals.

## RESPONSIBILITY / OWNS

- PromptSpec normalization
- compiler versions
- provider-family syntax templates
- input hashing
- prompt validation

## DOES NOT OWN / NON-GOALS

- generation submission
- creative project planning
- provider status polling
- retry policy

## INPUTS

- ShotVersion
- Character/Style constraints
- ResolvedAssetSet
- ProviderCapabilities

## OUTPUTS

- PromptVersion proposal
- compile diagnostics
- input_hash

## PUBLIC API / CONTRACT

- CompilePrompt
- ValidatePrompt
- RecompileForProvider
- ExplainCompileDiagnostics

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Stateless; compiler/template versions shipped with release.

## DEPENDENCIES

- avf-contracts
- avf-provider-sdk capability types

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- unsupported capability
- prompt length/format invalid
- missing required reference
- LLM enrichment invalid

## RETRY STRATEGY

Optional enrichment repair bounded; deterministic compiler errors fail fast.

## IDEMPOTENCY

Same normalized inputs + compiler version => same input_hash; output expected semantically repeatable.

## OBSERVABILITY

- compiler version
- compile latency
- unsupported-capability rate
- enrichment model usage

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- golden prompt fixtures
- capability matrix tests
- hash stability tests
- provider syntax contract tests

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Deterministic Google Flow prompt compiler plus generic provider-neutral PromptSpec.

## PRODUCTION VERSION

Multiple provider compilers, automatic capability-aware degradation policy.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- PromptVersion provenance includes all input versions
- no provider/browser side effect
- compiler golden suite stable
- unsupported requests fail explicitly rather than silently dropping constraints

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
