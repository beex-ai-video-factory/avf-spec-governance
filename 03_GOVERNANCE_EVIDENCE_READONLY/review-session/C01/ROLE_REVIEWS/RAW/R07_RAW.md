# Round C01 Independent Review — Security / Trust Boundary / Compliance Reviewer (R07_SECURITY)

**Reviewer Role:** R07_SECURITY (Security / Trust Boundary / Compliance Reviewer)  
**Session ID:** `04c090d3-6dde-488b-a40a-67e6feeffb0f`  
**Timestamp:** `2026-08-15T11:30:00+07:00`  
**Review Status:** COMPLETE / INDEPENDENT BLIND SUBMISSION  

---

## 1. Executive Summary

As the independent **R07_SECURITY** reviewer for Round C01, I have conducted a comprehensive trust-boundary, secret-protection, local IPC, extension-privilege, and anti-abuse compliance audit of the AI Video Factory (AVF) architectural specifications.

The core architecture correctly establishes key defense-in-depth principles:
1. **Isolation of browser credentials** in a privileged local execution zone (`SECURITY_MODEL.md:L21-28`).
2. **Strict prohibition of automated CAPTCHA/challenge evasion** (`ADR-007_BROWSER_SECURITY.md:L7`, `INV-012`).
3. **Canonical state ownership** in PostgreSQL rather than untrusted client runtimes (`ADR-002`, `INV-005`).

However, the specification currently exhibits critical security gaps that must be resolved before v1.0 freeze:
- **Diagnostic Screenshot Retention & Encryption Defect (GAP-006 / F-R07-001)**: The specification delegates screenshot lifecycle to vague "configurable" statements without mandating encryption standards (AES-256-GCM / KMS envelope), retention TTL (default 7 days), or visual PII masking for captured Google account headers.
- **Missing Operator Override Audit Schema & Non-Repudiation (GAP-010 / F-R07-002)**: High-privilege operator actions (prompt overrides, budget increases, security challenge bypass acknowledgments) lack an explicit audit event schema, authentication verification, and database-level immutability guarantees.
- **Loopback IPC Authentication & Handshake Gap (F-R07-003)**: Track A Option A2 (WebSocket) allows unauthenticated local processes to connect if port discovery occurs, and `browser-command.schema.json` defines unconstrained generic `params` without a formal handshake protocol.
- **Fallback Commercial API Provider Security (GAP-005 / F-R07-004)**: Fallback to commercial APIs (Veo/Runway) lacks explicit credential isolation, outbound network egress filtering (SSRF prevention), short-lived presigned URL handling, and pre-generation budget containment.
- **Secret Redaction Specification in Error Payloads & Logs (F-R07-007)**: `details.provider` in error taxonomy and raw browser worker logs lack a defined regex/key sanitization pipeline.

This review provides evidence-backed findings, threat models, and drop-in specification patches to solidify AVF's security posture without compromising core system capability.

---

## 2. Specification Files Inspected

The following blueprint kit files, contracts, and baseline registers were examined in full:

1. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md` (Primary Assigned)
2. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-007_BROWSER_SECURITY.md` (Primary Assigned)
3. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md`
4. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md`
5. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json`
6. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json`
7. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json`
8. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/event-envelope.schema.json`
9. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json`
10. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md`
11. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
12. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md`
13. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`
14. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
15. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md`
16. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
17. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md`
18. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md`
19. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/LOCAL_DEVELOPMENT.md`
20. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md`
21. Baseline Registers: `review-session/C00_FINAL/PROTECTED_CAPABILITY_REGISTER.md`, `SYSTEM_INVARIANT_INVENTORY.md`, `C00_GAP_TO_C01_SEED_REGISTER.md`.

---

## 3. System Invariants & Contracts Relevant to Security

| INVARIANT_ID | INVARIANT STATEMENT | SECURITY RELEVANCE | ENFORCEMENT LOCATION |
|---|---|---|---|
| `INV-004` | LLMs and agents may propose state changes but cannot directly mutate canonical project state. | Defense against Prompt Injection and unauthorized state alteration by autonomous agents. | `R02_CORE_STATE` Command API validation; LLM agents hold zero write credentials to PostgreSQL. |
| `INV-005` | Browser/extension/FlowKit state is never canonical business state. | Untrusted local runtime isolation; compromise or wipe of worker profile cannot corrupt canonical database state. | `R09_BROWSER_WORKER`, `R10_FLOWKIT_BRIDGE`, `R02_CORE_STATE`. |
| `INV-007` | Google Flow-specific fields do not appear in core Shot/Project contracts unless represented as namespaced provider metadata. | Prevents provider-specific secret leakage or model contamination across domain boundaries. | `avf-contracts` schema validation; JSON Schema `additionalProperties: false`. |
| `INV-008` | Provider adapters cannot directly modify Project/Shot records. | Principle of Least Privilege; adapters hold no DB write credentials and communicate strictly via result contracts. | Network/Database credential isolation; IAM segmentation. |
| `INV-012` | Authentication/security challenges do not trigger automated bypass behavior. | Policy compliance, anti-abuse containment, avoiding account termination and legal exposure (ADR-007). | `R09_BROWSER_WORKER`, `R10_FLOWKIT_BRIDGE`, `R08_GOOGLE_FLOW_ADAPTER`. |
| `INV-013` | A repo cannot read another repo's private database schema directly. | Zero Trust network segmentation; prevents lateral movement and unauthorized cross-repo data exfiltration. | Database role separation; VPC / Docker network boundaries. |
| `INV-014` | Contract consumers must validate schema versions at boundaries. | Input sanitization; blocks malformed or adversarial payloads at perimeter gateways. | Boundary middleware across all services. |
| `INV-015` | Correlation IDs must propagate across workflow, provider, browser execution, QC, and media processing. | Full forensic auditability and end-to-end traceability of every action. | `OpenTelemetry` W3C context propagation in headers and command envelopes. |
| `INV-018` | Budget limits are enforced by deterministic policy before external generation requests. | Denial-of-Wallet prevention; protects against financial exhaustion attacks or unbounded retry spend. | `R06_WORKFLOW` pre-generation budget evaluation gate. |
| `C-15` | Security boundaries (Protected Capability). | Isolates browser secrets, cookies, session tokens, and local profiles from core backend services. | `SECURITY_MODEL.md`, `ADR-007_BROWSER_SECURITY.md`. |

---

## 4. Threat Modeling & Trust Boundary Analysis

```
 +---------------------------------------------------------------------------------------+
 | TRUST ZONE 1: Core & Workflow Services (Server/Cloud Infrastructure)                   |
 | - avf-core-state (PostgreSQL canonical DB, IAM protected)                             |
 | - avf-workflow (Temporal orchestrator, state machines)                                |
 | - avf-creative / avf-prompt-compiler / avf-qc / avf-media                             |
 | - avf-platform-observability (Traces, Metrics, Audit Logs)                            |
 |                                                                                       |
 |  [Policy: ZERO browser cookies or Google account tokens stored or accepted]           |
 +-------------------------------------------+-------------------------------------------+
                                             |
                   Authenticated Contracts & Presigned URLs (Short TTL <= 15m)
                   Correlation: trace_id, workflow_run_id, generation_job_id
                                             |
                                             v
 +---------------------------------------------------------------------------------------+
 | TRUST ZONE 2: Privileged Local Execution Zone (Local Workstation / Dedicated Worker)  |
 | - avf-google-flow-adapter (R08)                                                       |
 |                                                                                       |
 |       +------------------------------------+------------------------------------+     |
 |       | Track A: avf-browser-worker (R09)  | Track B: avf-flowkit-bridge (R10)  |     |
 |       | - Local daemon / Native Host       | - Isolated bridge daemon           |     |
 |       | - Loopback WS (127.0.0.1 + Token)  | - Pinned FlowKit process (Sandboxed|     |
 |       +-----------------+------------------+-----------------+------------------+     |
 |                         |                                    |                        |
 |       Local Native Msg / Authenticated WS           Loopback IPC / Pinned DB         |
 |                         |                                    |                        |
 |                         v                                    v                        |
 |       +------------------------------------+   +--------------------------------+     |
 |       | Dedicated Chrome MV3 Profile       |   | FlowKit Worker Process / DB    |     |
 |       | - MV3 Extension (Content Scripts)  |   | (Disposable execution state)   |     |
 |       | - Isolated host permissions        |   |                                |     |
 |       +------------------------------------+   +--------------------------------+     |
 +-------------------------------------------+-------------------------------------------+
                                             |
                                     HTTPS TLS 1.3
                                             |
                                             v
 +---------------------------------------------------------------------------------------+
 | TRUST ZONE 3: External Generation Providers (Google Flow / Commercial Video APIs)     |
 | - Google Flow Web UI / Studio                                                         |
 | - Fallback Commercial Providers (Veo API, Runway API, etc.)                           |
 +---------------------------------------------------------------------------------------+
```

### Trust Zone Boundary Enforcement Rules:
1. **Zone 1 -> Zone 2 Boundary**: Zone 1 passes only abstract `ProviderGenerationRequest` or `FlowExecutionCommand` payloads and short-lived S3 presigned upload/download URLs. Zone 1 NEVER accepts or stores browser profile directories, raw cookies, or session authentication headers.
2. **Zone 2 Host Boundary (IPC Transport)**:
   - Option A1 (Native Messaging): Preferred. Standard I/O communication between Chrome extension and native binary. Extension ID must be strictly matched in the native messaging manifest (`allowed_origins: ["chrome-extension://<EXTENSION_ID>/"]`).
   - Option A2 (Loopback WebSocket): If utilized, the server MUST bind strictly to `127.0.0.1`, generate a cryptographically random session secret (minimum 256 bits of entropy) at startup, require authentication handshake before processing any command, and validate the `Origin` header (`Origin: chrome-extension://<EXTENSION_ID>`).
3. **Zone 2 -> Zone 3 Boundary**:
   - Outbound browser traffic to Google Flow is restricted to legitimate endpoints (`flow.google`, `labs.google`, `accounts.google.com`).
   - Anti-abuse challenges (reCAPTCHA, Cloudflare, Google Security Checkpoints) must trigger an immediate halt, returning error class `SECURITY_CHALLENGE` or `AUTH_REQUIRED`. Automated solving/evasion is strictly prohibited (`ADR-007`).

---

## 5. Assigned Gap Seed Resolutions

### 5.1 GAP-005 Resolution: Fallback API Provider Security Architecture
- **Problem Statement**: When Google Flow is blocked (`AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`), the system falls back to commercial API providers. The blueprint lacked concrete security requirements for credential management, egress isolation, asset presigning, and financial containment.
- **Architectural Resolution**:
  1. *Credential Isolation*: API keys for commercial providers (Runway, Veo, OpenAI) must be stored in a dedicated KMS/Secret Manager (e.g. AWS Secrets Manager / HashiCorp Vault) and injected into provider worker environment variables. Keys must never appear in `avf-core-state` database rows, Temporal workflow histories, or log messages.
  2. *SSRF Prevention & Outbound Egress Whitelist*: Provider adapter HTTP clients must enforce strict egress domain whitelisting (e.g. `api.runwayml.com`, `generativelanguage.googleapis.com`), blocking requests to link-local metadata IP (`169.254.169.254`), RFC 1918 private subnets, and loopback addresses.
  3. *Short-Lived Presigned Asset Delivery*: Reference image/video assets passed to external providers must use temporary presigned URLs with read-only permissions and a maximum TTL of 15 minutes.
  4. *Deterministic Budget Containment*: The fallback provider path must strictly pass through `INV-018` budget validation before calling external endpoints. If the estimated cost exceeds the configured `max_credits` or project budget, the workflow transitions to `BLOCKED` (`BUDGET_EXHAUSTED`) without triggering API charges.

### 5.2 GAP-006 Resolution: Diagnostic Screenshot Storage, Encryption, and Retention Policy
- **Problem Statement**: Diagnostic screenshots taken on browser automation failures may capture sensitive Google account emails, user avatars, active tab URLs, and proprietary script text. `SECURITY_MODEL.md` lacked storage format, encryption, retention TTL, and masking specifications.
- **Architectural Resolution**:
  1. *Storage Location & Encryption Standard*: Screenshots must be stored in a dedicated private object storage bucket (`avf-diagnostics/screenshots/{project_id}/{generation_job_id}/{attempt_id}.png`). Data at rest must be encrypted using AES-256-GCM / AWS KMS envelope encryption. In-transit transmission must enforce TLS 1.3.
  2. *Mandatory Retention TTL*: Diagnostic screenshots must have a default lifecycle expiration of **7 days** (168 hours) in production/staging environments, and **24 hours** in local/development environments, after which object storage lifecycle rules permanently purge the files.
  3. *Visual Header Masking / PII Sanitization*: Browser worker screenshot capture routines (`CAPTURE_DIAGNOSTIC`) must apply a pre-render visual crop or rectangular blur over the top header bar (Google account avatar, email text, browser navigation bar) prior to saving the artifact to disk or object storage.
  4. *Access Control*: Access to raw diagnostic screenshots in `R13_OPERATOR_CONSOLE` must require authenticated operator credentials with the `operator:diagnostics:read` RBAC permission, and every view action must emit an immutable audit event.

### 5.3 GAP-010 Resolution: Operator Override Authentication, RBAC, and Immutable Audit Log Schema
- **Problem Statement**: Operator overrides (manual prompt edits, budget increases, security challenge acknowledgments, forced retries) in `R13_OPERATOR_CONSOLE` were not formally defined with an audit schema, authentication protocol, or tamper-proof persistence mechanism.
- **Architectural Resolution**:
  1. *Authentication & RBAC*: Operator Console must authenticate users via OIDC / OAuth2 (PKCE flow) with role-based access control (`ROLE_VIEWER`, `ROLE_OPERATOR`, `ROLE_ADMIN`). High-privilege mutations (budget increase, prompt overwrite) require `ROLE_OPERATOR` or higher.
  2. *Canonical Audit Event Schema*: Every operator mutation must produce an `OperatorAuditEvent` recorded in PostgreSQL table `operator_audit_log`.
  3. *Non-Repudiation & Immutability*: The `operator_audit_log` table must have PostgreSQL row-level security and trigger constraints prohibiting `UPDATE` and `DELETE` operations for all application roles.
  4. *Mandatory Justification*: High-impact operator actions must require a non-empty `reason` string (minimum 10 characters) detailing why the manual intervention was executed.

---

## 6. Formal Council Findings

```
================================================================================
FINDING ID: F-R07-001
================================================================================
ROLE: R07_SECURITY
SEVERITY: BLOCKER_BEFORE_FREEZE
CATEGORY: SPECIFICATION_GAP / SECURITY_DATA_PROTECTION
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
AFFECTED_CONTRACTS:
  - 02_contracts/browser-command.schema.json
  - 02_contracts/CONTRACTS_OVERVIEW.md
EVIDENCE:
  - SECURITY_MODEL.md:L38 states: "diagnostics screenshot retention is configurable and access-controlled."
  - R09_BROWSER_WORKER.md:L17,93 lists "screenshots/diagnostics" and "screenshots on failure" as outputs, but specifies no encryption standard, retention window, or PII scrubbing.
  - C00_GAP_TO_C01_SEED_REGISTER.md lists GAP-006 as BLOCKER_BEFORE_FREEZE.
FAILURE_SCENARIO:
  A browser worker encounters an element timeout on Google Flow and captures a full-page diagnostic screenshot. The screenshot contains the operator's personal Google Account email, profile picture, active workspace tabs, and a unreleased client prompt. The screenshot is written to an unencrypted local directory or public bucket with infinite retention. Three months later, an unauthorized entity gains read access to the storage volume and harvests personal PII and proprietary prompts.
WHY_IT_MATTERS:
  Diagnostic screenshots are essential for debugging DOM changes, but without strict retention TTL, encryption at rest, and PII masking, they represent a severe privacy, GDPR/CCPA compliance, and intellectual property exposure risk.
PROPOSED_SOLUTION:
  1. Update `SECURITY_MODEL.md` to specify:
     - Storage: Dedicated private bucket (`avf-diagnostics/screenshots/`) with AES-256-GCM / KMS encryption at rest.
     - Retention: Enforced 7-day TTL (168 hours) in production via S3 Lifecycle Expiration; 24-hour TTL in local development.
     - PII Scrubbing: Implement client-side header masking in R09 screenshot capture to blur the top 64px (Google account banner/avatar).
     - Access Control: Presigned download URLs generated by Core API with max 5-minute expiry, restricted to authenticated operators with `operator:diagnostics:read` permission.
  2. Extend `browser-command.schema.json` under `CAPTURE_DIAGNOSTIC` params to support `mask_headers: boolean` (default `true`).
ALTERNATIVES_CONSIDERED:
  - Storing screenshots indefinitely for historical training: Rejected due to privacy violation risk and unnecessary storage cost.
  - Completely disabling screenshots: Rejected because visual failure context is critical for debugging Google Flow selector drift (`R1`).
CAPABILITY_IMPACT:
  None. Preserves full debugging capabilities while enforcing security compliance.
COMPATIBILITY_IMPACT:
  Non-breaking addition of default storage policy and optional schema parameters.
MIGRATION_IMPACT:
  Requires configuring S3/MinIO bucket lifecycle policies and encryption keys during deployment setup.
TEST_OR_BENCHMARK_REQUIRED:
  - Unit test in R09 verifying header masking bounding box.
  - S3 bucket policy audit verifying AES-256 encryption and 7-day expiration rule.
RESIDUAL_RISK:
  In rare cases, PII might appear in the center canvas area (e.g. user-generated prompt text containing names). This is mitigated by restricting access to authorized operators only.
CONFIDENCE:
  HIGH (99%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-002
================================================================================
ROLE: R07_SECURITY
SEVERITY: BLOCKER_BEFORE_FREEZE
CATEGORY: SPECIFICATION_GAP / COMPLIANCE_AUDITABILITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/COMMAND_EVENT_CATALOG.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json
AFFECTED_CONTRACTS:
  - 02_contracts/event-envelope.schema.json
  - 02_contracts/domain-entities.schema.json
EVIDENCE:
  - SECURITY_MODEL.md:L73 lists "operator actions authorization/audit" under Threat-oriented tests, but defines no data structure or storage mechanism.
  - R13_OPERATOR_CONSOLE.md:L71,113 notes "operator action audit" and "all mutations auditable", but provides no schema.
  - COMMAND_EVENT_CATALOG.md:L23-41 omits operator override events entirely from Domain events.
  - C00_GAP_TO_C01_SEED_REGISTER.md lists GAP-010 for R07_SECURITY.
FAILURE_SCENARIO:
  An operator manually increases the generation credit budget on a failed project from 50 to 500 credits and edits a prompt to bypass creative guidelines. The generation completes, incurring substantial unexpected API costs and producing non-compliant media. During post-incident review, logs show the project budget changed, but cannot identify which operator executed the change, what workstation IP initiated it, what the prior budget was, or what justification was provided.
WHY_IT_MATTERS:
  Without an immutable, non-repudiable audit log schema, manual operator interventions violate enterprise compliance standards (SOC 2, ISO 27001) and prevent accountability for budget overruns or unauthorized creative modifications.
PROPOSED_SOLUTION:
  1. Add canonical `OperatorAuditEvent` schema to `avf-contracts` and domain events:
     ```json
     {
       "schema_version": "1.0",
       "audit_id": "uuid",
       "occurred_at": "RFC3339",
       "operator_id": "string",
       "operator_email": "string",
       "role": "string",
       "client_ip": "string",
       "action_type": "PROMPT_OVERRIDE | BUDGET_OVERRIDE | MANUAL_RETRY | SECURITY_ACK | PROVIDER_FALLBACK | TAKE_OVERRIDE",
       "target_entity_type": "Project | Shot | GenerationJob | Take",
       "target_entity_id": "uuid",
       "previous_state": {},
       "new_state": {},
       "justification": "string (min length 10)",
       "correlation": {
         "trace_id": "string",
         "workflow_run_id": "uuid"
       }
     }
     ```
  2. Require PostgreSQL `operator_audit_log` table with database triggers disallowing `UPDATE` and `DELETE` (append-only ledger).
  3. Update `R13_OPERATOR_CONSOLE.md` and `COMMAND_EVENT_CATALOG.md` to mandate emission of `OperatorActionExecuted` event on every manual mutation.
ALTERNATIVES_CONSIDERED:
  - Storing operator actions only in unstructured application text logs: Rejected because text logs are vulnerable to truncation, rotation loss, and lack relational querying.
CAPABILITY_IMPACT:
  None. Enhances operator control and enterprise governance.
COMPATIBILITY_IMPACT:
  Additive contract schema and table migration.
MIGRATION_IMPACT:
  Add `operator_audit_log` migration script to `R02_CORE_STATE`.
TEST_OR_BENCHMARK_REQUIRED:
  - Integration test verifying mutation fails if operator context or justification is omitted.
  - SQL constraint test verifying `UPDATE`/`DELETE` queries fail against `operator_audit_log`.
RESIDUAL_RISK:
  Minimal. Slight storage overhead in PostgreSQL, well within standard relational capacity.
CONFIDENCE:
  HIGH (99%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-003
================================================================================
ROLE: R07_SECURITY
SEVERITY: BLOCKER_BEFORE_FREEZE
CATEGORY: ARCHITECTURAL_DEFECT / IPC_TRANSPORT_AUTHENTICATION
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json
AFFECTED_CONTRACTS:
  - 02_contracts/browser-command.schema.json
EVIDENCE:
  - SECURITY_MODEL.md:L42-50 specifies loopback WebSocket requirements ("bind 127.0.0.1 only; random installation secret/handshake; reject unauthenticated clients"), but no message structure or handshake protocol exists in `browser-command.schema.json`.
  - `browser-command.schema.json`:L36-39 defines `params` as generic `additionalProperties: true` without an `AUTH_HANDSHAKE` or `HEARTBEAT` command schema.
  - R09_BROWSER_WORKER.md:L63 lists "option A2 authenticated loopback WebSocket" without specifying the handshake authentication token exchange.
FAILURE_SCENARIO:
  Track A is deployed on an operator workstation using Option A2 (loopback WebSocket on `127.0.0.1:8765`). A local malicious script, unprivileged process, or malicious browser tab running on the same workstation scans `127.0.0.1` ports, discovers port 8765, and connects. Because the JSON schema defines no authentication token in the command envelope and no pre-auth handshake is mandated, the attacker sends a `SUBMIT_PROMPT` or `DOWNLOAD_OUTPUT` command, manipulating the operator's Google Flow session.
WHY_IT_MATTERS:
  Loopback network sockets on multi-tenant or developer machines are accessible to any local OS user process. Without a strict cryptographic handshake, origin header validation, and token authentication, the browser worker interface is vulnerable to local command injection and session hijacking.
PROPOSED_SOLUTION:
  1. Specify the Option A2 Loopback Security Protocol in `SECURITY_MODEL.md`:
     - Handshake Phase: Upon connection, the client must send an `AUTH_HANDSHAKE` message within 2000ms containing a cryptographically random token (`secret_token`) generated by the local worker host at startup and passed via secure local configuration (OS keychain / 0600 file).
     - Origin Check: WebSocket server must strictly reject connections where the `Origin` header does not match `chrome-extension://<EXTENSION_ID>` or `http://127.0.0.1:<R08_PORT>`.
     - Reject & Close: Unauthenticated or non-matching connections must be immediately terminated with WebSocket close code 1008 (Policy Violation).
  2. Add `AUTH_HANDSHAKE` method to `browser-command.schema.json` with required `token` property.
ALTERNATIVES_CONSIDERED:
  - Exclusively supporting Option A1 (Native Messaging): While Native Messaging has superior OS-level access control, Option A2 is required for containerized or headless dev environments where Native Messaging is unavailable. Both must be cryptographically secured.
CAPABILITY_IMPACT:
  None. Ensures secure execution across both Option A1 and Option A2.
COMPATIBILITY_IMPACT:
  Contract addition of `AUTH_HANDSHAKE` command.
MIGRATION_IMPACT:
  None before v1.0 freeze.
TEST_OR_BENCHMARK_REQUIRED:
  - Security integration test: Connect unauthorized loopback WS client with bad token and assert immediate socket termination.
  - Security integration test: Connect WS client with wrong `Origin` header and assert HTTP 403 / close code 1008.
RESIDUAL_RISK:
  If the token file permissions on disk are misconfigured by an operator, another root/admin user could read it. Standard 0600 file permissions and OS keychain mitigation resolve this.
CONFIDENCE:
  HIGH (98%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-004
================================================================================
ROLE: R07_SECURITY
SEVERITY: NON_BLOCKING
CATEGORY: SPECIFICATION_GAP / PROVIDER_SECURITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md
AFFECTED_CONTRACTS:
  - 02_contracts/provider-request.schema.json
EVIDENCE:
  - MASTER_BLUEPRINT.md:L27 diagram lists "Future API Providers" and RISK_REGISTER.md:L8 mentions "supported API provider" as fallback, but SECURITY_MODEL.md provides no specification for commercial API credential handling, outbound egress restrictions, or presigned URL lifetime.
  - C00_GAP_TO_C01_SEED_REGISTER.md identifies GAP-005.
FAILURE_SCENARIO:
  Google Flow encounters a persistent anti-abuse challenge, triggering fallback to a commercial video API provider (e.g. Runway / Veo). The adapter makes an HTTP request with an asset URL pointing to an internal S3 URL with a 7-day expiration token, and reads provider secrets from a world-readable config file. A malicious prompt injection directs the adapter to fetch an internal AWS metadata URL (`http://169.254.169.254/latest/meta-data/`), leaking cloud IAM role credentials.
WHY_IT_MATTERS:
  Fallback providers interact directly with external third-party cloud services. Without strict SSRF defenses, credential isolation, and time-bounded asset presigning, the fallback mechanism introduces critical cloud infrastructure vulnerabilities.
PROPOSED_SOLUTION:
  1. Add "Commercial API Provider Security Baseline" section to `SECURITY_MODEL.md`:
     - Secrets: Commercial provider API keys must be injected as environment variables via secret manager; never stored in core state tables.
     - Outbound Egress & SSRF Protection: All provider adapters must validate target URIs against a strict HTTPS domain allowlist and explicitly block private/link-local IP addresses (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`).
     - Asset URL Expiry: Asset URLs supplied in `asset_refs` must be presigned S3/GCS URLs with read-only permissions and a strict maximum expiration of 15 minutes.
     - Rate & Budget Protection: Fallback provider invocation must enforce `INV-018` deterministic pre-check against provider credit allocations.
ALTERNATIVES_CONSIDERED:
  - Passing raw binary asset data inline in base64: Rejected due to memory overhead and payload size limits on video assets.
CAPABILITY_IMPACT:
  None. Formalizes safe multi-provider extensibility (C-17).
COMPATIBILITY_IMPACT:
  Fully compatible with `provider-request.schema.json`.
MIGRATION_IMPACT:
  None.
TEST_OR_BENCHMARK_REQUIRED:
  - SSRF test suite attempting to submit internal IP / metadata URLs in provider request.
  - Test verifying presigned URL generator sets expiration <= 900 seconds.
RESIDUAL_RISK:
  Third-party provider logging of user prompts is subject to vendor privacy policies. Enterprise agreements should include zero-data-retention clauses.
CONFIDENCE:
  HIGH (95%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-005
================================================================================
ROLE: R07_SECURITY
SEVERITY: NON_BLOCKING
CATEGORY: SPECIFICATION_GAP / BROWSER_EXTENSION_SECURITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-007_BROWSER_SECURITY.md
AFFECTED_CONTRACTS:
  - 02_contracts/CONTRACTS_OVERVIEW.md
EVIDENCE:
  - SECURITY_MODEL.md:L32-37 states "minimal host permissions restricted to required Flow origins; no remotely hosted executable code; extension bundle versioned and checksummed".
  - It omits explicit enumeration of required Manifest V3 permissions, CSP policy directives, and origin matching rules.
FAILURE_SCENARIO:
  A developer building R09 configures broad host permissions (`"<all_urls>"` or `"*://*/*"`) in `manifest.json` for convenience. A malicious web page opened in another tab attempts to interact with the extension via `window.postMessage` or DOM event listeners, reading sensitive Flow generation states.
WHY_IT_MATTERS:
  Over-privileged Chrome extensions violate Google Web Store / enterprise security baselines and expose the host to cross-tab session leakage or DOM-based exploitation.
PROPOSED_SOLUTION:
  Codify the exact MV3 manifest security contract in `R09_BROWSER_WORKER.md` and `SECURITY_MODEL.md`:
  1. *Host Permissions*: Restrict strictly to `https://flow.google/*`, `https://labs.google/*`, `https://accounts.google.com/*`.
  2. *Extension Permissions*: Minimal set only: `["activeTab", "scripting", "storage", "downloads", "nativeMessaging"]`.
  3. *Content Security Policy*: Mandatory MV3 CSP:
     `"content_security_policy": { "extension_pages": "script-src 'self'; object-src 'none';" }`
  4. *Messaging Isolation*: Content scripts must strictly validate sender origin and reject any `window.postMessage` communication from untrusted web page scripts.
ALTERNATIVES_CONSIDERED:
  - Using broad `*://*.google.com/*`: Rejected as overly permissive; violates the principle of least privilege.
CAPABILITY_IMPACT:
  None. Covers 100% of required Google Flow interaction paths.
COMPATIBILITY_IMPACT:
  Fully compatible with Chrome MV3 standards.
MIGRATION_IMPACT:
  None.
TEST_OR_BENCHMARK_REQUIRED:
  - Manifest lint test during extension build checking permissions against the approved whitelist.
  - Cross-origin message injection test verifying untrusted page scripts cannot trigger extension actions.
RESIDUAL_RISK:
  Google Flow domain rebranding (e.g. if Google migrates Flow to a new top-level domain). Handled via standard extension version updates.
CONFIDENCE:
  HIGH (97%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-006
================================================================================
ROLE: R07_SECURITY
SEVERITY: NON_BLOCKING
CATEGORY: SPECIFICATION_GAP / SUPPLY_CHAIN_SANDBOXING
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md
AFFECTED_CONTRACTS:
  - 02_contracts/CONTRACTS_OVERVIEW.md
EVIDENCE:
  - SECURITY_MODEL.md:L53-61 requires pinning exact FlowKit commit and isolating process permissions, but lacks specific OS/filesystem containment requirements.
  - R10_FLOWKIT_BRIDGE.md:L22,46,58 specifies non-goals (not exposing SQLite, no DB coupling), but does not mandate OS-level sandbox flags.
FAILURE_SCENARIO:
  FlowKit (Track B) relies on a third-party npm package with a newly disclosed remote code execution vulnerability. When FlowKit processes a video generation request, the malicious payload attempts to traverse the local filesystem, search for `.env` files, read Core State database connection strings, or open unauthorized outbound network connections.
WHY_IT_MATTERS:
  FlowKit is third-party open-source code running in the privileged local execution zone. Without process sandboxing and filesystem jail enforcement, a supply chain flaw in FlowKit could compromise the host environment.
PROPOSED_SOLUTION:
  Update `SECURITY_MODEL.md` and `R10_FLOWKIT_BRIDGE.md` with concrete sandboxing directives:
  1. *Dedicated Unprivileged User*: FlowKit must execute under a dedicated non-root OS user (`avf-flowkit`) with restricted filesystem permissions.
  2. *Filesystem Confinement*: FlowKit write access is jailed to a single ephemeral directory (`/tmp/avf-flowkit-run/` or Docker volume). Read access to parent directories, `.env` files, and other repos is blocked.
  3. *Network Segmentation*: If containerized, FlowKit container network egress is restricted via firewall/Docker network to Google Flow domains and the local bridge port, blocking access to Core State PostgreSQL and internal service ports.
  4. *Input Sanitization*: `avf-flowkit-bridge` must validate and sanitize all prompt strings and parameter objects before passing them to FlowKit CLI/IPC.
ALTERNATIVES_CONSIDERED:
  - Running FlowKit in the same container/user as Core State: Strongly rejected due to blast radius containment failure.
CAPABILITY_IMPACT:
  None. FlowKit operates normally within its designated workdir.
COMPATIBILITY_IMPACT:
  None.
MIGRATION_IMPACT:
  Docker Compose profile `track-b` must include dedicated unprivileged user and volume isolation definitions.
TEST_OR_BENCHMARK_REQUIRED:
  - Container breakout and filesystem traversal integration test.
  - Dependency vulnerability scan (e.g. `npm audit`, `trivy`) in R10 CI pipeline.
RESIDUAL_RISK:
  Zero-day vulnerabilities in underlying Chrome/Node.js runtime. Mitigated by keeping OS packages and container base images updated.
CONFIDENCE:
  HIGH (95%)
================================================================================
```

```
================================================================================
FINDING ID: F-R07-007
================================================================================
ROLE: R07_SECURITY
SEVERITY: BLOCKER_BEFORE_FREEZE
CATEGORY: SPECIFICATION_GAP / SECRET_LEAKAGE_PREVENTION
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md
AFFECTED_CONTRACTS:
  - 02_contracts/provider-result.schema.json
  - 02_contracts/CONTRACTS_OVERVIEW.md
EVIDENCE:
  - SECURITY_MODEL.md:L37,71,74 mandates: "logs redact cookies, bearer tokens, reCAPTCHA/security artifacts, API keys; token/cookie redaction test; FlowKit raw response redaction before central logs."
  - `CONTRACTS_OVERVIEW.md`:L61 states: "Errors may contain provider-specific detail under `details.provider`".
  - `provider-result.schema.json`:L83-86 defines `error.details` as generic `additionalProperties: true` without schema-level redaction rules or size caps.
FAILURE_SCENARIO:
  A Google Flow network call fails due to an expired session or rejected request. The browser worker captures the raw response headers and body (containing `Set-Cookie: SAPISID=...`, `Authorization: Bearer ya29...`, or reCAPTCHA verification tokens) and embeds them into `error.details.provider.raw_response`. This error object is returned in `ProviderGenerationResult`, written to PostgreSQL `GenerationJob.error_details`, and broadcast over OpenTelemetry spans to centralized log aggregation. The long-lived Google session cookies are now exposed to all developers and log viewers.
WHY_IT_MATTERS:
  Accidental token/cookie leakage into error payloads and observability traces completely breaks the trust boundary between Zone 2 and Zone 1, turning local browser session credentials into widely accessible log data.
PROPOSED_SOLUTION:
  1. Define a mandatory boundary **Secret Sanitization Pipeline** in `SECURITY_MODEL.md`:
     - Redaction Filters: Before any `details.provider`, diagnostic log, or error message is emitted across the repository boundary, it must pass through an automated redaction filter that masks:
       * Bearer tokens (`Bearer [A-Za-z0-9\-\._~\+\/]+=*` -> `[REDACTED_BEARER_TOKEN]`)
       * Google Session Cookies (`(SAPISID|APISID|SSID|HSID|SID|OSID|__Secure-[A-Za-z0-9]+)=[^;]+` -> `$1=[REDACTED_COOKIE]`)
       * Authorization headers, API keys, and private URLs.
     - Payload Size Limit: Cap `error.details` to a maximum of 4096 bytes to prevent log flooding.
  2. Mandate Contract & Integration tests in `R07_PROVIDER_SDK`, `R08_GOOGLE_FLOW_ADAPTER`, `R09_BROWSER_WORKER`, `R10_FLOWKIT_BRIDGE`, and `R14_PLATFORM_OBSERVABILITY` that inject raw credential strings and assert 100% redaction before serialization.
ALTERNATIVES_CONSIDERED:
  - Completely disallowing `details.provider`: Rejected because sanitized error codes and HTTP status numbers are necessary for debugging provider failures.
CAPABILITY_IMPACT:
  None. Sanitized diagnostics preserve error classification while protecting secrets.
COMPATIBILITY_IMPACT:
  Non-breaking data-cleaning enforcement.
MIGRATION_IMPACT:
  Implementation of standard sanitization middleware across all adapter and worker repos.
TEST_OR_BENCHMARK_REQUIRED:
  - Comprehensive regex and token redaction unit/contract test suite with positive/negative test cases.
RESIDUAL_RISK:
  Novel token formats not matching standard patterns. Mitigated by combining pattern regex with key-name blocklists (`cookie`, `authorization`, `set-cookie`, `token`, `secret`, `key`, `password`).
CONFIDENCE:
  HIGH (99%)
================================================================================
```

---

## 7. Residual Uncertainties & Recommended Spikes

1. **Native Messaging Packaging vs WebSocket in Headless Linux (Option A1 vs Option A2)**:
   - *Uncertainty*: Native Messaging requires registering a manifest in the OS user directory (`~/.config/google-chrome/NativeMessagingHosts/`). In containerized CI/CD test environments running headless Chrome, loopback WebSocket might be easier to provision.
   - *Recommended Spike*: Execute Phase 0 Spike benchmarking Option A1 (Native Messaging) vs Option A2 (Authenticated WebSocket with token handshake) in both macOS workstation and Linux headless Docker environments to validate handshake latency, connection stability upon service worker restart, and security ergonomics.
2. **Dynamic reCAPTCHA / Anti-Abuse Escalation Latency**:
   - *Uncertainty*: How quickly can an operator be alerted via `R13_OPERATOR_CONSOLE` when Google Flow presents a security checkpoint, and what is the maximum idle timeout before Google Flow drops the generation draft?
   - *Recommended Spike*: Measure Google Flow session timeout behavior during human challenge pauses to establish the optimal `HUMAN_REQUIRED` pause deadline in `R06_WORKFLOW`.

---

## 8. Capability Preservation & Invariant Compliance Confirmation

I have verified that none of the proposed security solutions degrade the core system capabilities:
- **C-01 through C-03 (State, Immutability, Provenance)**: Fully preserved; strengthened by adding immutable operator audit logs.
- **C-04 through C-06 (Provider Abstraction, Flow Isolation, Track A/B Interchangeability)**: Fully preserved; boundary contracts and sanitization ensure zero credential leakage across interfaces.
- **C-07 through C-10 (Idempotency, Durable Workflow, Bounded Retries, Fake Provider)**: Fully preserved; budget enforcement and challenge halting integrate seamlessly with Temporal state machines.
- **C-14 & C-15 (Human Escalation & Security Boundaries)**: Directly fulfilled and elevated to enterprise-grade compliance.
- **C-17 (Future Provider Extensibility)**: Secured with SSRF protections, credential isolation, and short-lived presigned URL contracts.

---

## 9. Reviewer Sign-Off

```text
================================================================================
COUNCIL REVIEW SIGNATURE
================================================================================
Role: R07_SECURITY (Security / Trust Boundary / Compliance Reviewer)
Model: Gemini 2.5 Flash
Session ID: 04c090d3-6dde-488b-a40a-67e6feeffb0f
Timestamp: 2026-08-15T11:30:00+07:00
Review Mode: Round C01 Independent Blind Review
Status: SUBMITTED - CANDIDATE FOR CONSOLIDATION
================================================================================
```
