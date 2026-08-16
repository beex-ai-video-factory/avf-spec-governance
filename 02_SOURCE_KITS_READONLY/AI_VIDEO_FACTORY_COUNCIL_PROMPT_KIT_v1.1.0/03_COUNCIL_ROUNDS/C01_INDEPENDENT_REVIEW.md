# C01 — Independent Blind Specialist Review (v1.1)

Authority: Master v1.1.

Dispatch all 15 voting roles as actual isolated subagents using the exact role charter files.

Each role receives only:
- candidate spec;
- evidence ledger;
- protected capability register;
- business objectives;
- its role charter;
- Council governance.

No role may see another role's findings before submitting.

Persist every raw role output before synthesis.
Record/hash:
- role;
- model/reasoning mode;
- skill versions/hashes;
- role prompt hash;
- raw review artifact.

After all submissions:
- build files × requirements × invariants × roles coverage matrix;
- detect suspicious duplication/model-correlation;
- identify unreviewed critical areas;
- normalize findings without mutating raw reviews.

FAIL if:
- any mandatory role is absent;
- isolation was violated;
- critical coverage is missing;
- raw reviews were altered before persistence.

Output:
`C01_RESULT = PASS | FAIL`
and
`WAITING_FOR_HUMAN_GATE_01`

STOP. Never auto-start C02.
