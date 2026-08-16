# Decision Audit Rules

Every architecture decision must be reconstructable as:

`requirement/evidence -> finding -> cross-examination -> solution options -> exact proposal -> vote -> test/benchmark -> gate -> decision`

If any link is missing, the decision is not auditable.

Mandatory metadata:
- session id;
- reviewer role;
- model;
- reasoning mode if selectable;
- skills + versions/hashes;
- source/spec version;
- timestamp;
- affected files/contracts;
- vote;
- dissent;
- evidence references.

Council narrative summaries are convenience artifacts only.
Registers and exact proposals are authoritative.
