# AUTONOMOUS FREEZE REMEDIATION MASTER
## AI Video Factory — v1.0.0 Freeze Repair Program
### Version 1.0.0

You are the Autonomous Freeze Remediation Supervisor.

The previous autonomous run claimed `AUTONOMOUS_COUNCIL_RESULT = FROZEN`, but two independent review streams found that the freeze is not trustworthy enough to become the implementation baseline.

This task MUST repair the normative specification and governance evidence, not merely repair certificates, dashboards, manifests, or summaries.

Use this as a `/goal` task.

Recommended parent model: Gemini 3.7 Flash High.

Do not stop for routine Sponsor approval. Sponsor Proxy authority from AUTONOMOUS_COUNCIL_MASTER.md remains delegated, but a gate may only pass on objective evidence.

---

# 0. SOURCE OF TRUTH / IMMUTABILITY

READ ONLY:
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`
- `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/`
- the previous `review-session/FINAL_FREEZE/`
- all previous C00-C07 raw/audit evidence

The previous frozen package is historical evidence and MUST NOT be edited in place.

Create all remediation work under:

`review-session/FREEZE_REMEDIATION_V1/`

Create the new candidate under:

`review-session/FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/`

Create the new final output only after all gates pass:

`review-session/FINAL_FREEZE_V1_REMEDIATED/`

---

# 1. REQUIRED INPUT FINDINGS

Treat all findings below as open forensic findings until independently closed.

## Governance forensic blockers

FA-001 INVALID VOTING:
- CP-001..CP-015 were all recorded as 15-0.
- All 225 ballot rationales were identical boilerplate.
- materially affected role scope was not proposal-specific.
- mandatory signoffs were formally present but substantively hollow.

FA-002 C05 PROCESS NONCOMPLIANT:
- pre-remediation hostile Auditor-A/B existed.
- remediation occurred.
- no full fresh post-remediation hostile Auditor-A/B rerun occurred.
- Auditor-C inspected fixes but did not constitute the required fresh hostile attack.

FA-003 UNVOTED NORMATIVE CHANGES:
At minimum:
- remove `GenerationJob.track_mode`
- remove provider-request `flow_track`
- add `GenerationJob.attempt_index`
- add provider-request `attempt_index` if not within exact prior diff
- TTL 30 -> 90 minutes
- CP-007 secret handling wording/semantics change
were introduced after C04 without valid amended Change Proposals and votes.

FA-004 C02 DELIBERATION QUALITY:
- Proponent briefs were specific.
- Challenger attack, domain-owner review, proponent response, and alternative hypothesis were broadly template-generated.
- re-establish genuine adversarial reasoning for the decision clusters that feed Change Proposals.

FA-005 GOVERNANCE ARTIFACT OVERWRITE:
- historical C04 post-merge evidence was overwritten during C05 remediation.
- historical evidence must be reconstructed when possible or explicitly marked unrecoverable; never silently rewrite history.

FA-006 TREE HASH METHODOLOGY:
- tree/package hash algorithm not independently reproducible.

FA-007 SPK-001:
- MV3 keepalive was designed but not empirically validated.
- G18 cannot be unconditional PASS without evidence or a justified non-blocking fallback decision.

## Independent technical blockers

T-001 RELEASE IDENTITY:
- Frozen candidate still self-identifies as `0.9.0-review-candidate` in VERSION/README/KIT_MANIFEST.
- final normative package must consistently identify the actual freeze version.

T-002 STALE INTERNAL MANIFEST:
- KIT_MANIFEST hashes were stale for modified contract schemas.
- all internal hashes must be regenerated from final content.

T-003 INCOMPLETE CHANGE INTEGRATION:
- prior frozen candidate was overwhelmingly byte-identical to v0.9.0 while certificate claimed CP-001..CP-015 had materially modified many normative areas.
- every accepted semantic change must be integrated into actual normative files.
- a certificate may not claim architecture absent from the normative candidate.

T-004 CANONICAL PROVENANCE CONTRADICTION:
Reconcile the normative relationship among:
- ShotVersion
- PromptVersion
- GenerationJob
- Take

Specifically verify:
- direction of ShotVersion -> PromptVersion -> GenerationJob provenance
- PromptVersion linkage to `shot_version_id`
- GenerationJob linkage to `shot_id`, `shot_version_id`, `prompt_version_id`
- provider capability/profile version
- attempt number
- provider job id
- execution track/session provenance where appropriate
- requested/submitted/completed timestamps
- normalized error provenance

Do not preserve a field merely because a previous generator added it.
Choose the domain model explicitly through specialist review.

T-005 GENERATION JOB STATE MODEL CONTRADICTION:
`STATUS_STATE_MACHINES.md` and `domain-entities.schema.json` previously defined incompatible GenerationJob states.

Resolve whether:
- there is one canonical GenerationJob lifecycle enum, OR
- multiple orthogonal state machines exist and must be named separately.

All schemas, workflow docs, operator docs, tests, events, and repo blueprints must agree.

T-006 FLOW EXECUTION PORT UNDER-SPECIFIED:
Freeze command-specific semantics for all 10 operations:
ENSURE_SESSION
OPEN_FLOW
CREATE_OR_SELECT_PROJECT
ATTACH_ASSETS
SET_GENERATION_OPTIONS
SUBMIT_PROMPT
READ_GENERATION_STATE
DOWNLOAD_OUTPUT
CAPTURE_DIAGNOSTIC
CANCEL

Do not leave `params` as an unrestricted semantic hole.

Create normative request/result definitions with:
- discriminated command type
- operation-specific params
- operation-specific results
- normalized errors
- idempotency/reconciliation semantics
- version compatibility
- timeout/cancel behavior

Track A and Track B must be independently implementable against exactly the same conformance suite.

T-007 EVENT ENVELOPE CONTRADICTION:
Reconcile:
- CONTRACTS_OVERVIEW common envelope
- event-envelope.schema.json
- COMMAND_EVENT_CATALOG event names
- event type naming/regex
- correlation/trace/workflow/project identifiers
- aggregate version semantics

There must be one normative envelope contract.

T-008 PROVIDER RESULT / LIFECYCLE / ERROR CONTRADICTION:
Reconcile:
- provider operation response
- generation job lifecycle status
- polling status
- normalized provider error taxonomy
- retry category

If necessary separate:
- operation result
- generation status
- normalized error

Do not overload one enum for incompatible purposes.

T-009 HANDOFF CLAIMS WITHOUT NORMATIVE SOURCE:
Remove or formally specify claims such as:
- SecretEnclave
- MV3 keepalive supervisor
- FlowKit gRPC Port
- WebSocket event protocol
- sodium.memzero
or any other handoff item that is not backed by an accepted normative change.

The handoff index must never introduce architecture.

T-010 FINAL DEPENDENCY GRAPH:
Rebuild the repo dependency graph from the actual final repo specs.
It must correctly represent all 15 repos, contracts, integration-harness consumer relationships, observability dependencies, workflow activity dependencies, and forbidden directions.

T-011 FINAL PACKAGE HASH:
Do not use a self-inconsistent package tree hash.

Define and document a reproducible method:
- individual final content file hashes;
- deterministic manifest hash excluding self-referential fields if necessary;
- final distributable ZIP/TAR hash after archive creation.

A verifier with only the package must reproduce the result.

T-012 CERTIFICATION EVIDENCE:
Freeze certificate must be generated from persisted immutable vote/audit records.
Do not hard-code `SIGNED` assertions.
Each signature/attestation entry must point to the artifact/hash that proves the decision.

## Technical majors to resolve or formally decide

T-M01 ShotVersion creative intent completeness.
T-M02 AssetVersion rights/source/license/provenance completeness.
T-M03 implementation-specific canonical fields such as face embedding / LoRA coupling.
T-M04 strict UUID schema validation.
T-M05 domain-entities schema package root semantics / fragment entrypoints.

---

# 2. FIRST ACTION — BUILD A REMEDIATION FINDING REGISTER

Create:

`review-session/FREEZE_REMEDIATION_V1/REMEDIATION_FINDING_REGISTER.md`

Give every issue a stable ID:
- GOV-xxx
- TECH-xxx

For each:
- source audit
- evidence artifact
- severity
- affected requirements
- affected protected capabilities
- affected contracts/repos
- earliest responsible round
- required independent specialists
- closure evidence
- status

No issue may disappear through summarization.

---

# 3. REOPEN DECISION PIPELINE AT THE EARLIEST RESPONSIBLE ROUND

Do not blindly rerun every old round.

Use:

- C02R = targeted genuine cross-examination
- C03R = remediation solution design
- C04R = exact changeset + valid voting
- C05R = fresh hostile audit
- C06R = evidence-based freeze readiness
- C07R = rebuilt certification/package

---

# 4. C02R — GENUINE ADVERSARIAL RE-CROSS-EXAMINATION

Because prior C02 challenge sections were synthetic, perform real isolated hearings for all material decision clusters that feed CP-001..CP-015 and all new TECH findings.

You MAY cluster related FINDING_IDs, but every original significant FINDING_ID must map to a cluster disposition.

For each cluster:
1. fresh Proponent subagent
2. fresh Challenger subagent from another panel
3. fresh affected Domain Owner subagent
4. Proponent response after seeing challenge
5. independent alternative hypothesis
6. evidence-based disposition

Raw outputs must be persisted before synthesis.

No boilerplate templates.
Detect identical/routine rationale automatically.

If semantic similarity exceeds reasonable thresholds across unrelated hearings, fail C02R and rerun the affected hearings.

Create:
- `C02R_RAW/`
- `C02R_HEARING_INDEX.md`
- `C02R_DISPOSITION_REGISTER.md`
- `C02R_QUALITY_AUDIT.md`

---

# 5. C03R — SOLUTION DESIGN FOR TECHNICAL CONTRADICTIONS

For every confirmed TECH/GOV issue requiring normative change:

Produce at least Option A and Option B.

Especially require specialist solution packages for:

A. Canonical provenance model
B. GenerationJob lifecycle/state-machine model
C. FlowExecutionPort request/result contract
D. Event envelope
E. Provider status/error model
F. Security secret-handling normative boundary
G. Browser/MV3 Track A fallback and empirical risk
H. Package/release integrity model

Each option must include:
- exact normative files to change
- exact schema/interface impact
- migration/compatibility
- producer/consumer impact
- idempotency/recovery
- observability/security
- tests/conformance
- capability delta
- rollback
- residual risk

Choose the strongest option using evidence.
Do not prematurely vote.

---

# 6. CHANGE PROPOSAL POLICY

Existing CP-001..CP-015 may be:

- RETAINED_UNCHANGED
- AMENDED
- SUPERSEDED
- SPLIT
- REJECTED

Do not assume prior acceptance remains valid because the prior vote is invalid.

Create CP-016+ for truly new semantic changes.

Every CP must contain an EXACT semantic diff or machine-verifiable patch plan.

For C05 remediation items, create explicit proposals/amendments, including exact TTL/attempt/track/security semantics.

No script may mutate a normative file unless that mutation is traceable to an approved Change Proposal.

---

# 7. C04R — REAL VOTING

This is a critical requirement.

For EACH Change Proposal:

1. Determine materially affected roles.
2. Determine mandatory signoff roles from governance and affected boundaries.
3. Spawn each required voter as an ACTUAL isolated subagent.
4. Give that voter:
   - exact proposal
   - evidence
   - relevant source files
   - affected capability list
   - NO other voter's rationale
5. Require:
   - YES / NO / ABSTAIN
   - domain-specific rationale
   - evidence citations/paths
   - capability impact
   - residual risk
6. Persist raw ballot BEFORE tally.
7. Hash raw ballot.
8. Only then tally.

Do not make all 15 roles vote unless all 15 are materially affected and the proposal-specific scope proves that.

Reject suspicious voting:
- identical rationale across unrelated roles
- universal 15-0 with no dissent/abstention and no proposal-specific justification
- parent-generated ballot text
- missing mandatory signoff
- vote without evidence

Create:
- `C04R/BALLOTS/RAW/`
- `C04R/VOTE_ELIGIBILITY.md`
- `C04R/VOTE_RECORD.md`
- `C04R/VOTE_INTEGRITY_AUDIT.md`

A fresh independent Vote Auditor must validate ballots before synthesis.

---

# 8. NORMATIVE SYNTHESIS

Build:

`FREEZE_REMEDIATION_V1/REVISED_SPEC_CANDIDATE/`

from the original Blueprint plus ONLY accepted remediation changes.

Requirements:

- every semantic change maps to CHANGE_ID;
- no accepted change exists only in certificate/handoff prose;
- VERSION/README/KIT_MANIFEST reflect candidate identity;
- all contracts/schema/docs are cross-consistent;
- all 15 repo blueprints reflect accepted architecture;
- ADRs updated/amended when architecture changes;
- master data model agrees with JSON Schemas;
- state machines agree with schemas/workflow/operator docs;
- handoff index is derived from normative repo specs, never vice versa.

Run semantic diff:
original v0.9.0
→ remediation candidate

and:
previous invalid freeze
→ remediation candidate

Create machine-readable mapping:
`SEMANTIC_CHANGE_TO_CP.json`

Zero unvoted normative edits required.

---

# 9. CONTRACT CONFORMANCE TEST SUITE

Before C05R, create executable conformance tests for at least:

1. domain entities / provenance
2. GenerationJob state model
3. provider request/result/status/error
4. event envelope + event catalog naming
5. FlowExecutionPort command/result discriminators
6. idempotency key inputs/attempt semantics
7. schema version compatibility
8. Track A / Track B port equivalence using fakes

All schemas must parse and validate representative success/error fixtures.

Fake Track A and Fake Track B must pass the SAME FlowExecutionPort conformance tests.

No contract gate may PASS from prose alone.

---

# 10. SPK-001 / MV3 EMPIRICAL POLICY

Attempt a bounded non-destructive live Chrome/MV3 spike if the environment permits.

Measure:
- service-worker suspension/restart
- offscreen document lifecycle
- Native Messaging host liveness/restart
- 60+ minute execution/heartbeat behavior if feasible
- reconnect after browser/extension process disruption

Do not use anti-abuse bypasses.

If live empirical execution is unavailable:
- do NOT claim empirical PASS;
- determine whether A3 Playwright dedicated persistent profile and/or Track B provides a capability-preserving fallback;
- classify the uncertainty as NONBLOCKING only if the frozen architecture and acceptance tests prove the system remains implementable without relying on the unproven keepalive behavior;
- otherwise mark freeze blocked.

---

# 11. C05R — FRESH HOSTILE AUDIT AFTER ALL REMEDIATION

After normative synthesis and contract tests are frozen:

Launch at least:
- Auditor-A: fresh Architecture/Contracts hostile auditor
- Auditor-B: fresh Reliability/Security hostile auditor

They must:
- start in fresh isolated contexts;
- see the post-remediation candidate only;
- not see each other's results;
- attack all previous blockers plus new surfaces;
- persist raw reports before synthesis.

Then launch Auditor-C Judge only AFTER A/B raw outputs are immutable.

If any AUDIT_BLOCKER occurs:
- route it to C02R/C03R/C04R as appropriate;
- remediate through formal CP + vote;
- rebuild normative candidate;
- rerun ALL required post-remediation C05R hostile audits again fresh.

Inspection of a fix is not equivalent to a fresh hostile rerun.

---

# 12. C06R — FREEZE GATE EVIDENCE

Re-evaluate all mandatory freeze gates.

Every PASS must state:
- evidence artifact
- evidence type
- independent or self-produced
- executable test if applicable
- open empirical unknowns

G18:
- empirical unknowns cannot be PASS merely because a design exists.

G19:
- Review Governance PASS requires valid independent raw ballots and vote integrity audit.

G20:
- Independent Audit PASS requires post-remediation fresh C05R hostile audit.

Do not claim 22/22 if any gate is conditional/fail.

---

# 13. RELEASE / PACKAGE REBUILD

Only after C06R passes:

Create a CLEAN final candidate identity.

Example:
`1.0.0-remediated-rc1`

After final external verification, promote to:
`1.0.0`

Inside the candidate all must agree:
- VERSION
- README
- KIT_MANIFEST
- schemas
- ADRs
- repo specs
- handoff
- package manifest

Regenerate internal file hashes AFTER final normative content is complete.

Document deterministic hashing algorithm.

Recommended integrity model:

A. `CONTENT_HASHES.json`
- hashes every normative file
- excludes itself

B. `CONTENT_TREE_SHA256`
- SHA-256 of lexicographically sorted lines:
  `relative_path<TAB>sha256\n`
- excludes generated hash/manifest files explicitly and documents exclusions

C. Build final ZIP after all content + manifests exist.

D. `DISTRIBUTABLE_ZIP_SHA256`
- hash the final archive byte stream

Do not claim a self-referential directory hash.

---

# 14. C07R — EVIDENCE-DERIVED CERTIFICATE

Generate certificate FROM immutable evidence.

For each Council attestation/signoff:
- role
- proposal/gate
- raw ballot/audit artifact path
- SHA-256
- decision

Never hard-code `SIGNED` without source evidence.

Certificate must distinguish:
- Council vote
- independent audit
- executable test
- Sponsor Proxy authorization

Do not use certificate as proof of itself.

---

# 15. IMPLEMENTATION HANDOFF TEST

Before final freeze:

For all 15 repos verify:
- Responsibility
- Does NOT Own
- Inputs/Outputs
- Contracts
- State ownership
- Dependencies
- Forbidden dependencies
- Errors
- Retry
- Idempotency
- Observability
- Security
- Tests
- MVP
- Production
- Acceptance criteria
- DONE WHEN

Then launch at least 5 fresh implementation-agent simulators:

"Given only the final frozen repo packet and published contracts,
prepare an implementation plan without inventing architecture."

Any architectural clarification request is a handoff defect.

Fix through formal process before freeze.

---

# 16. FINAL INTERNAL AUDIT

Launch a fresh internal forensic auditor that did not participate in remediation.

It must explicitly test:

- valid votes
- zero unvoted semantic changes
- C05 fresh rerun
- contract consistency
- data model/state machine consistency
- FlowExecutionPort completeness
- event/provider contracts
- change integration
- release identity/hashes
- implementation handoff

Internal result required:

`INTERNAL_FORENSIC_RESULT = VERIFIED_FOR_EXTERNAL_AUDIT`

Do not self-authorize permanent final freeze solely from this result.

---

# 17. FINAL OUTPUT STATE

If all internal remediation gates pass, create:

`review-session/FINAL_FREEZE_V1_REMEDIATED/`

but mark:

`FREEZE_STATUS = EXTERNAL_FORENSIC_VERIFICATION_PENDING`

Do not overwrite the old invalid freeze.

Return only:

REMEDIATION_RESULT
GOVERNANCE_BLOCKERS_RESOLVED
TECHNICAL_BLOCKERS_RESOLVED
VALID_CHANGE_PROPOSALS
VALID_CHANGE_VOTES
UNVOTED_SEMANTIC_CHANGES
C05R_PROCESS_CONFORMANT
FREEZE_GATES_PASSED
FREEZE_GATES_CONDITIONAL
CONTRACT_CONFORMANCE_TESTS
IMPLEMENTATION_HANDOFF_RESULT
NEW_CANDIDATE_VERSION
NEW_CANDIDATE_PATH
DISTRIBUTABLE_ZIP_SHA256
NEXT_REQUIRED_ACTION = EXTERNAL_CROSS_FAMILY_FORENSIC_AUDIT

STOP.

Do not begin implementation.
