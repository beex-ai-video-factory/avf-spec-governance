# C02 — Formal Research Requests

The following formal architectural research requests were chartered during C02 cross-examination and are assigned for investigation prior to or during C03 solution design.

| REQUEST_ID | SOURCE_FINDING | TOPIC | ASSIGNED_OWNERS | DELIVERABLE |
|---|---|---|---|---|
| RES-001 | F-R01-006 | Deterministic Cross-Language JSON Canonicalization (RFC 8785 vs Proto3) | R01 (Domain) & R05 (Data) | Benchmark and RFC recommendation for cross-language canonical serialization in R02/R05/R07 |

---

## Research Request Details

### RES-001: Deterministic Cross-Language JSON Canonicalization (RFC 8785 vs Proto3)
- **Source Finding:** `F-R01-006`
- **Assigned Owners:** `R01 (Domain) & R05 (Data)`
- **Objective:** Evaluate RFC 8785 (JSON Canonicalization Scheme - JCS) implementation libraries across Python (`canonicaljson`), Node.js (`canonicalize`), and Go. Verify whether binary hash compatibility can be guaranteed across microservices with zero field-ordering ambiguity.
- **Expected Deliverable:** Benchmark and RFC recommendation for cross-language canonical serialization in R02/R05/R07
- **Exit Criteria:** Working cross-language test suite proving identical SHA-256 hash for complex domain entities.

