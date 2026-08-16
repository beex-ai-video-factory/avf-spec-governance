# Phase Roadmap

Every phase produces a working vertical slice.

## Phase 0 — Architecture spikes

**Objective:** remove critical uncertainty before platform build-out.

Scope:
- prove one-shot submit/status/download;
- test asset attachment;
- compare Track A and Track B;
- measure disconnect/recovery;
- document authentication/security challenge behavior;
- define a 100-run benchmark protocol.

Deliverables:
- spike reports;
- measured failure taxonomy;
- decision ADR selecting primary MVP execution track;
- fallback decision.

Failure criterion:
- if neither track can meet an agreed reliability threshold without unacceptable manual/security/policy risk, Google Flow remains experimental and the MVP must use a supported API provider.

## Phase 1 — Single-shot core

`ShotVersion -> PromptVersion -> GenerationJob -> Provider -> Take -> persistence`

Uses FakeProvider first, then one Flow track.

Exit:
- crash/restart cannot accidentally duplicate a generation in deterministic tests.

## Phase 2 — Multi-shot durable project

Add:
- project queue;
- workflow resume;
- media storage;
- browser/worker restart tests;
- budget records.

## Phase 3 — Creative automation

Add:
- Brief -> CreativeSpec -> Script -> Scene -> ShotVersion;
- structured outputs;
- bounded LLM repair.

Generation core unchanged.

## Phase 4 — Assets and continuity

Add:
- CharacterVersion;
- StyleVersion;
- reference asset sets;
- asset resolver;
- prompt compiler provider profiles.

## Phase 5 — Automated QC

Add technical QC, semantic QC, deterministic RetryPolicyEngine.

## Phase 6 — Operator control

Add dashboard, approvals, retries, prompt/asset intervention, browser-session health.

## Phase 7 — Scale

Only after stable measurements:
- concurrency;
- worker pools;
- multi-provider routing;
- distributed deployment.
