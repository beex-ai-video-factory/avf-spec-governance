# C02R HEARING TRANSCRIPT: CLUSTER 04 — PROVIDER RESULT, LIFECYCLE & ERROR TAXONOMY
**CLUSTER_ID:** CLUSTER-04
**FINDINGS_COVERED:** FINDING_005, FINDING_022, FINDING_051, TECH-008
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R04 (Contracts Specialist) & R09 (AI/Provider Specialist)
- **Position:** `provider-result.schema.json` previously conflated immediate synchronous operation status (`SUCCESS`, `FAILED`, `RETRYABLE_ERROR`) with asynchronous generation lifecycle status, and only provided 4 generic error categories (`TRANSIENT`, `PERMANENT`, `POLICY`, `RESOURCE`). In reality, R08 Google Flow and R07 Provider SDK need to distinguish:
  1. *Operation Response Status:* Whether the immediate HTTP/CDP request succeeded (`SUCCESS`, `FAILED`, `PENDING`, `RUNNING`).
  2. *Provider Generation Status:* The state of generation inside the remote engine (`QUEUED`, `PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELLED`).
  3. *Normalized Error Taxonomy:* A rich domain error code (`PROVIDER_RATE_LIMIT`, `AUTH_REQUIRED`, `SECURITY_CHALLENGE`, `UI_CHANGED`, `BUDGET_EXHAUSTED`, `UNSUPPORTED_CAPABILITY`, `NETWORK_TIMEOUT`, `BAD_REQUEST`, `PROVIDER_INTERNAL_ERROR`).
  4. *Retry Classification:* Strategic classification driving the workflow backoff engine (`TRANSIENT`, `PERMANENT`, `POLICY_BLOCKED`, `RESOURCE_EXHAUSTED`).
- **Evidence:** `CONTRACTS_OVERVIEW.md` §3 vs `provider-result.schema.json`.
- **Failure Scenario:** An account encounters a CAPTCHA or Google auth challenge. The provider adapter returns `FAILED` with category `PERMANENT`. The workflow fails permanently and cancels the user pipeline instead of entering `SECURITY_CHALLENGE` human-intervention pause mode.

## 2. Challenger Attack
- **Challenger:** R02 (Reliability Specialist)
- **Attack Vector:**
  1. *Taxonomy Complexity:* Having 4 distinct status/error enums increases developer error when constructing adapter responses.
  2. *State Polling Overload:* How does a polling loop distinguish between "the status check request succeeded, and the job is still generating" vs "the status check request succeeded, and the job finished with an error"?

## 3. Domain Owner Review
- **Domain Owner:** R04 (Contracts Specialist)
- **Evaluation:**
  - Clear separation is strictly necessary. The top-level response envelope represents the HTTP/RPC call. Inside the payload, `generation_status` represents the remote video generator state.
  - When `status = 'SUCCESS'` and `generation_status = 'PROCESSING'`, the workflow knows to schedule the next poll.
  - When `status = 'SUCCESS'` and `generation_status = 'FAILED'`, `normalized_error` is required and populated with the exact error code, message, and retry classification.
  - When the RPC call itself fails (e.g. network timeout to browser), `status = 'FAILED'` and `normalized_error` describes the transport failure.

## 4. Proponent Response
- **Response:**
  - We formalize this structure in `provider-result.schema.json` with conditional validation: if `status == 'FAILED'` or `generation_status == 'FAILED'`, `error` object is mandatory.
  - We update `R07_PROVIDER_SDK.md` and `R08_GOOGLE_FLOW_ADAPTER.md` with exact mapping tables translating provider HTTP codes and DOM error dialogs into the normalized error taxonomy.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Keep a flat string error message and let R06 Workflow use regex matching to decide retries.
- **Why Rejected:** String regex matching across third-party error messages is brittle, untestable, and directly violates system invariant INV-008 (Normalized Provider Abstraction).

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-004 amended to:
  1. Update `provider-result.schema.json` with separated operation status, generation status, normalized error enum, and retry class.
  2. Update `CONTRACTS_OVERVIEW.md` and adapter specifications.
  3. Implement schema validation test fixtures for all error categories.
