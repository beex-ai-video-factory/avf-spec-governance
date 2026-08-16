# C04 — Exact Changeset Voting & Controlled Synthesis (v1.1)

Authority: Master v1.1.

Vote only on exact Change Proposals with reviewable text/schema diffs.

For each proposal:
1. determine materially affected voting scope;
2. determine mandatory sign-offs;
3. review Capability Delta;
4. check objective tests/benchmarks;
5. collect YES / NO / ABSTAIN + rationale;
6. preserve dissent;
7. apply Master quorum/threshold rules.

Votes cannot override failed objective evidence.

After voting:
- integrate accepted proposals only;
- create exact original -> revised semantic diff;
- annotate every semantic change with CHANGE_ID;
- reject unvoted semantic edits;
- run contract compatibility;
- rerun requirement traceability;
- rerun dependency graph validation;
- get mandatory owners to confirm integrated wording.

Create:
- `VOTE_RECORD.md`;
- `SPEC_CHANGESET.md`;
- `SPEC_SEMANTIC_DIFF.md`;
- `CONTRACT_DIFF_REPORT.md`;
- `POST_MERGE_CONSISTENCY_REPORT.md`.

Output:
`C04_RESULT = PASS | FAIL`
and
`WAITING_FOR_HUMAN_GATE_04`

STOP. Never auto-start C05.
