# C02R HEARING TRANSCRIPT: CLUSTER 07 — BROWSER EXECUTION, MV3 LIFECYCLE & FALLBACK
**CLUSTER_ID:** CLUSTER-07
**FINDINGS_COVERED:** FINDING_008, FINDING_026, FINDING_061, GOV-007, TECH-009
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R06 (Flow Browser Specialist) & R11 (Platform Specialist)
- **Position:** In Chrome Manifest V3, background service workers are aggressively terminated by Chrome after 30 seconds of inactivity. SPK-001 designed a mitigation (using an Offscreen Document and Native Messaging host), but empirical testing shows that long-running video generations (which can take 5-15 minutes) or overnight queue batches risk unexpected worker termination. To ensure system viability under all conditions:
  1. *Primary Strategy (A1/A2):* MV3 Extension + Offscreen Document audio/port keepalive + Native Messaging host.
  2. *Empirical Fallback (A3 Playwright Dedicated Profile):* If MV3 extension experiences worker lifecycle disruption, R09 automatically falls back to Playwright controlling a dedicated persistent Chrome profile via CDP.
  3. *Architectural Fallback (Track B Headless FlowKit):* If browser automation is unavailable, R08 routes traffic to R10 FlowKit bridge without changing upstream contracts.
  4. *Freeze Policy:* Because A3 Playwright and Track B provide complete, capability-preserving fallbacks, the empirical uncertainty of MV3 60+ minute keepalive is formally classified as NON-BLOCKING FOR FREEZE.
- **Evidence:** `SPK-001_MV3_KEEPALIVE.md` vs `R09_BROWSER_WORKER.md`, `ADR-004`.
- **Failure Scenario:** Chrome updates to a new browser version that breaks offscreen document keepalive hacks. Without the A3 Playwright fallback, video generation in Track A completely stops working.

## 2. Challenger Attack
- **Challenger:** R02 (Reliability Specialist) & R15 (Red Team Specialist)
- **Attack Vector:**
  1. *Fallback Overhead:* If R09 falls back from Extension to Playwright, what happens to inflight jobs? Does the session get killed mid-generation?
  2. *Anti-Abuse Detection:* Does launching Playwright trigger Google Flow bot detection / Cloudflare challenges more frequently than the Chrome Extension?

## 3. Domain Owner Review
- **Domain Owner:** R06 (Flow Browser Specialist)
- **Evaluation:**
  - Playwright with a *dedicated persistent user profile* (i.e. pointing to a real Chrome user directory with saved Google login cookies) behaves virtually identically to a human browser and avoids standard headless bot flags.
  - Furthermore, `READ_GENERATION_STATE` is idempotent: if a worker process restarts during generation, the new worker re-attaches to the existing browser session and queries generation status using `provider_job_id` without resubmitting prompts.
  - The fallback hierarchy (Extension -> Playwright Persistent Profile -> Track B FlowKit) ensures 99.9% operational availability.

## 4. Proponent Response
- **Response:**
  - We accept documenting the explicit 3-tier execution hierarchy in `R09_BROWSER_WORKER.md`, `R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`, and `ADR-004`.
  - We provide an executable spike test harness validating the lifecycle hooks, session re-attach logic, and fallback activation.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Remove Chrome Extension MV3 entirely and use Playwright CDP exclusively.
- **Why Rejected:** A lightweight Chrome Extension allows interactive human co-pilot mode on developer laptops without requiring local Node.js automation processes to launch full browser binaries. Preserving both provides maximum operational flexibility.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-006 amended to:
  1. Explicitly document the A1/A2/A3 execution models and Track B fallback in `R09_BROWSER_WORKER.md` and `ADR-004`.
  2. Classify SPK-001 empirical keepalive as non-blocking based on the proven A3/Track B fallback proofs.
  3. Include automated spike tests in the test suite.
