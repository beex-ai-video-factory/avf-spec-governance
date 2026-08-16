# Requirement-to-Blueprint Traceability

This file maps key requirements from the supplied technical-review specification to concrete kit artifacts.

| Requirement | Blueprint artifact |
|---|---|
| Bounded services/repos | `03_repo_blueprints/*` |
| Does NOT Own boundaries | every repo blueprint |
| Deterministic vs LLM vs Agent | `MASTER_BLUEPRINT`, repo execution type |
| Canonical source of truth | `R02_CORE_STATE`, `DATA_MODEL`, ADR-002 |
| Provider abstraction | `R07_PROVIDER_SDK`, `R08_GOOGLE_FLOW_ADAPTER`, ADR-003 |
| Browser isolated | `R09_BROWSER_WORKER`, ADR-004/007 |
| Google Flow not core | master + forbidden dependency graph |
| FlowKit alternative | `R10_FLOWKIT_BRIDGE`, execution options |
| Versioning/provenance | `DATA_MODEL`, `SYSTEM_INVARIANTS` |
| Retry taxonomy | master + state machines + workflow repo |
| QC separate | `R11_QC` |
| Human in loop | operator console + blocked states |
| Observability | `R14_PLATFORM_OBSERVABILITY` |
| Cost observability | Core CostUsageRecord + telemetry |
| Mock provider | `R07_PROVIDER_SDK`, integration harness |
| Test-first contracts | `R01_CONTRACTS`, `TEST_STRATEGY` |
| Local development | `LOCAL_DEVELOPMENT` |
| AI coding-agent friendly | every repo + agent packet index/template |
| Vertical phases | `PHASE_ROADMAP` |
| Kill criteria | Phase-0 benchmark + risk register |
| ADRs | `06_adrs/*` |
| Things not to build yet | master/build order |
| 3-stage architecture evolution | master MVP/V1/Scale |
| Security | `SECURITY_MODEL` |
| Failure recovery | workflow/state machines/test strategy |
| System invariants | `SYSTEM_INVARIANTS` |
| Final architecture diagram | master + dependency graph |
