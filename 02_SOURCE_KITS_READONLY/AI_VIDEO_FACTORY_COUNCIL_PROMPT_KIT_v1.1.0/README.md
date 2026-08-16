# AI Video Factory — Council & Implementation Prompt Kit v1.1.0

## Purpose

This kit is the operating procedure for:

1. convening a multi-role expert council to review and strengthen `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0`;
2. producing evidence-backed changes without allowing any individual agent to unilaterally modify the architecture;
3. freezing a reviewed specification;
4. implementing each repository/subproject independently with coding agents;
5. verifying that independently built repositories still conform to the frozen contracts and integrate correctly;
6. preserving long-term handoff quality for future human and AI maintainers.

The kit deliberately separates:

- **architecture/specification governance** from implementation;
- **role capabilities** from third-party skill libraries;
- **independent review** from synthesis;
- **proposal** from approval;
- **implementation** from verification.

## Non-negotiable principle

The council is constructive, not defeatist.

It MUST NOT remove capabilities, modularity, recoverability, replaceability, observability, security, testability, or long-term extensibility merely because a problem is difficult.

A simplification is allowed only when it demonstrates equal-or-better satisfaction of the system invariants and acceptance criteria with lower complexity/risk.

When a difficult problem exists, the default action is:

`identify -> decompose -> research -> propose alternatives -> test/benchmark -> decide`

not:

`remove requirement because it is hard`.

## Artifacts consumed

Expected adjacent specification kit:

`AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`

The council should start from:

- `00_governance/00_REVIEWER_ENTRYPOINT.md`
- `01_master/MASTER_BLUEPRINT.md`
- `01_master/SYSTEM_INVARIANTS.md`
- `01_master/DATA_MODEL.md`
- `02_contracts/*`
- `03_repo_blueprints/*`
- `04_integration/*`
- `05_phases/*`
- `06_adrs/*`
- `07_risk/*`
- `08_evidence/*`
- `09_agent_packets/*`

## Human run order — specification review

Run prompts in this order:

1. `01_COUNCIL_MASTER/MASTER_COUNCIL_PROMPT.md`
2. `03_COUNCIL_ROUNDS/C00_BOOTSTRAP_AND_EVIDENCE.md`
3. `03_COUNCIL_ROUNDS/C01_INDEPENDENT_REVIEW.md`
4. `03_COUNCIL_ROUNDS/C02_CROSS_EXAMINATION.md`
5. `03_COUNCIL_ROUNDS/C03_SOLUTION_DESIGN.md`
6. `03_COUNCIL_ROUNDS/C04_CHANGESET_VOTING.md`
7. `03_COUNCIL_ROUNDS/C05_ADVERSARIAL_AUDIT.md`
8. `03_COUNCIL_ROUNDS/C06_FREEZE_READINESS.md`
9. `03_COUNCIL_ROUNDS/C07_FREEZE_CERTIFICATION.md`

Do not skip C05.

## Human run order — each implementation repository

For every repository R01–R15:

1. load the frozen blueprint + the matching file in `07_REPO_CONTEXT_PROFILES/`;
2. execute prompts `I00` through `I12` in `06_IMPLEMENTATION_RUNBOOK/`;
3. do not pass a gate merely because code compiles;
4. run the independent verification prompt using a fresh subagent/context;
5. publish a Repo Release Evidence Pack;
6. only then integrate it via `avf-integration-harness`.

## Required persistent review artifacts

The council maintains:

- `COUNCIL_ROSTER.md`
- `EVIDENCE_LEDGER.md`
- `ASSUMPTION_REGISTER.md`
- `FINDINGS_REGISTER.md`
- `DISSENT_REGISTER.md`
- `CHANGE_PROPOSALS/`
- `DECISION_LOG.md`
- `TRACEABILITY_MATRIX.md`
- `GATE_RESULTS.md`
- `FREEZE_CERTIFICATE.md`

No result exists only in chat memory.

## Third-party skills

Skills are optional execution aids, not architecture authorities.

Recommended policy:

- Superpowers: process discipline/TDD/review/verification.
- ECC: selectively supply specialist roles/skills.
- Do NOT inject every available skill into every agent.
- Pin repository/skill versions.
- Audit skill source and permissions before enabling.
- Create per-role allowlists.
- Freeze skill versions during a council session and during a repository implementation cycle.
- Record skill name/version/hash in evidence outputs.

See `05_SKILL_ADAPTERS/`.

## Version

Prompt kit: `1.1.0`

Specification target at creation: `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0`

## v1.1 governance hardening

Added protected capability baseline, evidence grades, formal cross-examination, quorum/voting scope, exact human round gates, post-vote semantic-diff audit, requirement traceability, and stronger implementation-handoff freeze criteria.
