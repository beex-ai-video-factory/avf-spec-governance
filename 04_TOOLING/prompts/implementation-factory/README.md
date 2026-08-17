# AVF Human Runbook Factory Kit v1.0.0

This kit creates, audits, and freezes the human-operable implementation prompt system for AI Video Factory.

Run in this order:

1. `01_BUILD_HUMAN_IMPLEMENTATION_RUNBOOK.md`
   - Model: Gemini 3.7 Flash High
   - Workspace: `AVF_SPEC_REVIEW/`
   - Generates the complete sequential operator prompt pack.
   - Must end with `READY_FOR_EXTERNAL_RUNBOOK_AUDIT`.

2. `02_AUDIT_HUMAN_IMPLEMENTATION_RUNBOOK.md`
   - NEW conversation.
   - Model: Claude Opus 4.6 Thinking.
   - Independently walks the prompt graph and checks dependency/safety/human usability.
   - Must end with `VERIFIED_OPERATOR_RUNBOOK`.

3. `03_FREEZE_HUMAN_IMPLEMENTATION_RUNBOOK.md`
   - Model: Gemini 3.7 Flash High.
   - Freezes/hash-locks the verified runbook, creates root `IMPLEMENTATION_START_HERE.md`, and creates writable operator runtime state.
   - Must end with `READY_FOR_HUMAN_IMPLEMENTATION`.

After step 3, the human should stop using this factory kit and follow only:

`AVF_SPEC_REVIEW/IMPLEMENTATION_START_HERE.md`

Golden rule:

> After each implementation prompt, run only the path returned in `RECOMMENDED_NEXT_PROMPT`. If the result is FAIL/BLOCKED, run the returned recovery prompt instead. Do not manually choose the next repo.
