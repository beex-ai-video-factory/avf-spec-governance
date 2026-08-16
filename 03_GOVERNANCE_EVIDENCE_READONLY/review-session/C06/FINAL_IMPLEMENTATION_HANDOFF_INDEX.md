# Final Implementation Handoff Index (v1.0.0)

Every repository has a self-contained, frozen implementation specification allowing independent coding agents to implement the codebase without architectural guessing.

| REPO_ID | REPOSITORY_NAME | BLUEPRINT_SPECIFICATION | PRIMARY_CONTRACTS | TEST_HARNESS_FIXTURES |
|---|---|---|---|---|
| R01 | avf-contracts | `03_repo_blueprints/R01_CONTRACTS.md` | `domain-entities.schema.json` | JSON Schema validation suite |
| R02 | avf-core-state | `03_repo_blueprints/R02_CORE_STATE.md` | `domain-entities`, PostgreSQL models | Optimistic concurrency & lease tests |
| R03 | avf-creative | `03_repo_blueprints/R03_CREATIVE.md` | Scene/Shot narrative contracts | Narrative AST generation fixtures |
| R04 | avf-assets-continuity | `03_repo_blueprints/R04_ASSETS_CONTINUITY.md` | AssetVersion schemas, pHash | Continuity comparison test suite |
| R05 | avf-prompt-compiler | `03_repo_blueprints/R05_PROMPT_COMPILER.md` | PromptVersion, AST lowering | AST compilation & deterministic hash tests |
| R06 | avf-workflow | `03_repo_blueprints/R06_WORKFLOW.md` | WorkflowRun, State Machines | Workflow pause/resume & retry engine tests |
| R07 | avf-provider-sdk | `03_repo_blueprints/R07_PROVIDER_SDK.md` | `provider-request`, `provider-result` | Provider SDK retry & SecretEnclave tests |
| R08 | avf-google-flow-adapter | `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md` | `FlowExecutionPort` | Dual-track adapter conformance tests |
| R09 | avf-browser-worker | `03_repo_blueprints/R09_BROWSER_WORKER.md` | `browser-command.schema.json` | MV3 keepalive & CDP worker tests |
| R10 | avf-flowkit-bridge | `03_repo_blueprints/R10_FLOWKIT_BRIDGE.md` | FlowKit gRPC Port | Standalone FlowKit bridge tests |
| R11 | avf-qc | `03_repo_blueprints/R11_QC.md` | `QCResult` schema | Multi-modal AQC scoring & retry rules |
| R12 | avf-media | `03_repo_blueprints/R12_MEDIA.md` | FFmpeg probe/transcode contracts | Media container normalization tests |
| R13 | avf-operator-console | `03_repo_blueprints/R13_OPERATOR_CONSOLE.md` | WebSocket event protocol | HITL override & audit log tests |
| R14 | avf-platform-observability | `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` | OpenTelemetry, Prometheus | W3C trace propagation & metrics tests |
| R15 | avf-integration-harness | `03_repo_blueprints/R15_INTEGRATION_HARNESS.md` | Conformance Test Runner | Hermetic mock provider simulators |
