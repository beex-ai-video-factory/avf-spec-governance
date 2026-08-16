# AI Video Factory — Implementation Workspace
## Root Workspace for Downstream Engineering

**Status:** READY FOR IMPLEMENTATION  
**Baseline Version:** `v1.0.0` (Frozen)  

---

## 1. Overview

This directory (`05_IMPLEMENTATION/`) is the designated writable workspace for all AI Video Factory implementation activities.

- **Authoritative Baseline:** [IMPLEMENTATION_BASELINE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/IMPLEMENTATION_BASELINE.md)
- **Repository Registry:** [repo-registry.yaml](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repo-registry.yaml) (R01 through R15)
- **Dependency Gates:** [dependency-gates.yaml](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/dependency-gates.yaml)
- **Environment & Doctor:** [environment/](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/environment/)
- **Change Requests:** [change-requests/](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/change-requests/)
- **Implementation Decisions:** [decisions/](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/decisions/)
- **R01 Hardening Register:** [R01_PREIMPLEMENTATION_HARDENING.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md)

---

## 2. Implementation Rules

1. **Do not modify frozen files:** All files in `01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, and `90_ARCHIVE_READONLY/` are read-only.
2. **Start with R01 Contracts:** R01 Contracts must be implemented, typed, and tested before downstream services begin.
3. **No Unjustified Infrastructure:** Use only PostgreSQL, Temporal, local S3 emulator (MinIO), and OpenTelemetry as justified in the frozen architecture.
4. **Use FakeVideoProvider:** Offline development and testing must not depend on live Google Flow credentials.
