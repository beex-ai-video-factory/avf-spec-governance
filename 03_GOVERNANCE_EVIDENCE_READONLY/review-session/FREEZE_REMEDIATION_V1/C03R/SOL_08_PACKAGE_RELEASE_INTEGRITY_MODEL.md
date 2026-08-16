# C03R SOLUTION PACKAGE 08: RELEASE INTEGRITY & DETERMINISTIC HASHING
**SOLUTION_ID:** SOL-08
**FINDINGS_ADDRESSED:** GOV-001, GOV-006, TECH-001, TECH-002, TECH-011, TECH-012
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
The previous freeze package had stale hashes in `KIT_MANIFEST.yaml`, retained `0.9.0-review-candidate` in `VERSION` and `README.md`, used a non-reproducible tree hash, and hard-coded signature strings in the certificate.

---

## 2. Options Analysis

### Option A: 4-Stage Deterministic Hashing & Evidence-Derived Certification (Recommended)
- **Architecture:**
  1. *Version Identity:* Set version to `1.0.0-remediated-rc1` (promoted to `1.0.0` at final freeze) across `VERSION`, `README.md`, `KIT_MANIFEST.yaml`, and `COMMITTEE_REVIEW_EDITION.md`.
  2. *Content Hashing (Stage 1):* Compute individual SHA-256 for all normative content files in `00_governance/`, `01_master/`, `02_contracts/`, `03_repo_blueprints/`, `04_integration/`, `05_phases/`, `06_adrs/`, `07_risk/`, `08_evidence/`, `09_agent_packets/`, and `VERSION`, `README.md`.
  3. *Deterministic Tree Hash (Stage 2):* Compute `CONTENT_TREE_SHA256` by SHA-256 hashing the lexicographically sorted lines of `relative_path	sha256
` for all content files (excluding self-referential manifest/hash files).
  4. *Manifest & Certificate Generation (Stage 3):* Generate `KIT_MANIFEST.yaml`, `CONTENT_HASHES.json`, and `FINAL_SPEC_MANIFEST.md` recording the content hashes. Generate `FREEZE_CERTIFICATE.md` with signatures dynamically linked to raw ballot artifact paths and SHA-256 hashes from `C04R/BALLOTS/RAW/`.
  5. *Archive Hashing (Stage 4):* Create `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip` and record `DISTRIBUTABLE_ZIP_SHA256`.
- **Exact Normative Files to Change:**
  - `VERSION`, `README.md`, `KIT_MANIFEST.yaml`, `COMMITTEE_REVIEW_EDITION.md`
  - Freeze builder scripts and manifests.

### Option B: Exclude Manifests from Hashing
- **Drawbacks:** Leaves manifests unverified.

---

## 3. Decision
**Selected: Option A.** Eliminates all circularity and provides an exact, reproducible verification protocol.
