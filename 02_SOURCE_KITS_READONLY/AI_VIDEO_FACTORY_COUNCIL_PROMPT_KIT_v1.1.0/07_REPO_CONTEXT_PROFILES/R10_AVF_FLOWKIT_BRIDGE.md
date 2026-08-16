# REPOSITORY CONTEXT PROFILE — avf-flowkit-bridge

## Mission
Track B: map frozen FlowExecutionPort to a pinned FlowKit integration while containing FlowKit internals.

## Non-goal
Must not allow FlowKit SQLite/models/protocol to become AVF contracts.

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
