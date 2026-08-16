# REMEDIATION FINDING REGISTER
## AI Video Factory — v1.0.0 Freeze Repair Program
**SUPERVISOR:** Autonomous Freeze Remediation Supervisor  
**DATE:** 2026-08-15  
**STATUS:** ACTIVE_REMEDIATION  
**VERSION:** 1.0.0  

---

## 1. Governance Forensic Findings (GOV-xxx)

### GOV-001: Invalid Voting — Universal Boilerplate Rationale (FA-001)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-001), `review-session/FINAL_FORENSIC_AUDIT/VOTE_FORENSICS.md`
- **Evidence Artifact:** `review-session/C04/VOTE_RECORD.md`
- **Severity:** AUDIT_BLOCKER
- **Affected Requirements:** G19 (Review Governance), AUTONOMOUS_COUNCIL_MASTER.md §12, §15
- **Affected Protected Capabilities:** CAP-ALL (All governance integrity)
- **Affected Contracts / Repos:** All Change Proposals (CP-001 through CP-015+)
- **Earliest Responsible Round:** C04R
- **Required Independent Specialists:** Domain-specific voters per proposal + Independent Vote Auditor
- **Closure Evidence:** Real per-role domain-specific raw ballots in `C04R/BALLOTS/RAW/`, hashed before tally, verified by independent `C04R/VOTE_INTEGRITY_AUDIT.md`.
- **Status:** OPEN_IN_REMEDIATION

### GOV-002: Missing C05 Post-Remediation Fresh Hostile Audit Rerun (FA-002)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-002), `review-session/FINAL_FORENSIC_AUDIT/C05_PROCESS_AUDIT.md`
- **Evidence Artifact:** `review-session/AUDITS/C05_INDEPENDENT_AUDIT_REPORT.md`, `review-session/C05/remediate_and_recheck.py`
- **Severity:** AUDIT_BLOCKER
- **Affected Requirements:** G20 (Independent Audit), AUTONOMOUS_COUNCIL_MASTER.md §13
- **Affected Protected Capabilities:** CAP-ALL
- **Affected Contracts / Repos:** All contracts and repo blueprints
- **Earliest Responsible Round:** C05R
- **Required Independent Specialists:** Auditor-A (Architecture/Contracts hostile), Auditor-B (Reliability/Security hostile), Auditor-C (Judge)
- **Closure Evidence:** Persisted raw reports `C05R_RAW_AUDITOR_A.md` and `C05R_RAW_AUDITOR_B.md` executed on post-remediation spec, followed by `C05R_AUDIT_JUDGE_REPORT.md`.
- **Status:** OPEN_IN_REMEDIATION

### GOV-003: Unvoted Normative Semantic Changes Post-C04 (FA-003)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-003), `review-session/FINAL_FORENSIC_AUDIT/SEMANTIC_CHANGE_TRACEABILITY.md`
- **Evidence Artifact:** `review-session/C05/remediate_and_recheck.py`
- **Severity:** AUDIT_BLOCKER
- **Affected Requirements:** G19, AUTONOMOUS_COUNCIL_MASTER.md §12, §15
- **Affected Protected Capabilities:** CAP-01, CAP-03, CAP-05, CAP-06
- **Affected Contracts / Repos:** `domain-entities.schema.json`, `provider-request.schema.json`, `R02_CORE_STATE.md`, `R07_PROVIDER_SDK.md`, `SECURITY_MODEL.md`
- **Earliest Responsible Round:** C03R / C04R
- **Required Independent Specialists:** Contracts (R04), Reliability (R02), Security (R07), Data (R05)
- **Closure Evidence:** Creation of formal Change Proposals (CP-016 through CP-024) covering all semantic modifications, followed by valid voting in C04R.
- **Status:** OPEN_IN_REMEDIATION

### GOV-004: C02 Deliberation Quality — Synthetic Adversarial Deliberation (FA-004)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-004), `review-session/FINAL_FORENSIC_AUDIT/FINDING_ACCOUNTING.md`
- **Evidence Artifact:** `review-session/C02/CROSS_EXAMINATION_LOG.md`
- **Severity:** AUDIT_MAJOR
- **Affected Requirements:** G19, C02 Quality standard
- **Affected Protected Capabilities:** Architecture soundness across all domains
- **Affected Contracts / Repos:** All findings contributing to CP-001..CP-024
- **Earliest Responsible Round:** C02R
- **Required Independent Specialists:** Dedicated Proponent, Challenger, and Domain Owner subagents per decision cluster
- **Closure Evidence:** Persisted raw hearing logs in `C02R_RAW/`, `C02R_HEARING_INDEX.md`, `C02R_DISPOSITION_REGISTER.md`, and `C02R_QUALITY_AUDIT.md` passing semantic diversity tests.
- **Status:** OPEN_IN_REMEDIATION

### GOV-005: Governance Artifact Overwrite (FA-005)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-005), `review-session/FINAL_FORENSIC_AUDIT/C05_PROCESS_AUDIT.md`
- **Evidence Artifact:** `review-session/C04/POST_MERGE_CONSISTENCY_REPORT.md`
- **Severity:** AUDIT_MAJOR
- **Affected Requirements:** Source & evidence immutability
- **Affected Protected Capabilities:** Governance audit trail
- **Affected Contracts / Repos:** Governance records
- **Earliest Responsible Round:** C00R / C04R
- **Required Independent Specialists:** Audit Supervisor
- **Closure Evidence:** Reconstructed immutable baseline; all remediation artifacts strictly isolated in `FREEZE_REMEDIATION_V1/` without mutating previous round directories.
- **Status:** OPEN_IN_REMEDIATION

### GOV-006: Tree Hash Methodology Not Independently Reproducible (FA-006)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-006), `EXTERNAL_TECHNICAL_REVIEW.md` (B11)
- **Evidence Artifact:** `review-session/FINAL_FREEZE/FILE_HASHES.json`, `build_final_freeze.py`
- **Severity:** AUDIT_MINOR
- **Affected Requirements:** Release integrity & reproducibility
- **Affected Protected Capabilities:** Verification tooling
- **Affected Contracts / Repos:** Manifests and freeze builder
- **Earliest Responsible Round:** C03R / C07R
- **Required Independent Specialists:** Platform (R11), Security (R07)
- **Closure Evidence:** Explicit deterministic hashing specification: `CONTENT_HASHES.json`, `CONTENT_TREE_SHA256` computed from sorted `path\tsha256\n` of content files (excluding self-referential manifests), and `DISTRIBUTABLE_ZIP_SHA256` of final zip archive.
- **Status:** OPEN_IN_REMEDIATION

### GOV-007: SPK-001 MV3 Keepalive Designed But Not Empirically Validated (FA-007)
- **Source Audit:** `FINAL_FORENSIC_AUDIT.md` (FA-007), `EXTERNAL_TECHNICAL_REVIEW.md` (B09)
- **Evidence Artifact:** `review-session/SPIKES/SPK-001_MV3_KEEPALIVE.md`
- **Severity:** AUDIT_MINOR / EMPIRICAL_GOVERNANCE
- **Affected Requirements:** G18 (Spikes & Feasibility), CAP-02 (Browser Flow execution)
- **Affected Contracts / Repos:** `R09_BROWSER_WORKER.md`, `R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`, `ADR-004`
- **Earliest Responsible Round:** C03R / Spike suite
- **Required Independent Specialists:** Flow/Browser (R06), AI/Platform (R09/R11)
- **Closure Evidence:** Executable test/spike harness running MV3 lifecycle checks and verifying Playwright dedicated persistent profile / Track B fallback guarantee; G18 gate justified with non-blocking fallback proof.
- **Status:** OPEN_IN_REMEDIATION

---

## 2. Technical Forensic & Review Blockers (TECH-xxx)

### TECH-001: Release Identity Ambiguity (T-001 / B01)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B01), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `review-session/FINAL_FREEZE/FROZEN_SPEC_CANDIDATE/VERSION`, `README.md`, `KIT_MANIFEST.yaml`
- **Severity:** BLOCKER
- **Affected Requirements:** Release identity consistency
- **Affected Protected Capabilities:** Implementation agent handoff
- **Affected Contracts / Repos:** `VERSION`, `README.md`, `KIT_MANIFEST.yaml`, `COMMITTEE_REVIEW_EDITION.md`
- **Earliest Responsible Round:** C03R / C04R
- **Required Independent Specialists:** DX (R10), Platform (R11)
- **Closure Evidence:** All identity files inside candidate consistently state version `1.0.0-remediated-rc1` (promoted to `1.0.0` at final freeze).
- **Status:** OPEN_IN_REMEDIATION

### TECH-002: Stale Internal KIT_MANIFEST Hashes (T-002 / B02)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B02)
- **Evidence Artifact:** `KIT_MANIFEST.yaml` in prior freeze candidate
- **Severity:** BLOCKER
- **Affected Requirements:** Kit integrity verification
- **Affected Protected Capabilities:** Integrity verification
- **Affected Contracts / Repos:** `KIT_MANIFEST.yaml`, `FILE_HASHES.json`
- **Earliest Responsible Round:** C07R
- **Required Independent Specialists:** QA (R08), Platform (R11)
- **Closure Evidence:** Re-generation of all internal file hashes from actual final content AFTER synthesis.
- **Status:** OPEN_IN_REMEDIATION

### TECH-003: Incomplete Change Integration — Prior Candidate Byte-Identical to v0.9.0 (T-003 / B03)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B03)
- **Evidence Artifact:** `review-session/FINAL_FREEZE/FROZEN_SPEC_CANDIDATE/` vs `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`
- **Severity:** BLOCKER
- **Affected Requirements:** All Change Proposals CP-001 through CP-024
- **Affected Protected Capabilities:** CAP-01 through CAP-19
- **Affected Contracts / Repos:** All 60+ specification files (contracts, master architecture, repo blueprints, ADRs, risk register, test strategy)
- **Earliest Responsible Round:** C03R / C04R / Synthesis
- **Required Independent Specialists:** Domain DDD (R01), Contracts (R04), Reliability (R02), Security (R07), All Domain Owners
- **Closure Evidence:** Every accepted Change Proposal is integrated into the actual normative files in `REVISED_SPEC_CANDIDATE/`, verified by semantic diff and `SEMANTIC_CHANGE_TO_CP.json`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-004: Canonical Provenance Contradiction (T-004 / B04)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B04), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `DATA_MODEL.md` vs `domain-entities.schema.json`
- **Severity:** BLOCKER
- **Affected Requirements:** Canonical provenance `ShotVersion -> PromptVersion -> GenerationJob -> Take`
- **Affected Protected Capabilities:** CAP-01, CAP-05, CAP-06
- **Affected Contracts / Repos:** `domain-entities.schema.json`, `DATA_MODEL.md`, `R01_CONTRACTS.md`, `R02_CORE_STATE.md`, `R05_PROMPT_COMPILER.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Domain DDD (R01), Data (R05), Contracts (R04)
- **Closure Evidence:** Unified canonical data schema where:
  - `ShotVersion` contains creative intent and has `shot_version_id`; does NOT require `prompt_version_id`.
  - `PromptVersion` references `shot_version_id` (and `shot_id`).
  - `GenerationJob` references `shot_id`, `shot_version_id`, `prompt_version_id`, `provider_id`, `attempt_index`, `provider_job_id`, `flow_track`, `requested_at`, `submitted_at`, `completed_at`, `normalized_error`.
  - `Take` references `job_id`, `shot_version_id`, `prompt_version_id`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-005: GenerationJob State Model Contradiction (T-005 / B05)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B05), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `STATUS_STATE_MACHINES.md` vs `domain-entities.schema.json`
- **Severity:** BLOCKER
- **Affected Requirements:** GenerationJob lifecycle state machine
- **Affected Protected Capabilities:** CAP-01, CAP-03, CAP-04
- **Affected Contracts / Repos:** `STATUS_STATE_MACHINES.md`, `domain-entities.schema.json`, `R02_CORE_STATE.md`, `R06_WORKFLOW.md`, `R13_OPERATOR_CONSOLE.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Reliability (R02), Workflow (R03), Contracts (R04)
- **Closure Evidence:** Fully reconciled GenerationJob lifecycle states:
  - High-level Canonical Core State (`domain-entities.schema.json`): `QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`.
  - Detailed Execution/Workflow Sub-states explicitly defined in `STATUS_STATE_MACHINES.md` and mapped to canonical parent states (`WAITING_FOR_ASSETS`, `PROMPT_READY`, `SUBMITTING`, `SUBMITTED`, `GENERATING`, `DOWNLOADING`, `DOWNLOADED`, `QC_RUNNING`, `APPROVED`, `BLOCKED`, `ABORTED`).
  - Contract conformance test verifying mapping and valid transitions.
- **Status:** OPEN_IN_REMEDIATION

### TECH-006: FlowExecutionPort Under-Specified (T-006 / B06)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B06), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `browser-command.schema.json`
- **Severity:** BLOCKER
- **Affected Requirements:** FlowExecutionPort request/result contracts for all 10 operations
- **Affected Protected Capabilities:** CAP-02 (Google Flow Adapter), CAP-18 (Track A / Track B Port Equivalence)
- **Affected Contracts / Repos:** `browser-command.schema.json`, `flow-execution-result.schema.json` (NEW), `R08_GOOGLE_FLOW_ADAPTER.md`, `R09_BROWSER_WORKER.md`, `R10_FLOWKIT_BRIDGE.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Flow/Browser (R06), Contracts (R04), Reliability (R02), QA (R08)
- **Closure Evidence:**
  - Normative JSON schemas with strict typed `oneOf` discriminators for all 10 operations:
    1. `ENSURE_SESSION`
    2. `OPEN_FLOW`
    3. `CREATE_OR_SELECT_PROJECT`
    4. `ATTACH_ASSETS`
    5. `SET_GENERATION_OPTIONS`
    6. `SUBMIT_PROMPT`
    7. `READ_GENERATION_STATE`
    8. `DOWNLOAD_OUTPUT`
    9. `CAPTURE_DIAGNOSTIC`
    10. `CANCEL`
  - Strict typed parameter schemas, result schemas, normalized error schemas, timeout, and idempotency semantics.
  - Conformance test verifying Fake Track A and Fake Track B pass identical test suite.
- **Status:** OPEN_IN_REMEDIATION

### TECH-007: Event Envelope Contradiction (T-007 / B07)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B07), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `CONTRACTS_OVERVIEW.md` vs `event-envelope.schema.json` vs `COMMAND_EVENT_CATALOG.md`
- **Severity:** BLOCKER
- **Affected Requirements:** Event envelope schema and event naming convention
- **Affected Protected Capabilities:** CAP-04 (Event-driven integration), CAP-14 (Platform Observability)
- **Affected Contracts / Repos:** `event-envelope.schema.json`, `CONTRACTS_OVERVIEW.md`, `COMMAND_EVENT_CATALOG.md`, `R01_CONTRACTS.md`, `R14_PLATFORM_OBSERVABILITY.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Contracts (R04), Platform (R11), Reliability (R02)
- **Closure Evidence:** One canonical event envelope schema with:
  - `event_id`, `event_type`, `aggregate_id`, `aggregate_version`, `timestamp_utc`, `correlation_id`, `trace_id`, `workflow_run_id`, `schema_version`, `payload`.
  - Canonical event type regex allowing dot-notated domain events e.g. `^[a-z0-9_]+(\\.[a-z0-9_]+)+$` or PascalCase/dotted aliases defined in catalog.
  - Event catalog and contracts overview updated to match schema exactly.
- **Status:** OPEN_IN_REMEDIATION

### TECH-008: Provider Result / Lifecycle / Error Contradiction (T-008 / B08)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B08), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `provider-result.schema.json` vs `CONTRACTS_OVERVIEW.md`
- **Severity:** BLOCKER
- **Affected Requirements:** Provider response contract, status polling, normalized error taxonomy, retry category
- **Affected Protected Capabilities:** CAP-03, CAP-12
- **Affected Contracts / Repos:** `provider-result.schema.json`, `CONTRACTS_OVERVIEW.md`, `R07_PROVIDER_SDK.md`, `R08_GOOGLE_FLOW_ADAPTER.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Contracts (R04), Reliability (R02), AI (R09)
- **Closure Evidence:**
  - Clear separation of:
    1. Operation execution status: `SUCCESS`, `FAILED`, `PENDING`, `RUNNING`.
    2. Generation status: `QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`.
    3. Normalized error class enum: `PROVIDER_RATE_LIMIT`, `AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`, `BUDGET_EXHAUSTED`, `UNSUPPORTED_CAPABILITY`, `NETWORK_TIMEOUT`, `BAD_REQUEST`, `PROVIDER_INTERNAL_ERROR`.
    4. Retry classification: `TRANSIENT`, `PERMANENT`, `POLICY_BLOCKED`, `RESOURCE_EXHAUSTED`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-009: Handoff Claims Without Normative Source (T-009 / B09)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B09), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `review-session/FINAL_FREEZE/FINAL_IMPLEMENTATION_HANDOFF_INDEX.md`
- **Severity:** BLOCKER
- **Affected Requirements:** Handoff integrity and architectural boundary consistency
- **Affected Protected Capabilities:** Handoff trustworthiness
- **Affected Contracts / Repos:** `AGENT_BUILD_PACKET_INDEX.md`, Repo blueprints R01-R15, `FINAL_IMPLEMENTATION_HANDOFF_INDEX.md`
- **Earliest Responsible Round:** C03R / C04R / Synthesis
- **Required Independent Specialists:** Security (R07), DX (R10), Domain DDD (R01)
- **Closure Evidence:** Remove unbacked architectural claims (e.g. SecretEnclave hardware module, gRPC port on R10, raw WebSocket server on R13) and ensure all handoff claims are backed by formal repo blueprints and schemas.
- **Status:** OPEN_IN_REMEDIATION

### TECH-010: Repository Dependency Graph Incomplete/Inconsistent (T-010 / B10)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B10), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §1
- **Evidence Artifact:** `DEPENDENCY_GRAPH.md`
- **Severity:** BLOCKER
- **Affected Requirements:** Strict polyrepo acyclic dependency DAG
- **Affected Protected Capabilities:** Modularity, independent testability
- **Affected Contracts / Repos:** `DEPENDENCY_GRAPH.md`, `REPOSITORY_STRATEGY.md`, All 15 repo blueprints
- **Earliest Responsible Round:** C03R / C04R
- **Required Independent Specialists:** Domain DDD (R01), Contracts (R04), Platform (R11)
- **Closure Evidence:** Rebuilt complete, acyclic dependency matrix representing all 15 repos, public contract imports, R14 platform telemetry ingestion, R15 harness consumption, workflow activity dependencies, and explicit forbidden dependency assertions.
- **Status:** OPEN_IN_REMEDIATION

### TECH-011: Package Hash Methodology Non-Self-Referential (T-011 / B11)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B11), `FINAL_FORENSIC_AUDIT.md` (FA-006)
- **Evidence Artifact:** `build_final_freeze.py`, `FILE_HASHES.json`
- **Severity:** BLOCKER
- **Affected Requirements:** Package integrity verification
- **Affected Protected Capabilities:** Auditability
- **Affected Contracts / Repos:** Freeze builder tooling, manifests
- **Earliest Responsible Round:** C03R / C07R
- **Required Independent Specialists:** Platform (R11), Security (R07)
- **Closure Evidence:** Explicit deterministic hashing pipeline:
  1. Calculate individual file SHA-256 for all normative content files.
  2. Compute `CONTENT_TREE_SHA256` from sorted `relative_path\tsha256\n` of content files (excluding manifest/hash files).
  3. Write `CONTENT_HASHES.json` and `FINAL_SPEC_MANIFEST.md`.
  4. Create final `.zip` archive.
  5. Compute `DISTRIBUTABLE_ZIP_SHA256`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-012: Certification Signatures Linked to Immutable Records (T-012 / B12)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (B12), `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` §14
- **Evidence Artifact:** `FREEZE_CERTIFICATE.md`
- **Severity:** BLOCKER
- **Affected Requirements:** Council certification governance
- **Affected Protected Capabilities:** Audit trail
- **Affected Contracts / Repos:** `FREEZE_CERTIFICATE.md`, `C04R/BALLOTS/RAW/`
- **Earliest Responsible Round:** C07R
- **Required Independent Specialists:** Council Secretary, Audit Supervisor
- **Closure Evidence:** Freeze certificate dynamically generated from persisted immutable vote/audit records, linking each signoff to its raw ballot artifact path and SHA-256 hash.
- **Status:** OPEN_IN_REMEDIATION

### TECH-013: ShotVersion Creative Intent Completeness (TECH-M01 / M01)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (M01)
- **Evidence Artifact:** `DATA_MODEL.md`, `domain-entities.schema.json`
- **Severity:** MAJOR
- **Affected Requirements:** ShotVersion creative specification fidelity
- **Affected Protected Capabilities:** CAP-01, CAP-05
- **Affected Contracts / Repos:** `domain-entities.schema.json`, `DATA_MODEL.md`, `R03_CREATIVE.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Domain DDD (R01), Creative/AI (R09), Contracts (R04)
- **Closure Evidence:** Expanded `ShotVersion` schema in `domain-entities.schema.json` containing `duration_ms`, `action_description`, `camera_motion`, `environment_settings`, `character_refs`, `style_refs`, `asset_refs`, `constraints`, `continuity_refs`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-014: AssetVersion Rights/Source/License Provenance Completeness (TECH-M02 / M02)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (M02)
- **Evidence Artifact:** `domain-entities.schema.json`, `DATA_MODEL.md`
- **Severity:** MAJOR
- **Affected Requirements:** Asset metadata and rights provenance
- **Affected Protected Capabilities:** CAP-06 (Assets & Continuity)
- **Affected Contracts / Repos:** `domain-entities.schema.json`, `DATA_MODEL.md`, `R04_ASSETS_CONTINUITY.md`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Domain DDD (R01), Data (R05), Security (R07)
- **Closure Evidence:** Expanded `AssetVersion` schema containing `source_type`, `license_type`, `rights_attribution`, `origin_uri`, `content_hash`, `mime_type`, `byte_size`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-015: Decouple Implementation-Specific Canonical Fields (TECH-M03 / M03)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (M03)
- **Evidence Artifact:** `domain-entities.schema.json`
- **Severity:** MAJOR
- **Affected Requirements:** Canonical domain model generality
- **Affected Protected Capabilities:** CAP-01, CAP-06
- **Affected Contracts / Repos:** `domain-entities.schema.json`
- **Earliest Responsible Round:** C02R / C03R / C04R
- **Required Independent Specialists:** Domain DDD (R01), AI (R09)
- **Closure Evidence:** Made fields like `face_embedding_hash` and `lora_weights_uri` optional/extensible metadata rather than rigid required top-level entity fields.
- **Status:** OPEN_IN_REMEDIATION

### TECH-016: Strict UUID Schema Validation (TECH-M04 / M04)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (M04)
- **Evidence Artifact:** `domain-entities.schema.json`, other contract schemas
- **Severity:** MAJOR
- **Affected Requirements:** Schema validation strictness
- **Affected Protected Capabilities:** Contract integrity
- **Affected Contracts / Repos:** All JSON schemas in `02_contracts/`
- **Earliest Responsible Round:** C03R / C04R
- **Required Independent Specialists:** Contracts (R04)
- **Closure Evidence:** Standardized UUID `$defs/UUID` to use `"format": "uuid"` and strict RFC 4122 pattern `^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$`.
- **Status:** OPEN_IN_REMEDIATION

### TECH-017: Domain Entities Schema Root Semantics and Entrypoints (TECH-M05 / M05)
- **Source Audit:** `EXTERNAL_TECHNICAL_REVIEW.md` (M05)
- **Evidence Artifact:** `domain-entities.schema.json`, `CONTRACTS_OVERVIEW.md`
- **Severity:** MAJOR
- **Affected Requirements:** Schema packaging and tooling integration
- **Affected Protected Capabilities:** DX and test tooling
- **Affected Contracts / Repos:** `domain-entities.schema.json`, `CONTRACTS_OVERVIEW.md`
- **Earliest Responsible Round:** C03R / C04R
- **Required Independent Specialists:** Contracts (R04), DX (R10)
- **Closure Evidence:** Documented fragment entrypoints (`#/$defs/Project`, `#/$defs/ShotVersion`, etc.) and defined root schema behavior in `CONTRACTS_OVERVIEW.md`.
- **Status:** OPEN_IN_REMEDIATION

---

## 3. Summary Table

| ID | Title | Severity | Round | Mandatory Roles | Status |
|---|---|---|---|---|---|
| GOV-001 | Invalid Voting Rationale Boilerplate | AUDIT_BLOCKER | C04R | All affected roles + Vote Auditor | OPEN |
| GOV-002 | Missing C05 Post-Remediation Fresh Hostile Rerun | AUDIT_BLOCKER | C05R | Auditor-A, Auditor-B, Auditor-C | OPEN |
| GOV-003 | Unvoted Normative Semantic Changes Post-C04 | AUDIT_BLOCKER | C03R/C04R | R04, R02, R07, R05 | OPEN |
| GOV-004 | C02 Deliberation Quality / Synthetic Templates | AUDIT_MAJOR | C02R | Proponent, Challenger, Domain Owner | OPEN |
| GOV-005 | Governance Artifact Overwrite | AUDIT_MAJOR | C00R/C04R | Audit Supervisor | OPEN |
| GOV-006 | Tree Hash Methodology Reproducibility | AUDIT_MINOR | C03R/C07R | R11, R07 | OPEN |
| GOV-007 | SPK-001 MV3 Keepalive Empirical Validation | AUDIT_MINOR | C03R/Spikes | R06, R09, R11 | OPEN |
| TECH-001 | Release Identity Ambiguity (0.9.0 vs 1.0.0) | BLOCKER | C03R/C04R | R10, R11 | OPEN |
| TECH-002 | Stale Internal KIT_MANIFEST Hashes | BLOCKER | C07R | R08, R11 | OPEN |
| TECH-003 | Incomplete Change Integration in Normative Spec | BLOCKER | C03R/C04R | R01, R04, R02, R07 | OPEN |
| TECH-004 | Canonical Provenance Contradiction | BLOCKER | C02R/C03R/C04R | R01, R05, R04 | OPEN |
| TECH-005 | GenerationJob State Model Contradiction | BLOCKER | C02R/C03R/C04R | R02, R03, R04 | OPEN |
| TECH-006 | FlowExecutionPort Under-Specified (10 ops) | BLOCKER | C02R/C03R/C04R | R06, R04, R02, R08 | OPEN |
| TECH-007 | Event Envelope Contradiction | BLOCKER | C02R/C03R/C04R | R04, R11, R02 | OPEN |
| TECH-008 | Provider Result/Lifecycle/Error Contradiction | BLOCKER | C02R/C03R/C04R | R04, R02, R09 | OPEN |
| TECH-009 | Handoff Claims Without Normative Source | BLOCKER | C03R/C04R | R07, R10, R01 | OPEN |
| TECH-010 | Repo Dependency Graph Incomplete/Inconsistent | BLOCKER | C03R/C04R | R01, R04, R11 | OPEN |
| TECH-011 | Final Package Hash Methodology | BLOCKER | C03R/C07R | R11, R07 | OPEN |
| TECH-012 | Certification Evidence Traceability | BLOCKER | C07R | Council Secretary, Audit Sup. | OPEN |
| TECH-013 | ShotVersion Creative Intent Completeness | MAJOR | C02R/C03R/C04R | R01, R09, R04 | OPEN |
| TECH-014 | AssetVersion Rights/Provenance Completeness | MAJOR | C02R/C03R/C04R | R01, R05, R07 | OPEN |
| TECH-015 | Decouple Implementation-Specific Canonical Fields | MAJOR | C02R/C03R/C04R | R01, R09 | OPEN |
| TECH-016 | Strict UUID Schema Validation | MAJOR | C03R/C04R | R04 | OPEN |
| TECH-017 | Domain Schema Root Semantics and Entrypoints | MAJOR | C03R/C04R | R04, R10 | OPEN |
