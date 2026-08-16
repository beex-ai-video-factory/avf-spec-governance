# REPOSITORY CONTEXT PROFILE — avf-core-state

## Mission
Own canonical business state, entity version semantics, idempotent command layer and persistence.

## Non-goal
Must not own browser execution, provider-specific UI logic, or creative model reasoning.

## Required authority
The frozen repository blueprint with the same R-number and the current frozen `avf-contracts` release.

## Implementation law
- consume only documented contracts;
- do not import another repo's private modules;
- do not change frozen schema locally;
- do not hide external effects;
- all material behavior requires tests;
- no self-approval.

## Human execution
Run prompts I00 through I12 in order.
When a frozen-spec ambiguity is found, stop the affected task and create `SPEC_CLARIFICATION_REQUEST`; do not guess.
