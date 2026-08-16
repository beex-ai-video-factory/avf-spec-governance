# C03R SOLUTION PACKAGE 07: BROWSER EXECUTION & MV3 FALLBACK HIERARCHY
**SOLUTION_ID:** SOL-07
**FINDINGS_ADDRESSED:** GOV-007, TECH-009, FINDING_008
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
Chrome MV3 service worker keepalive mechanisms are susceptible to browser platform changes during long video generation jobs (5-15 min). G18 gate cannot claim unconditional PASS without live empirical proof or a proven non-blocking fallback guarantee.

---

## 2. Options Analysis

### Option A: 3-Tier Execution Hierarchy with Guaranteed Fallbacks (Recommended)
- **Architecture:**
  - Primary (A1/A2): MV3 Extension + Offscreen Document + Native Messaging Host.
  - Local Fallback (A3): Playwright automation using a dedicated persistent Chrome profile with saved Google session cookies.
  - Headless Fallback (Track B): FlowKit Bridge bypassing browser extension entirely.
  - Re-attach Semantics: If an extension worker crashes, `READ_GENERATION_STATE` allows any new worker to re-attach to the existing session via `provider_job_id` without re-submitting prompts.
  - Gate Decision: Classify G18 as CONDITIONAL_PASS / JUSTIFIED_NONBLOCKING because A3 Playwright and Track B guarantee uninterrupted production operation even if MV3 keepalive fails.
- **Exact Normative Files to Change:**
  - `03_repo_blueprints/R09_BROWSER_WORKER.md`
  - `03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`
  - `06_adrs/ADR-004_DUAL_FLOW_EXECUTION.md`
  - `07_risk/RISK_REGISTER.md`

### Option B: Completely Deprecate MV3 Extension
- **Drawbacks:** Destroys co-pilot interactive developer debugging mode in Chrome.

---

## 3. Decision
**Selected: Option A.** Preserves both execution modes while providing bulletproof fallback guarantees.
