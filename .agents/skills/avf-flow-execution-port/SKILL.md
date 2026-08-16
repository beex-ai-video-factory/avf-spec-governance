---
name: avf-flow-execution-port
description: Implement and verify the frozen 10-operation Google Flow execution port ensuring semantic equivalence between Track A (Browser Automation) and Track B (Direct Protocol Bridge).
---

# Skill: AVF Flow Execution Port (Track A & Track B)

## Purpose
Enforces the dual-track execution architecture for Google Flow (ADR-004) where R09 (Browser Worker) and R10 (FlowKit Bridge) both implement the unified 10-operation execution port.

## The 10 Frozen Port Operations
1. `OPEN_PROJECT`
2. `CREATE_SCENE`
3. `SET_PROMPT`
4. `SET_CAMERA_MOTION`
5. `TRIGGER_GENERATE`
6. `WAIT_FOR_GENERATION`
7. `GET_GENERATION_STATUS`
8. `DOWNLOAD_VIDEO`
9. `CANCEL_GENERATION`
10. `CHECK_HEALTH_SESSION`

## Interoperability Invariants
- **Common Contract:** Both tracks must accept `browser-command.schema.json` and return `flow-execution-result.schema.json`.
- **Zero Upstream Leakage:** No DOM selector, Playwright locator, or session cookie details may leak into R08 or R06.
- **Track Parity:** A single test suite running against the mock harness must pass identically on Track A and Track B adapters.
