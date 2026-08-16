# Model Orchestration Strategy

## Recommended pattern

Use model diversity when the harness supports it.

- Parallel specialist reviewers: fastest strong high-reasoning agent/coding model available.
- High-impact architecture synthesis: strongest reasoning model available.
- Fresh-context audit: preferably a different model family from the majority of reviewers.
- Coding implementation: strong coding/agent model.
- Mechanical checks: deterministic tools, not a model vote.

## If Antigravity exposes Gemini 3.7 Flash High

Use it as the default parallel reviewer/worker model after a small smoke evaluation.

## If Gemini 3.5 Pro is actually available in your UI

Use it selectively for:
- Architecture Judge;
- difficult cross-domain synthesis;
- final freeze dispute resolution.

Do not spend a flagship model on every mechanical subtask if a Flash High reviewer can do the work with objective gates.

## If only one model can be used

Prefer the strongest current high-reasoning agent model that is stable in the harness, then compensate for correlated errors with:
- blind role isolation;
- adversarial rounds;
- fresh-context audit;
- executable tests;
- evidence gates.

The governance mechanism matters more than model naming alone.
