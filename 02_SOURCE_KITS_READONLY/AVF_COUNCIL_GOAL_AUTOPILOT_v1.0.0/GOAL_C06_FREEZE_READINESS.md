# /goal Task — C06 Freeze Readiness

Prerequisite: Human accepted C05 or all C05 blockers have been resolved/re-audited.

Use Gemini 3.7 Flash High.

Run the complete Freeze Gate Matrix and all Master hard-fail rules.
Regenerate requirement traceability, contract compatibility, dependency graph,
protected capability delta, implementation handoff and post-merge consistency.

For mechanical validation use tools/scripts.
For ambiguous critical gate interpretation invoke a fresh Pro-tier verifier.

A PASS statement must cite evidence.
Never vote a failed objective check into PASS.

Output:
C06_RESULT = PASS | FAIL
MANDATORY_GATES_PASSED
MANDATORY_GATES_FAILED
FREEZE_BLOCKERS
WAITING_FOR_HUMAN_GATE_06

STOP.
