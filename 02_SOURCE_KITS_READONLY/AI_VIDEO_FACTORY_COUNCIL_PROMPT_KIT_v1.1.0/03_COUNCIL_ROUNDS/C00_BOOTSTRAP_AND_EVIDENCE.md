# C00 — Baseline, Evidence & Governance Bootstrap (v1.1)

Authority: `01_COUNCIL_MASTER/MASTER_COUNCIL_PROMPT.md`.
If this file and the Master differ, the Master governs.

Run C00 only.

Create:
- exact Blueprint candidate version/hash;
- Prompt Kit version/hash;
- specification file inventory;
- Council roster;
- model/reasoning/skill provenance;
- role prompt hashes;
- `PROTECTED_CAPABILITY_REGISTER.md`;
- `REQUIREMENT_TRACEABILITY_MATRIX.md`;
- `EVIDENCE_LEDGER.md` using E0–E4 grades;
- `ASSUMPTION_REGISTER.md`;
- contract inventory;
- repository/service inventory;
- ADR inventory;
- external facts needing verification;
- open architectural decisions;
- review coverage plan.

Do not propose final architecture changes in C00.

PASS only if:
- baseline is unambiguous;
- protected capabilities are explicit;
- MUST requirements have been enumerated;
- evidence versus assumption is distinguishable;
- all 15 voting roles can be dispatched with isolated contexts.

Output:
`C00_RESULT = PASS | FAIL`
and
`WAITING_FOR_HUMAN_GATE_00`

STOP. Never auto-start C01.
