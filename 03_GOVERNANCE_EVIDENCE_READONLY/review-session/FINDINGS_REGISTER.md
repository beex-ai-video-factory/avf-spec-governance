# Master Findings Register (Post-C02 Cross-Examination)

**Council Round:** C02 Cross-Examination Complete  
**Total Findings Tracked:** 158  
**Status Breakdown:**
- `CONFIRMED`: 153  
- `DOWNGRADED`: 1  
- `NEEDS_RESEARCH`: 1  
- `NEEDS_SPIKE`: 3  
- `REJECTED_WITH_EVIDENCE`: 0  
- `MERGED_DUPLICATE`: 0  

---

## Complete Register Table

| FINDING_ID | ROLE | ORIGINAL_SEV | RESOLVED_SEV | STATUS | CATEGORY | TITLE / SCOPE | RESOLUTION SUMMARY |
|---|---|---|---|---|---|---|---|
| F-R01-001 | R01 | HIGH | HIGH | **CONFIRMED** | CONTRACT_DEFICIENCY | R01 Finding F-R01-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R01-002 | R01 | HIGH | HIGH | **CONFIRMED** | BOUNDED_CONTEXT / OWNERSHIP_AMBIGUITY | R01 Finding F-R01-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R01-003 | R01 | HIGH | HIGH | **CONFIRMED** | DOMAIN_STATE_MACHINE / COMMAND_CONTRACT | R01 Finding F-R01-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R01-004 | R01 | MEDIUM | MEDIUM | **CONFIRMED** | ARCHITECTURAL_GOVERNANCE / ADR_METADATA | R01 Finding F-R01-004 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R01-005 | R01 | MEDIUM | MEDIUM | **CONFIRMED** | DOMAIN_MODEL / ENTITY_RELATIONSHIPS | R01 Finding F-R01-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R01-006 | R01 | MEDIUM | MEDIUM | **NEEDS_RESEARCH** | DOMAIN_INVARIANTS / DETERMINISM | R01 Finding F-R01-006 | Research required into RFC 8785 JSON Canonicalization Scheme (JCS) vs SHA-256 binary hash compatibility across Node.js, Python, and Go microservices. |
| F-R01-007 | R01 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | DOMAIN_MODEL / AGGREGATE_NAVIGATION | R01 Finding F-R01-007 | Non-blocking improvement accepted for baseline polish. |
| F-R02-001 | R02 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | CONTRACTS_ERROR_HANDLING | R02 Finding F-R02-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R02-002 | R02 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | TIMEOUTS_AND_CONCURRENCY | R02 Finding F-R02-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R02-003 | R02 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | IDEMPOTENCY_AND_RECONCILIATION | R02 Finding F-R02-003 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R02-004 | R02 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | CONCURRENCY_AND_SPLIT_BRAIN | R02 Finding F-R02-004 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R02-005 | R02 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | DISTRIBUTED_TRANSACTIONS_AND_BUDGET | R02 Finding F-R02-005 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R02-006 | R02 | MEDIUM | MEDIUM | **NEEDS_SPIKE** | BROWSER_EXTENSION_LIFECYCLE | R02 Finding F-R02-006 | Chrome Extension MV3 service worker lifecycle and offscreen document IPC keepalive behavior under high concurrency must be validated with an empirical test harness. |
| F-R03-001 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-001 | Non-blocking improvement accepted for baseline polish. |
| F-R03-001 | R03 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | LOGIC_ERROR | R03 Finding F-R03-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R03-002 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-002 | Non-blocking improvement accepted for baseline polish. |
| F-R03-002 | R03 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SPEC_DEFECT | R03 Finding F-R03-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R03-003 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-003 | Non-blocking improvement accepted for baseline polish. |
| F-R03-003 | R03 | HIGH | HIGH | **CONFIRMED** | MISSING_EDGE_CASE | R03 Finding F-R03-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R03-004 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-004 | Non-blocking improvement accepted for baseline polish. |
| F-R03-004 | R03 | HIGH | HIGH | **CONFIRMED** | ARCHITECTURAL_DEFECT | R03 Finding F-R03-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R03-005 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-005 | Non-blocking improvement accepted for baseline polish. |
| F-R03-005 | R03 | HIGH | HIGH | **CONFIRMED** | ARCHITECTURAL_DEFECT | R03 Finding F-R03-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R03-006 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-006 | Non-blocking improvement accepted for baseline polish. |
| F-R03-006 | R03 | MEDIUM | MEDIUM | **CONFIRMED** | SPEC_DEFECT | R03 Finding F-R03-006 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R03-007 | R03 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R03 Finding F-R03-007 | Non-blocking improvement accepted for baseline polish. |
| F-R03-007 | R03 | MEDIUM | MEDIUM | **CONFIRMED** | RESOURCE_MANAGEMENT | R03 Finding F-R03-007 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R04-001 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-001 | Non-blocking improvement accepted for baseline polish. |
| F-R04-001 | R04 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | ERROR_TAXONOMY / SCHEMA_COMPLETENESS | R04 Finding F-R04-001 | Co-referenced and cross-validated with F-R02-001. Error taxonomy with standardized machine-readable error codes (RETRYABLE_RATE_LIMIT, FATAL_AUTH, TEMPORARY_PROVIDER_UNAVAILABLE) is confirmed as a mandatory contract requirement. |
| F-R04-002 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-002 | Non-blocking improvement accepted for baseline polish. |
| F-R04-002 | R04 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | CONTRACT_COMPLETENESS / BOUNDARY_VALIDATION | R04 Finding F-R04-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R04-003 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-003 | Non-blocking improvement accepted for baseline polish. |
| F-R04-003 | R04 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SCHEMA_COMPLETENESS / DATA_MODEL_ALIGNMENT | R04 Finding F-R04-003 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R04-004 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-004 | Non-blocking improvement accepted for baseline polish. |
| F-R04-004 | R04 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | EVENT_CONTRACTS / ASYNC_COMMUNICATION | R04 Finding F-R04-004 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R04-005 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-005 | Non-blocking improvement accepted for baseline polish. |
| F-R04-005 | R04 | HIGH | HIGH | **CONFIRMED** | API_COMPATIBILITY / VERSIONING | R04 Finding F-R04-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R04-006 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-006 | Non-blocking improvement accepted for baseline polish. |
| F-R04-006 | R04 | HIGH | HIGH | **CONFIRMED** | OBSERVABILITY / TRACEABILITY | R04 Finding F-R04-006 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R04-007 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-007 | Non-blocking improvement accepted for baseline polish. |
| F-R04-007 | R04 | HIGH | HIGH | **CONFIRMED** | CONTRACT_COMPLETENESS | R04 Finding F-R04-007 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R04-008 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R04 Finding F-R04-008 | Non-blocking improvement accepted for baseline polish. |
| F-R04-008 | R04 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | API_COMPATIBILITY / EXTENSIBILITY | R04 Finding F-R04-008 | Non-blocking improvement accepted for baseline polish. |
| F-R05-001 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-001 | Non-blocking improvement accepted for baseline polish. |
| F-R05-001 | R05 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | Architecture / Data Model Integrity | R05 Finding F-R05-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R05-002 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-002 | Non-blocking improvement accepted for baseline polish. |
| F-R05-002 | R05 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | Provenance / Schema Completeness | R05 Finding F-R05-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R05-003 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-003 | Non-blocking improvement accepted for baseline polish. |
| F-R05-003 | R05 | HIGH | HIGH | **CONFIRMED** | Database Schema / Relational Integrity | R05 Finding F-R05-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R05-004 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-004 | Non-blocking improvement accepted for baseline polish. |
| F-R05-004 | R05 | HIGH | HIGH | **CONFIRMED** | Database Schema / Concurrency & Performance | R05 Finding F-R05-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R05-005 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-005 | Non-blocking improvement accepted for baseline polish. |
| F-R05-005 | R05 | HIGH | HIGH | **CONFIRMED** | Event Publishing / Data Consistency | R05 Finding F-R05-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R05-006 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-006 | Non-blocking improvement accepted for baseline polish. |
| F-R05-006 | R05 | MEDIUM | MEDIUM | **CONFIRMED** | Data Lifecycle / Retention / Provenance | R05 Finding F-R05-006 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R05-007 | R05 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R05 Finding F-R05-007 | Non-blocking improvement accepted for baseline polish. |
| F-R05-007 | R05 | MEDIUM | MEDIUM | **CONFIRMED** | Operations / Persistence Reliability | R05 Finding F-R05-007 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R06-001 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-001 | Non-blocking improvement accepted for baseline polish. |
| F-R06-001 | R06 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | CONTRACT_DEFECT | R06 Finding F-R06-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R06-002 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-002 | Non-blocking improvement accepted for baseline polish. |
| F-R06-002 | R06 | HIGH | HIGH | **CONFIRMED** | RESILIENCE_DEFECT | R06 Finding F-R06-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R06-003 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-003 | Non-blocking improvement accepted for baseline polish. |
| F-R06-003 | R06 | HIGH | HIGH | **CONFIRMED** | PROCESS_SUPERVISION | R06 Finding F-R06-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R06-004 | R06 | NON_BLOCKING | NON_BLOCKING | **NEEDS_SPIKE** | Architecture | R06 Finding F-R06-004 | Chrome Extension MV3 service worker lifecycle and offscreen document IPC keepalive behavior under high concurrency must be validated with an empirical test harness. |
| F-R06-004 | R06 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **NEEDS_SPIKE** | LIFECYCLE_HAZARD | R06 Finding F-R06-004 | Chrome Extension MV3 service worker lifecycle and offscreen document IPC keepalive behavior under high concurrency must be validated with an empirical test harness. |
| F-R06-005 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-005 | Non-blocking improvement accepted for baseline polish. |
| F-R06-005 | R06 | HIGH | HIGH | **CONFIRMED** | LIFECYCLE_HAZARD | R06 Finding F-R06-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R06-006 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-006 | Non-blocking improvement accepted for baseline polish. |
| F-R06-006 | R06 | HIGH | HIGH | **CONFIRMED** | SECURITY_HAZARD | R06 Finding F-R06-006 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R06-007 | R06 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R06 Finding F-R06-007 | Non-blocking improvement accepted for baseline polish. |
| F-R06-007 | R06 | MEDIUM | MEDIUM | **CONFIRMED** | RESILIENCE_DEFECT | R06 Finding F-R06-007 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R07-001 | R07 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SPECIFICATION_GAP / SECURITY_DATA_PROTECTION | R07 Finding F-R07-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R07-002 | R07 | BLOCKER_BEFORE_FREEZE | HIGH | **DOWNGRADED** | SPECIFICATION_GAP / COMPLIANCE_AUDITABILITY | R07 Finding F-R07-002 | Cryptographic audit log signing is valuable for enterprise compliance but is not an MVP freeze blocker. Basic immutable append-only event logging with HMAC authentication is sufficient for v1.0. Downgraded from BLOCKER to HIGH. |
| F-R07-003 | R07 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | ARCHITECTURAL_DEFECT / IPC_TRANSPORT_AUTHENTICATION | R07 Finding F-R07-003 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R07-004 | R07 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | SPECIFICATION_GAP / PROVIDER_SECURITY | R07 Finding F-R07-004 | Non-blocking improvement accepted for baseline polish. |
| F-R07-005 | R07 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | SPECIFICATION_GAP / BROWSER_EXTENSION_SECURITY | R07 Finding F-R07-005 | Non-blocking improvement accepted for baseline polish. |
| F-R07-006 | R07 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | SPECIFICATION_GAP / SUPPLY_CHAIN_SANDBOXING | R07 Finding F-R07-006 | Non-blocking improvement accepted for baseline polish. |
| F-R07-007 | R07 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SPECIFICATION_GAP / SECRET_LEAKAGE_PREVENTION | R07 Finding F-R07-007 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R08-001 | R08 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | CONTRACT_DEFECT | R08 Finding F-R08-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R08-002 | R08 | HIGH | HIGH | **CONFIRMED** | TEST_HARNESS_DEFECT | R08 Finding F-R08-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R08-003 | R08 | HIGH | HIGH | **CONFIRMED** | VERIFICATION_GAP | R08 Finding F-R08-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R08-004 | R08 | MEDIUM | MEDIUM | **CONFIRMED** | INTEGRATION_VERIFICATION_GAP | R08 Finding F-R08-004 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R08-005 | R08 | MEDIUM | MEDIUM | **CONFIRMED** | REGRESSION_TESTING_DEFECT | R08 Finding F-R08-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R08-006 | R08 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | CI_STABILITY | R08 Finding F-R08-006 | Non-blocking improvement accepted for baseline polish. |
| F-R09-001 | R09 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R09 Finding F-R09-001 | Non-blocking improvement accepted for baseline polish. |
| F-R09-001 | R09 | HIGH | HIGH | **CONFIRMED** | ARCHITECTURE / CONTRACTS / CAPABILITY | R09 Finding F-R09-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R09-002 | R09 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R09 Finding F-R09-002 | Non-blocking improvement accepted for baseline polish. |
| F-R09-002 | R09 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | DETERMINISM / PROVENANCE / LLM_BOUNDARY | R09 Finding F-R09-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R09-003 | R09 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R09 Finding F-R09-003 | Non-blocking improvement accepted for baseline polish. |
| F-R09-003 | R09 | HIGH | HIGH | **CONFIRMED** | CONTRACTS / DATA_MODEL / REPRODUCIBILITY | R09 Finding F-R09-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R09-004 | R09 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R09 Finding F-R09-004 | Non-blocking improvement accepted for baseline polish. |
| F-R09-004 | R09 | HIGH | HIGH | **CONFIRMED** | LLM_RELIABILITY / VALIDATION / BOUNDED_AUTONOMY | R09 Finding F-R09-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R09-005 | R09 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R09 Finding F-R09-005 | Non-blocking improvement accepted for baseline polish. |
| F-R09-005 | R09 | MEDIUM | MEDIUM | **CONFIRMED** | AI_EVALUATION / QUALITY_CONTROL / RETRY_POLICY | R09 Finding F-R09-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R10-001 | R10 | HIGH | HIGH | **CONFIRMED** | Architecture Decisions & AI Handoff (GAP-003) * **AFFECTED_FILES:**   - | R10 Finding F-R10-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R10-002 | R10 | HIGH | HIGH | **CONFIRMED** | AI Build Packets & Task Boundaries * **AFFECTED_FILES:**   - | R10 Finding F-R10-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R10-003 | R10 | HIGH | HIGH | **CONFIRMED** | Local Development & Environment Reproducibility * **AFFECTED_FILES:**   - | R10 Finding F-R10-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R10-004 | R10 | HIGH | HIGH | **CONFIRMED** | Mock / Fake Availability & Zero-Cost Testing * **AFFECTED_FILES:**   - | R10 Finding F-R10-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R10-005 | R10 | HIGH | HIGH | **CONFIRMED** | Contract Generation & Repository Scaffolding * **AFFECTED_FILES:**   - | R10 Finding F-R10-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R10-006 | R10 | MEDIUM | MEDIUM | **CONFIRMED** | Freeze Readiness & Governance Checklist * **AFFECTED_FILES:**   - | R10 Finding F-R10-006 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R11-001 | R11 | HIGH | HIGH | **CONFIRMED** | : CONTRACTS / OBSERVABILITY - **AFFECTED_FILES**:    - | R11 Finding F-R11-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R11-002 | R11 | HIGH | HIGH | **CONFIRMED** | : SECURITY / PLATFORM / STORAGE - **AFFECTED_FILES**:    - | R11 Finding F-R11-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R11-003 | R11 | MEDIUM | MEDIUM | **CONFIRMED** | : PLATFORM / METRICS - **AFFECTED_FILES**:    - | R11 Finding F-R11-003 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R11-004 | R11 | HIGH | HIGH | **CONFIRMED** | : RELIABILITY / PLATFORM / STATE - **AFFECTED_FILES**:    - | R11 Finding F-R11-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R11-005 | R11 | MEDIUM | MEDIUM | **CONFIRMED** | : OBSERVABILITY / LOGGING - **AFFECTED_FILES**:    - | R11 Finding F-R11-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R11-006 | R11 | HIGH | HIGH | **CONFIRMED** | : OPERATIONS / RELIABILITY - **AFFECTED_FILES**:    - | R11 Finding F-R11-006 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R11-007 | R11 | HIGH | HIGH | **CONFIRMED** | : PLATFORM / DATA INTEGRITY - **AFFECTED_FILES**:    - | R11 Finding F-R11-007 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R11-008 | R11 | MEDIUM | MEDIUM | **CONFIRMED** | : PLATFORM / CONFIGURATION - **AFFECTED_FILES**:    - | R11 Finding F-R11-008 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R12-001 | R12 | HIGH | HIGH | **CONFIRMED** | SPEC_GAP | R12 Finding F-R12-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R12-002 | R12 | HIGH | HIGH | **CONFIRMED** | CONTRACT | R12 Finding F-R12-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R12-003 | R12 | HIGH | HIGH | **CONFIRMED** | STATE_MACHINE | R12 Finding F-R12-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R12-004 | R12 | HIGH | HIGH | **CONFIRMED** | PROVENANCE | R12 Finding F-R12-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R12-005 | R12 | MEDIUM | MEDIUM | **CONFIRMED** | PRODUCT_POLICY | R12 Finding F-R12-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R12-006 | R12 | HIGH | HIGH | **CONFIRMED** | ROADMAP | R12 Finding F-R12-006 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R12-007 | R12 | MEDIUM | MEDIUM | **CONFIRMED** | UI_SPEC | R12 Finding F-R12-007 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R12-008 | R12 | MEDIUM | MEDIUM | **CONFIRMED** | COST_CONTROL | R12 Finding F-R12-008 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R13-001 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-001 | FlowKit dependency isolation is a core system invariant (INV-004, INV-010). Upstream contracts must remain completely provider-agnostic so Track A and Track B are drop-in replaceable. |
| F-R13-001 | R13 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | ARCHITECTURE | R13 Finding F-R13-001 | FlowKit dependency isolation is a core system invariant (INV-004, INV-010). Upstream contracts must remain completely provider-agnostic so Track A and Track B are drop-in replaceable. |
| F-R13-002 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-002 | Non-blocking improvement accepted for baseline polish. |
| F-R13-002 | R13 | HIGH | HIGH | **CONFIRMED** | SUPPLY_CHAIN | R13 Finding F-R13-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R13-003 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-003 | Non-blocking improvement accepted for baseline polish. |
| F-R13-003 | R13 | HIGH | HIGH | **CONFIRMED** | LEGAL_LICENSING | R13 Finding F-R13-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R13-004 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-004 | Non-blocking improvement accepted for baseline polish. |
| F-R13-004 | R13 | MEDIUM | MEDIUM | **CONFIRMED** | SECURITY | R13 Finding F-R13-004 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R13-005 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-005 | Non-blocking improvement accepted for baseline polish. |
| F-R13-005 | R13 | MEDIUM | MEDIUM | **CONFIRMED** | ARCHITECTURE | R13 Finding F-R13-005 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R13-006 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-006 | Non-blocking improvement accepted for baseline polish. |
| F-R13-006 | R13 | MEDIUM | MEDIUM | **CONFIRMED** | SUPPLY_CHAIN | R13 Finding F-R13-006 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R13-007 | R13 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R13 Finding F-R13-007 | Non-blocking improvement accepted for baseline polish. |
| F-R13-007 | R13 | MEDIUM | MEDIUM | **CONFIRMED** | ARCHITECTURE | R13 Finding F-R13-007 | Medium-severity specification improvement confirmed. Scheduled for resolution in C03. |
| F-R14-001 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-001 | Non-blocking improvement accepted for baseline polish. |
| F-R14-001 | R14 | HIGH | HIGH | **CONFIRMED** | OBSERVABILITY | R14 Finding F-R14-001 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R14-002 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-002 | Non-blocking improvement accepted for baseline polish. |
| F-R14-002 | R14 | HIGH | HIGH | **CONFIRMED** | COST | R14 Finding F-R14-002 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R14-003 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-003 | Non-blocking improvement accepted for baseline polish. |
| F-R14-003 | R14 | HIGH | HIGH | **CONFIRMED** | CAPACITY | R14 Finding F-R14-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R14-004 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-004 | Non-blocking improvement accepted for baseline polish. |
| F-R14-004 | R14 | HIGH | HIGH | **CONFIRMED** | PERFORMANCE | R14 Finding F-R14-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R14-005 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-005 | Non-blocking improvement accepted for baseline polish. |
| F-R14-005 | R14 | HIGH | HIGH | **CONFIRMED** | BENCHMARK | R14 Finding F-R14-005 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R14-006 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-006 | Non-blocking improvement accepted for baseline polish. |
| F-R14-006 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | COST | R14 Finding F-R14-006 | Non-blocking improvement accepted for baseline polish. |
| F-R14-007 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R14 Finding F-R14-007 | Non-blocking improvement accepted for baseline polish. |
| F-R14-007 | R14 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | CAPACITY | R14 Finding F-R14-007 | Non-blocking improvement accepted for baseline polish. |
| F-R15-001 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-001 | Non-blocking improvement accepted for baseline polish. |
| F-R15-001 | R15 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SECURITY | R15 Finding F-R15-001 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R15-002 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-002 | Non-blocking improvement accepted for baseline polish. |
| F-R15-002 | R15 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | SECURITY | R15 Finding F-R15-002 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R15-003 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-003 | Non-blocking improvement accepted for baseline polish. |
| F-R15-003 | R15 | HIGH | HIGH | **CONFIRMED** | SECURITY | R15 Finding F-R15-003 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R15-004 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-004 | Non-blocking improvement accepted for baseline polish. |
| F-R15-004 | R15 | HIGH | HIGH | **CONFIRMED** | SECURITY | R15 Finding F-R15-004 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R15-005 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-005 | Non-blocking improvement accepted for baseline polish. |
| F-R15-005 | R15 | BLOCKER_BEFORE_FREEZE | BLOCKER_BEFORE_FREEZE | **CONFIRMED** | RELIABILITY | R15 Finding F-R15-005 | Defect validated with primary specification evidence. Blocker classification confirmed; requires formal Change Proposal in C03. |
| F-R15-006 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-006 | Non-blocking improvement accepted for baseline polish. |
| F-R15-006 | R15 | HIGH | HIGH | **CONFIRMED** | RELIABILITY | R15 Finding F-R15-006 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
| F-R15-007 | R15 | NON_BLOCKING | NON_BLOCKING | **CONFIRMED** | Architecture | R15 Finding F-R15-007 | Non-blocking improvement accepted for baseline polish. |
| F-R15-007 | R15 | HIGH | HIGH | **CONFIRMED** | SECURITY | R15 Finding F-R15-007 | High-severity architectural gap confirmed. Must be addressed during C03 solution design. |
