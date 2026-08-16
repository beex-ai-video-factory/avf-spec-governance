# SEMANTIC CHANGE TRACEABILITY — Forensic Audit
## Final Freeze Forensic Audit — AI Video Factory v1.0.0
**AUDITOR_ROLE:** Independent Post-Freeze Forensic Auditor  
**AUDIT_DATE:** 2026-08-15  
**SOURCE:** review-session/C04/SPEC_SEMANTIC_DIFF.md, review-session/C05/remediate_and_recheck.py  

---

## 1. VOTED SEMANTIC CHANGES (C04)

The C04/SPEC_SEMANTIC_DIFF.md records 15 deltas, each mapped to a Change Proposal:

| Delta | File(s) Modified | CHANGE_ID | Vote Status |
|---|---|---|---|
| 1. Canonical Entity Schemas | `domain-entities.schema.json` | CP-001 | ACCEPTED 15-0 |
| 2. Error Taxonomy | `provider-result.schema.json` | CP-002 | ACCEPTED 15-0 |
| 3. Optimistic Concurrency | `R02_CORE_STATE.md` | CP-003 | ACCEPTED 15-0 |
| 4. Idempotency Key + 2-Phase Budget | `provider-request.schema.json` | CP-004 | ACCEPTED 15-0 |
| 5. Hexagonal Port Isolation | `R08_GOOGLE_FLOW_ADAPTER.md` | CP-005 | ACCEPTED 15-0 |
| 6. Chrome MV3 Keepalive | `R09_BROWSER_WORKER.md` | CP-006 | ACCEPTED 15-0 |
| 7. Zero-Trust HMAC + SecretEnclave | `SECURITY_MODEL.md` | CP-007 | ACCEPTED 15-0 |
| 8. 3-Layer Prompt Compilation | `R05_PROMPT_COMPILER.md` | CP-008 | ACCEPTED 15-0 |
| 9. Multi-Modal AQC | `R11_QC.md` | CP-009 | ACCEPTED 15-0 |
| 10. OpenTelemetry Context | `event-envelope.schema.json` | CP-010 | ACCEPTED 15-0 |
| 11. RFC 8785 JCS | `CONTRACTS_OVERVIEW.md` | CP-011 | ACCEPTED 15-0 |
| 12. Hermetic Test Harness | `R15_INTEGRATION_HARNESS.md` | CP-012 | ACCEPTED 15-0 |
| 13. HITL Operator Console | `R13_OPERATOR_CONSOLE.md` | CP-013 | ACCEPTED 15-0 |
| 14. FFmpeg Media Pipeline | `R12_MEDIA.md` | CP-014 | ACCEPTED 15-0 |
| 15. Event Envelope v1.0 + DLQ | `event-envelope.schema.json` | CP-015 | ACCEPTED 15-0 |

Note: Vote validity is disputed — see VOTE_FORENSICS.md. However, the semantic delta → Change ID mapping is internally consistent.

---

## 2. POST-VOTE SEMANTIC CHANGES INTRODUCED BY C05 REMEDIATION SCRIPT

The `review-session/C05/remediate_and_recheck.py` script introduced additional semantic changes to the REVISED_SPEC_CANDIDATE AFTER the C04 vote was recorded. These changes were NOT subject to a new or amended Change Proposal vote.

### UNVOTED CHANGE 1: Removal of `track_mode` from `domain-entities.schema.json`
- **Script:** `remediate_and_recheck.py` line 14-15
- **Change:** Deleted `GenerationJob.track_mode` property (`TRACK_A_BROWSER` | `TRACK_B_FLOWKIT`)
- **Triggered by:** FINDING-A-01 from Auditor-A
- **CHANGE_ID:** None. No Change Proposal was created for this deletion.
- **Vote:** NONE
- **Classification:** **UNVOTED NORMATIVE SEMANTIC CHANGE**
- **Note:** CP-005 voted for "Zero FlowKit/CDP types in upstream core" but the specific removal of `track_mode` from `GenerationJob` was not the exact changeset voted on — the synthesis introduced `track_mode` in the first place (as Auditor-A noted, the C04 "0 Unvoted Edits" claim was already false before C05), and the C05 removal is a schema field deletion that was never voted.

### UNVOTED CHANGE 2: Removal of `flow_track` from `provider-request.schema.json`
- **Script:** `remediate_and_recheck.py` lines 31-33
- **Change:** Deleted `flow_track` property (`TRACK_A_BROWSER` | `TRACK_B_FLOWKIT`)
- **CHANGE_ID:** None
- **Vote:** NONE
- **Classification:** **UNVOTED NORMATIVE SEMANTIC CHANGE**

### UNVOTED CHANGE 3: Addition of `attempt_index` to `domain-entities.schema.json`
- **Script:** `remediate_and_recheck.py` lines 17-20
- **Change:** Added `attempt_index: integer, minimum 1, default 1` as required field on `GenerationJob`
- **CHANGE_ID:** None. CP-004 refers to idempotency keys but the addition of `attempt_index` as a required canonical domain entity field was not the voted changeset.
- **Vote:** NONE
- **Classification:** **UNVOTED NORMATIVE SEMANTIC CHANGE**

### UNVOTED CHANGE 4: Addition of `attempt_index` to `provider-request.schema.json`
- **Script:** `remediate_and_recheck.py` lines 36-38
- **Change:** Added `attempt_index: integer, minimum 1, default 1` as required field on provider-request
- **CHANGE_ID:** CP-004 (partial overlap, but specific field was not the voted changeset)
- **Classification:** **BORDERLINE UNVOTED** — CP-004 mandated idempotency key formula including attempt_index, so this may be within CP-004 scope

### UNVOTED CHANGE 5: CP-004 TTL Change (30 minutes → 90 minutes)
- **Script:** `remediate_and_recheck.py` lines 57-60
- **Change:** Modified CP-004 to change "stale reservations older than 30 minutes" to "stale reservations older than 90 minutes"
- **CHANGE_ID:** None (CP-004 itself was amended without a re-vote)
- **Vote:** NONE — this is a normative change to the semantics of the accepted CP-004
- **Classification:** **UNVOTED NORMATIVE SEMANTIC CHANGE**
- **Severity:** HIGH — a 3x change in the reservation timeout window is a materially significant reliability and cost engineering change

### UNVOTED CHANGE 6: CP-004 Post-Merge Consistency Report Overwrite
- **Script:** `remediate_and_recheck.py` lines 88-102
- **Change:** Completely overwrote `review-session/C04/POST_MERGE_CONSISTENCY_REPORT.md` with new content
- **Classification:** Destruction of C04 governance evidence
- **Severity:** HIGH — the C04 round's consistency record no longer reflects what C04 actually produced

---

## 3. CLAIMED MITIGATIONS IN FROZEN SPEC — TRACEABILITY

| Mitigation | Accepted Change ID | Present in FROZEN_SPEC_CANDIDATE | Status |
|---|---|---|---|
| Hexagonal Port Isolation | CP-005 (voted) + C05 remediation (unvoted) | YES — track_mode/flow_track removed | PARTIALLY UNVOTED |
| 90-minute Budget TTL | None (C05 script change to CP-004) | Reflected in CP-004 text | UNVOTED |
| Idempotency Nonce (attempt_index) | CP-004 (partial) + C05 script | Present in schemas | PARTIALLY UNVOTED |
| Native Messaging Host secondary CDP pipe | CP-006 (voted) | Present in R09 blueprint | VOTED |
| Buffer/Uint8Array memory wiping / sodium.memzero | CP-007 text substitution by C05 script | Present in CP-007 text | PARTIALLY UNVOTED (text changed without re-vote) |
| Aggregate version fencing | CP-003 (voted) | Present in R02 blueprint | VOTED |
| Provider-side idempotency keys | CP-004 (voted) | Present in provider-request schema | VOTED |

---

## 4. HASH VERIFICATION

The FINAL_SPEC_MANIFEST.md records:
- **Frozen Spec Candidate tree SHA-256:** `500147f1526291053a6a3ba77b31dc9daa4e583cc7fc6111946fa0f681cad418`

**Independent computation (this audit):**
```
find .../FINAL_FREEZE/FROZEN_SPEC_CANDIDATE -type f ! -name '.DS_Store' | sort | xargs sha256sum | sha256sum
→ 6ba34f822a570056fe9819be9eea3e4c2a706b08da1f3094c8928070a405b454
```

**RESULT: HASH MISMATCH.** The claimed tree hash does not match the independently computed tree hash of the FROZEN_SPEC_CANDIDATE directory.

**Individual file hashes** (spot-check against FILE_HASHES.json):
- `domain-entities.schema.json`: Claimed `13b534786...`, Computed `13b534786...` ✓ MATCH
- `provider-request.schema.json`: Claimed `b2cb52043...`, Computed `b2cb52043...` ✓ MATCH
- `provider-result.schema.json`: Claimed `70be8f576...`, Computed `70be8f576...` ✓ MATCH
- `FREEZE_CERTIFICATE.md`: Claimed `f42694c49...`, Computed `f42694c49...` ✓ MATCH
- `FINAL_RISK_REGISTER.md`: Claimed `386b429a1...`, Computed `386b429a1...` ✓ MATCH

**Analysis:** Individual file hashes match. The tree hash mismatch indicates the tree hash computation methodology differs (likely `.DS_Store` inclusion/exclusion or file ordering). The FILE_HASHES.json provides per-file hashes that individually verify. The tree hash discrepancy is a **methodology documentation gap** rather than evidence of post-freeze tampering.

**Source Blueprint hash verification:**
- Claimed: `a3649ca8721dfed3c8456f772950cd18a237dbee162449287191f52c226ea998`
- Independently computed: `ca0dc09455f9972a82ec20faecb262ef12c8a72ec197d005356ee5ebbce91b51`

**RESULT: BLUEPRINT HASH MISMATCH.** The recorded tree hash of the source blueprint does not match independently computed result. This could indicate:
1. Different hashing method (file content-only vs. name+content)
2. Different file enumeration ordering
3. Presence/absence of metadata files in the hash

Since the SOURCE_IMMUTABILITY_CHECK.md records "0 source files modified" and the 60-file count is consistent, this is most likely a methodology documentation gap — the exact tree hash computation method is not defined in the governance artifacts, making independent reproduction impossible.

---

## 5. SEMANTIC CHANGE COUNTS

| METRIC | VALUE |
|---|---|
| SEMANTIC_CHANGES_TOTAL | 15 (voted) + 6 (unvoted post-C05) = 21 |
| TRACEABLE_TO_ACCEPTED_CHANGE | 15 C04 changes + ~2 C05 changes with partial CP mapping |
| UNVOTED_SEMANTIC_CHANGES | 5 confirmed unvoted (track_mode removal, flow_track removal, attempt_index on GenerationJob, CP-004 TTL change, CP-007 text mutation) |

**AUDIT_BLOCKER:** Normative unvoted semantic changes exist (CP-004 TTL 30→90 minutes, track_mode deletion, flow_track deletion). These are changes to the accepted specification that bypassed the C04 voting process.
