# G18 EMPIRICAL AUDIT
## Independent Assessment of SPK-001 / MV3 Conditional Pass Claim — Second Run
**AUDITOR:** Final Independent Cross-Family Forensic Auditor
**DATE:** 2026-08-16
**TARGET:** G18 gate, CONDITIONAL_PASS claim, test_08_spk001_mv3_fallback_spike.py
**AUDIT_CYCLE:** Second run — prior ADVISORY-02 (certificate "proven" overclaim) now resolved

---

## 1. G18 Claim Under Review (Updated Documents)

The audit mandate (§11) states G18 may remain CONDITIONAL_PASS only if:
1. MV3 reliability remains empirically unproven unless primary evidence exists
2. No unsupported 99.9% availability claim
3. No unsupported claim that Playwright avoids bot/anti-abuse detection
4. No anti-abuse bypass
5. CAPTCHA/security challenges → HUMAN_REQUIRED or BLOCKED_PROVIDER
6. A3/Track B preserve capability through the same upstream contract
7. Flag CERTIFICATE_OVERCLAIM if fallbacks were "proven" when only architecture/conformance evidence exists

**Current FREEZE_CERTIFICATE.md G18 wording (updated 2026-08-16):**
> "Conditional Pass: 1 (G18 — Fallback architecture specified and conformance-tested; MV3 long-duration reliability remains empirically unproven but non-blocking because alternate conforming execution paths preserve capability.)"

**Current C06R/GATE_RESULTS.md G18 entry:**
> "G18 — Spikes & Feasibility — CONDITIONAL_PASS — Evidence: test_08_spk001_mv3_fallback_spike.py, ADR-004 — Open unknowns: fallback architecture specified and conformance-tested; MV3 long-duration reliability remains empirically unproven but non-blocking because alternate conforming execution paths preserve capability. Security challenge/CAPTCHA encounters strictly trigger HUMAN_REQUIRED / BLOCKED_PROVIDER with no automated bypass."

---

## 2. Nature of test_08_spk001_mv3_fallback_spike.py

The test is a conformance/harness test for fallback logic:
- Name: "fallback_spike" — confirms it tests fallback path behavior, not live MV3 keepalive measurement
- C05R Judge Report §4.4: "SPK-001 MV3 Session Recovery & Fallback — 4/4 assertions — PASSED"
- The test validates: when MV3 worker encounters lifecycle suspension → session safely recovered via A3 Playwright persistent context re-attach without resubmitting prompts or corrupting active generation state

**Critical distinction:** This is a CONFORMANCE test of the FALLBACK MECHANISM, not empirical measurement of MV3 keepalive reliability over 60+ minutes in a live Chrome browser.

**The test passes because:** The A3 Playwright fallback path is correctly implemented in the spec — it does not claim the MV3 primary path is reliable.

---

## 3. Each Condition Verification

### Condition 1: MV3 reliability empirically unproven
**Current wording:** "MV3 long-duration reliability remains empirically unproven"
**VERDICT: HONEST — condition met ✓**

### Condition 2: No 99.9% availability claim
**Check:** No such claim found in FREEZE_CERTIFICATE.md, C06R/GATE_RESULTS.md, or C05R reports.
**VERDICT: CLEAN ✓**

### Condition 3: No claim Playwright avoids bot/anti-abuse detection
**C05R Auditor-B:** "The system never attempts automated evasion or bypass of security challenges."
**INV-012:** Strictly forbids CAPTCHA bypass.
**VERDICT: CLEAN ✓**

### Condition 4: No anti-abuse bypass
**SYSTEM_INVARIANTS.md INV-012:** Explicitly forbids automated bot/anti-abuse bypass.
**VERDICT: CLEAN ✓**

### Condition 5: CAPTCHA/security challenges → HUMAN_REQUIRED or BLOCKED_PROVIDER
**C06R/GATE_RESULTS.md:** "Security challenge/CAPTCHA encounters strictly trigger HUMAN_REQUIRED / BLOCKED_PROVIDER with no automated bypass."
**C05R Auditor-B:** "when Google Flow or Cloudflare triggers a CAPTCHA, bot challenge, or re-authentication prompt, the worker immediately traps the event, emits SECURITY_CHALLENGE with retry_category = POLICY_BLOCKED."
**VERDICT: CLEAN ✓**

### Condition 6: A3/Track B preserve capability through same upstream contract
**test_07_track_a_track_b_equivalence.py:** FakeTrackABrowserWorker and FakeTrackBFlowKitBridge both pass identical FlowExecutionPort conformance tests.
**VERDICT: VERIFIED ✓**

### Condition 7: No CERTIFICATE_OVERCLAIM for "proven"
**Prior audit finding (ADVISORY-02):** FREEZE_CERTIFICATE.md previously said "empirical fallback proven via A3 Playwright / Track B" — the word "proven" overclaimed conformance as empirical proof.

**Current FREEZE_CERTIFICATE.md:** "Fallback architecture specified and conformance-tested; MV3 long-duration reliability remains empirically unproven but non-blocking because alternate conforming execution paths preserve capability."

**Analysis:** The word "proven" has been removed. The wording now correctly distinguishes:
- "architecture specified" = design exists ✓
- "conformance-tested" = test_07 and test_08 pass ✓  
- "empirically unproven" = live Chrome 60+ min not tested ✓
- "non-blocking because..." = honest justification for conditional pass ✓

**VERDICT: CERTIFICATE_OVERCLAIMS = 0 (corrected) ✓**

---

## 4. G18 Architecture Fallback Logic Assessment

**The audit mandate §11 states:** "Architecture fallback can make MV3 uncertainty non-blocking without claiming empirical reliability."

**Does the current architecture satisfy this?**

The 3-tier execution hierarchy:
- Tier A1: Native Messaging (MV3 primary) — empirically uncertain for 60+ min keepalive
- Tier A2: Loopback WebSocket (MV3 variant) — same uncertainty
- Tier A3: Playwright dedicated persistent profile — NOT subject to MV3 service worker suspension
- Track B: FlowKit Bridge — entirely separate HTTP-based implementation, no browser dependency

**Key insight:** The spec does NOT rely on MV3 keepalive being reliable. The FlowExecutionPort contract is implemented by both Track A (with A3 fallback when A1/A2 fail) and Track B. Full generation capability is preserved through Track B or Track A3 even if MV3 service workers are unreliable.

**VERDICT: G18 CONDITIONAL_PASS IS ARCHITECTURALLY JUSTIFIED. The uncertainty is non-blocking because capability is preserved through fallback paths without empirical reliance on MV3 keepalive.**

---

## 5. Summary

| Claim | Evidence | Verdict |
|---|---|---|
| G18 CONDITIONAL_PASS classification | Correctly labeled — empirical gap acknowledged | APPROPRIATE ✓ |
| MV3 keepalive empirically validated | Not validated — 60+ min live Chrome test not performed | CORRECTLY UNPROVEN |
| test_08 is empirical spike | Conformance/harness test only | CONFIRMED HARNESS (honest) |
| 99.9% availability claim | Not made | CLEAN ✓ |
| Anti-abuse bypass | Explicitly forbidden by INV-012 | CLEAN ✓ |
| CAPTCHA → HUMAN_REQUIRED | SECURITY_CHALLENGE → POLICY_BLOCKED → HUMAN_REQUIRED | SPECIFIED ✓ |
| A3/Track B contract equivalence | Verified via test_07 | VERIFIED ✓ |
| Certificate word "proven" | REMOVED — corrected to "conformance-tested, empirically unproven" | RESOLVED ✓ |

```
G18_RESULT = CONDITIONAL_PASS (VALID — empirical gap honestly acknowledged; fallback architecture specified and conformance-tested; non-blocking via Track B/A3)
CERTIFICATE_OVERCLAIMS = 0 (corrected since prior audit)
SPK_001_STATUS = CONFORMANCE_TESTED (not empirically validated in live Chrome)
```
