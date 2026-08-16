# C01 Master Findings Catalog

**Total Raw Reviews Analyzed:** 15  
**Total Formal Findings Cataloged:** 158  
**Blockers Before Freeze:** 25  
**High Severity Findings:** 47  
**Medium Severity Findings:** 23  
**Non-Blocking / Polish:** 63  

---

## Master Table of Findings

| FINDING_ID | ROLE | SEVERITY | CATEGORY | TITLE | AFFECTED_CONTRACTS_OR_FILES |
|---|---|---|---|---|---|
| F-R01-001 | R01 | HIGH | CONTRACT_DEFICIENCY | R01 Finding F-R01-001 | - `domain-entities.schema.json` - `CONTR |
| F-R01-002 | R01 | HIGH | BOUNDED_CONTEXT / OWNERSHIP_AMBIGUITY | R01 Finding F-R01-002 | - `R02_CORE_STATE` Public API - `R04_ASS |
| F-R01-003 | R01 | HIGH | DOMAIN_STATE_MACHINE / COMMAND_CONTRACT | R01 Finding F-R01-003 | - `R02_CORE_STATE` Public API - `STATUS_ |
| F-R01-004 | R01 | MEDIUM | ARCHITECTURAL_GOVERNANCE / ADR_METADATA | R01 Finding F-R01-004 | - Baseline ADRs ADR-001 through ADR-008  |
| F-R01-005 | R01 | MEDIUM | DOMAIN_MODEL / ENTITY_RELATIONSHIPS | R01 Finding F-R01-005 | - `DATA_MODEL.md` ERD - `domain-entities |
| F-R01-006 | R01 | MEDIUM | DOMAIN_INVARIANTS / DETERMINISM | R01 Finding F-R01-006 | - `domain-entities.schema.json` - `R05_P |
| F-R01-007 | R01 | NON_BLOCKING | DOMAIN_MODEL / AGGREGATE_NAVIGATION | R01 Finding F-R01-007 | - `domain-entities.schema.json` - `R02_C |
| F-R02-001 | R02 | BLOCKER_BEFORE_FREEZE | CONTRACTS_ERROR_HANDLING | R02 Finding F-R02-001 | `https://avf.local/contracts/provider-re |
| F-R02-002 | R02 | BLOCKER_BEFORE_FREEZE | TIMEOUTS_AND_CONCURRENCY | R02 Finding F-R02-002 | `https://avf.local/contracts/browser-com |
| F-R02-003 | R02 | BLOCKER_BEFORE_FREEZE | IDEMPOTENCY_AND_RECONCILIATION | R02 Finding F-R02-003 | `STATUS_STATE_MACHINES.md`, `GenerationJ |
| F-R02-004 | R02 | BLOCKER_BEFORE_FREEZE | CONCURRENCY_AND_SPLIT_BRAIN | R02 Finding F-R02-004 | `STATUS_STATE_MACHINES.md` (Browser exec |
| F-R02-005 | R02 | BLOCKER_BEFORE_FREEZE | DISTRIBUTED_TRANSACTIONS_AND_BUDGET | R02 Finding F-R02-005 | `R02_CORE_STATE.md` Public API (`AppendU |
| F-R02-006 | R02 | MEDIUM | BROWSER_EXTENSION_LIFECYCLE | R02 Finding F-R02-006 | Track A Browser Worker Host-Extension Pr |
| F-R03-001 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-001 | NOT_SPECIFIED |
| F-R03-001 | R03 | BLOCKER_BEFORE_FREEZE | LOGIC_ERROR | R03 Finding F-R03-001 | - STATUS_STATE_MACHINES   - provider-req |
| F-R03-002 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-002 | NOT_SPECIFIED |
| F-R03-002 | R03 | BLOCKER_BEFORE_FREEZE | SPEC_DEFECT | R03 Finding F-R03-002 | - STATUS_STATE_MACHINES   - browser-comm |
| F-R03-003 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-003 | NOT_SPECIFIED |
| F-R03-003 | R03 | HIGH | MISSING_EDGE_CASE | R03 Finding F-R03-003 | - STATUS_STATE_MACHINES   - domain-entit |
| F-R03-004 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-004 | NOT_SPECIFIED |
| F-R03-004 | R03 | HIGH | ARCHITECTURAL_DEFECT | R03 Finding F-R03-004 | - STATUS_STATE_MACHINES   - browser-comm |
| F-R03-005 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-005 | NOT_SPECIFIED |
| F-R03-005 | R03 | HIGH | ARCHITECTURAL_DEFECT | R03 Finding F-R03-005 | - STATUS_STATE_MACHINES   - domain-entit |
| F-R03-006 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-006 | NOT_SPECIFIED |
| F-R03-006 | R03 | MEDIUM | SPEC_DEFECT | R03 Finding F-R03-006 | - CONTRACTS_OVERVIEW.md   - API_COMPATIB |
| F-R03-007 | R03 | NON_BLOCKING | Architecture | R03 Finding F-R03-007 | NOT_SPECIFIED |
| F-R03-007 | R03 | MEDIUM | RESOURCE_MANAGEMENT | R03 Finding F-R03-007 | - STATUS_STATE_MACHINES   - browser-comm |
| F-R04-001 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-001 | NOT_SPECIFIED |
| F-R04-001 | R04 | BLOCKER_BEFORE_FREEZE | ERROR_TAXONOMY / SCHEMA_COMPLETENESS | R04 Finding F-R04-001 | - CONTRACTS_OVERVIEW   - provider-result |
| F-R04-002 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-002 | NOT_SPECIFIED |
| F-R04-002 | R04 | BLOCKER_BEFORE_FREEZE | CONTRACT_COMPLETENESS / BOUNDARY_VALIDATION | R04 Finding F-R04-002 | - browser-command   - browser-command-re |
| F-R04-003 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-003 | NOT_SPECIFIED |
| F-R04-003 | R04 | BLOCKER_BEFORE_FREEZE | SCHEMA_COMPLETENESS / DATA_MODEL_ALIGNMENT | R04 Finding F-R04-003 | - domain-entities |
| F-R04-004 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-004 | NOT_SPECIFIED |
| F-R04-004 | R04 | BLOCKER_BEFORE_FREEZE | EVENT_CONTRACTS / ASYNC_COMMUNICATION | R04 Finding F-R04-004 | - event-envelope   - domain-events (miss |
| F-R04-005 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-005 | NOT_SPECIFIED |
| F-R04-005 | R04 | HIGH | API_COMPATIBILITY / VERSIONING | R04 Finding F-R04-005 | - ALL schemas |
| F-R04-006 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-006 | NOT_SPECIFIED |
| F-R04-006 | R04 | HIGH | OBSERVABILITY / TRACEABILITY | R04 Finding F-R04-006 | - provider-request   - browser-command   |
| F-R04-007 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-007 | NOT_SPECIFIED |
| F-R04-007 | R04 | HIGH | CONTRACT_COMPLETENESS | R04 Finding F-R04-007 | - qc-evaluator (missing)   - media-proce |
| F-R04-008 | R04 | NON_BLOCKING | Architecture | R04 Finding F-R04-008 | NOT_SPECIFIED |
| F-R04-008 | R04 | NON_BLOCKING | API_COMPATIBILITY / EXTENSIBILITY | R04 Finding F-R04-008 | - provider-request |
| F-R05-001 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-001 | NOT_SPECIFIED |
| F-R05-001 | R05 | BLOCKER_BEFORE_FREEZE | Architecture / Data Model Integrity | R05 Finding F-R05-001 | - domain-entities.schema.json   - COMMAN |
| F-R05-002 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-002 | NOT_SPECIFIED |
| F-R05-002 | R05 | BLOCKER_BEFORE_FREEZE | Provenance / Schema Completeness | R05 Finding F-R05-002 | - domain-entities.schema.json ($defs/pro |
| F-R05-003 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-003 | NOT_SPECIFIED |
| F-R05-003 | R05 | HIGH | Database Schema / Relational Integrity | R05 Finding F-R05-003 | - domain-entities.schema.json   - STATUS |
| F-R05-004 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-004 | NOT_SPECIFIED |
| F-R05-004 | R05 | HIGH | Database Schema / Concurrency & Performance | R05 Finding F-R05-004 | - domain-entities.schema.json   - STATUS |
| F-R05-005 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-005 | NOT_SPECIFIED |
| F-R05-005 | R05 | HIGH | Event Publishing / Data Consistency | R05 Finding F-R05-005 | - event-envelope.schema.json   - COMMAND |
| F-R05-006 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-006 | NOT_SPECIFIED |
| F-R05-006 | R05 | MEDIUM | Data Lifecycle / Retention / Provenance | R05 Finding F-R05-006 | - domain-entities.schema.json   - STATUS |
| F-R05-007 | R05 | NON_BLOCKING | Architecture | R05 Finding F-R05-007 | NOT_SPECIFIED |
| F-R05-007 | R05 | MEDIUM | Operations / Persistence Reliability | R05 Finding F-R05-007 | - API_COMPATIBILITY_POLICY.md |
| F-R06-001 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-001 | NOT_SPECIFIED |
| F-R06-001 | R06 | BLOCKER_BEFORE_FREEZE | CONTRACT_DEFECT | R06 Finding F-R06-001 | - browser-command.schema.json   - (Missi |
| F-R06-002 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-002 | NOT_SPECIFIED |
| F-R06-002 | R06 | HIGH | RESILIENCE_DEFECT | R06 Finding F-R06-002 | - STATUS_STATE_MACHINES.md   - browser-c |
| F-R06-003 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-003 | NOT_SPECIFIED |
| F-R06-003 | R06 | HIGH | PROCESS_SUPERVISION | R06 Finding F-R06-003 | - STATUS_STATE_MACHINES.md |
| F-R06-004 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-004 | NOT_SPECIFIED |
| F-R06-004 | R06 | BLOCKER_BEFORE_FREEZE | LIFECYCLE_HAZARD | R06 Finding F-R06-004 | - STATUS_STATE_MACHINES.md   - browser-c |
| F-R06-005 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-005 | NOT_SPECIFIED |
| F-R06-005 | R06 | HIGH | LIFECYCLE_HAZARD | R06 Finding F-R06-005 | - STATUS_STATE_MACHINES.md   - browser-c |
| F-R06-006 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-006 | NOT_SPECIFIED |
| F-R06-006 | R06 | HIGH | SECURITY_HAZARD | R06 Finding F-R06-006 | - STATUS_STATE_MACHINES.md   - CONTRACTS |
| F-R06-007 | R06 | NON_BLOCKING | Architecture | R06 Finding F-R06-007 | NOT_SPECIFIED |
| F-R06-007 | R06 | MEDIUM | RESILIENCE_DEFECT | R06 Finding F-R06-007 | - browser-command.schema.json   - event- |
| F-R07-001 | R07 | BLOCKER_BEFORE_FREEZE | SPECIFICATION_GAP / SECURITY_DATA_PROTECTION | R07 Finding F-R07-001 | - 02_contracts/browser-command.schema.js |
| F-R07-002 | R07 | BLOCKER_BEFORE_FREEZE | SPECIFICATION_GAP / COMPLIANCE_AUDITABILITY | R07 Finding F-R07-002 | - 02_contracts/event-envelope.schema.jso |
| F-R07-003 | R07 | BLOCKER_BEFORE_FREEZE | ARCHITECTURAL_DEFECT / IPC_TRANSPORT_AUTHENTICATION | R07 Finding F-R07-003 | - 02_contracts/browser-command.schema.js |
| F-R07-004 | R07 | NON_BLOCKING | SPECIFICATION_GAP / PROVIDER_SECURITY | R07 Finding F-R07-004 | - 02_contracts/provider-request.schema.j |
| F-R07-005 | R07 | NON_BLOCKING | SPECIFICATION_GAP / BROWSER_EXTENSION_SECURITY | R07 Finding F-R07-005 | - 02_contracts/CONTRACTS_OVERVIEW.md |
| F-R07-006 | R07 | NON_BLOCKING | SPECIFICATION_GAP / SUPPLY_CHAIN_SANDBOXING | R07 Finding F-R07-006 | - 02_contracts/CONTRACTS_OVERVIEW.md |
| F-R07-007 | R07 | BLOCKER_BEFORE_FREEZE | SPECIFICATION_GAP / SECRET_LEAKAGE_PREVENTION | R07 Finding F-R07-007 | - 02_contracts/provider-result.schema.js |
| F-R08-001 | R08 | BLOCKER_BEFORE_FREEZE | CONTRACT_DEFECT | R08 Finding F-R08-001 | - domain-entities   - CONTRACTS_OVERVIEW |
| F-R08-002 | R08 | HIGH | TEST_HARNESS_DEFECT | R08 Finding F-R08-002 | - provider-request   - provider-result   |
| F-R08-003 | R08 | HIGH | VERIFICATION_GAP | R08 Finding F-R08-003 | - STATUS_STATE_MACHINES   - domain-entit |
| F-R08-004 | R08 | MEDIUM | INTEGRATION_VERIFICATION_GAP | R08 Finding F-R08-004 | - browser-command   - provider-result |
| F-R08-005 | R08 | MEDIUM | REGRESSION_TESTING_DEFECT | R08 Finding F-R08-005 | - domain-entities   - provider-result |
| F-R08-006 | R08 | NON_BLOCKING | CI_STABILITY | R08 Finding F-R08-006 | NOT_SPECIFIED |
| F-R09-001 | R09 | NON_BLOCKING | Architecture | R09 Finding F-R09-001 | NOT_SPECIFIED |
| F-R09-001 | R09 | HIGH | ARCHITECTURE / CONTRACTS / CAPABILITY | R09 Finding F-R09-001 | - provider-request.schema.json   - provi |
| F-R09-002 | R09 | NON_BLOCKING | Architecture | R09 Finding F-R09-002 | NOT_SPECIFIED |
| F-R09-002 | R09 | BLOCKER_BEFORE_FREEZE | DETERMINISM / PROVENANCE / LLM_BOUNDARY | R09 Finding F-R09-002 | - domain-entities.schema.json ($defs.pro |
| F-R09-003 | R09 | NON_BLOCKING | Architecture | R09 Finding F-R09-003 | NOT_SPECIFIED |
| F-R09-003 | R09 | HIGH | CONTRACTS / DATA_MODEL / REPRODUCIBILITY | R09 Finding F-R09-003 | - domain-entities.schema.json ($defs.pro |
| F-R09-004 | R09 | NON_BLOCKING | Architecture | R09 Finding F-R09-004 | NOT_SPECIFIED |
| F-R09-004 | R09 | HIGH | LLM_RELIABILITY / VALIDATION / BOUNDED_AUTONOMY | R09 Finding F-R09-004 | - domain-entities.schema.json ($defs.sho |
| F-R09-005 | R09 | NON_BLOCKING | Architecture | R09 Finding F-R09-005 | NOT_SPECIFIED |
| F-R09-005 | R09 | MEDIUM | AI_EVALUATION / QUALITY_CONTROL / RETRY_POLICY | R09 Finding F-R09-005 | - domain-entities.schema.json ($defs.qcR |
| F-R10-001 | R10 | HIGH | Architecture Decisions & AI Handoff (GAP-003) * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-001_MODULAR_POLYREPO.md` through `ADR-008_WORKFLOW_ENGINE.md`   - `AI_VIDEO_F | R10 Finding F-R10-001 | INV-013, INV-014, REQ-016 to REQ-023 * * |
| F-R10-002 | R10 | HIGH | AI Build Packets & Task Boundaries * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/09_agent_packets/AGENT_BUILD_PACKET_INDEX.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/09_agent_pa | R10 Finding F-R10-002 | All Invariants (INV-001 to INV-020) * ** |
| F-R10-003 | R10 | HIGH | Local Development & Environment Reproducibility * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/LOCAL_DEVELOPMENT.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo | R10 Finding F-R10-003 | INV-003, INV-005, INV-013, INV-015 * **E |
| F-R10-004 | R10 | HIGH | Mock / Fake Availability & Zero-Cost Testing * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo | R10 Finding F-R10-004 | INV-003, INV-006, INV-007, INV-020 * **E |
| F-R10-005 | R10 | HIGH | Contract Generation & Repository Scaffolding * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R01_CONTRACTS.md`   - `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/06_IM | R10 Finding F-R10-005 | INV-013, INV-014 * **EVIDENCE:**   1. `R |
| F-R10-006 | R10 | MEDIUM | Freeze Readiness & Governance Checklist * **AFFECTED_FILES:**   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/FREEZE_CHECKLIST.md` * **AFFECTED_CONTRACTS:** INV-014, REQ-016 * **EVIDENCE:**  | R10 Finding F-R10-006 | INV-014, REQ-016 * **EVIDENCE:**   1. `F |
| F-R11-001 | R11 | HIGH | : CONTRACTS / OBSERVABILITY - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-c | R11 Finding F-R11-001 | :    - `event-envelope.schema.json`   -  |
| F-R11-002 | R11 | HIGH | : SECURITY / PLATFORM / STORAGE - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PL | R11 Finding F-R11-002 | :    - `SECURITY_MODEL.md`   - `R14_PLAT |
| F-R11-003 | R11 | MEDIUM | : PLATFORM / METRICS - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`   - `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md`  | R11 Finding F-R11-003 | :    - `R14_PLATFORM_OBSERVABILITY.md` - |
| F-R11-004 | R11 | HIGH | : RELIABILITY / PLATFORM / STATE - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprint | R11 Finding F-R11-004 | :    - `COMMAND_EVENT_CATALOG.md`   - `e |
| F-R11-005 | R11 | MEDIUM | : OBSERVABILITY / LOGGING - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/ | R11 Finding F-R11-005 | :    - `R14_PLATFORM_OBSERVABILITY.md`   |
| F-R11-006 | R11 | HIGH | : OPERATIONS / RELIABILITY - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10 | R11 Finding F-R11-006 | :    - `browser-command.schema.json`   - |
| F-R11-007 | R11 | HIGH | : PLATFORM / DATA INTEGRITY - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_bluep | R11 Finding F-R11-007 | :    - `R14_PLATFORM_OBSERVABILITY.md`   |
| F-R11-008 | R11 | MEDIUM | : PLATFORM / CONFIGURATION - **AFFECTED_FILES**:    - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`   - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration | R11 Finding F-R11-008 | :    - `R14_PLATFORM_OBSERVABILITY.md`   |
| F-R12-001 | R12 | HIGH | SPEC_GAP | R12 Finding F-R12-001 | - domain-entities.schema.json - STATUS_S |
| F-R12-002 | R12 | HIGH | CONTRACT | R12 Finding F-R12-002 | - CONTRACTS_OVERVIEW.md - domain-entitie |
| F-R12-003 | R12 | HIGH | STATE_MACHINE | R12 Finding F-R12-003 | - STATUS_STATE_MACHINES.md - COMMAND_EVE |
| F-R12-004 | R12 | HIGH | PROVENANCE | R12 Finding F-R12-004 | - domain-entities.schema.json - COMMAND_ |
| F-R12-005 | R12 | MEDIUM | PRODUCT_POLICY | R12 Finding F-R12-005 | - domain-entities.schema.json - STATUS_S |
| F-R12-006 | R12 | HIGH | ROADMAP | R12 Finding F-R12-006 | - API_COMPATIBILITY_POLICY.md |
| F-R12-007 | R12 | MEDIUM | UI_SPEC | R12 Finding F-R12-007 | - CONTRACTS_OVERVIEW.md |
| F-R12-008 | R12 | MEDIUM | COST_CONTROL | R12 Finding F-R12-008 | - domain-entities.schema.json - STATUS_S |
| F-R13-001 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-001 | NOT_SPECIFIED |
| F-R13-001 | R13 | BLOCKER_BEFORE_FREEZE | ARCHITECTURE | R13 Finding F-R13-001 | - FlowExecutionPort (browser-command.sch |
| F-R13-002 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-002 | NOT_SPECIFIED |
| F-R13-002 | R13 | HIGH | SUPPLY_CHAIN | R13 Finding F-R13-002 | - API_COMPATIBILITY_POLICY.md |
| F-R13-003 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-003 | NOT_SPECIFIED |
| F-R13-003 | R13 | HIGH | LEGAL_LICENSING | R13 Finding F-R13-003 | - domain-entities.schema.json   - DEPEND |
| F-R13-004 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-004 | NOT_SPECIFIED |
| F-R13-004 | R13 | MEDIUM | SECURITY | R13 Finding F-R13-004 | - API_COMPATIBILITY_POLICY.md |
| F-R13-005 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-005 | NOT_SPECIFIED |
| F-R13-005 | R13 | MEDIUM | ARCHITECTURE | R13 Finding F-R13-005 | - domain-entities.schema.json   - event- |
| F-R13-006 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-006 | NOT_SPECIFIED |
| F-R13-006 | R13 | MEDIUM | SUPPLY_CHAIN | R13 Finding F-R13-006 | - FlowExecutionPort (browser-command.sch |
| F-R13-007 | R13 | NON_BLOCKING | Architecture | R13 Finding F-R13-007 | NOT_SPECIFIED |
| F-R13-007 | R13 | MEDIUM | ARCHITECTURE | R13 Finding F-R13-007 | - DEPENDENCY_GRAPH.md |
| F-R14-001 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-001 | NOT_SPECIFIED |
| F-R14-001 | R14 | HIGH | OBSERVABILITY | R14 Finding F-R14-001 | - CONTRACTS_OVERVIEW (Contract Family 7: |
| F-R14-002 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-002 | NOT_SPECIFIED |
| F-R14-002 | R14 | HIGH | COST | R14 Finding F-R14-002 | - domain-entities.schema.json   - REQ-00 |
| F-R14-003 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-003 | NOT_SPECIFIED |
| F-R14-003 | R14 | HIGH | CAPACITY | R14 Finding F-R14-003 | - browser-command.schema.json (READ_GENE |
| F-R14-004 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-004 | NOT_SPECIFIED |
| F-R14-004 | R14 | HIGH | PERFORMANCE | R14 Finding F-R14-004 | - CONTRACTS_OVERVIEW (Error Taxonomy: PR |
| F-R14-005 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-005 | NOT_SPECIFIED |
| F-R14-005 | R14 | HIGH | BENCHMARK | R14 Finding F-R14-005 | - REQ-053   - ADR-004 |
| F-R14-006 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-006 | NOT_SPECIFIED |
| F-R14-006 | R14 | NON_BLOCKING | COST | R14 Finding F-R14-006 | - domain-entities.schema.json (QCResult) |
| F-R14-007 | R14 | NON_BLOCKING | Architecture | R14 Finding F-R14-007 | NOT_SPECIFIED |
| F-R14-007 | R14 | NON_BLOCKING | CAPACITY | R14 Finding F-R14-007 | - REQ-006, REQ-019 |
| F-R15-001 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-001 | NOT_SPECIFIED |
| F-R15-001 | R15 | BLOCKER_BEFORE_FREEZE | SECURITY | R15 Finding F-R15-001 | - browser-command.schema.json (CAPTURE_D |
| F-R15-002 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-002 | NOT_SPECIFIED |
| F-R15-002 | R15 | BLOCKER_BEFORE_FREEZE | SECURITY | R15 Finding F-R15-002 | - event-envelope   - domain-entities   - |
| F-R15-003 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-003 | NOT_SPECIFIED |
| F-R15-003 | R15 | HIGH | SECURITY | R15 Finding F-R15-003 | - browser-command.schema.json   - SECURI |
| F-R15-004 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-004 | NOT_SPECIFIED |
| F-R15-004 | R15 | HIGH | SECURITY | R15 Finding F-R15-004 | - provider-request   - browser-command.s |
| F-R15-005 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-005 | NOT_SPECIFIED |
| F-R15-005 | R15 | BLOCKER_BEFORE_FREEZE | RELIABILITY | R15 Finding F-R15-005 | - STATUS_STATE_MACHINES   - browser-comm |
| F-R15-006 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-006 | NOT_SPECIFIED |
| F-R15-006 | R15 | HIGH | RELIABILITY | R15 Finding F-R15-006 | - STATUS_STATE_MACHINES   - CONTRACTS_OV |
| F-R15-007 | R15 | NON_BLOCKING | Architecture | R15 Finding F-R15-007 | NOT_SPECIFIED |
| F-R15-007 | R15 | HIGH | SECURITY | R15 Finding F-R15-007 | - SECURITY_MODEL   - browser-command.sch |
