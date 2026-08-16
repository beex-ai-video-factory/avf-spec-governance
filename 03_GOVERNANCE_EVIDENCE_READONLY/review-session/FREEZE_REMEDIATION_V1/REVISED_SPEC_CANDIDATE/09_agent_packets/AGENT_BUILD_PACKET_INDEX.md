# AGENT BUILD PACKET INDEX
## AI Video Factory — Autonomous Coding Agent Implementation Packets
**VERSION:** 1.0.0

All 15 repositories have standalone build packets derived directly from the normative repository blueprints and contracts:

| Code | Repo Name | Target Layer | Primary Contract Schemas | Build Packet Artifact |
|---|---|---|---|---|
| R01 | `avf-contracts` | Layer 0 | All schemas | `03_repo_blueprints/R01_CONTRACTS.md` |
| R02 | `avf-core-state` | Layer 1 | `domain-entities.schema.json` | `03_repo_blueprints/R02_CORE_STATE.md` |
| R03 | `avf-creative` | Layer 2 | `domain-entities.schema.json` | `03_repo_blueprints/R03_CREATIVE.md` |
| R04 | `avf-assets-continuity` | Layer 2 | `domain-entities.schema.json` | `03_repo_blueprints/R04_ASSETS_CONTINUITY.md` |
| R05 | `avf-prompt-compiler` | Layer 2 | `domain-entities.schema.json` | `03_repo_blueprints/R05_PROMPT_COMPILER.md` |
| R06 | `avf-workflow` | Layer 5 | `event-envelope.schema.json` | `03_repo_blueprints/R06_WORKFLOW.md` |
| R07 | `avf-provider-sdk` | Layer 3 | `provider-request.schema.json`, `provider-result.schema.json` | `03_repo_blueprints/R07_PROVIDER_SDK.md` |
| R08 | `avf-google-flow-adapter`| Layer 3 | `browser-command.schema.json`, `flow-execution-result.schema.json` | `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md` |
| R09 | `avf-browser-worker` | Layer 4 | `browser-command.schema.json`, `flow-execution-result.schema.json` | `03_repo_blueprints/R09_BROWSER_WORKER.md` |
| R10 | `avf-flowkit-bridge` | Layer 4 | `browser-command.schema.json`, `flow-execution-result.schema.json` | `03_repo_blueprints/R10_FLOWKIT_BRIDGE.md` |
| R11 | `avf-qc` | Layer 2 | `domain-entities.schema.json` | `03_repo_blueprints/R11_QC.md` |
| R12 | `avf-media` | Layer 2 | `domain-entities.schema.json` | `03_repo_blueprints/R12_MEDIA.md` |
| R13 | `avf-operator-console` | Layer 5 | REST / OpenAPI schemas | `03_repo_blueprints/R13_OPERATOR_CONSOLE.md` |
| R14 | `avf-platform-observability`| Cross-Cutting | OTel / OpenTelemetry Envelopes | `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` |
| R15 | `avf-integration-harness` | Cross-Cutting | All contracts & Fake Adapters | `03_repo_blueprints/R15_INTEGRATION_HARNESS.md` |
