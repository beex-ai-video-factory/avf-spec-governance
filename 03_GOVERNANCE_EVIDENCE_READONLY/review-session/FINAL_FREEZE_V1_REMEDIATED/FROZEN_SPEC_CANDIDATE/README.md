# AI Video Factory — Specification Kit
## Release Version: v1.0.0 (Remediated Baseline)
### Specification Version: 1.0.0

This repository contains the complete, normative, multi-agent implementation specification for the **AI Video Factory (AVF)** platform.

---

## 1. Structure
- `00_governance/`: Freeze policy, change control, DoD.
- `01_master/`: Master architecture blueprint, canonical data model, system invariants, polyrepo strategy.
- `02_contracts/`: Normative JSON Schemas, status state machines, and contract overview.
- `03_repo_blueprints/`: Standalone build specifications for all 15 repositories (R01–R15).
- `04_integration/`: Dependency graph, command & event catalog, security model, E2E protocol, test strategy.
- `05_phases/`: Implementation phase roadmap and build order.
- `06_adrs/`: Architectural Decision Records (ADR-001 through ADR-009).
- `07_risk/`: System risk register and mitigations.
- `08_evidence/`: Requirement traceability and source ledger.
- `09_agent_packets/`: Agent build packets for autonomous coding agents.

---

## 2. Integrity Verification
Run `python3 verify_package.py` to independently verify file hashes and tree integrity.
