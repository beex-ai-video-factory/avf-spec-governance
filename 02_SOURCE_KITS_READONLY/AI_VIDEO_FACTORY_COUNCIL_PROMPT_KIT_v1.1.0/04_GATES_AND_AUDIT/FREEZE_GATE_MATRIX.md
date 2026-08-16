# Freeze Gate Matrix

## G01 Baseline Integrity
Exact specification version/hash known.

## G02 Objective Integrity
Business objectives and non-negotiable capabilities trace to requirements.

## G03 Canonical State
One unambiguous source of truth; ownership for every canonical entity.

## G04 Repository Boundaries
Every repo has OWNS / DOES-NOT-OWN / inputs / outputs / dependencies.

## G05 Dependency Direction
No cycles or forbidden dependency leakage.

## G06 Contract Completeness
Provider, FlowExecutionPort, event envelope, errors, IDs, versioning and compatibility defined.

## G07 Idempotency
Every external/paid side effect has key + reconciliation semantics.

## G08 Recovery
Crash/restart/uncertain-submit/browser failure paths end in a defined stable state.

## G09 Security
Secrets, browser profiles, cookies, transport auth, permissions, logs/screenshots and dependency trust defined.

## G10 Flow Replaceability
Track A/Track B can be replaced without changing upstream business entities/contracts.

## G11 FlowKit Containment
FlowKit private schemas/state/protocol do not become AVF canonical contracts.

## G12 Testability
Each repo can be tested independently; deterministic fakes exist where needed.

## G13 Integration Testability
Cross-repo contract/conformance tests and integration harness are specified.

## G14 Observability/Provenance
A Take can be traced to exact versions/assets/provider/attempt/QC/workflow.

## G15 Version/Migration
Schema/API/event versions and migration/backward-compatibility behavior defined.

## G16 Agent Handoff
Fresh agent can implement a repo without reading unrelated internal code.

## G17 Capability Preservation
No accepted change weakens frozen capability without explicit preservation proof.

## G18 Empirical Unknowns
Every material uncertainty has spike/benchmark + success/kill criteria.

## G19 Review Governance
All accepted changes have required votes/sign-offs; dissent preserved.

## G20 Independent Audit
Fresh-context audit completed and all blockers resolved.

## G21 Implementation Readiness
Build packets and acceptance tests can be generated from frozen spec.

## G22 No Hidden Magic
No box labelled "agent", "AI", "worker", or "adapter" lacks inputs/outputs/state/failure semantics.
