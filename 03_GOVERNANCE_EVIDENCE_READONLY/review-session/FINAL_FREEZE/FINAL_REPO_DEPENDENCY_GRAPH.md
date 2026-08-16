# Final Repository Dependency Graph (v1.0.0 DAG)

```mermaid
graph TD
    R01[R01 CONTRACTS] --> R02[R02 CORE_STATE]
    R01 --> R04[R04 ASSETS_CONTINUITY]
    R01 --> R05[R05 PROMPT_COMPILER]
    R01 --> R07[R07 PROVIDER_SDK]
    
    R02 --> R06[R06 WORKFLOW]
    R03[R03 CREATIVE] --> R05
    R04 --> R05
    R05 --> R06
    
    R06 --> R08[R08 GOOGLE_FLOW_ADAPTER]
    R06 --> R07
    
    R08 -. FlowExecutionPort .-> R09[R09 BROWSER_WORKER]
    R08 -. FlowExecutionPort .-> R10[R10 FLOWKIT_BRIDGE]
    
    R06 --> R11[R11 QC]
    R11 --> R12[R12 MEDIA]
    R06 --> R13[R13 OPERATOR_CONSOLE]
    
    R02 --> R14[R14 PLATFORM_OBSERVABILITY]
    R06 --> R14
    
    R15[R15 INTEGRATION_HARNESS] --> R01
    R15 --> R08
    R15 --> R07
```

## Dependency Direction Invariants
- **INV-014 / G05:** Strict Unidirectional DAG (Zero Cycles).
- **CP-005 / G11:** FlowExecutionPort cleanly encapsulates Track A (R09) and Track B (R10) without upward dependency leakage.
