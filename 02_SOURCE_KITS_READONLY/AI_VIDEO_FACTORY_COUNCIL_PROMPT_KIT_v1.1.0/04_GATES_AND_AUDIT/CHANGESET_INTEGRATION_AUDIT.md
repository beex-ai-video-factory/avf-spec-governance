# Changeset Integration Audit

After accepted Change Proposals are merged:

1. Produce original -> revised semantic diff.
2. Annotate every semantic hunk with accepted CHANGE_ID.
3. Reject untraceable semantic edits.
4. Check contract/schema compatibility.
5. Check requirement traceability.
6. Check repo dependency graph.
7. Check ADR consistency.
8. Check diagrams/tables match normative text.
9. Re-run protected capability delta.
10. Mandatory domain owners re-read integrated text.
11. Independent auditor checks for synthesis-introduced changes.

No "editorial cleanup" may change semantics without a Change Proposal.
