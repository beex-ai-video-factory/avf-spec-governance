# Normalized Specialist Review — R02

**Reviewer Role:** `R02`  
**Original Raw File:** `review-session/C01/ROLE_REVIEWS/RAW/R02_RAW.md`  
**Raw SHA-256:** `2d7cdf9fcbd0d4121f0f840fa1a4bb0bb0e7e16c1dfd33213262a184ca5a0d0a`  
**Normalization Status:** Verified & Normalized (Raw semantics preserved verbatim)

---

## Role Findings Summary

### F-R02-001: R02 Finding F-R02-001
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `CONTRACTS_ERROR_HANDLING`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0`
- **Affected Contracts:** ``https://avf.local/contracts/provider-result/1.0`, `https://avf.local/contracts/error-detail/1.0``
- **Summary:** A provider adapter encounters a rate limit and returns `PROVIDER_RATE_LIMIT` with details `{ "backoff": 120 }` instead of `{ "retry_after_sec": 120 }`
- **Proposed Solution:** Create a formal, normative schema `error-detail.schema.json` in `avf-contracts` and update `provider-result.schema.json` to reference it. The schema m
- **Confidence:** `1.0 (Certain)`

### F-R02-002: R02 Finding F-R02-002
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `TIMEOUTS_AND_CONCURRENCY`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json` - `review-session/C00_FINAL/C00_GA`
- **Affected Contracts:** ``https://avf.local/contracts/browser-command/1.0``
- **Summary:** A selector changes on Google Flow. The browser worker's DOM wait loop hangs indefinitely waiting for a button that will never appear. Because no inter
- **Proposed Solution:** Explicitly specify normative timeout contracts in `R09_BROWSER_WORKER.md` and `browser-command.schema.json`: 1. Add `timeout_ms` property per command 
- **Confidence:** `1.0 (Certain)`

### F-R02-003: R02 Finding F-R02-003
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `IDEMPOTENCY_AND_RECONCILIATION`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-003) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.`
- **Affected Contracts:** ``STATUS_STATE_MACHINES.md`, `GenerationJob` lifecycle`
- **Summary:** The browser worker submits a prompt to Google Flow. The generation starts on Google's backend, but the worker crashes before capturing the job ID. The
- **Proposed Solution:** Formalize the **Uncertain Submit Reconciliation Protocol** in `avf-workflow` and `avf-google-flow-adapter`: 1. Add an explicit intermediate state `SUB
- **Confidence:** `0.95 (High)`

### F-R02-004: R02 Finding F-R02-004
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `CONCURRENCY_AND_SPLIT_BRAIN`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/browser-command.schema.json` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.`
- **Affected Contracts:** ``STATUS_STATE_MACHINES.md` (Browser execution command), `browser-command.schema.json``
- **Summary:** Browser Worker A leases command $C_1$. Worker A encounters a 45-second network partition or CPU throttle. The lease expires, and the queue issues $C_1
- **Proposed Solution:** 1. Add `lease_epoch: integer (minimum: 1)` to `browser-command.schema.json` and all command status payloads. 2. In `avf-core-state`, implement monoton
- **Confidence:** `1.0 (Certain)`

### F-R02-005: R02 Finding F-R02-005
- **Severity:** `BLOCKER_BEFORE_FREEZE`
- **Category:** `DISTRIBUTED_TRANSACTIONS_AND_BUDGET`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md` (INV-018) - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9`
- **Affected Contracts:** ``R02_CORE_STATE.md` Public API (`AppendUsageRecord`, budget tracking)`
- **Summary:** Core State decrements a project's budget before calling the provider. The generation activity fails due to a transient browser crash or network outage
- **Proposed Solution:** Introduce a **Two-Phase Budget Reservation Protocol** in `avf-core-state`: 1. Add commands to `R02_CORE_STATE.md`:    - `ReserveBudget(project_id, gen
- **Confidence:** `1.0 (Certain)`

### F-R02-006: R02 Finding F-R02-006
- **Severity:** `MEDIUM`
- **Category:** `BROWSER_EXTENSION_LIFECYCLE`
- **Affected Files:** `- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md` - `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/07_risk/RISK_REGISTER.md` (Risk R8)`
- **Affected Contracts:** `Track A Browser Worker Host-Extension Protocol`
- **Summary:** During a 5-minute video generation in Google Flow, the MV3 background service worker becomes idle according to Chromium's internal lifecycle timer and
- **Proposed Solution:** Specify the MV3 lifecycle management architecture in `R09_BROWSER_WORKER.md`: 1. Use **Chrome Native Messaging** as primary transport: Native Messagin
- **Confidence:** `0.95 (High)`
