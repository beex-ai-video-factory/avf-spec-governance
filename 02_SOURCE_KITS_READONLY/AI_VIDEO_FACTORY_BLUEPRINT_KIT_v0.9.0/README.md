# AI Video Factory Blueprint Kit

**Specification candidate:** `v0.9.0-review-candidate`  
**Purpose:** technical review, architecture freeze, contract freeze, then independent implementation by coding agents/teams.  
**Language:** Vietnamese with English identifiers for contracts/code artifacts.

## What this kit is

This is a **specification repository**, not an implementation repository. It decomposes the AI Video Factory into independently buildable repositories/subprojects with explicit ownership, versioned contracts, test obligations, acceptance criteria, failure semantics, and integration gates.

The governing principle is:

> AI supplies intelligence. Software engineering supplies correctness, recoverability, traceability, and replaceability.

The kit deliberately prevents Google Flow, Chrome automation, FlowKit, LangGraph, or any single provider from becoming the core domain.

## Review order

1. `00_governance/00_REVIEWER_ENTRYPOINT.md`
2. `01_master/MASTER_BLUEPRINT.md`
3. `01_master/SYSTEM_INVARIANTS.md`
4. `02_contracts/CONTRACTS_OVERVIEW.md`
5. `03_repo_blueprints/*`
6. `04_integration/*`
7. `05_phases/*`
8. `06_adrs/*`
9. `07_risk/RISK_REGISTER.md`
10. `08_evidence/SOURCE_LEDGER.md`

## Freeze model

- `v0.9.x`: review candidate; architecture can still change.
- `v1.0.0-rcN`: architecture accepted; contract defects only.
- `v1.0.0`: frozen implementation baseline.
- After `v1.0.0`, breaking changes require an ADR plus major contract version.

## Implementation model

Each blueprint under `03_repo_blueprints/` can be handed to a separate coding agent. Agents must implement only against frozen contracts from `avf-contracts`, and must pass contract tests before integration.

The system can be assembled with **Google Flow Execution Track A** (controlled browser worker/extension) or **Track B** (FlowKit compatibility bridge) without changing the upstream generation domain.

## Non-goals of this kit

- It does not implement production code.
- It does not guarantee Google Flow automation reliability.
- It does not encode or encourage bypassing CAPTCHA, anti-abuse controls, provider security, or rate limits.
- It does not lock the product to Google Flow pricing or UI behavior.
- It does not mandate Kubernetes, Kafka, service mesh, or dozens of independently deployed microservices.
