# /goal Task — C00 Semantic Baseline Completion

Operate under the AVF Council Master Prompt v1.1.

CURRENT STATE:
- C00 Iteration 03 mechanical validation passed.
- Human semantic spot audit reported LOW confidence and identified four C01-blocking categories:
  contract semantics, ADR impact mapping, invariant ownership/enforcement/test mapping, and protected-capability mappings.
- Evidence Ledger was explicitly judged insufficient.
- Do NOT proceed to C01.

OBJECTIVE:
Complete C00 to a genuinely usable semantic review baseline without inventing missing specification facts.

IMPORTANT:
C00 is an inventory/review-bootstrap stage, not the stage that fixes architecture defects.
A missing value in the Blueprint is allowed to remain `NOT_SPECIFIED_IN_SOURCE` if and only if:
1. the absence is proven by semantic inspection;
2. it is registered as a review gap;
3. it has concrete C01 reviewer ownership;
4. it has a required finding/question seed;
5. its absence does not make the review baseline ambiguous.

Therefore, do NOT manufacture contract producers, ADR impacts, invariant owners, or verification semantics merely to make C00 look complete.

WORK LOOP:
Repeat autonomously until exit criteria pass:

1. Read the authoritative Blueprint documents semantically, not only by regex.
2. Cross-reference related repo blueprints, contracts, ADRs, master architecture, dependency graph, testing, security, and integration documents.
3. Improve mappings only when supported by source.
4. For unresolved source gaps create:
   `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md`
   with:
   GAP_ID
   missing semantic
   exact source inspected
   why source is insufficient
   affected requirements/capabilities
   primary C01 reviewer
   secondary/challenger reviewer
   mandatory question/finding seed
   required resolution round
   freeze impact.
5. Expand Evidence Ledger so every Protected Capability and every material external assumption is supported/challenged by at least one explicit evidence item.
6. Repair Requirement/Capability/Invariant/Contract/ADR cross-references.
7. Build C01 coverage from actual IDs, not arbitrary rotation or wildcards.
8. Validate coverage:
   - every MUST requirement >=1 primary reviewer;
   - every critical invariant >=2 different specialist lenses;
   - every public contract = Contracts reviewer + >=1 consuming-domain reviewer;
   - every C00 semantic gap has named C01 owner/challenger;
   - Flow Track A/B covered by Flow/Browser + Reliability + Security/QA.
9. Run referential-integrity validator.
10. Run source immutability validator.
11. Run a fresh internal C00 semantic auditor subagent that did NOT create the artifacts.
12. If the auditor finds a C00-baseline defect, repair and rerun validation.
13. Do not attempt to resolve architectural findings that belong in C01-C04. Seed them instead.

MODEL ESCALATION:
- Main execution: current Gemini 3.7 Flash High.
- For ambiguous BLOCKER-level cross-document semantic mapping, invoke a fresh Pro-tier subagent as an advisory verifier.
- Do not let the verifier edit source kits.

C00 EXIT CRITERIA:
- semantic baseline confidence >= MEDIUM, target HIGH;
- zero ambiguous review-baseline blockers;
- zero dangling references;
- zero unowned C01 semantic gaps;
- no arbitrary/sequential capability mappings;
- no wildcard-only C01 coverage;
- Evidence Ledger covers all 19 protected capabilities and all registered external assumptions;
- actual source gaps remain explicit rather than invented;
- source kits unchanged;
- all outputs under review-session.

Create/promote a clean candidate baseline under:
`review-session/C00_FINAL/`

Required output:
- `C00_FINAL_AUDIT.md`
- `C00_GAP_TO_C01_SEED_REGISTER.md`
- all accepted baseline inventories/matrices
- validation reports
- exact baseline hashes
- migration note from Iteration 03 to C00_FINAL.

At completion output:

C00_FINAL_RESULT = PASS | FAIL
SEMANTIC_BASELINE_CONFIDENCE = HIGH | MEDIUM | LOW
C01_BLOCKING_BASELINE_GAPS = N
C01_SEEDED_SPEC_GAPS = N
DANGLING_REFERENCES = N
SOURCE_FILES_MODIFIED = N

If and only if PASS:
`WAITING_FOR_HUMAN_GATE_00`

STOP.
DO NOT START C01.
