---
name: avf-baseline-reader
description: Locate, read, and interpret normative requirements, JSON schemas, system invariants, and repo blueprints from the frozen AI Video Factory v1.0.0 baseline while distinguishing them from historical audit evidence.
---

# Skill: AVF Baseline Reader

## Purpose
Enables implementation agents to reliably locate authoritative frozen specifications, schemas, ADRs, and repository packets in `01_FROZEN_RELEASE/v1.0.0/` without confusing them with historical deliberations or superseded documents.

## Authoritative Frozen Paths
All normative specification files reside strictly under:
- **Root Manifest:** `01_FROZEN_RELEASE/v1.0.0/FINAL_SPEC_MANIFEST.md`
- **Normative Spec Tree:** `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/`
  - **Master Architecture:** `01_master/` (`MASTER_BLUEPRINT.md`, `SYSTEM_INVARIANTS.md`, `DATA_MODEL.md`, `REPOSITORY_STRATEGY.md`)
  - **Contracts & Schemas:** `02_contracts/` (`domain-entities.schema.json`, `event-envelope.schema.json`, `provider-request.schema.json`, `provider-result.schema.json`, `browser-command.schema.json`, `flow-execution-result.schema.json`, `API_COMPATIBILITY_POLICY.md`, `STATUS_STATE_MACHINES.md`)
  - **Repository Blueprints:** `03_repo_blueprints/R01_CONTRACTS.md` through `R15_INTEGRATION_HARNESS.md`
  - **Integration & Governance:** `04_integration/`, `00_governance/`, `05_phases/`, `06_adrs/`, `07_risk/`, `08_evidence/`, `09_agent_packets/`

## Guidelines for Agents
1. Always verify that you are reading from `01_FROZEN_RELEASE/v1.0.0/` or `05_IMPLEMENTATION/`.
2. Do not use legacy paths in `02_SOURCE_KITS_READONLY/` as current requirements; they are historical inputs.
3. Check `01_FROZEN_RELEASE/v1.0.0/CONTENT_HASHES.json` if verifying spec integrity.
