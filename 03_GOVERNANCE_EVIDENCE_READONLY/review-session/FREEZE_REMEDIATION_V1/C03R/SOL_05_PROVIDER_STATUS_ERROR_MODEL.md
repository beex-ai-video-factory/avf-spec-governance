# C03R SOLUTION PACKAGE 05: PROVIDER RESULT, LIFECYCLE & ERROR TAXONOMY
**SOLUTION_ID:** SOL-05
**FINDINGS_ADDRESSED:** TECH-008, FINDING_005, FINDING_022
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
`provider-result.schema.json` conflated transport-level response status with asynchronous video generation status and provided an inadequate 4-category error enum that could not drive retry policies.

---

## 2. Options Analysis

### Option A: Separated Multi-Tier Provider Response & Rich Normalized Error Taxonomy (Recommended)
- **Architecture:**
  - `status` (OperationStatus): `SUCCESS`, `FAILED`, `PENDING`, `RUNNING`
  - `generation_status` (ProviderGenerationStatus): `QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`
  - `error` (NormalizedProviderError):
    - `code`: `PROVIDER_RATE_LIMIT`, `AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`, `BUDGET_EXHAUSTED`, `UNSUPPORTED_CAPABILITY`, `NETWORK_TIMEOUT`, `BAD_REQUEST`, `PROVIDER_INTERNAL_ERROR`
    - `message`: human-readable diagnostic message
    - `retry_category`: `TRANSIENT`, `PERMANENT`, `POLICY_BLOCKED`, `RESOURCE_EXHAUSTED`
    - `suggested_backoff_ms`: integer
    - `raw_provider_error`: optional object for debugging
- **Exact Normative Files to Change:**
  - `02_contracts/provider-result.schema.json`
  - `02_contracts/CONTRACTS_OVERVIEW.md`
  - `03_repo_blueprints/R07_PROVIDER_SDK.md`
  - `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
  - `06_adrs/ADR-003_PROVIDER_ABSTRACTION.md`
  - `06_adrs/ADR-006_RETRY_POLICY.md`

### Option B: Raw HTTP Status Pass-Through
- **Drawbacks:** Leaks provider-specific HTTP codes and DOM error strings to workflow orchestrator, violating INV-008 (Normalized Provider Abstraction).

---

## 3. Decision
**Selected: Option A.** Unambiguous separation between synchronous RPC outcome, asynchronous video engine progress, and strategic retry classification.
