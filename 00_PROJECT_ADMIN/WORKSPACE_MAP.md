# WORKSPACE NORMALIZATION MAP
## AI Video Factory — Spec Review to Implementation Workspace Transformation

**Execution Date:** 2026-08-16  
**Custodian:** Pre-Implementation Workspace Custodian  
**Status:** COMPLETED & VERIFIED  

---

## 1. Before & After Layout Comparison

### Before Normalization (Review/Audit Workspace)
```text
AVF_SPEC_REVIEW/
├── .DS_Store (and nested .DS_Store caches)
├── AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/
├── AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/
├── AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0/
├── AUTONOMOUS_COUNCIL_MASTER.md
├── AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md
├── AVF_FINAL_FREEZE_v1.0.0.zip
├── AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip
├── AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256
├── FINAL_FREEZE_FORENSIC_AUDIT.md
├── FINAL_PACKAGE_HASH_CANONICALIZATION.md
├── FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md
├── FINAL_TARGETED_GOVERNANCE_PATCH.md
├── PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md
└── review-session/ (51 subdirectories & raw deliberation artifacts)
```

### After Normalization (Clean Implementation Workspace)
```text
AVF_SPEC_REVIEW/
├── PROJECT.md                                # Root entrypoint
├── BASELINE.lock.json                        # Baseline lockfile
├── .gitignore                                # Git ignore rules
├── .editorconfig                             # Code style config
├── .agents/                                  # Agent rules, skills, hooks
├── 00_PROJECT_ADMIN/                         # Governance certificates & plans
├── 01_FROZEN_RELEASE/                        # [READ-ONLY] v1.0.0 & canonical zip
├── 02_SOURCE_KITS_READONLY/                  # [READ-ONLY] Input kits
├── 03_GOVERNANCE_EVIDENCE_READONLY/          # [READ-ONLY] Council deliberation evidence
├── 04_TOOLING/                               # Historical prompts & validators
├── 05_IMPLEMENTATION/                        # [WRITABLE] Implementation workspace
├── 90_ARCHIVE_READONLY/                      # [READ-ONLY] Superseded release zips
├── 99_TEMP/                                  # Scratch directory
├── AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0 -> 02_SOURCE_KITS_READONLY/...
├── AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0 -> 02_SOURCE_KITS_READONLY/...
├── AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0 -> 02_SOURCE_KITS_READONLY/...
└── review-session -> 03_GOVERNANCE_EVIDENCE_READONLY/review-session
```

---

## 2. File Relocations & Moves Table

| Original Path | Normalized Destination | Classification |
|---|---|---|
| `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` | `01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` | CANONICAL_RELEASE_ZIP |
| `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256` | `01_FROZEN_RELEASE/distributable/AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip.sha256` | CANONICAL_SIDECAR |
| `review-session/FINAL_FREEZE_V1_REMEDIATED/*` | `01_FROZEN_RELEASE/v1.0.0/*` | FROZEN_SPEC_BASELINE |
| `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0` | `02_SOURCE_KITS_READONLY/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0` | SOURCE_KIT |
| `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0` | `02_SOURCE_KITS_READONLY/AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0` | SOURCE_KIT |
| `AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0` | `02_SOURCE_KITS_READONLY/AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0` | SOURCE_KIT |
| `review-session` | `03_GOVERNANCE_EVIDENCE_READONLY/review-session` | GOVERNANCE_EVIDENCE |
| `AUTONOMOUS_COUNCIL_MASTER.md` | `04_TOOLING/prompts/historical/AUTONOMOUS_COUNCIL_MASTER.md` | HISTORICAL_PROMPT |
| `AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` | `04_TOOLING/prompts/historical/AUTONOMOUS_FREEZE_REMEDIATION_MASTER.md` | HISTORICAL_PROMPT |
| `FINAL_FREEZE_FORENSIC_AUDIT.md` | `04_TOOLING/prompts/historical/FINAL_FREEZE_FORENSIC_AUDIT.md` | HISTORICAL_PROMPT |
| `FINAL_PACKAGE_HASH_CANONICALIZATION.md` | `04_TOOLING/prompts/historical/FINAL_PACKAGE_HASH_CANONICALIZATION.md` | HISTORICAL_PROMPT |
| `FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md` | `04_TOOLING/prompts/historical/FINAL_REMEDIATED_CROSS_FAMILY_AUDIT.md` | HISTORICAL_PROMPT |
| `FINAL_TARGETED_GOVERNANCE_PATCH.md` | `04_TOOLING/prompts/historical/FINAL_TARGETED_GOVERNANCE_PATCH.md` | HISTORICAL_PROMPT |
| `PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md` | `04_TOOLING/prompts/historical/PRE_IMPLEMENTATION_WORKSPACE_FREEZE_AND_NORMALIZE.md` | HISTORICAL_PROMPT |
| `AVF_FINAL_FREEZE_v1.0.0.zip` | `90_ARCHIVE_READONLY/superseded-releases/AVF_FINAL_FREEZE_v1.0.0.zip` | SUPERSEDED_ZIP |
| `review-session/FINAL_REMEDIATED_FORENSIC_AUDIT.zip` | `90_ARCHIVE_READONLY/superseded-releases/FINAL_REMEDIATED_FORENSIC_AUDIT.zip` | SUPERSEDED_ZIP |

---

## 3. Deletions (Zero Evidentiary Loss)

- **Deleted Items:** All 8 `.DS_Store` macOS metadata cache files.
- **Evidentiary Data Loss:** Exactly 0 bytes.

---

## 4. Permission Model

- **Read-Only Paths (`chmod -R a-w`):**
  - `01_FROZEN_RELEASE/`
  - `02_SOURCE_KITS_READONLY/`
  - `03_GOVERNANCE_EVIDENCE_READONLY/`
  - `90_ARCHIVE_READONLY/`
- **Writable Paths:**
  - `05_IMPLEMENTATION/`
  - `04_TOOLING/`
  - `00_PROJECT_ADMIN/`
  - `99_TEMP/`
  - `.agents/`
