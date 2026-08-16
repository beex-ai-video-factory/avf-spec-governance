# C02 — Structured Cross-Examination (v1.1)

Authority: Master v1.1.

For every BLOCKER / CRITICAL / MAJOR finding run a mini-hearing:

1. Proponent brief.
2. Challenger from a different panel attacks evidence/severity/assumptions.
3. Mandatory affected domain owners analyze consequences.
4. Proponent responds.
5. Generate at least one alternative hypothesis/design.
6. Resolve status:
   CONFIRMED
   DOWNGRADED
   REJECTED_WITH_EVIDENCE
   NEEDS_RESEARCH
   NEEDS_SPIKE
   MERGED_DUPLICATE

Preserve raw disagreement.

If material disagreement remains, schedule another C02 iteration.
Do not advance merely because discussion took place.

Create:
- `CROSS_EXAMINATION_LOG.md`;
- updated `FINDINGS_REGISTER.md`;
- `RESEARCH_REQUESTS.md` / `SPIKE_REQUESTS.md` as needed;
- unresolved controversy list.

Output:
`C02_RESULT = PASS | FAIL | REQUIRES_ANOTHER_C02_ITERATION`
and
`WAITING_FOR_HUMAN_GATE_02`

STOP. Never auto-start C03.
