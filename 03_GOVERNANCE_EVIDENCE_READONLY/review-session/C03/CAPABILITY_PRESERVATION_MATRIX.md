# Protected Capability Preservation Matrix (C03)

| CAPABILITY_ID | CAPABILITY_NAME | BASELINE_STATUS | C03_PROPOSAL_STATUS | PRIMARY_CP | PRESERVATION_PROOF |
|---|---|---|---|---|---|
| C-01 | End-to-End Generation Pipeline | SPECIFIED | PRESERVED & STRENGTHENED | CP-001, CP-015 | Full 14-entity schema coverage and robust event envelope. |
| C-02 | Canonical State & Data Consistency | SPECIFIED | PRESERVED & STRENGTHENED | CP-001, CP-003, CP-011 | Version fencing, RFC 8785 JCS hashing, strict aggregate roots. |
| C-03 | Google Flow Deep Integration | SPECIFIED | PRESERVED & STRENGTHENED | CP-005, CP-006 | Hexagonal port isolation and MV3 keepalive supervisor. |
| C-04 | Pluggable Provider Abstraction | SPECIFIED | PRESERVED & STRENGTHENED | CP-002, CP-004 | Unified error taxonomy and deterministic idempotency keys. |
| C-05 | Cost & Budget Guardrails | SPECIFIED | PRESERVED & STRENGTHENED | CP-004, CP-010 | Two-phase credit reservation & settlement with reconciliation. |
| C-06 | Multi-Job Concurrency | SPECIFIED | PRESERVED & STRENGTHENED | CP-003 | Distributed worker leases and optimistic version locking. |
| C-07 | Automated Recovery & Resilience | SPECIFIED | PRESERVED & STRENGTHENED | CP-002, CP-006, CP-015 | Standard error retry engine and DLQ replay mechanics. |
| C-08 | Creative Intent & Scripting | SPECIFIED | PRESERVED & STRENGTHENED | CP-008 | 3-layer prompt compiler with narrative AST intermediate repr. |
| C-09 | Character & Style Continuity | SPECIFIED | PRESERVED & STRENGTHENED | CP-008, CP-014 | Style profile anchors and perceptual hash frame verification. |
| C-10 | Automated Quality Control (AQC) | SPECIFIED | PRESERVED & STRENGTHENED | CP-009 | 4-pillar scoring matrix with automated remediation decision tree. |
| C-11 | Media Assembly & Normalization | SPECIFIED | PRESERVED & STRENGTHENED | CP-014 | FFmpeg container probe, transcoding, and faststart optimization. |
| C-12 | Distributed Observability | SPECIFIED | PRESERVED & STRENGTHENED | CP-010 | OpenTelemetry W3C trace context propagation across all transports. |
| C-13 | Immutable Provenance Ledger | SPECIFIED | PRESERVED & STRENGTHENED | CP-010 | Complete Take lineage graph linking prompt, seed, cost, and media. |
| C-14 | Zero-Trust Security & Secrets | SPECIFIED | PRESERVED & STRENGTHENED | CP-007 | Memory-wiped secret enclave and internal HMAC IPC authentication. |
| C-15 | Audit Logging & Compliance | SPECIFIED | PRESERVED & STRENGTHENED | CP-007, CP-013 | Immutable append-only audit event stream and operator logging. |
| C-16 | Hermetic Simulation & Testing | SPECIFIED | PRESERVED & STRENGTHENED | CP-012 | Containerized mock provider servers with fault injection. |
| C-17 | Browser Worker Robustness | SPECIFIED | PRESERVED & STRENGTHENED | CP-006 | Offscreen keepalive channel and Native Messaging supervisor. |
| C-18 | Dual-Track Replaceability | SPECIFIED | PRESERVED & STRENGTHENED | CP-005 | FlowExecutionPort allows zero-code-change track switching. |
| C-19 | Operator Console & HITL | SPECIFIED | PRESERVED & STRENGTHENED | CP-013 | Real-time WebSocket bridge and workflow override state machine. |
