# AI VIDEO FACTORY — POST-v1.0.0 MAINTENANCE LIFECYCLE & ROUTING GUIDE
## Standard Operational Procedures for Post-Release Maintenance, Patches & Evolution

**Document Version:** 1.0.0  
**Authority:** Technical Architecture Board & Security Custodian  
**Applies To:** AI Video Factory Post-v1.0.0 Operations  

---

## 1. Non-Negotiable Maintenance Invariants

> [!IMPORTANT]
> **GOVERNANCE & SYSTEM INVARIANTS:**
> 1. **Baseline Immutability:** The frozen v1.0.0 baseline under `01_FROZEN_RELEASE/v1.0.0/` is permanently locked. Post-release changes never edit frozen baseline directories.
> 2. **Polyrepo Isolation:** Any code modification must observe `ALLOWED_WRITE_ROOT: 05_IMPLEMENTATION/repos/<repo_name>/`. Cross-repo edits in a single branch are forbidden.
> 3. **Single Database Owner:** Only `R02_core_state` owns database schema migrations and direct PostgreSQL connections.
> 4. **Deterministic Conformance:** Any change affecting contracts or provider adapters must pass `GATE-00`, `GATE-01`, and `GATE-02`.
> 5. **Strict SemVer:**
>    - **Patch (`v1.0.X`):** Backward-compatible bugfixes, security patches, internal refactors.
>    - **Minor (`v1.X.0`):** Backward-compatible contract additions, new features, new provider adapters.
>    - **Major (`vX.0.0`):** Breaking schema changes, core architecture revisions (requires new baseline lock & ADR).

---

## 2. Maintenance Routing Matrix

| Route ID | Maintenance Class | Scope | Branch Pattern | Verification Required | Release Action |
|---|---|---|---|---|---|
| **MAINT-01** | Hotfix | Critical production defect in single repo | `hotfix/v1.0.X-<issue>` | Local `*-03` + Affected Gates | Tag `v1.0.X` (`--no-ff`) |
| **MAINT-02** | Security Patch | Vulnerable dependency or secret redaction leak | `secpatch/v1.0.X-<cve>` | Local `*-03` + GATE-00 + GATE-04 | Tag `v1.0.X` (`--no-ff`) |
| **MAINT-03** | Contract Patch | Additive schema update in R01 | `contract/v1.X.0-<feature>` | R01 `*-03` + GATE-00 + GATE-02 + GATE-03 | Tag `v1.X.0` (`--no-ff`) |
| **MAINT-04** | Implementation Bugfix | Non-urgent logic fix | `fix/rXX-<issue>` | Local `*-03` + Local `*-04` | Merge to `main` |
| **MAINT-05** | Frozen Spec Defect (CR) | Inconsistency in specification | `governance/CR-YYYYMMDD-XX` | Formal CR Approval + ADR | New Baseline Candidate |
| **MAINT-06** | Minor Feature Release | Backward-compatible feature set | `release/v1.X.0` | GATE-00 through GATE-05 | Tag `v1.X.0` (`--no-ff`) |
| **MAINT-07** | Emergency Rollback | Production regression / outage | N/A (Tag checkout) | `REL-03` Health Verification | Point deployment to `v1.0.0` |

---

## 3. Standard Maintenance Procedures

### Route MAINT-01: Production Hotfix Protocol
1. **Branching:** In the affected repository directory `05_IMPLEMENTATION/repos/<repo_name>/`, create branch `hotfix/v1.0.X-<desc>` from the release tag.
2. **Remediation:** Apply minimal targeted code fix inside `src/`.
3. **Local Testing:** Run the repository test suite via `<REPO>_03_TEST_AND_REVIEW.md`. Assert 100% pass and coverage >= 85%.
4. **Gate Re-verification:** If the repository is in the foundation layer (R01, R02, R07, R14), execute `GATE-00`. If workflow-related, execute `GATE-01`. If adapter-related, execute `GATE-02`.
5. **Tagging & Release:** Execute `<REPO>_04_ACCEPT_RELEASE.md` with patch version increment (e.g. `v1.0.1`), using non-fast-forward merge and signed/annotated git tag.

---

### Route MAINT-02: Dependency & Security Patch Protocol
1. **Identify Vulnerability:** Run security audit scanner on dependencies or inspect secret redaction rules in `R14_platform_observability`.
2. **Update Dependency / Filter:** Update `package.json` / `requirements.txt` or enhance regex token sanitization in R14.
3. **Verify Zero Secret Leaks:** Run R14 secret redaction verification test suite.
4. **Regression Gate:** Run `GATE-00_FOUNDATION_GATE.md` and `GATE-04_SYSTEM_INTEGRATION_GATE.md`.
5. **Release:** Tag updated repository with patch version.

---

### Route MAINT-03: Contract Schema Patch Protocol (R01)
1. **Additive Schema Modification:** Edit JSON schemas under `05_IMPLEMENTATION/repos/R01_contracts/schemas/`. Breaking modifications (field removal, type changes) are forbidden.
2. **Regenerate Types:** Run `npm run generate:types` in R01.
3. **Add Positive & Negative Fixtures:** Add at least 1 positive fixture and 1 negative fixture for the new schema elements.
4. **Contract Verification:** Run `R01_03_TEST_AND_REVIEW.md`.
5. **Dependent Repository Alignment:** Downstream consumers update their imported R01 contract dependency. Run `GATE-00`, `GATE-02`, and `GATE-03`.

---

### Route MAINT-04: Implementation Bugfix Protocol
1. **Locate Defect:** Use `FAILURE_DECISION_TREE.md` to confirm localized implementation bug in repository `<REPO>`.
2. **Execute Recovery:** Run `<REPO>_RECOVERY.md`.
3. **Execute Implementation Fix:** Run `<REPO>_02_IMPLEMENT.md` to patch source logic.
4. **Execute Review:** Run `<REPO>_03_TEST_AND_REVIEW.md`.
5. **Accept & Commit:** Run `<REPO>_04_ACCEPT_RELEASE.md`.

---

### Route MAINT-05: Frozen-Spec Defect & Change Request (CR) Protocol
1. **File Change Request:** Run `99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md` to generate `05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-XX.md`.
2. **Human Review Gate:** Human Architecture Board sponsor reviews, assigns impact assessment, and records decision (`APPROVED` / `REJECTED`).
3. **ADR Documentation:** If approved, draft Architectural Decision Record (ADR) under `05_IMPLEMENTATION/governance/adr/`.
4. **Draft Spec Increment:** Prepare `v1.1.0` candidate release directory under `01_FROZEN_RELEASE/v1.1.0/` without altering `v1.0.0`.
5. **Resume Execution:** Execute `RESUME_PROJECT.md` to resume implementation against updated specification.

---

### Route MAINT-06: Minor Feature Release Protocol
1. **Feature Planning:** Ensure all planned feature repositories adhere to the 16 blueprint sections.
2. **Sequential Implementation:** Implement feature repos following canonical sequential operator order.
3. **Full Gate Progression:** Execute all 6 integration gates sequentially:
   `GATE-00` -> `GATE-01` -> `GATE-02` -> `GATE-03` -> `GATE-04` -> `GATE-05`.
4. **Pre-Release Audit:** Execute `18_RELEASE/RELEASE_01_FINAL_PRE_RELEASE_AUDIT.md`.
5. **Publish & Tag:** Execute `18_RELEASE/RELEASE_02_TAG_AND_PUBLISH.md` with minor version increment (e.g. `v1.1.0`).

---

### Route MAINT-07: Emergency Production Rollback Protocol
1. **Initiate Rollback:** In event of critical live failure, halt active generation workflows in `R06_workflow`.
2. **Check Out Release Tag:** Switch all 15 repositories to previous stable release tag:
   ```bash
   git checkout tags/v1.0.0
   ```
3. **Reset Environment:** Execute `99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md` to restart Docker compose services and reset state.
4. **Verify Health:** Execute `18_RELEASE/RELEASE_03_POST_RELEASE_VERIFICATION.md` to verify all health check endpoints.
5. **Log Incident:** Record rollback rationale and root cause in `05_IMPLEMENTATION/operator-state/INCIDENT_LOG.md`.
