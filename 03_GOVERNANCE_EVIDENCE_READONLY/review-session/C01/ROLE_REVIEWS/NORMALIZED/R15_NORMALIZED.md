# Normalized Specialist Review — R15

**Reviewer Role:** `R15`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R15_RAW.md`  
**Raw SHA-256:** `c33e04c2962bd1b33fde53f7e09be31628608550e510afdc256c15a36dfc07a3`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R15-001: R15 Finding F-R15-001
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-001: R15 Finding F-R15-001
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07`
- **Affected Contracts:** `- browser-command.schema.json (CAPTURE_DIAGNOSTIC)   - SECURITY_MODEL`
- **Summary:** Browser worker captures diagnostic screenshots on UI failures. The screenshots capture Google profile email addresses, account avatars, workspace name
- **Proposed Solution:** 1. Mandate Client-Side Redaction: `R09_BROWSER_WORKER` content script must apply CSS masking/blurring over user profile headers, email pills, and sens
- **Confidence:** `HIGH (Defect proven by spec omission in SECURITY_MODEL.md). ````

### F-R15-002: R15 Finding F-R15-002
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-002: R15 Finding F-R15-002
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/`
- **Affected Contracts:** `- event-envelope   - domain-entities   - STATUS_STATE_MACHINES`
- **Summary:** A compromised operator session or rogue insider modifies prompt text to bypass safety policies, forces approval on a rejected QC take, or inflates pro
- **Proposed Solution:** 1. Define Canonical Audit Contract: Add `operator-override-audit.schema.json` requiring: `operator_id`, `role`, `timestamp`, `action_type` (e.g. `BUDG
- **Confidence:** `HIGH (Defect proven by lack of audit schema and escalation controls in R13 and contracts). ````

### F-R15-003: R15 Finding F-R15-003
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-003: R15 Finding F-R15-003
- **Severity:** `HIGH`
- **Category:** `SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06`
- **Affected Contracts:** `- browser-command.schema.json   - SECURITY_MODEL`
- **Summary:** A developer or operator running the browser worker locally visits an external website in their personal browser. The external website runs malicious J
- **Proposed Solution:** 1. Mandate Native Messaging as Primary: Explicitly specify Chrome Native Messaging (A1) as the default and required production transport; downgrade lo
- **Confidence:** `HIGH (Established browser security vulnerability pattern with standard web mitigation). ````

### F-R15-004: R15 Finding F-R15-004
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-004: R15 Finding F-R15-004
- **Severity:** `HIGH`
- **Category:** `SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_`
- **Affected Contracts:** `- provider-request   - browser-command.schema.json`
- **Summary:** A script brief incorporates untrusted third-party character descriptions containing indirect prompt injection payloads (e.g. text containing HTML cont
- **Proposed Solution:** 1. Structural Prompt Sanitization in R05: Enforce strict input filtering in `R05_PROMPT_COMPILER`: strip control characters, enforce maximum token/cha
- **Confidence:** `HIGH (Standard AI/web injection surface requiring defensive architecture). ````

### F-R15-005: R15 Finding F-R15-005
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-005: R15 Finding F-R15-005
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `RELIABILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk`
- **Affected Contracts:** `- STATUS_STATE_MACHINES   - browser-command.schema.json   - provider-request`
- **Summary:** The browser worker submits a video generation command to Google Flow. Google Flow starts the generation job (incurring cost). At that exact instant, t
- **Proposed Solution:** 1. Add Explicit State `RECONCILING`: In `STATUS_STATE_MACHINES.md`, add an explicit transition: `SUBMITTING -> RECONCILING` upon worker crash or commu
- **Confidence:** `HIGH (Core distributed systems failure mode in non-idempotent UI automation). ````

### F-R15-006: R15 Finding F-R15-006
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-006: R15 Finding F-R15-006
- **Severity:** `HIGH`
- **Category:** `RELIABILITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blue`
- **Affected Contracts:** `- STATUS_STATE_MACHINES   - CONTRACTS_OVERVIEW (Error Taxonomy)`
- **Summary:** Google Flow deploys a breaking frontend change. 30 concurrent shot jobs fail DOM selector lookups and are classified as `TRANSIENT_BROWSER`. Each work
- **Proposed Solution:** 1. Centralized Circuit Breaker in R07 / R06: Implement a cross-worker circuit breaker in `avf-provider-sdk` / `avf-workflow` tracking failure rates ac
- **Confidence:** `HIGH (Standard distributed systems resilience pattern essential for fragile web automation). ````

### F-R15-007: R15 Finding F-R15-007
- **Severity:** `NON_BLOCKING`
- **Category:** `Architecture`
- **Affected Files:** `NOT_SPECIFIED`
- **Affected Contracts:** `NOT_SPECIFIED`
- **Summary:** NOT_SPECIFIED
- **Proposed Solution:** NOT_SPECIFIED
- **Confidence:** `HIGH`

### F-R15-007: R15 Finding F-R15-007
- **Severity:** `HIGH`
- **Category:** `SECURITY`
- **Affected Files:** `- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md   - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01`
- **Affected Contracts:** `- SECURITY_MODEL   - browser-command.schema.json`
- **Summary:** FlowKit is installed as an external OSS engine. A compromised npm/python dependency in FlowKit's dependency tree or an unauthenticated local debug end
- **Proposed Solution:** 1. Sandboxed Process Isolation: Mandate that `avf-flowkit-bridge` and FlowKit execute within an isolated container or restricted OS user profile with 
- **Confidence:** `HIGH (Fundamental zero-trust supply chain defense for OSS dependencies). ````
