# /goal Task — C01 Independent Blind Review

Prerequisite: Human has explicitly approved C00.

Operate under Master v1.1 and C01 round prompt.

Use Gemini 3.7 Flash High as the parent.
Spawn all 15 actual isolated subagents using their role charters.
Use model=inherit/flash unless a role explicitly requires a Pro advisory verifier.
No reviewer may see another raw review before persistence.

Each role receives:
- C00_FINAL baseline;
- exact Blueprint candidate;
- its own role charter;
- protected capabilities;
- requirement/evidence/gap seed registers;
- governance rules.

For each role:
- inspect assigned requirements/files;
- also follow material dependency edges discovered during review;
- produce evidence-backed findings and constructive solutions;
- explicitly respond to C00 gap seeds assigned to that role;
- persist raw output before any synthesis.

Autonomously retry failed/hung reviewer tasks without breaking blindness.
Do not synthesize until all mandatory raw reviews exist.

After all complete:
- hash raw outputs;
- normalize without changing raw meaning;
- generate coverage matrix;
- detect suspicious duplicate/correlated findings;
- detect uncovered MUST requirements/contracts/invariants;
- if coverage holes exist, dispatch targeted blind supplemental reviewer subagents;
- repeat until C01 exit criteria pass.

Do not cross-examine findings in C01.

Exit:
- all 15 mandatory roles submitted;
- raw review integrity preserved;
- 100% required coverage;
- C00 gap seeds addressed by assigned reviewers;
- no critical area unreviewed.

Output:
C01_RESULT = PASS | FAIL
RAW_REVIEWS = N
COVERAGE_GAPS = N
UNANSWERED_C00_GAP_SEEDS = N
WAITING_FOR_HUMAN_GATE_01

STOP.
