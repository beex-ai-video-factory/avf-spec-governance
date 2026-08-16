# R11 — avf-qc Blueprint

**Repository type:** QC worker/service  
**Execution Type:** Hybrid deterministic + MLLM  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Evaluate generated Takes using deterministic technical checks plus versioned semantic/multimodal evaluators and return typed QCResult recommendations.

## RESPONSIBILITY / OWNS

- technical validation
- frame sampling policy
- evaluator interface/version
- score normalization
- issue taxonomy

## DOES NOT OWN / NON-GOALS

- retry execution
- generation submission
- canonical approval mutation
- browser actions

## INPUTS

- ShotVersion
- Take/Asset descriptor
- continuity refs
- QC profile

## OUTPUTS

- QCResult proposal
- technical findings
- semantic scores/issues
- recommendation

## PUBLIC API / CONTRACT

- EvaluateTechnical
- EvaluateSemantic
- EvaluateTake
- GetEvaluatorInfo

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

No canonical state; evaluator versions/config shipped or registered. Core stores accepted QCResult.

## DEPENDENCIES

- avf-contracts
- media decoding tools
- MLLM provider/local model

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- media unreadable
- model unavailable
- evaluation timeout
- low confidence
- schema invalid

## RETRY STRATEGY

Technical tool retry for transient I/O; semantic evaluator bounded retry; low confidence can recommend HUMAN_REVIEW.

## IDEMPOTENCY

Evaluation keyed by take checksum + evaluator version + QC profile hash.

## OBSERVABILITY

- evaluation latency
- model/version
- score distribution
- low-confidence rate
- accept/reject drift

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- technical media fixtures
- fake semantic evaluator
- golden labeled set
- version reproducibility
- model outage fallback

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

ffprobe/decode/duration/resolution checks + simple semantic evaluator interface.

## PRODUCTION VERSION

Benchmark-driven evaluator choices, character/style continuity metrics, calibration set.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- QC cannot call provider generate
- same take/evaluator profile yields traceable versioned result
- technical and semantic failures separated
- recommendation is typed and policy-neutral

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
