# I12 — Repository Release Evidence Gate

A release candidate requires:

- frozen contract version recorded;
- all mandatory tests green;
- contract conformance pass;
- independent code review pass;
- security/failure audit pass;
- observability gate pass;
- no unresolved CRITICAL/BLOCKER;
- migrations tested where applicable;
- documentation/handoff pass;
- dependency version manifest;
- reproducible build/test commands;
- release notes;
- residual risk register.

Produce `REPO_RELEASE_EVIDENCE_PACK.md`.

Only integration harness / release authority can accept it into the system compatibility set.
