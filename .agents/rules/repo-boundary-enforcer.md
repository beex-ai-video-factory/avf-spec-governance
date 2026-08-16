# RULE: Repository Boundary & Dependency DAG Enforcer
# Trigger: Always On for 05_IMPLEMENTATION/repos/**

## Objective
Enforce strict domain boundaries (OWNS / DOES NOT OWN) and prevent cyclic or illegal cross-repository dependencies according to the frozen modular polyrepo architecture (ADR-001).

## Mandatory Directives
1. **Enforce OWNS / DOES NOT OWN:** Every repo must strictly implement only what is specified in its blueprint (`01_FROZEN_RELEASE/v1.0.0/03_repo_blueprints/Rxx_*.md`).
2. **Canonical State Ownership (R02 Core State):** Only R02 owns database schemas, entity persistence, and state transitions (ADR-002). No other repository may directly connect to the primary PostgreSQL database or perform state writes without going through R02 APIs/events.
3. **Google Flow Encapsulation (R08 Adapter):** Google Flow specific concepts, payloads, and protocols must be fully encapsulated within R08. Upstream workflows (R06), prompt compilers (R05), and state engines (R02) must use provider-neutral contracts (`provider-request` / `provider-result`).
4. **Independent Flow Execution Tracks (R09 vs R10):**
   - R09 (`R09_browser_worker`) implements Track A (Browser Automation / CDP).
   - R10 (`R10_flowkit_bridge`) implements Track B (Direct HTTP / FlowKit Bridge).
   - **R09 and R10 MUST NOT depend on each other.** Both implement the common `flow-execution-result` contract port for R08.
5. **Enforce Dependency DAG:** Dependency edges must strictly follow `05_IMPLEMENTATION/dependency-gates.yaml`. No backwards or unauthorized cross-layer imports are permitted.
