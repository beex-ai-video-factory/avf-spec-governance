# Committee Review Edition — AI Video Factory Blueprint Kit

This file is a compact navigation edition. Normative details live in the referenced kit documents.

## Freeze recommendation

Freeze a contract-first architecture in which:

- `avf-core-state` owns canonical PostgreSQL state;
- `avf-workflow` owns durable sequencing, not business truth;
- all generation uses `VideoGenerationProvider`;
- Google Flow uses `avf-google-flow-adapter` and a frozen `FlowExecutionPort`;
- Google Flow execution may be Track A (our controlled browser worker) or Track B (FlowKit compatibility bridge);
- no FlowKit/browser private state leaks upstream;
- LLMs propose structured intelligence but do not directly mutate canonical state;
- retry/budget/idempotency are deterministic;
- contract tests and FakeProvider precede live Flow development.

## What council must decide

1. Are repository boundaries correct?
2. Is one canonical state owner acceptable?
3. Are provider/browser contracts sufficient to swap Track A/B?
4. Is FlowKit correctly treated as an external execution engine instead of core architecture?
5. Are security-challenge boundaries appropriate?
6. Are state machines/idempotency semantics sufficient for crash recovery?
7. Are Phase-0 benchmark/kill criteria sufficient before production reliance on Google Flow?

## Most consequential engineering choice

The kit intentionally recommends **FlowKit-first execution may be used for speed, but FlowKit-first architecture is forbidden**. The bridge allows reuse now while preserving the ability to replace it later.

## Primary review files

- `01_master/MASTER_BLUEPRINT.md`
- `01_master/SYSTEM_INVARIANTS.md`
- `01_master/DATA_MODEL.md`
- `02_contracts/*`
- `03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`
- `04_integration/FREEZE_CHECKLIST.md`
- `05_phases/PHASE_0_BENCHMARK.md`
- `07_risk/RISK_REGISTER.md`
