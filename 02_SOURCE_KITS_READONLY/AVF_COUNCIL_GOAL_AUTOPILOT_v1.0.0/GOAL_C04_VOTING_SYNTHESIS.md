# /goal Task — C04 Exact Voting + Controlled Synthesis

Prerequisite: Human approved C03.

Use Gemini 3.7 Flash High.
For critical invariant/contract/security/data changes, use a fresh Pro-tier verifier before vote finalization.

Perform:
- exact diff finalization;
- voting eligibility/quorum;
- mandatory specialist sign-offs;
- YES/NO/ABSTAIN records;
- dissent preservation;
- accepted-change-only synthesis;
- semantic diff -> Change ID annotation;
- contract compatibility;
- requirement traceability;
- dependency validation;
- post-merge consistency check.

Autonomously repair synthesis defects, but never create a new semantic architecture decision without returning it to a formal Change Proposal/vote inside C04.

Do not start C05.

Output:
C04_RESULT
ACCEPTED_CHANGES
REJECTED_CHANGES
DEFERRED_CHANGES
UNVOTED_SEMANTIC_CHANGES = 0 required
WAITING_FOR_HUMAN_GATE_04

STOP.
