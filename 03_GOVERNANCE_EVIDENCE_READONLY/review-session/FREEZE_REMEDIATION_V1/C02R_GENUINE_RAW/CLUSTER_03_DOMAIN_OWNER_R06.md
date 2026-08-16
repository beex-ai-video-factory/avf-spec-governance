# DOMAIN OWNER ARCHITECTURAL REVIEW & VERDICT
## Cluster 03: FlowExecutionPort Hexagonal Port & 10 Operation Strict Contracts
**DOMAIN_OWNER:** R06 (Flow Browser Specialist)  
**AFFILIATION:** AI Video Factory Architecture Council — C02R Genuine Adversarial Cross-Examination  
**TARGET_SPEC_VERSION:** v1.0.0 Freeze Candidate  
**DOCUMENT_STATUS:** AUTHORITATIVE_VERDICT  
**DATE:** 2026-08-15  
**CORRESPONDING_FINDINGS:** TECH-006, FINDING_003, FINDING_020, FINDING_048  
**TARGET_SCHEMAS & BLUEPRINTS:**  
- `02_contracts/browser-command.schema.json`
- `02_contracts/flow-execution-result.schema.json` (NEW)
- `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`
- `03_repo_blueprints/R09_BROWSER_WORKER.md`
- `03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
- `03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`
- `review-session/FREEZE_REMEDIATION_V1/C03R/SOL_03_FLOW_EXECUTION_PORT_CONTRACT.md`
- `review-session/FREEZE_REMEDIATION_V1/CHANGE_PROPOSALS/CP-003_FLOW_EXECUTION_PORT_DISCRIMINATED_OPERATIONS.md`

---

## 1. Executive Summary & Domain Authority Statement

As the Flow Browser Specialist and designated Domain Owner for **Cluster 03 (FlowExecutionPort Strict Operations & Results)**, I have conducted an exhaustive, rigorous evaluation of the port proposal defined in SOL-03 / CP-003 and the adversarial cross-examination brief submitted by Challenger **R04 (Contracts Specialist)** in [`CLUSTER_03_CHALLENGER_R04.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW/CLUSTER_03_CHALLENGER_R04.md).

### 1.1 The Criticality of FlowExecutionPort
The `FlowExecutionPort` is the single most sensitive integration boundary in the AI Video Factory. It enforces **Protected Capability CAP-18**: the absolute hot-swappability of **Track A** (`avf-browser-worker` Chrome MV3 Extension + CDP / Native Messaging) and **Track B** (`avf-flowkit-bridge` Headless OSS Bridge) beneath `avf-google-flow-adapter` (R08) without changing a single line of upstream workflow orchestration logic (`avf-workflow` R06).

In the v0.9.0 baseline, `browser-command.schema.json` contained an open-ended `params: { "type": "object", "additionalProperties": true }` and completely lacked a corresponding normative result schema. This defect invited architectural drift, type leakage, and uncoordinated breaking changes between Track A and Track B.

### 1.2 Evaluation of the Challenger Attack
Challenger R04 correctly attacked three critical vulnerabilities in the Candidate v1.0 draft:
1. **$O(N)$ Validation Overhead & SDK Codegen Degradation:** A naive root `oneOf` without discriminator metadata forces deep branch evaluation and generates broken intersection types across TypeScript, Go, and Python.
2. **Hexagonal Boundary Pollution:** Exposing `wait_for_selector` in `OPEN_FLOW` violates R08 non-goals, couples upstream orchestrators to volatile Google Flow DOM hashes, and breaks Track B compatibility.
3. **Payload & Memory Hazards:** Synchronous remote object storage assumptions during browser failures cause diagnostic loss, while unfiltered HAR capture in Chrome MV3 service workers triggers fatal Out-Of-Memory (`SIGKILL`) crashes.

### 1.3 Authoritative Ruling
I **UPHOLD** all three challenges levied by R04 and issue this authoritative Domain Owner Review to establish a frozen, hardened, fully symmetric hexagonal port specification. Below, I systematically review all 10 operations, prove the decoupling of UI volatility, mandate a zero-binary storage URI passing protocol, and issue binding implementation directives for freeze certification.

---

## 2. Comprehensive Review of All 10 FlowExecutionPort Operations

To guarantee complete parity and deterministic hot-swappability between Track A and Track B, every operation across the `FlowExecutionPort` must possess an explicit command schema, a symmetric typed result schema, a deterministic timeout envelope, and a normalized error mapping.

```
+-----------------------------------------------------------------------------+
|                      avf-workflow / Orchestrator (R06)                      |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
|                     avf-google-flow-adapter (R08)                          |
+-----------------------------------------------------------------------------+
                                       |
                     FlowExecutionPort Hexagonal Boundary
       (browser-command.schema.json <---> flow-execution-result.schema.json)
                                       |
            +--------------------------+--------------------------+
            |                                                     |
            v                                                     v
+-----------------------+                             +-----------------------+
|  Track A (R09 Worker) |                             |  Track B (R10 Bridge) |
| Chrome MV3 Extension  |                             | Headless FlowKit API  |
| CDP / Native Message  |                             | Py Local Engine / WS  |
+-----------------------+                             +-----------------------+
            |                                                     |
            +--------------------------+--------------------------+
                                       |
                                       v
                     +-----------------------------------+
                     |       Google Flow Platform        |
                     +-----------------------------------+
```

### 2.1 Operation 1: `ENSURE_SESSION`
- **Domain Purpose:** Validates or initializes an execution worker session against Google Flow, verifying authenticated credentials, browser context readiness, and worker lease viability.
- **Contract Signature:**
  - **Command `EnsureSessionCommand`:**
    ```json
    {
      "command_id": "c1a2b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
      "command_type": "ENSURE_SESSION",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:00Z",
      "timeout_ms": 30000,
      "params": {
        "account_alias": "studio_prod_primary",
        "headless": true,
        "profile_directory": "profiles/prod_flow_user_01"
      }
    }
    ```
  - **Result `EnsureSessionResult`:**
    ```json
    {
      "command_id": "c1a2b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "ENSURE_SESSION",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:02Z",
      "duration_ms": 2150,
      "result": {
        "session_state": "READY",
        "account_alias": "studio_prod_primary",
        "authenticated_user_email": "prod-flow-agent@studio.internal",
        "worker_version": "1.0.0-rc3",
        "active_tab_id": 1042
      },
      "error": null
    }
    ```
- **Execution & Failure Semantics:** If authentication is missing or expired, the worker MUST NOT attempt automated credential harvesting or CAPTCHA solving. It returns `status: "FAILED"`, `error.code: "AUTH_REQUIRED"` or `"SECURITY_CHALLENGE"`, and `retry_category: "POLICY_BLOCKED"` to trigger the human escalation gate.

---

### 2.2 Operation 2: `OPEN_FLOW`
- **Domain Purpose:** Navigates the worker context to the designated Google Flow environment and verifies readiness of the target semantic surface.
- **Purge of `wait_for_selector`:** Candidate v1.0 leaked DOM selector parameters into this command. In the frozen specification, `wait_for_selector` is **strictly expunged**. The caller specifies target semantic intent via `target_surface`.
- **Contract Signature:**
  - **Command `OpenFlowCommand`:**
    ```json
    {
      "command_id": "e4f5a6b7-c8d9-0e1f-2a3b-4c5d6e7f8a9b",
      "command_type": "OPEN_FLOW",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:02Z",
      "timeout_ms": 45000,
      "params": {
        "flow_url": "https://flow.google.com/studio",
        "target_surface": "STUDIO_WORKSPACE"
      }
    }
    ```
  - **Result `OpenFlowResult`:**
    ```json
    {
      "command_id": "e4f5a6b7-c8d9-0e1f-2a3b-4c5d6e7f8a9b",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "OPEN_FLOW",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:05Z",
      "duration_ms": 3200,
      "result": {
        "current_url": "https://flow.google.com/studio/workspace",
        "surface_state": "READY_FOR_PROMPT",
        "page_title": "Google Flow Studio"
      },
      "error": null
    }
    ```
- **Execution & Failure Semantics:** R09 (Track A) resolves surface readiness internally via its private `SelectorRegistry` (evaluating ARIA accessibility landmarks, text content anchors, and test-IDs). R10 (Track B) executes an HTTP session handshake against FlowKit. If the page fails to reach the semantic milestone within `timeout_ms`, the worker returns `error.code: "UI_CHANGED"` or `"NETWORK_TIMEOUT"`.

---

### 2.3 Operation 3: `CREATE_OR_SELECT_PROJECT`
- **Domain Purpose:** Binds the execution session to a designated Google Flow workspace/project, creating it if it does not exist or selecting an existing workspace.
- **Contract Signature:**
  - **Command `CreateOrSelectProjectCommand`:**
    ```json
    {
      "command_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "command_type": "CREATE_OR_SELECT_PROJECT",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:05Z",
      "timeout_ms": 30000,
      "params": {
        "project_name": "AVF_PROJ_9B1DEB4D",
        "project_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
      }
    }
    ```
  - **Result `CreateOrSelectProjectResult`:**
    ```json
    {
      "command_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "CREATE_OR_SELECT_PROJECT",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:07Z",
      "duration_ms": 1800,
      "result": {
        "project_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "project_name": "AVF_PROJ_9B1DEB4D",
        "flow_internal_project_id": "gflow_prj_88492019",
        "is_newly_created": true
      },
      "error": null
    }
    ```

---

### 2.4 Operation 4: `ATTACH_ASSETS`
- **Domain Purpose:** Uploads and binds character visual references, style reference frames, or start/end framing images into the active Google Flow generation slot.
- **Contract Signature:**
  - **Command `AttachAssetsCommand`:**
    ```json
    {
      "command_id": "f5e4d3c2-b1a0-9f8e-7d6c-5b4a3f2e1d0c",
      "command_type": "ATTACH_ASSETS",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:07Z",
      "timeout_ms": 60000,
      "params": {
        "assets": [
          {
            "asset_id": "d3b07384-d113-40f7-8739-9d5a57041f12",
            "storage_uri": "s3://avf-production-assets/projects/proj-101/chars/vance_head.png",
            "mime_type": "image/png",
            "role": "CHARACTER",
            "slot_index": 0
          },
          {
            "asset_id": "e4c18495-e224-51a8-9840-0e6b68152a23",
            "storage_uri": "s3://avf-production-assets/projects/proj-101/styles/noir_ref.png",
            "mime_type": "image/png",
            "role": "STYLE",
            "slot_index": 1
          }
        ]
      }
    }
    ```
  - **Result `AttachAssetsResult`:**
    ```json
    {
      "command_id": "f5e4d3c2-b1a0-9f8e-7d6c-5b4a3f2e1d0c",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "ATTACH_ASSETS",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:11Z",
      "duration_ms": 4100,
      "result": {
        "attached_assets": [
          {
            "asset_id": "d3b07384-d113-40f7-8739-9d5a57041f12",
            "flow_asset_slot_id": "slot_char_0",
            "upload_status": "ATTACHED"
          },
          {
            "asset_id": "e4c18495-e224-51a8-9840-0e6b68152a23",
            "flow_asset_slot_id": "slot_style_1",
            "upload_status": "ATTACHED"
          }
        ]
      },
      "error": null
    }
    ```
- **Decoupling Invariant:** The command contract accepts ONLY `storage_uri` references. R09/R10 worker logic fetches the binary stream into local scratch storage, verifies byte counts, and injects the files via standard OS file chooser hooks or internal API payloads.

---

### 2.5 Operation 5: `SET_GENERATION_OPTIONS`
- **Domain Purpose:** Sets rendering constraints such as aspect ratio, resolution, duration, seed, and model version in Google Flow.
- **Contract Signature:**
  - **Command `SetGenerationOptionsCommand`:**
    ```json
    {
      "command_id": "7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e",
      "command_type": "SET_GENERATION_OPTIONS",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:11Z",
      "timeout_ms": 20000,
      "params": {
        "aspect_ratio": "16:9",
        "resolution": "1080p",
        "duration_seconds": 5.0,
        "seed": 429810,
        "model_version": "veo-2.0-generate-preview",
        "camera_controls": {
          "motion_type": "PAN_LEFT",
          "speed": 2
        }
      }
    }
    ```
  - **Result `SetGenerationOptionsResult`:**
    ```json
    {
      "command_id": "7b8c9d0e-1f2a-3b4c-5d6e-7f8a9b0c1d2e",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "SET_GENERATION_OPTIONS",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:12Z",
      "duration_ms": 950,
      "result": {
        "applied_options": {
          "aspect_ratio": "16:9",
          "resolution": "1080p",
          "duration_seconds": 5.0,
          "seed": 429810,
          "model_version": "veo-2.0-generate-preview"
        }
      },
      "error": null
    }
    ```

---

### 2.6 Operation 6: `SUBMIT_PROMPT`
- **Domain Purpose:** Enters the compiled prompt text and triggers the generation action, returning a tracked provider job ID.
- **Contract Signature:**
  - **Command `SubmitPromptCommand`:**
    ```json
    {
      "command_id": "3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
      "command_type": "SUBMIT_PROMPT",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:12Z",
      "timeout_ms": 30000,
      "params": {
        "prompt_text": "Cinematic shot of Detective Vance walking through neo-noir rain-slicked alley, 35mm anamorphic lens, high contrast rim lighting.",
        "negative_prompt": "cartoon, 3d render, oversaturated, blurry, bad anatomy",
        "idempotency_key": "idemp_job_8f3c7e4d1a2b_att1",
        "attempt_index": 1
      }
    }
    ```
  - **Result `SubmitPromptResult`:**
    ```json
    {
      "command_id": "3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "SUBMIT_PROMPT",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:15Z",
      "duration_ms": 2850,
      "result": {
        "provider_job_id": "flow_gen_job_998241029",
        "initial_status": "ACCEPTED",
        "queue_position": 1,
        "submission_timestamp_utc": "2026-08-15T21:30:14Z"
      },
      "error": null
    }
    ```
- **Ambiguity Invariant:** If `SUBMIT_PROMPT` times out or disconnects mid-click, the worker MUST NOT blind-retry. It returns `status: "FAILED"`, `error.code: "UNCERTAIN_SUBMISSION"`, and `retry_category: "RECONCILIATION_REQUIRED"` to force the adapter (R08) to query generation state before re-dispatching.

---

### 2.7 Operation 7: `READ_GENERATION_STATE`
- **Domain Purpose:** Queries the progress, queue state, ETA, and completion status of an in-flight video generation job.
- **Contract Signature:**
  - **Command `ReadGenerationStateCommand`:**
    ```json
    {
      "command_id": "9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d",
      "command_type": "READ_GENERATION_STATE",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:30:30Z",
      "timeout_ms": 15000,
      "params": {
        "provider_job_id": "flow_gen_job_998241029"
      }
    }
    ```
  - **Result `ReadGenerationStateResult`:**
    ```json
    {
      "command_id": "9a0b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "READ_GENERATION_STATE",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:30:31Z",
      "duration_ms": 420,
      "result": {
        "provider_job_id": "flow_gen_job_998241029",
        "generation_status": "COMPLETED",
        "progress_pct": 100,
        "eta_seconds": 0,
        "has_render_output": true,
        "output_preview_uri": "https://flow.google.com/previews/flow_gen_job_998241029_thumb.jpg"
      },
      "error": null
    }
    ```

---

### 2.8 Operation 8: `DOWNLOAD_OUTPUT`
- **Domain Purpose:** Downloads the finished MP4 video from Google Flow, computes its SHA-256 digest, extracts video dimensions/duration, and stages it to the designated storage URI.
- **Contract Signature:**
  - **Command `DownloadOutputCommand`:**
    ```json
    {
      "command_id": "2d3e4f5a-6b7c-8d9e-0f1a-2b3c4d5e6f7a",
      "command_type": "DOWNLOAD_OUTPUT",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:31:00Z",
      "timeout_ms": 120000,
      "params": {
        "provider_job_id": "flow_gen_job_998241029",
        "destination_storage_uri": "s3://avf-production-media/projects/proj-101/takes/take_001.mp4",
        "expected_mime_type": "video/mp4"
      }
    }
    ```
  - **Result `DownloadOutputResult`:**
    ```json
    {
      "command_id": "2d3e4f5a-6b7c-8d9e-0f1a-2b3c4d5e6f7a",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "DOWNLOAD_OUTPUT",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:31:12Z",
      "duration_ms": 11800,
      "result": {
        "provider_job_id": "flow_gen_job_998241029",
        "storage_uri": "s3://avf-production-media/projects/proj-101/takes/take_001.mp4",
        "byte_size": 18450192,
        "checksum_sha256": "9f83c68a0a8f7c9e5b4a3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a",
        "mime_type": "video/mp4",
        "dimensions": {
          "width": 1920,
          "height": 1080
        },
        "duration_ms": 5000
      },
      "error": null
    }
    ```

---

### 2.9 Operation 9: `CAPTURE_DIAGNOSTIC`
- **Domain Purpose:** Captures a bounded bundle containing failure screenshots, sanitized console logs, and filtered network telemetry, writing to a local or remote storage URI.
- **Contract Signature:**
  - **Command `CaptureDiagnosticCommand`:**
    ```json
    {
      "command_id": "8f7e6d5c-4b3a-2f1e-0d9c-8b7a6f5e4d3c",
      "command_type": "CAPTURE_DIAGNOSTIC",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:31:15Z",
      "timeout_ms": 30000,
      "params": {
        "destination_diagnostic_uri": "file:///tmp/avf/diagnostics/diag_sess_worker_node_01_ch01.zip",
        "include_screenshot": true,
        "include_har": true,
        "har_capture_mode": "METADATA_ONLY",
        "include_console_logs": true,
        "max_bundle_size_bytes": 26214400
      }
    }
    ```
  - **Result `CaptureDiagnosticResult`:**
    ```json
    {
      "command_id": "8f7e6d5c-4b3a-2f1e-0d9c-8b7a6f5e4d3c",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "CAPTURE_DIAGNOSTIC",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:31:17Z",
      "duration_ms": 1950,
      "result": {
        "diagnostic_bundle_uri": "file:///tmp/avf/diagnostics/diag_sess_worker_node_01_ch01.zip",
        "byte_size": 4210984,
        "checksum_sha256": "4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c",
        "diagnostics_summary": {
          "screenshot_captured": true,
          "har_captured": true,
          "logs_captured": true,
          "truncated": false,
          "captured_components": ["SCREENSHOT_PNG", "HAR_FILTERED", "CONSOLE_LOGS"],
          "dropped_components": []
        }
      },
      "error": null
    }
    ```

---

### 2.10 Operation 10: `CANCEL`
- **Domain Purpose:** Instructs the worker to cancel an active prompt submission or rendering job on Google Flow and reset page interactive state.
- **Contract Signature:**
  - **Command `CancelCommand`:**
    ```json
    {
      "command_id": "6a5b4c3d-2e1f-0a9b-8c7d-6e5f4a3b2c1d",
      "command_type": "CANCEL",
      "session_id": "sess_worker_node_01_ch01",
      "timestamp_utc": "2026-08-15T21:31:20Z",
      "timeout_ms": 15000,
      "params": {
        "provider_job_id": "flow_gen_job_998241029",
        "reason": "OPERATOR_ABORT_REQUESTED"
      }
    }
    ```
  - **Result `CancelResult`:**
    ```json
    {
      "command_id": "6a5b4c3d-2e1f-0a9b-8c7d-6e5f4a3b2c1d",
      "session_id": "sess_worker_node_01_ch01",
      "command_type": "CANCEL",
      "status": "SUCCESS",
      "timestamp_utc": "2026-08-15T21:31:21Z",
      "duration_ms": 780,
      "result": {
        "provider_job_id": "flow_gen_job_998241029",
        "cancellation_status": "CANCELLED",
        "cancelled_at": "2026-08-15T21:31:21Z"
      },
      "error": null
    }
    ```

---

## 3. Hexagonal Isolation & Complete DOM Selector Decoupling

### 3.1 Architectural Analysis of the Selector Leak
In the Candidate v1.0 schema, `OPEN_FLOW` declared `wait_for_selector: { "type": "string" }`. This represented an unacceptable boundary leak:
1. **Coupling Violation:** The orchestrator (R06) and adapter (R08) have explicit Non-Goals: *"DOES NOT OWN: DOM selectors"*. Exposing selector parameters in the port contract forced the adapter to become aware of Google Flow's client-side DOM layout.
2. **Blast Radius of Webpack Rebuilds:** Google regularly updates internal class names (e.g. `.sc-bxivhb`, `.flow-btn-generate_v2-9q8x`). If a selector is part of the port contract, every UI change requires modifying callers and bumping schema versions across multiple repositories.
3. **Track B Disruption:** Track B (`avf-flowkit-bridge`) communicates with FlowKit's Python agent via REST/WebSocket, having no DOM runtime. Passing DOM selectors over the port makes Track B either reject the contract or handle dead fields.

### 3.2 The SelectorRegistry Pattern in Track A (`avf-browser-worker`)
All DOM selector definitions, traversal mechanics, and Shadow DOM piercing logic are strictly encapsulated within `avf-browser-worker` (R09). 

R09 MUST implement the **`SelectorRegistry` Strategy Pattern**, utilizing a prioritized 4-tier element resolution hierarchy:

```
Tier 1: Semantic ARIA Landmarks & Accessible Names
        (e.g., role='button', name='Generate video')
                        |
                        v (if unavailable/unmatched)
Tier 2: Visible Text Content & Text Regex Matchers
        (e.g., textContent ~= /^Create Project$/i)
                        |
                        v (if unavailable/unmatched)
Tier 3: Stable Test Attributes & Data Tags
        (e.g., [data-testid='prompt-submit-button'])
                        |
                        v (if unavailable/unmatched)
Tier 4: Geometric & Visual Anchor Proximity
        (e.g., relative bounding box within prompt container)
```

By decoupling selectors into R09 internal versioned bundles (`selectors_v2026_08.json`), UI churn is resolved by hot-patching R09 worker configuration without altering `avf-contracts` or restarting `avf-workflow`.

### 3.3 Standardized Telemetry for `UI_CHANGED` Errors
When all 4 selector tiers fail in R09, the worker returns `status: "FAILED"`, `error.code: "UI_CHANGED"`, and `retry_category: "POLICY_BLOCKED"`.

To prevent PII leakage while enabling automated diagnostics, the `error.raw_details` payload MUST conform to the structured `UIChangedDetails` schema:

```json
{
  "code": "UI_CHANGED",
  "message": "Failed to locate prompt submission button on studio workspace.",
  "retry_category": "POLICY_BLOCKED",
  "suggested_backoff_ms": 0,
  "raw_details": {
    "target_semantic_surface": "STUDIO_WORKSPACE",
    "failed_element_role": "PROMPT_SUBMIT_BUTTON",
    "attempted_strategies": ["ARIA_ROLE", "TEXT_CONTENT", "TEST_ID", "VISUAL_ANCHOR"],
    "dom_hierarchy_snippet": "<div class='prompt-panel'><textarea id='p1'>...</textarea><button class='new-gen-btn-v3'>Generate</button></div>",
    "sanitized": true,
    "viewport_dimensions": { "width": 1920, "height": 1080 }
  }
}
```

---

## 4. Heavy Binary & Diagnostic Payload Passing Architecture

### 4.1 The Zero-Binary-in-JSON Invariant
**Invariant Statement:** *Under no circumstance may raw video streams (MP4/WebM), binary reference images (PNG/JPEG), or raw diagnostic dump strings (HAR/Heap) be serialized as inline base64 or binary buffers inside FlowExecutionPort JSON messages.*

**Technical Justification:**
1. Base64 encoding inflates binary payload size by **33.3%**.
2. Serializing a 50MB video file into JSON requires allocating a ~67MB contiguous string in V8 memory, creating immediate garbage collection freezes (100–400ms event loop pauses).
3. Transporting multi-megabyte JSON strings over Native Messaging or WebSocket channels risks message buffer overflows and drops.

### 4.2 Two-Phase Asset Handshake Protocol
All binary transfers across `FlowExecutionPort` use URI-based references with SHA-256 verification:

```
[Upstream Caller]                  [FlowExecutionPort Worker]                [Storage Layer]
       |                                       |                                    |
       |--- 1. ATTACH_ASSETS(storage_uri) ---->|                                    |
       |                                       |--- 2. Fetch binary stream -------->|
       |                                       |<-- 3. Return bytes & SHA-256 ------|
       |                                       | (Injects into Google Flow)         |
       |<-- 4. Result(flow_asset_slot_id) -----|                                    |
       |                                       |                                    |
       | ... (Generation Completes) ...        |                                    |
       |                                       |                                    |
       |--- 5. DOWNLOAD_OUTPUT(dest_uri) ----->|                                    |
       |                                       | (Downloads video from Flow)        |
       |                                       | (Computes SHA-256 & Metadata)      |
       |                                       |--- 6. Stream video to dest_uri --->|
       |<-- 7. Result(sha256, bytes, dims) ----|                                    |
```

### 4.3 Resilient Local-First Diagnostic Protocol (`CAPTURE_DIAGNOSTIC`)
Challenger R04 correctly highlighted that during catastrophic node failures (network partition, DNS failure, cloud credential expiration), requiring a remote `s3://` destination URI causes `CAPTURE_DIAGNOSTIC` to fail, permanently destroying the crash logs.

**Remediation Rule:**
1. `destination_diagnostic_uri` supports both `file://` (POSIX local staging) and `s3://` / `gcs://` URIs.
2. If remote upload fails, the worker falls back to staging the diagnostic bundle under `file:///tmp/avf/diagnostics/` and returns the local URI with `storage_fallback: true`.

### 4.4 Chrome MV3 Memory Guardrails & Filtered HAR Capture
Google Chrome MV3 background service workers operate under strict OS/browser memory quotas (~256MB–512MB RAM). Capturing full raw HAR logs on Google Flow can stream hundreds of megabytes of binary WebM chunks into memory, triggering uncatchable OOM process kills (`SIGKILL`).

To eliminate OOM risk, R09 MUST enforce the **Filtered HAR Protocol**:
1. **Network Body Exclusion:** Binary response bodies (`video/*`, `image/*`, `application/octet-stream`) are stripped from the HAR capture stream; only HTTP headers, status codes, timing metrics, and text JSON API responses are captured.
2. **Hard Buffer Cap:** The in-memory diagnostic builder enforces `max_bundle_size_bytes` (default: 25MB, maximum: 50MB). If logs exceed this threshold, the capture engine truncates console history and sets `truncated: true` in the result summary.

---

## 5. High-Throughput Schema Compilation & Polyglot SDK Ergonomics

### 5.1 $O(1)$ Fast-Path Discriminator Compilation
To resolve R04's attack regarding $O(N)$ branch evaluation in JSON Schema engines (such as Node.js `Ajv`, Python `fastjsonschema`, Go `kin-openapi`), the schema contracts MUST include explicit discriminator metadata and modular `$defs`.

In `browser-command.schema.json`:
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aivideofactory.com/v1/browser-command.schema.json",
  "title": "FlowExecutionCommand",
  "type": "object",
  "discriminator": {
    "propertyName": "command_type"
  },
  "oneOf": [
    { "$ref": "#/$defs/EnsureSessionCommand" },
    { "$ref": "#/$defs/OpenFlowCommand" },
    { "$ref": "#/$defs/CreateOrSelectProjectCommand" },
    { "$ref": "#/$defs/AttachAssetsCommand" },
    { "$ref": "#/$defs/SetGenerationOptionsCommand" },
    { "$ref": "#/$defs/SubmitPromptCommand" },
    { "$ref": "#/$defs/ReadGenerationStateCommand" },
    { "$ref": "#/$defs/DownloadOutputCommand" },
    { "$ref": "#/$defs/CaptureDiagnosticCommand" },
    { "$ref": "#/$defs/CancelCommand" }
  ]
}
```

### 5.2 Elimination of Asymmetric Typing in `flow-execution-result.schema.json`
`flow-execution-result.schema.json` is upgraded from an untyped open object to a fully typed discriminated union matching all 10 operations:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aivideofactory.com/v1/flow-execution-result.schema.json",
  "title": "FlowExecutionResult",
  "type": "object",
  "discriminator": {
    "propertyName": "command_type"
  },
  "oneOf": [
    { "$ref": "#/$defs/EnsureSessionResult" },
    { "$ref": "#/$defs/OpenFlowResult" },
    { "$ref": "#/$defs/CreateOrSelectProjectResult" },
    { "$ref": "#/$defs/AttachAssetsResult" },
    { "$ref": "#/$defs/SetGenerationOptionsResult" },
    { "$ref": "#/$defs/SubmitPromptResult" },
    { "$ref": "#/$defs/ReadGenerationStateResult" },
    { "$ref": "#/$defs/DownloadOutputResult" },
    { "$ref": "#/$defs/CaptureDiagnosticResult" },
    { "$ref": "#/$defs/CancelResult" }
  ]
}
```

### 5.3 Polyglot SDK Codegen Verification
With this modular architecture:
- **TypeScript:** Generates clean tagged unions (`type FlowExecutionCommand = EnsureSessionCommand | OpenFlowCommand | ...`) with exhaustiveness checking (`switch (cmd.command_type)`).
- **Python / Pydantic:** Generates discriminated `Union[EnsureSessionCommand, ...]` with `Field(discriminator='command_type')`.
- **Go:** Generates concrete structs implementing a common `FlowExecutionCommand` interface with unmarshaling dispatch tables.

---

## 6. Evaluation of Challenger (R04) Arguments & Concurrence

| Challenge Raised by R04 (Contracts) | Domain Owner Analysis & Authoritative Determination |
|---|---|
| **1. Naive `oneOf` Validation Overhead:** Polyglot SDKs suffer $O(N)$ validation latency and produce unreadable multi-branch error trees. | **CONCUR & ADOPTED.** Discriminator property metadata (`"discriminator": { "propertyName": "command_type" }`) is mandated across command and result schemas, enabling $O(1)$ dispatch in JIT engines (Ajv) and clean tagged union codegen in TypeScript/Python/Go. |
| **2. Hexagonal Violation (`wait_for_selector` Leak):** Injecting `wait_for_selector` into `OPEN_FLOW` couples callers to DOM hashes and breaks Track B compatibility. | **CONCUR & ADOPTED.** `wait_for_selector` is purged from `OPEN_FLOW`. R09 encapsulates all DOM selector traversal in internal `SelectorRegistry` bundles; the public port specifies only `target_surface` semantic intent. |
| **3. Asymmetric Result Typing:** Result schema used `result: { additionalProperties: true }`, destroying static contract guarantees for `READ_GENERATION_STATE` and `DOWNLOAD_OUTPUT`. | **CONCUR & ADOPTED.** `flow-execution-result.schema.json` is updated with 10 strictly typed `$defs` result branches with `additionalProperties: false`. |
| **4. Diagnostic Storage OOM & Partition Vulnerability:** Synchronous remote upload fails during network drops; unfiltered HAR dumps crash MV3 service workers with OOM. | **CONCUR & ADOPTED.** Mandated local POSIX staging fallback (`file://`), 25MB max bundle limit, and network body stripping (`har_capture_mode: "METADATA_ONLY"`). |

---

## 7. Formal Domain Owner Verdict & Binding Directives

### 7.1 Authoritative Verdict
**STATUS: CONFIRMED_WITH_DIRECTIVES**  
The remediated `FlowExecutionPort` specification—comprising the 10 strictly typed command and result contracts, complete DOM selector decoupling, zero-binary URI passing, and OOM-hardened diagnostics—is mathematically sound, architecturally robust, and satisfies all requirements of TECH-006, FINDING_003, FINDING_020, and FINDING_048.

### 7.2 Binding Implementation Directives for C03R / C04R

1. **Directive to R01 / R04 (`avf-contracts`):**
   - Update `02_contracts/browser-command.schema.json` to include `"discriminator": { "propertyName": "command_type" }` and 10 modular command `$defs`.
   - Purge `"wait_for_selector"` from `OpenFlowCommand`, replacing with `target_surface: "STUDIO_WORKSPACE" | "PROJECT_GALLERY"`.
   - Create normative `02_contracts/flow-execution-result.schema.json` with 10 matching modular result `$defs` and structured error taxonomy.
   - Enforce `additionalProperties: false` across all command and result schemas.

2. **Directive to R08 (`avf-google-flow-adapter`):**
   - Implement `VideoGenerationProvider` utilizing exclusively the 10 `FlowExecutionPort` operations.
   - Enforce reconciliation-before-resubmit logic when `SUBMIT_PROMPT` encounters network ambiguity.
   - Ensure zero DOM selector logic or FlowKit-specific types exist within the R08 adapter codebase.

3. **Directive to R09 (`avf-browser-worker` - Track A):**
   - Implement the internal 4-tier `SelectorRegistry` (ARIA -> Text -> TestID -> Visual) isolated behind versioned configuration files.
   - Enforce the Filtered HAR protocol (stripping binary media) and cap in-memory diagnostic bundles at 25MB.
   - Support `file://` local POSIX staging fallback for diagnostic bundles during network failures.

4. **Directive to R10 (`avf-flowkit-bridge` - Track B):**
   - Map the identical 10 `FlowExecutionPort` operations to FlowKit's Python agent / WebSocket interfaces.
   - Guarantee that FlowKit SQLite database tables, internal queue IDs, and private protocols remain 100% private to R10.

5. **Directive to R15 (`avf-integration-harness`):**
   - Develop fake test doubles (`FakeTrackABrowserWorker` and `FakeTrackBBridge`) validating 100% schema conformance against the shared `avf-contracts` test suite.
   - Implement automated conformance assertions verifying that switching between Track A and Track B causes zero behavioral drift in `avf-google-flow-adapter`.

---
**DOMAIN OWNER SIGN-OFF:**  
*R06 — Flow Browser Specialist & Workflow Architect, AI Video Factory Architecture Council*  
*Timestamp: 2026-08-15T21:35:00Z*
