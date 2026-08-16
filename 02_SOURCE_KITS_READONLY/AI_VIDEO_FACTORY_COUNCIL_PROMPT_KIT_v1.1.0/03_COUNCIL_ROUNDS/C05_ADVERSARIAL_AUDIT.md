# C05 — Fresh-Context Adversarial Audit (v1.1)

Authority: Master v1.1.

This round MUST be executed by a NEW Independent Audit Judge.
Prefer a different model family if available.

The Judge did not participate in C01–C04.

Provide:
- original candidate;
- revised candidate;
- evidence ledger;
- requirement traceability;
- protected capabilities;
- raw findings;
- Change Proposals;
- votes/dissent;
- semantic diff;
- compatibility reports;
- gate definitions.

Do not provide persuasive Chair summaries.

Attempt to falsify the council result across all attack categories listed in Master v1.1, including:
- capability regression;
- unvoted semantic changes;
- provider/FlowKit leakage;
- contract contradictions;
- idempotency/recovery;
- security;
- provenance;
- testability;
- agent handoff;
- evidence laundering;
- groupthink.

Any `AUDIT_BLOCKER` reopens the required earlier round(s).

Create independent audit artifact under `AUDITS/`.

Output:
`C05_RESULT = PASS_WITH_RESIDUAL_RISK | FAIL_AUDIT_BLOCKER`
and
`WAITING_FOR_HUMAN_GATE_05`

STOP. Never auto-start C06.
