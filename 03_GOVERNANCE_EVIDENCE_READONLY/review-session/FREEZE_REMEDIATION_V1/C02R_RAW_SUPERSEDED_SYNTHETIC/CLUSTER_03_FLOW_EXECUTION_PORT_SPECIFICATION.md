# C02R HEARING TRANSCRIPT: CLUSTER 03 — FLOW EXECUTION PORT & COMMAND/RESULT CONTRACTS
**CLUSTER_ID:** CLUSTER-03
**FINDINGS_COVERED:** FINDING_003, FINDING_020, FINDING_048, TECH-006
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R06 (Flow Browser Specialist) & R04 (Contracts Specialist)
- **Position:** Protected capability CAP-18 requires that Track A (Browser Worker extension/CDP) and Track B (FlowKit headless bridge) be 100% swappable behind the `FlowExecutionPort` without changing upstream orchestrator code. However, `browser-command.schema.json` previously left `params` as an unrestricted object (`additionalProperties: true`) and lacked a corresponding normative `flow-execution-result.schema.json`. We must freeze the exact request parameters, expected response payloads, timeout behavior, and normalized error returns for all 10 operations:
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
- **Evidence:** `browser-command.schema.json` vs `R08_GOOGLE_FLOW_ADAPTER.md`, `R09_BROWSER_WORKER.md`, `R10_FLOWKIT_BRIDGE.md`.
- **Failure Scenario:** Two different developers implement R09 and R10. R09 expects `ATTACH_ASSETS` to take `asset_urls: []` while R10 expects `assets: [{uri, mime_type}]`. When swapping from Track A to Track B in production, the adapter crashes due to deserialization mismatch.

## 2. Challenger Attack
- **Challenger:** R15 (Red Team Specialist) & R08 (QA Specialist)
- **Attack Vector:**
  1. *UI Volatility:* Google Flow UI changes frequently. If the schema specifies rigid DOM selector parameters or engine-specific fields in the contract, every UI change will require bumping the core contract version.
  2. *Binary Payload Handling:* For `DOWNLOAD_OUTPUT` and `CAPTURE_DIAGNOSTIC`, passing multi-megabyte video files or PNG screenshots over JSON command responses will cause buffer exhaustion and high latency in Node.js IPC/event bridges.

## 3. Domain Owner Review
- **Domain Owner:** R06 (Flow Browser Specialist)
- **Evaluation:**
  - The port contract must define domain intent (e.g. "attach these asset URIs with these roles"), not raw DOM selectors. DOM selector resolution belongs strictly inside the R09/R10 implementation boundaries.
  - Large binary data (video files, screenshots, HAR logs) must NOT be passed in JSON strings. The port contract must mandate artifact storage references: R09/R10 writes binary data to local/shared staging storage or S3/GCS bucket and returns `storage_uri`, `byte_size`, `checksum_sha256`, and MIME metadata in the result JSON.
  - Conformance test harness in R15 must validate both Track A and Track B fake adapters against the identical JSON Schema test suite.

## 4. Proponent Response
- **Response:**
  - We accept separating DOM automation details from the hexagonal port contract. The 10 commands will pass semantic entities (asset IDs, prompt text, camera parameters, aspect ratio, seed, model version).
  - `flow-execution-result.schema.json` will return structured metadata with `output_uri` / `diagnostic_artifact_uri` rather than inline base64 blobs.
  - Every command discriminator in `browser-command.schema.json` and `flow-execution-result.schema.json` will use strict typed JSON Schema `oneOf` with `additionalProperties: false`.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Use gRPC with Protobuf definitions instead of JSON Schema for the FlowExecutionPort.
- **Why Rejected:** While gRPC is efficient, the primary AVF contract standard across all repos is JSON Schema / TypeScript definitions. Introducing gRPC creates unnecessary build tooling overhead for Chrome Extension MV3 environments where gRPC-web proxies would be required.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-003 amended to:
  1. Fully specify all 10 operations with strict parameter and result schemas in `browser-command.schema.json` and create `flow-execution-result.schema.json`.
  2. Define normalized error structures and timeout policies for every operation.
  3. Mandate storage URI return semantics for heavy binary outputs.
  4. Implement Track A and Track B fake conformance tests.
