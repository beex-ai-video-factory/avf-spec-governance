# Specification Semantic Diff & Change Traceability

**Every semantic delta between Blueprint Kit v0.9.0 and Candidate v1.0.0 is mapped to its accepted CHANGE_ID.**

---

### Delta 1: Canonical Entity JSON Schemas (CHANGE_ID: CP-001)
- **File:** `02_contracts/domain-entities.schema.json`
- **Baseline (v0.9.0):** Defined only 3 `$defs` (`versionRef`, `shotVersion`, `promptVersion`).
- **Candidate (v1.0.0):** Defines all 14 canonical entities (`Project`, `Scene`, `Shot`, `ShotVersion`, `Character`, `CharacterVersion`, `StyleProfile`, `StyleVersion`, `Asset`, `AssetVersion`, `PromptVersion`, `GenerationJob`, `Take`, `QCResult`, `WorkflowRun`, `CostUsageRecord`).

### Delta 2: Hierarchical Error Taxonomy & Codes (CHANGE_ID: CP-002)
- **File:** `02_contracts/provider-result.schema.json`
- **Baseline (v0.9.0):** Unstructured error message strings.
- **Candidate (v1.0.0):** Structured error envelope with `error_code`, `category` (TRANSIENT/PERMANENT/POLICY/RESOURCE), `retryable`, and `retry_after_ms`.

### Delta 3: Optimistic Concurrency & Leases (CHANGE_ID: CP-003)
- **File:** `03_repo_blueprints/R02_CORE_STATE.md`
- **Baseline (v0.9.0):** Undefined concurrency control.
- **Candidate (v1.0.0):** Explicit `entity_version` on all aggregates and distributed worker leases with heartbeats.

### Delta 4: Idempotency Key & Two-Phase Budgeting (CHANGE_ID: CP-004)
- **File:** `02_contracts/provider-request.schema.json`
- **Baseline (v0.9.0):** No mandatory idempotency key; immediate billing.
- **Candidate (v1.0.0):** Mandatory SHA-256 idempotency key and 2-phase reservation/settlement protocol.

### Delta 5: Google Flow Hexagonal Port Isolation (CHANGE_ID: CP-005)
- **File:** `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
- **Baseline (v0.9.0):** Ambiguous isolation between Track A and Track B.
- **Candidate (v1.0.0):** Pure `FlowExecutionPort` contract. Zero FlowKit/CDP types in upstream core.

### Delta 6: Chrome MV3 Offscreen Keepalive (CHANGE_ID: CP-006)
- **File:** `03_repo_blueprints/R09_BROWSER_WORKER.md`
- **Baseline (v0.9.0):** Unprotected MV3 service worker subject to 5-min idle termination.
- **Candidate (v1.0.0):** Offscreen document keepalive + Native Messaging supervisor daemon.

### Delta 7: Zero-Trust HMAC IPC & Secret Enclave (CHANGE_ID: CP-007)
- **File:** `04_integration/SECURITY_MODEL.md`
- **Baseline (v0.9.0):** Plaintext environment variables and unauthenticated local IPC.
- **Candidate (v1.0.0):** HMAC-SHA256 request signatures, memory-wiping SecretEnclave, and log redaction.

### Delta 8: 3-Layer Prompt Compilation (CHANGE_ID: CP-008)
- **File:** `03_repo_blueprints/R05_PROMPT_COMPILER.md`
- **Baseline (v0.9.0):** Unstructured template string concatenation.
- **Candidate (v1.0.0):** 3-layer AST compiler (Creative -> Style/Anchor -> Provider Lowering) with AST caching.

### Delta 9: Multi-Modal Automated Quality Control (CHANGE_ID: CP-009)
- **File:** `03_repo_blueprints/R11_QC.md`
- **Baseline (v0.9.0):** Single binary QC pass/fail flag.
- **Candidate (v1.0.0):** 4-pillar scoring matrix (visual, temporal, audio, prompt) with deterministic retry decision tree.

### Delta 10: OpenTelemetry Context Propagation (CHANGE_ID: CP-010)
- **File:** `02_contracts/event-envelope.schema.json`
- **Baseline (v0.9.0):** Ad-hoc logging without distributed trace correlation.
- **Candidate (v1.0.0):** W3C Trace Context (`traceparent`) in all requests and immutable Take lineage graph.

### Delta 11: RFC 8785 JSON Canonicalization (CHANGE_ID: CP-011)
- **File:** `02_contracts/CONTRACTS_OVERVIEW.md`
- **Baseline (v0.9.0):** Non-canonical string serialization for state hashing.
- **Candidate (v1.0.0):** System-wide RFC 8785 JCS standard across TypeScript, Python, and Go.

### Delta 12: Hermetic Integration Test Harness (CHANGE_ID: CP-012)
- **File:** `03_repo_blueprints/R15_INTEGRATION_HARNESS.md`
- **Baseline (v0.9.0):** Direct dependency on live external provider APIs.
- **Candidate (v1.0.0):** Standalone containerized mock provider simulators with programmable fault injection.

### Delta 13: Operator Console HITL Override (CHANGE_ID: CP-013)
- **File:** `03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
- **Baseline (v0.9.0):** No formal workflow interruption hooks.
- **Candidate (v1.0.0):** First-class HITL workflow states and operator override audit log.

### Delta 14: FFmpeg Media Ingest Pipeline (CHANGE_ID: CP-014)
- **File:** `03_repo_blueprints/R12_MEDIA.md`
- **Baseline (v0.9.0):** Unstandardized video container handling.
- **Candidate (v1.0.0):** Standardized FFmpeg probe, faststart transcode, and perceptual hash indexing.

### Delta 15: Event Envelope v1.0 & DLQ Protocol (CHANGE_ID: CP-015)
- **File:** `02_contracts/event-envelope.schema.json`
- **Baseline (v0.9.0):** Unversioned async message payloads.
- **Candidate (v1.0.0):** Standard event envelope with causality tracking and Dead Letter Queue retry protocol.
