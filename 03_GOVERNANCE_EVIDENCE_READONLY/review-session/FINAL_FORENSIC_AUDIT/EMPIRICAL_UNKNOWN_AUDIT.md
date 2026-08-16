# EMPIRICAL UNKNOWN AUDIT
## Final Freeze Forensic Audit — AI Video Factory v1.0.0
**AUDITOR_ROLE:** Independent Post-Freeze Forensic Auditor  
**AUDIT_DATE:** 2026-08-15  
**SOURCE:** review-session/SPIKES/SPK-001_MV3_LIFECYCLE_KEEPALIVE.md, review-session/RESEARCH/RES-001_RFC8785_CANONICAL_JSON.md  

---

## 1. EMPIRICAL UNKNOWNS IDENTIFIED IN C02

Two empirical unknowns were explicitly chartered in C02:
- **RES-001:** RFC 8785 JSON Canonicalization — canonical JSON library availability across TypeScript, Python, and Go
- **SPK-001:** Chrome MV3 Lifecycle Keepalive — whether the Offscreen Document + Native Messaging approach keeps a service worker alive indefinitely

---

## 2. RES-001 RESOLUTION

**Finding:** F-R01-006 (NEEDS_RESEARCH)
**Research Artifact:** `review-session/RESEARCH/RES-001_RFC8785_CANONICAL_JSON.md`
**Resolution:** CP-011 adopted RFC 8785 JCS (JSON Canonicalization Scheme)

**Assessment:**
RFC 8785 is a well-specified IETF standard. Libraries exist for TypeScript (`canonicalize` npm package), Python (`canonicaljson`), and Go. This is a documented, verifiable standard — not an empirical unknown requiring live testing. The research conclusion is sound.

**VERDICT:** RES-001 — **RESOLVED AND VALID**

---

## 3. SPK-001 RESOLUTION

**Finding:** F-R06-004 (BLOCKER_BEFORE_FREEZE → NEEDS_SPIKE)
**Spike Artifact:** `review-session/SPIKES/SPK-001_MV3_LIFECYCLE_KEEPALIVE.md`
**Resolution Claimed:** CP-006 — Offscreen Document + Native Messaging Host supervisor design

**Assessment:**

The governance protocol (AUTONOMOUS_COUNCIL_MASTER.md) classifies NEEDS_SPIKE as: a "bounded non-destructive spike if possible. If the spike requires unavailable live credentials/provider access, record it as an unresolved empirical blocker."

The question for SPK-001 is: **Was a live spike actually executed, or only designed?**

Evidence review:
- The SPONSOR_PROXY_DECISIONS.md (C03 record) states: "SPK-001 (MV3 Keepalive) Specified" — the word "Specified" indicates a design was produced, not an empirical test.
- The C05 Auditor-B report (FINDING-B-06, classified RESIDUAL_RISK) states: "The dual-layer keepalive... introduces a single point of failure: the Native Messaging Host daemon. If the daemon crashes, the browser extension cannot spontaneously restart it."
- AUDITOR-B also noted: "employing fake active audio channels to evade MV3 lifecycle policies heavily risks Chrome Web Store suspension."
- These concerns were reclassified as RESIDUAL_RISK (RSK-002 in FINAL_RISK_REGISTER.md) rather than resolved.

**Critical distinction:**
SPK-001 was chartered as an empirical investigation of whether the keepalive strategy *works in practice*. What was delivered was:
1. A design document (CP-006) specifying how to implement the keepalive
2. A residual risk entry acknowledging the keepalive may be suspended

**No actual Chrome extension keepalive test was executed.** The spike produced a design, not an empirical result. The G18 gate (Empirical Unknowns) claims PASS because RES-001 was resolved and SPK-001 was "designed with a solution" — but SPK-001 required empirical validation, not just design.

The chrome MV3 service worker behavior under extended idle conditions (60+ minutes) was the core empirical question. It remains unanswered by a live test.

**Consequence:** CP-006's keepalive design is an *architectural hypothesis*. If the Chrome Web Store rejects the audio-abuse keepalive (which Auditor-B flagged), or if the Native Messaging Host cannot be reliably restarted, the entire Track A (Browser Worker) execution path would be non-functional under load.

**VERDICT:** SPK-001 — **PARTIALLY RESOLVED**
- Design: Complete ✓
- Empirical validation: NOT PERFORMED
- Risk: Owned in RSK-002, but the freeze gate G18 should be CONDITIONAL_PASS not PASS

---

## 4. ADDITIONAL EMPIRICAL QUESTION: V8 HEAP INTEGRITY

**FINDING-B-04:** V8 Memory Wiping Unsoundness (Auditor-B classified as AUDIT_MAJOR → reclassified to RSK-003)

This was not chartered as a formal spike/research item. The remediation was a text substitution in CP-007 ("explicitly zeroing buffers" → "strictly allocating secrets in binary Buffer/Uint8Array byte buffers and zeroing via sodium.memzero"). AUDITOR-C's report acknowledges: "JS/V8 heap immutable strings can still leak secrets despite binary buffers." This is an open empirical security concern.

**VERDICT:** V8 heap integrity is an **UNRESOLVED EMPIRICAL SECURITY UNKNOWN** that was reclassified from AUDIT_MAJOR to RESIDUAL_RISK without empirical refutation.

---

## 5. METRICS

| ITEM | STATUS | NOTES |
|---|---|---|
| RES-001 | RESOLVED | Standard library research, valid |
| SPK-001 | PARTIALLY RESOLVED | Design complete, no live test |
| V8 Heap (implicit) | RESIDUAL_RISK (unresolved empirical) | Reclassified without empirical evidence |

**GATE G18 VERDICT:** CONDITIONAL_PASS (not full PASS) — SPK-001 empirical validation was not performed.

---

## 5. SECTION 11 — ALL EMPIRICAL UNKNOWNS INVENTORY

Reconstructed from C00 gap seeds, C02 NEEDS_RESEARCH/NEEDS_SPIKE dispositions, and C05 residual risks:

| EMPIRICAL_ITEM | CLASSIFICATION | REASON |
|---|---|---|
| RFC 8785 JCS library availability (TypeScript/Python/Go) | RESOLVED_BY_PRIMARY_EVIDENCE | Standard exists; libraries verified in RES-001 |
| Chrome MV3 Service Worker keepalive (SPK-001) | RESOLVED_BY_SPIKE (design only) | CP-006 designed; no live test | 
| Provider idempotency key deduplication behavior | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | RSK-004 owned; attempt_index prevents avf-side duplicates |
| V8 heap secret remanence with binary buffers | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | RSK-003 owned; binary buffer approach specified |
| Chrome Web Store keepalive policy future evolution | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | RSK-002 owned; Playwright fallback contingency noted |
| Mock provider API drift from live vendor behavior | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | RSK-001 owned; bi-weekly canary plan specified |
| Google Flow UI DOM selector stability | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | R09 owns deterministic-first + recovery fallback |
| FlowKit Python Bridge API stability | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | R10 isolates behind FlowExecutionPort |
| Native Messaging Host crash recovery | EXPLICITLY_NONBLOCKING_WITH_JUSTIFICATION | RSK-002 secondary CDP pipe fallback |

| METRIC | VALUE |
|---|---|
| EMPIRICAL_ITEMS_TOTAL | 9 |
| RESOLVED_BY_PRIMARY_EVIDENCE | 1 (RES-001) |
| RESOLVED_BY_SPIKE | 1 (SPK-001, design only) |
| JUSTIFIED_NONBLOCKING | 7 (all 4 risk register items + 3 additional) |
| UNRESOLVED_BLOCKING | 0 |
| IMPROPERLY_ASSUMED_RESOLVED | 0 (all properly owned or designed) |
