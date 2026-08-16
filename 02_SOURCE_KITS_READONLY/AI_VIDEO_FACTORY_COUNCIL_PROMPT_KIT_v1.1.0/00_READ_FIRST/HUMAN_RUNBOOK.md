# Human Runbook

## A. Council review

Create a working directory `review-session/YYYY-MM-DD/`.

Paste `MASTER_COUNCIL_PROMPT.md` into the Antigravity primary agent.

Ask it to create isolated subagents using role charters in `02_COUNCIL_ROLES/`.

### Context isolation rule

Round 1 reviewers receive:
- frozen candidate specification;
- evidence/source ledger;
- their own role charter;
- council rules.

They MUST NOT receive other reviewers' conclusions before submitting Round 1.

### Human authority

Human is Sponsor/Owner, not day-to-day judge.

Human may:
- add a requirement;
- reject a council decision;
- request another round;
- mark an issue as business-policy constrained.

Human should not directly edit architectural contracts during a live council round. Convert requested edits into a council change proposal.

## B. Freeze

Freeze only after:
- all mandatory gates PASS;
- no unresolved BLOCKER;
- fresh-context audit PASS;
- contract compatibility analysis PASS;
- dissent is either resolved or explicitly accepted as residual risk.

## C. Implementation

Open one repository at a time.

Provide:
- frozen master blueprint version;
- frozen contract package version;
- matching repo context profile;
- latest dependency release manifest;
- relevant ADRs only.

Then execute I00–I12.

Do not give the coding agent unrelated repository internals unless needed by contract.

## D. Integration

`avf-integration-harness` is the independent referee.

A repository's own tests are necessary but insufficient.
