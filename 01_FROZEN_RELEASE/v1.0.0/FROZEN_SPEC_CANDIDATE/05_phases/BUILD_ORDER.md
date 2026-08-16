# Exact Build Order

## Critical path

1. Freeze `avf-contracts` v1 schemas.
2. Implement Core State entities/invariants.
3. Implement Provider SDK + FakeVideoProvider.
4. Implement GenerationJob state machine and idempotency persistence.
5. Implement SingleShot durable workflow against FakeProvider.
6. Implement integration/fault-injection harness.
7. Implement GoogleFlowAdapter against mocked FlowExecutionPort.
8. Implement minimal FlowKit Track B bridge for fast functional baseline.
9. Implement Track A A2/A3 spike in parallel.
10. Execute Phase-0 comparative benchmark.
11. ADR selects primary MVP execution track.
12. Integrate media ingest/storage.
13. Prove crash/reconcile/resume with chosen live track.
14. Implement sequential multi-shot project workflow.
15. Add asset/continuity MVP.
16. Add provider-aware prompt compiler.
17. Add creative automation.
18. Add technical QC.
19. Add semantic QC + RetryPolicyEngine.
20. Add operator console.
21. Add production telemetry/security hardening.
22. Add concurrency/worker pools only after measurements.
23. Add second non-Flow provider when business need/availability warrants.

## Parallelizable after step 1

- Core state implementation;
- Provider SDK/FakeProvider;
- media worker;
- observability package;
- asset data model;
- FlowExecutionPort test harness.

## Deliberately deferred

- Kubernetes;
- Kafka/event streaming platform;
- vector DB;
- automatic multi-provider optimizer;
- multi-agent negotiation;
- massive dashboard;
- advanced postproduction AI.
