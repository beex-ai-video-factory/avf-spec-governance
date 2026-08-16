# CHANGE PROPOSAL: CP-007 (AMENDED)
**CHANGE_ID:** CP-007
**TITLE:** Security Credential Injection, Buffer Zeroing & Telemetry Redaction
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** GOV-003, TECH-009, FINDING_007
**MATERIALLY_AFFECTED_ROLES:** R07 (Security), R15 (Red Team), R06 (Flow Browser), R14 (Observability)
**MANDATORY_SIGNOFF_ROLES:** R07 (Security), R15 (Red Team)

## 1. Rationale & Problem Description
Eliminates fictitious "SecretEnclave" claims and defines practical, robust security mechanisms: OS/Vault credential injection, in-memory buffer clearing (`buf.fill(0)`), and telemetry token redaction.

## 2. Exact Specification Changes
1. `04_integration/SECURITY_MODEL.md`: Specify credential lifecycle and redaction filters.
2. `03_repo_blueprints/R07_PROVIDER_SDK.md`, `R09_BROWSER_WORKER.md`, `R14_PLATFORM_OBSERVABILITY.md`: Implement secret policies.
3. `06_adrs/ADR-007_BROWSER_SECURITY.md`: Update ADR.

## 3. Capability Preservation Proof
Preserves CAP-07 (Security & Isolation).
