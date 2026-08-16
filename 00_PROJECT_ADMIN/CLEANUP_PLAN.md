# PRE-IMPLEMENTATION WORKSPACE CLEANUP PLAN
## AI Video Factory — Spec Review to Implementation Workspace Transformation

**Execution Date:** 2026-08-16  
**Status:** APPROVED FOR EXECUTION  
**Custodian:** Pre-Implementation Workspace Custodian  

---

## 1. Executive Summary & Objective

The AI Video Factory project has completed all governance, Council review, remediation, and external technical forensic audit phases for version **1.0.0**. The final verdict is:
$$\text{FORENSIC\_RESULT} = \text{VERIFIED\_IMPLEMENTATION\_BASELINE}$$

The goal of this cleanup plan is to transform the review workspace into a clean, reproducible, read-only frozen baseline plus a writable implementation workspace, preserving full auditability, zero data loss, and absolute immutability of the frozen release.

---

## 2. Non-Negotiable Rules

1. **Zero Blind Deletion:** Default obsolete-file action is **ARCHIVE**, not delete.
2. **Hard-Delete Scope:** Only `.DS_Store` OS caches, temporary runtime caches, exact duplicate files with identical SHA-256 hashes, and accidental disposable scratch output.
3. **Preserved Evidentiary Chains:** Source kits, freeze packages, Council ballots, subagent outputs, remediation history, Change Proposals, contract schemas, manifests, and forensic audit reports are permanently preserved.
4. **Path Compatibility:** Symlinks will be maintained at root for legacy paths (`review-session/`, source kits) to guarantee that absolute and relative references in existing audit reports remain valid.
5. **Read-Only Protection:** All frozen releases, source kits, governance evidence, and archives will be locked with read-only permissions (`chmod -R a-w`).

---

## 3. Migration Mapping

| Pre-Cleanup Location | Target Canonical Location | Classification | Migration Action |
|---|---|---|---|
| `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` | `01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` | CANONICAL_RELEASE_ZIP | Move |
| `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256` | `01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256` | CANONICAL_SIDECAR | Move |
| `review-session/FINAL_FREEZE_V1_REMEDIATED/` | `01_FROZEN_RELEASE/v1.0.0/` & preserved in evidence | FROZEN_SPEC_BASELINE | Copy / Mirror & Lock |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/` | `02_SOURCE_KITS_READONLY/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/` | SOURCE_KIT_BLUEPRINT | Move & Root Symlink |
| `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/` | `02_SOURCE_KITS_READONLY/AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/` | SOURCE_KIT_COUNCIL | Move & Root Symlink |
| `AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0/` | `02_SOURCE_KITS_READONLY/AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0/` | SOURCE_KIT_AUTOPILOT | Move & Root Symlink |
| `review-session/` | `03_GOVERNANCE_EVIDENCE_READONLY/review-session/` | GOVERNANCE_EVIDENCE | Move & Root Symlink |
| `AUTONOMOUS_COUNCIL_MASTER.md` | `04_TOOLING/prompts/historical/AUTONOMOUS_COUNCIL_MASTER.md` | HISTORICAL_PROMPT | Move |
| `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` | `04_TOOLING/prompts/historical/AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` | HISTORICAL_PROMPT | Move |
| `FINAL_FREEZE_FORENSIC_AUDIT.md` | `04_TOOLING/prompts/historical/FINAL_FREEZE_FORENSIC_AUDIT.md` | HISTORICAL_PROMPT | Move |
| `FINAL_PACKAGE_HASH_CANONICALIZATION.md` | `04_TOOLING/prompts/historical/FINAL_PACKAGE_HASH_CANONICALIZATION.md` | HISTORICAL_PROMPT | Move |
| `FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md` | `04_TOOLING/prompts/historical/FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md` | HISTORICAL_PROMPT | Move |
| `FINAL_TARGETED_GOVERNANCE_PATCH.md` | `04_TOOLING/prompts/historical/FINAL_TARGETED_GOVERNANCE_PATCH.md` | HISTORICAL_PROMPT | Move |
| `PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md` | `04_TOOLING/prompts/historical/PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md` | HISTORICAL_PROMPT | Move |
| `AVF_FINAL_FREEZE_v1.0.0.zip` | `90_ARCHIVE_READONLY/superseded-releases/AVF_FINAL_FREEZE_v1.0.0.zip` | SUPERSEDED_RELEASE_ZIP | Move to Archive |
| `review-session/FINAL_REMEDIATED_FORENSIC_AUDIT.zip` | `90_ARCHIVE_READONLY/superseded-releases/FINAL_REMEDIATED_FORENSIC_AUDIT.zip` | SUPERSEDED_AUDIT_ZIP | Move to Archive |
| `.DS_Store` (all instances) | N/A | OS_CACHE | Hard Delete |

---

## 4. Execution Sequence

1. **Inventory:** Generate `PRE_CLEANUP_FILE_INVENTORY.csv` (Completed).
2. **Directory Scaffold:** Create `00_PROJECT_ADMIN/`, `01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, `04_TOOLING/`, `05_IMPLEMENTATION/`, `90_ARCHIVE_READONLY/`, `99_TEMP/`, and `.agents/`.
3. **Move & Organize:**
   - Relocate loose historical prompts to `04_TOOLING/prompts/historical/`.
   - Relocate distributable release archive and detached sidecar to `01_FROZEN_RELEASE/distributable/`.
   - Establish `01_FROZEN_RELEASE/v1.0.0/` populated with the verified v1.0.0 baseline.
   - Relocate source kits to `02_SOURCE_KITS_READONLY/` and establish root symlinks.
   - Relocate `review-session/` to `03_GOVERNANCE_EVIDENCE_READONLY/` and establish root symlink.
   - Relocate superseded archives to `90_ARCHIVE_READONLY/superseded-releases/`.
4. **Delete Disposable OS Caches:** Remove `.DS_Store` files.
5. **Generate Post-Cleanup Inventory:** Write `00_PROJECT_ADMIN/POST_CLEANUP_FILE_INVENTORY.csv`.
6. **Implement Configuration & Customizations:**
   - `.agents/rules/` (5 standard rules)
   - `.agents/skills/` (10 domain-specific skills)
   - `.agents/hooks.json`
   - `00_PROJECT_ADMIN/` governance & security policies
   - `05_IMPLEMENTATION/` workspace setup (15 repos registered, environment bootstrap, doctor script, compose dev, gates)
   - Root `PROJECT.md`, `BASELINE.lock.json`, `.gitignore`, `.editorconfig`.
7. **Validation & Verification:** Run all validation scripts and environment doctor.
8. **Lockdown:** Apply POSIX read-only permissions (`chmod -R a-w`) across protected directories.
