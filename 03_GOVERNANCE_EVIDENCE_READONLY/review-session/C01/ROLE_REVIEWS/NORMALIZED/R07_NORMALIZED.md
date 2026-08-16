# Normalized Specialist Review — R07

**Reviewer Role:** `R07`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R07_RAW.md`  
**Raw SHA-256:** `97998c718af18bc45da3f2a65d04bf1dcbd3060a6049a00b419d3613859b4d47`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R07-001: R07 Finding F-R07-001
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SPECIFICATION_GAP / SECURITY_DATA_PROTECTION`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03`
- **Affected Contracts:** `- 02_contracts/browser-command.schema.json   - 02_contracts/CONTRACTS_OVERVIEW.md`
- **Summary:** A browser worker encounters an element timeout on Google Flow and captures a full-page diagnostic screenshot. The screenshot contains the operator's p
- **Proposed Solution:** 1. Update `SECURITY_MODEL.md` to specify:      - Storage: Dedicated private bucket (`avf-diagnostics/screenshots/`) with AES-256-GCM / KMS encryption 
- **Confidence:** `HIGH (99%) ================================================================================ ````

### F-R07-002: R07 Finding F-R07-002
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SPECIFICATION_GAP / COMPLIANCE_AUDITABILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`
- **Affected Contracts:** `- 02_contracts/event-envelope.schema.json   - 02_contracts/domain-entities.schema.json`
- **Summary:** An operator manually increases the generation credit budget on a failed project from 50 to 500 credits and edits a prompt to bypass creative guideline
- **Proposed Solution:** 1. Add canonical `OperatorAuditEvent` schema to `avf-contracts` and domain events:      ```json      {        "schema_version": "1.0",        "audit_i
- **Confidence:** `HIGH (99%) ================================================================================ ````

### F-R07-003: R07 Finding F-R07-003
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `ARCHITECTURAL_DEFECT / IPC_TRANSPORT_AUTHENTICATION`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02`
- **Affected Contracts:** `- 02_contracts/browser-command.schema.json`
- **Summary:** Track A is deployed on an operator workstation using Option A2 (loopback WebSocket on `127.0.0.1:8765`). A local malicious script, unprivileged proces
- **Proposed Solution:** 1. Specify the Option A2 Loopback Security Protocol in `SECURITY_MODEL.md`:      - Handshake Phase: Upon connection, the client must send an `AUTH_HAN
- **Confidence:** `HIGH (98%) ================================================================================ ````

### F-R07-004: R07 Finding F-R07-004
- **Severity:** `NON_BLOCKING`
- **Category:** `SPECIFICATION_GAP / PROVIDER_SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_m`
- **Affected Contracts:** `- 02_contracts/provider-request.schema.json`
- **Summary:** Google Flow encounters a persistent anti-abuse challenge, triggering fallback to a commercial video API provider (e.g. Runway / Veo). The adapter make
- **Proposed Solution:** 1. Add "Commercial API Provider Security Baseline" section to `SECURITY_MODEL.md`:      - Secrets: Commercial provider API keys must be injected as en
- **Confidence:** `HIGH (95%) ================================================================================ ````

### F-R07-005: R07 Finding F-R07-005
- **Severity:** `NON_BLOCKING`
- **Category:** `SPECIFICATION_GAP / BROWSER_EXTENSION_SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06`
- **Affected Contracts:** `- 02_contracts/CONTRACTS_OVERVIEW.md`
- **Summary:** A developer building R09 configures broad host permissions (`"<all_urls>"` or `"*://*/*"`) in `manifest.json` for convenience. A malicious web page op
- **Proposed Solution:** Codify the exact MV3 manifest security contract in `R09_BROWSER_WORKER.md` and `SECURITY_MODEL.md`:   1. *Host Permissions*: Restrict strictly to `htt
- **Confidence:** `HIGH (97%) ================================================================================ ````

### F-R07-006: R07 Finding F-R07-006
- **Severity:** `NON_BLOCKING`
- **Category:** `SPECIFICATION_GAP / SUPPLY_CHAIN_SANDBOXING`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04`
- **Affected Contracts:** `- 02_contracts/CONTRACTS_OVERVIEW.md`
- **Summary:** FlowKit (Track B) relies on a third-party npm package with a newly disclosed remote code execution vulnerability. When FlowKit processes a video gener
- **Proposed Solution:** Update `SECURITY_MODEL.md` and `R10_FLOWKIT_BRIDGE.md` with concrete sandboxing directives:   1. *Dedicated Unprivileged User*: FlowKit must execute u
- **Confidence:** `HIGH (95%) ================================================================================ ````

### F-R07-007: R07 Finding F-R07-007
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SPECIFICATION_GAP / SECRET_LEAKAGE_PREVENTION`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contr`
- **Affected Contracts:** `- 02_contracts/provider-result.schema.json   - 02_contracts/CONTRACTS_OVERVIEW.md`
- **Summary:** A Google Flow network call fails due to an expired session or rejected request. The browser worker captures the raw response headers and body (contain
- **Proposed Solution:** 1. Define a mandatory boundary **Secret Sanitization Pipeline** in `SECURITY_MODEL.md`:      - Redaction Filters: Before any `details.provider`, diagn
- **Confidence:** `HIGH (99%) ================================================================================ ````
