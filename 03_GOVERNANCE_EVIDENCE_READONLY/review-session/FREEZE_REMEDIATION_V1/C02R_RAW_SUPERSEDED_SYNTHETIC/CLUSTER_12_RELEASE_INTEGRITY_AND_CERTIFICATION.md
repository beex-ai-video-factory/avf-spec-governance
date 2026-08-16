# C02R HEARING TRANSCRIPT: CLUSTER 12 — RELEASE INTEGRITY, HASHING & CERTIFICATION
**CLUSTER_ID:** CLUSTER-12
**FINDINGS_COVERED:** FINDING_015, FINDING_035, FINDING_090, GOV-001, GOV-006, TECH-001, TECH-002, TECH-011, TECH-012
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R11 (Platform Specialist) & Council Audit Supervisor
- **Position:** The freeze release package must provide absolute, reproducible cryptographic integrity:
  1. *Consistent Identity:* All files (`VERSION`, `README.md`, `KIT_MANIFEST.yaml`, `COMMITTEE_REVIEW_EDITION.md`) must identify the true release version (`1.0.0-remediated-rc1` / `1.0.0`).
  2. *Deterministic Integrity Hashing:*
     - `CONTENT_HASHES.json`: SHA-256 of all normative specification files.
     - `CONTENT_TREE_SHA256`: SHA-256 of sorted `relative_path	sha256
` lines of all content files, explicitly excluding self-referential manifest files.
     - `DISTRIBUTABLE_ZIP_SHA256`: SHA-256 of the final zip package.
  3. *Evidence-Derived Certification:* The Freeze Certificate must not contain hard-coded assertion strings; every Council signature and audit verdict must reference the exact immutable ballot/report artifact path and its SHA-256 hash.
- **Evidence:** `EXTERNAL_TECHNICAL_REVIEW.md` (B01, B02, B11, B12), `FINAL_FORENSIC_AUDIT.md` (FA-001, FA-006).
- **Failure Scenario:** An external auditor receives the freeze zip, computes the tree hash, and gets a mismatch because the builder included self-referential hashes, invalidating the release certification.

## 2. Challenger Attack
- **Challenger:** R15 (Red Team Specialist)
- **Attack Vector:**
  1. *Self-Referential Circularity:* If `FINAL_SPEC_MANIFEST.md` contains the hash of the package, how can it be created without changing the hash of the package?
  2. *Automated Verification:* Can a third-party auditor verify the entire package with a single one-line shell command?

## 3. Domain Owner Review
- **Domain Owner:** R11 (Platform Specialist)
- **Evaluation:**
  - Clean separation: content files are hashed first to produce `CONTENT_HASHES.json` and `CONTENT_TREE_SHA256`.
  - Manifest and certificate files record `CONTENT_TREE_SHA256`.
  - The final distributable archive is created and its byte stream hash is published as `DISTRIBUTABLE_ZIP_SHA256`.
  - A simple verification script `verify_package.py` / `shasum -c` must be included to allow one-command independent verification.

## 4. Proponent Response
- **Response:**
  - We formalize this exact 4-step hashing protocol in `build_final_freeze_remediated.py` and document it in `FINAL_SPEC_MANIFEST.md`.
  - The Freeze Certificate builder will load raw ballots from `C04R/BALLOTS/RAW/` and insert their SHA-256 digests.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Use git commit hash only.
- **Why Rejected:** Zip archive distribution requires standalone filesystem hash verification independent of git repository metadata.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-015 amended to:
  1. Enforce version 1.0.0 consistency across candidate files.
  2. Implement deterministic non-self-referential tree hashing.
  3. Generate evidence-derived certificate linking to raw ballot hashes.
