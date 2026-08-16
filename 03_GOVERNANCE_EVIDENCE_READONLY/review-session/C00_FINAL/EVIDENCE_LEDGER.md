# Evidence Ledger

| EVIDENCE_ID | LEVEL | ASSERTION | SOURCE_FILE | SOURCE_SECTION | SUPPORTED_REQUIREMENT_IDS | SUPPORTED_OR_CHALLENGED_ASSUMPTIONS | VERSION/DATE | NOTES |
|---|---|---|---|---|---|---|---|---|
| EV-001 | E2_PROJECT_OBSERVED | Modular Polyrepo Architecture specified in ADR-001 and REPOSITORY_STRATEGY | ADR-001_MODULAR_POLYREPO.md | Decision | REQ-016 | GAP | v0.9.0 | Supports Capability C-11 |
| EV-002 | E2_PROJECT_OBSERVED | PostgreSQL Single Source of Truth specified in ADR-002 and R02_CORE_STATE | ADR-002_CANONICAL_STATE.md | Decision | REQ-002, REQ-017 | GAP | v0.9.0 | Supports Capability C-01 |
| EV-003 | E2_PROJECT_OBSERVED | Append-only creative versioning specified in DATA_MODEL and SYSTEM_INVARIANTS | DATA_MODEL.md | Shot / ShotVersion | REQ-031, REQ-045 | GAP | v0.9.0 | Supports Capability C-02 |
| EV-004 | E2_PROJECT_OBSERVED | Full provenance and SHA-256 checksum tracking required in DATA_MODEL | DATA_MODEL.md | PromptVersion | REQ-004, REQ-035 | GAP | v0.9.0 | Supports Capability C-03 |
| EV-005 | E2_PROJECT_OBSERVED | VideoGenerationProvider abstraction mandated in ADR-003 and R07_PROVIDER_SDK | ADR-003_PROVIDER_ABSTRACTION.md | Decision | REQ-007, REQ-018 | GAP | v0.9.0 | Supports Capability C-04 |
| EV-006 | E2_PROJECT_OBSERVED | Google Flow isolation from core domain contracts enforced in SYSTEM_INVARIANTS | SYSTEM_INVARIANTS.md | System Invariants | REQ-008, REQ-036 | GAP | v0.9.0 | Supports Capability C-05 |
| EV-007 | E2_PROJECT_OBSERVED | Dual-track Flow execution strategy mandated in ADR-004 and MASTER_BLUEPRINT | ADR-004_DUAL_FLOW_EXECUTION.md | Decision | REQ-008, REQ-019, REQ-049 | GAP | v0.9.0 | Supports Capability C-06 |
| EV-008 | E2_PROJECT_OBSERVED | Deterministic generation idempotency key format specified in MASTER_BLUEPRINT | MASTER_BLUEPRINT.md | Idempotency | REQ-006, REQ-032 | GAP | v0.9.0 | Supports Capability C-07 |
| EV-009 | E2_PROJECT_OBSERVED | Temporal-class durable workflow engine mandated in ADR-008 and R06_WORKFLOW | ADR-008_WORKFLOW_ENGINE.md | Decision | REQ-006, REQ-023 | GAP | v0.9.0 | Supports Capability C-08 |
| EV-010 | E2_PROJECT_OBSERVED | Four-tier retry taxonomy and deterministic policy engine specified in ADR-006 | ADR-006_RETRY_POLICY.md | Decision | REQ-021, REQ-038 | GAP | v0.9.0 | Supports Capability C-09 |
| EV-011 | E2_PROJECT_OBSERVED | FakeVideoProvider requirement for 80%+ zero-credit testing in TEST_STRATEGY | TEST_STRATEGY.md | FakeProvider requirement | REQ-007, REQ-052 | GAP | v0.9.0 | Supports Capability C-10 |
| EV-012 | E2_PROJECT_OBSERVED | Contract-first architecture with JSON Schemas mandated in CONTRACTS_OVERVIEW | CONTRACTS_OVERVIEW.md | Contract families | REQ-001, REQ-024 | GAP | v0.9.0 | Supports Capability C-12 |
| EV-013 | E2_PROJECT_OBSERVED | Distributed OpenTelemetry correlation context specified in R14_PLATFORM_OBSERVABILITY | R14_PLATFORM_OBSERVABILITY.md | RESPONSIBILITY / OWNS | REQ-014, REQ-044 | GAP | v0.9.0 | Supports Capability C-13 |
| EV-014 | E2_PROJECT_OBSERVED | Operator console recovery views and blocked state UX specified in R13_OPERATOR_CONSOLE | R13_OPERATOR_CONSOLE.md | RESPONSIBILITY / OWNS | REQ-013, REQ-041 | GAP | v0.9.0 | Supports Capability C-14 |
| EV-015 | E2_PROJECT_OBSERVED | Privileged local execution security trust zones specified in SECURITY_MODEL | SECURITY_MODEL.md | Trust zones | REQ-009, REQ-050 | GAP | v0.9.0 | Supports Capability C-15 |
| EV-016 | E2_PROJECT_OBSERVED | Two-tier technical and multimodal QC evaluation specified in R11_QC | R11_QC.md | RESPONSIBILITY / OWNS | REQ-011, REQ-038 | GAP | v0.9.0 | Supports Capability C-16 |
| EV-017 | E2_PROJECT_OBSERVED | Provider registry and multi-provider extensibility specified in R07_PROVIDER_SDK | R07_PROVIDER_SDK.md | RESPONSIBILITY / OWNS | REQ-007, REQ-018 | GAP | v0.9.0 | Supports Capability C-17 |
| EV-018 | E2_PROJECT_OBSERVED | Bounded LLM task boundary preventing direct state mutation in ADR-005 | ADR-005_LLM_STATE_MUTATION.md | Decision | REQ-003, REQ-020, REQ-033 | GAP | v0.9.0 | Supports Capability C-18 |
| EV-019 | E2_PROJECT_OBSERVED | Three-stage architecture evolution (MVP -> V1 -> Scale) in MASTER_BLUEPRINT | MASTER_BLUEPRINT.md | Architecture evolution | REQ-015, REQ-053 | GAP | v0.9.0 | Supports Capability C-19 |
| EV-020 | E0_ASSUMPTION | Google Flow UI selector stability and anti-bot challenge frequency under high concurrency | SOURCE_LEDGER.md | Implementation hypotheses | REQ-008, REQ-053 | A-01 | v0.9.0 | Hypothesis requiring Phase 0 benchmark |
| EV-021 | E0_ASSUMPTION | FlowKit codebase stability and private protocol maintainability across releases | SOURCE_LEDGER.md | FlowKit | REQ-010, REQ-054 | A-02 | v0.9.0 | Requires spike and bridge isolation |
| EV-022 | E0_ASSUMPTION | Chrome MV3 background service worker wake-up and lifecycle reliability under load | SOURCE_LEDGER.md | Chrome Extensions | REQ-009, REQ-048 | A-03 | v0.9.0 | Requires native messaging spike |
| EV-023 | E0_ASSUMPTION | Google Flow generation duration variance and rate limit thresholds | PHASE_0_BENCHMARK.md | Benchmark protocol | REQ-008, REQ-053 | A-04 | v0.9.0 | Requires 100-run benchmark measurement |
| EV-024 | E0_ASSUMPTION | Chrome extension security review and permissions acceptability in production environments | SECURITY_MODEL.md | Browser extension rules | REQ-009, REQ-050 | A-05 | v0.9.0 | Requires security audit |
| EV-025 | E0_ASSUMPTION | Unit economics and fixed-cost assumptions versus third-party video generation APIs | SOURCE_LEDGER.md | User-provided research | REQ-047, REQ-053 | A-06 | v0.9.0 | Requires empirical cost measurement |
