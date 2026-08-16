# CHANGE REQUESTS (CR) REGISTER
## AI Video Factory — Spec Defect & Errata Management

**Purpose:** When an implementation agent discovers a bug, logical contradiction, schema error, or missing requirement in the frozen v1.0.0 specification, it must NOT edit the frozen spec. Instead, a Change Request must be filed here for human sponsor review.

---

## Change Request Lifecycle

1. **Discovery:** Agent identifies specification defect and halts affected implementation branch.
2. **Filing:** Agent creates `CR-XXX_<short_title>.md` using `CR_TEMPLATE.md`.
3. **Triage & Review:** Human project sponsor evaluates the CR and selects an option.
4. **Resolution:**
   - **APPROVED:** Errata or version upgrade plan is documented; unblocked branch proceeds.
   - **REJECTED:** Implementation must conform to original frozen specification.
   - **DEFERRED:** Workaround implemented via Implementation Decision Record (IDR) without breaking frozen contracts.

---

## Active Change Requests

| CR ID | Title | Discovered By | Affected Repo | Severity | Status |
|---|---|---|---|---|---|
| *(None - Baseline Verified)* | - | - | - | - | - |
