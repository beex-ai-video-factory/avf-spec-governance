# Agent Build Packet Index

Recommended sequencing:

| Packet | Repository | Goal | Depends on |
|---|---|---|---|
| P001 | avf-contracts | Implement frozen schemas + generated models | freeze |
| P002 | avf-core-state | Canonical entities + idempotent command layer | P001 |
| P003 | avf-provider-sdk | Provider interface + FakeProvider | P001 |
| P004 | avf-workflow | SingleShotWorkflow using FakeProvider | P001-P003 |
| P005 | avf-integration-harness | Deterministic E2E/fault injection | P001-P004 |
| P006 | avf-google-flow-adapter | Adapter against mocked FlowExecutionPort | P001,P003 |
| P007 | avf-flowkit-bridge | Minimal Track B one-shot bridge | P001,P006 |
| P008 | avf-browser-worker | Track A A2/A3 spike | P001,P006 |
| P009 | avf-media | Provider output ingest/probe/storage | P001 |
| P010 | avf-assets-continuity | Asset/character/style MVP | P001,P002 |
| P011 | avf-prompt-compiler | Prompt compiler MVP | P001,P003,P010 |
| P012 | avf-creative | Structured creative proposals | P001,P002 |
| P013 | avf-qc | Technical QC + semantic interface | P001,P009 |
| P014 | avf-operator-console | Minimal control UI | P001,P002,P004 |
| P015 | avf-platform-observability | telemetry conventions/instrumentation | P001 |

Each packet is small enough for one focused coding-agent session/branch. Split further by acceptance tests during implementation rather than combining packets.
