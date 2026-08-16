# C06 — Freeze Readiness (v1.1)

Authority: Master v1.1.

Run every gate in `04_GATES_AND_AUDIT/FREEZE_GATE_MATRIX.md`
plus all hard-fail conditions in Master v1.1.

Every gate result includes:
- PASS / FAIL;
- evidence;
- affected requirement/invariant;
- responsible sign-offs;
- residual risk;
- provisional status if applicable.

Mandatory re-generation:
- final requirement traceability;
- contract compatibility matrix;
- repository dependency graph;
- implementation build packets;
- protected capability delta report.

Perform post-merge consistency and changeset integration audit.

FAIL if:
- any mandatory gate fails;
- any MUST requirement lacks owner/test;
- any accepted semantic change lacks Change ID;
- implementation agents would need architectural guessing.

Output:
`C06_RESULT = PASS | FAIL`
and
`WAITING_FOR_HUMAN_GATE_06`

STOP. Never auto-start C07.
