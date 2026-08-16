# Dependency Graph

```mermaid
flowchart LR
    C[avf-contracts] --> CORE[avf-core-state]
    C --> CREATIVE[avf-creative]
    C --> ASSET[avf-assets-continuity]
    C --> PROMPT[avf-prompt-compiler]
    C --> WF[avf-workflow]
    C --> SDK[avf-provider-sdk]
    SDK --> FLOW[avf-google-flow-adapter]
    C --> BW[avf-browser-worker]
    C --> FK[avf-flowkit-bridge]
    FLOW --> BW
    FLOW --> FK
    C --> QC[avf-qc]
    C --> MEDIA[avf-media]
    C --> UI[avf-operator-console]
    CORE --> UI
    CORE --> WF
    WF --> CREATIVE
    WF --> ASSET
    WF --> PROMPT
    WF --> SDK
    WF --> QC
    WF --> MEDIA
    OBS[avf-platform-observability] -. instrumentation .-> CORE
    OBS -.-> WF
    OBS -.-> BW
    OBS -.-> FK
    I[avf-integration-harness] --> CORE
    I --> WF
    I --> FLOW
    I --> BW
    I --> FK
    I --> QC
    I --> MEDIA
```

## Forbidden dependencies

- Creative -> Google Flow Adapter
- Asset Service -> Browser Worker
- Prompt Compiler -> FlowKit model/database
- QC -> browser selectors
- Browser Worker -> Core database
- FlowKit Bridge -> Core database
- Operator Console -> provider-specific database
