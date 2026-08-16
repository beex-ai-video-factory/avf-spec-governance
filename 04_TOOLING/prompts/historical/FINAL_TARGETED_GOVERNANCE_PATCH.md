# FINAL TARGETED GOVERNANCE PATCH
## AI Video Factory — Remediated Freeze Final Repair
### Scope: Only the blockers found by FINAL_REMEDIATED_FORENSIC_AUDIT

Run as a `/goal` in the SAME Gemini 3.7 Flash High remediation conversation.

Do NOT restart C00-C07.
Do NOT redo already-valid technical remediation.
Do NOT modify original source kits.
Preserve all existing genuine and synthetic audit evidence.

Your task is to repair only the remaining forensic blockers and then rebuild the remediated freeze candidate for one final external cross-family audit.

## Authoritative blocker source
Read:
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/FINAL_REMEDIATED_FORENSIC_REPORT.md
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/FINAL_BLOCKER_REGISTER.md
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/C02R_COVERAGE_AUDIT.md
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/C04R_VOTE_FORENSICS.md
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/C05R_PROCESS_AUDIT.md
- review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/RELEASE_INTEGRITY_AUDIT.md

## 1. Correct the forensic counting inconsistency first
The forensic report says "8 CPs without genuine hearing basis" but the explicit affected set is:

CP-010
CP-011
CP-012
CP-013
CP-014
CP-015
CP-022
CP-023
CP-024

That is 9 CPs.

Treat the explicit CP set as authoritative unless direct evidence proves otherwise.

Record:
FORENSIC_CP_COUNT_CORRECTION = 9

Do not silently preserve an incorrect count.

## 2. Genuine C02R for missing clusters only
Launch actual isolated subagents for:

CLUSTER-09 — Repository Dependency Architecture
CLUSTER-10 — Prompt AST + Asset Continuity
CLUSTER-11 — QC + Media + DLQ
CLUSTER-12 — Release Integrity + Hashing + Certification

For each cluster invoke:
- fresh Proponent
- fresh Challenger
- fresh Domain Owner

Persist each raw output independently in a new directory, e.g.:
review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW_PATCH/

Do not parent-author role content.

After initial outputs:
- provide Challenger output to Proponent for a response via actual subagent message/second invocation;
- obtain an independent alternative hypothesis if not already present;
- synthesize only after raw evidence is frozen.

Map every affected CP to genuine hearing basis:
CP-010, CP-011, CP-012, CP-013, CP-014, CP-015, CP-022, CP-023, CP-024.

If CP-022 does not logically belong to Cluster-12, assign it to the correct genuine cluster or run a dedicated supplemental hearing.

## 3. Re-evaluate affected Change Proposals
For each of the 9 affected CPs classify:
RETAIN_UNCHANGED
AMEND
SUPERSEDE
REJECT

Do not automatically preserve the old proposal.

If any semantic content changes:
- create exact amended CP;
- update semantic diff;
- rerun only affected voter set.

If unchanged:
- explicitly record that genuine deliberation independently confirmed the proposal.

## 4. Resolve CP-015 Secretary inconsistency correctly
Inspect Council governance definitions.

Determine whether Council Secretary is voting or non-voting.

If governance defines Secretary as non-voting:
- REMOVE Council Secretary from mandatory voting/signoff eligibility for CP-015;
- preserve Secretary only as non-voting record/certification role if appropriate;
- do NOT manufacture a ballot.

If governance actually grants Secretary voting/signoff authority:
- invoke the real Secretary subagent and obtain the required independent signoff.

Record the exact governing source that determines this.

## 5. Correct ballot accounting
Actual genuine ballot filesystem count is 84 before any patch votes.

Fix all stale 86-ballot claims in:
- FINAL_INTERNAL_FORENSIC_AUDIT_REPORT.md
- C05R Judge Report
- C06R/GATE_RESULTS.md
and any other generated summary.

If affected CPs are re-voted, recompute the final count from actual genuine ballot files rather than hard-coding a number.

Required:
BALLOTS_ON_DISK = N
BALLOTS_IN_VOTE_RECORD = N
BALLOTS_IN_JUDGE_REPORT = N
BALLOTS_IN_GATE_RESULTS = N
ALL_BALLOT_COUNTS_MATCH = YES

## 6. Genuine re-vote only if required
If genuine C02R changes the basis or content of any affected CP, invoke real isolated materially affected voters for those proposals only.

No parent-authored ballots.
No synthetic vote rationale.
No predetermined YES requirement.

Persist and hash real raw ballots before tally.

Independent Vote Auditor must be an actual isolated non-voting subagent.

## 7. Re-run C05R after governance/semantic patch
If any CP semantics or vote outcomes change:
- run fresh isolated Auditor-A
- run fresh isolated Auditor-B
- persist A/B raw reports
- run fresh Auditor-C Judge afterward

If no normative semantics change but governance evidence changes:
- at minimum invoke a fresh Auditor-C/Judge to re-adjudicate the corrected evidence,
  and run A/B again if required by the remediation governance rules.

Judge must inspect actual filesystem counts and genuine paths.
No stale "86" count.
No stale RAW path.

## 8. Fix G18 wording only, not evidence
Keep:
G18 = CONDITIONAL_PASS

unless new evidence changes it.

Replace unsupported wording such as:
"fallback proven"

with:
"fallback architecture specified and conformance-tested; MV3 long-duration reliability remains empirically unproven but non-blocking because alternate conforming execution paths preserve capability."

Never claim anti-bot avoidance or 99.9% availability without primary evidence.

Security challenge/CAPTCHA remains:
HUMAN_REQUIRED / BLOCKED_PROVIDER
with no bypass.

## 9. Resolve advisory technical documentation mismatches
Without changing architecture unless necessary:
- align execution-stage count (11 vs 17) with the actual normative schema;
- fix malformed JSON `$ref` / `$defs` serialization if confirmed;
- close FlowExecutionResult open-typing gap if it is still a normative contract defect.

Any semantic fix requires a Change Proposal and valid vote.
Purely factual summary correction does not.

## 10. Complete Stage-D package integrity
After all final content is stable:

Create the final distributable ZIP.

Compute SHA-256 of the exact archive byte stream.

Record it in:
review-session/FINAL_FREEZE_V1_REMEDIATED/DISTRIBUTABLE_ZIP_SHA256

Also record it in FINAL_SPEC_MANIFEST.md.

Verify independently:
shasum -a 256 AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip

The documented digest must match exactly.

## 11. Rebuild evidence-derived summaries
Regenerate:
- C02R hearing index
- disposition register
- vote record
- vote integrity report
- C05R judge report
- C06R gate results
- internal forensic report
- Freeze Certificate
- final manifest

All numbers must be derived from actual artifacts, never constants.

## 12. Final self-check before external audit
Required:

GENUINE_C02R_CLUSTERS = 12
MISSING_GENUINE_CLUSTERS = 0

AFFECTED_CPS_WITH_GENUINE_HEARING_BASIS = 9/9
CHANGE_PROPOSALS_WITHOUT_GENUINE_HEARING_BASIS = 0

CP015_SECRETARY_ROLE = VOTING | NON_VOTING
CP015_SIGNOFF_VALID = YES

ALL_BALLOT_COUNTS_MATCH = YES
INVALID_BALLOTS = 0
UNVOTED_SEMANTIC_CHANGES = 0

C05R_PROCESS_CONFORMANT = YES
G18 = CONDITIONAL_PASS

DISTRIBUTABLE_ZIP_SHA256_RECORDED = YES
ZIP_HASH_VERIFIED = YES

## Final result
Return only:

TARGETED_PATCH_RESULT =
READY_FOR_FINAL_EXTERNAL_AUDIT | BLOCKED

GENUINE_C02R_CLUSTERS
CHANGE_PROPOSALS_WITHOUT_GENUINE_HEARING_BASIS

CP015_SECRETARY_ROLE
CP015_SIGNOFF_VALID

FINAL_GENUINE_BALLOTS
YES
NO
ABSTAIN
ALL_BALLOT_COUNTS_MATCH

UNVOTED_SEMANTIC_CHANGES
C05R_PROCESS_CONFORMANT
G18

ZIP_HASH_VERIFIED
DISTRIBUTABLE_ZIP_SHA256

NEXT_REQUIRED_ACTION =
FINAL_EXTERNAL_CROSS_FAMILY_AUDIT | HUMAN_INTERVENTION

STOP.
Do not start implementation.
