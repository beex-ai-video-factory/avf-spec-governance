# AI VIDEO FACTORY v1.0.0 — WORKSPACE AND REPO MAP
## Polyrepo Layout, Boundaries, and Dependency Envelopes

**Version:** 1.0.0  
**Authority:** Technical Architecture Board

---

## 1. Local Filesystem Layout

```text
AVF_SPEC_REVIEW/
├── 00_PROJECT_ADMIN/              # Project governance & certificates
├── 01_FROZEN_RELEASE/             # READ-ONLY Frozen v1.0.0 Specification
├── 02_SOURCE_KITS_READONLY/       # READ-ONLY Reference source kits
├── 03_GOVERNANCE_EVIDENCE_READONLY# READ-ONLY Historical audit evidence
├── 04_TOOLING/                    # Operational tooling, validators, runbook
│   └── prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/
├── 05_IMPLEMENTATION/             # ALL PRODUCT CODE LIVES HERE
│   ├── operator-state/            # Runtime execution state & history
│   ├── change-requests/           # Formal Change Requests (CR)
│   ├── decisions/                 # Implementation Decision Records (IDR)
│   ├── environment/               # Docker composition & doctor scripts
│   └── repos/                     # 15 Independent Polyrepos
│       ├── R01_contracts/
│       ├── R02_core_state/
│       ├── R03_creative/
│       ├── R04_assets_continuity/
│       ├── R05_prompt_compiler/
│       ├── R06_workflow/
│       ├── R07_provider_sdk/
│       ├── R08_google_flow_adapter/
│       ├── R09_browser_worker/
│       ├── R10_flowkit_bridge/
│       ├── R11_qc/
│       ├── R12_media/
│       ├── R13_operator_console/
│       ├── R14_platform_observability/
│       └── R15_integration_harness/
└── 90_ARCHIVE_READONLY/           # READ-ONLY Archived packages
```

---

## 2. Repository Mapping & Boundary Table

| Code | Repo Name | Layer | Primary Path | Allowed Inbound Deps | Forbidden Dependencies |
|---|---|---|---|---|---|
| **R01** | `R01_contracts` | Layer 0 | `05_IMPLEMENTATION/repos/R01_contracts/` | All repos (R02–R15) | R02–R15 |
| **R02** | `R02_core_state` | Layer 1 | `05_IMPLEMENTATION/repos/R02_core_state/` | R03, R04, R05, R06, R13, R15 | R03–R13, R15 |
| **R03** | `R03_creative` | Layer 2 | `05_IMPLEMENTATION/repos/R03_creative/` | R06, R15 | R04–R13, R15, Direct DB |
| **R04** | `R04_assets_continuity` | Layer 2 | `05_IMPLEMENTATION/repos/R04_assets_continuity/` | R05, R06, R15 | R03, R05–R13, R15, Direct DB |
| **R05** | `R05_prompt_compiler` | Layer 2 | `05_IMPLEMENTATION/repos/R05_prompt_compiler/` | R06, R15 | R06–R13, R15, Direct DB |
| **R06** | `R06_workflow` | Layer 5 | `05_IMPLEMENTATION/repos/R06_workflow/` | R13, R15 | R09, R10, Direct DB |
| **R07** | `R07_provider_sdk` | Layer 3 | `05_IMPLEMENTATION/repos/R07_provider_sdk/` | R06, R08, R15 | R02–R06, R08–R13, R15, Direct DB |
| **R08** | `R08_google_flow_adapter` | Layer 3 | `05_IMPLEMENTATION/repos/R08_google_flow_adapter/`| R06, R15 | R02–R06, Direct DB |
| **R09** | `R09_browser_worker` | Layer 4 | `05_IMPLEMENTATION/repos/R09_browser_worker/` | R08 (via Port), R15 | R02–R08, R10, R11–R13, Direct DB |
| **R10** | `R10_flowkit_bridge` | Layer 4 | `05_IMPLEMENTATION/repos/R10_flowkit_bridge/` | R08 (via Port), R15 | R02–R09, R11–R13, Direct DB |
| **R11** | `R11_qc` | Layer 2 | `05_IMPLEMENTATION/repos/R11_qc/` | R06, R15 | R02–R10, R12, R13, Direct DB |
| **R12** | `R12_media` | Layer 2 | `05_IMPLEMENTATION/repos/R12_media/` | R06, R15 | R02–R11, R13, Direct DB |
| **R13** | `R13_operator_console` | Layer 5 | `05_IMPLEMENTATION/repos/R13_operator_console/` | Human Operator | R03, R04, R05, R07–R12, R15, Direct DB |
| **R14** | `R14_platform_observability`| Cross | `05_IMPLEMENTATION/repos/R14_platform_observability/`| All repos (R02–R15) | R02–R13, R15, Direct DB |
| **R15** | `R15_integration_harness` | Cross | `05_IMPLEMENTATION/repos/R15_integration_harness/`| Test Runners | Direct production DB mutation |
