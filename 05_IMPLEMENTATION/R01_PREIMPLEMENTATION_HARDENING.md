# R01 CONTRACTS — PRE-IMPLEMENTATION HARDENING REGISTER
## Technical Hardening Checklist Derived from External Forensic Audit

**Target Repository:** `R01_contracts`  
**Status:** OPEN FOR R01 IMPLEMENTATION SPRINT  
**Audit Source:** `03_GOVERNANCE_EVIDENCE_READONLY/review-session/FINAL_REMEDIATED_FORENSIC_AUDIT/`  

---

## 1. Hardening Items & Action Plan

The following non-blocking advisories from the external technical forensic audit are registered as mandatory hardening objectives during the R01 Contracts implementation sprint:

### Item 1: Raw JSON Schema `$id`, `$defs`, and `$ref` Serialization Standardization
- **Origin:** Forensic Audit ADVISORY-03 (Auditor-A F-01).
- **Issue:** Some raw JSON schema files contain non-standard empty-string keys (`""`) in place of standard `$defs` keywords.
- **R01 Implementation Task:** Standardize all JSON Schemas in `R01_contracts/schemas/` to strictly compliant Draft-07 / 2020-12 specifications before npm packaging. Validate with `ajv-cli` or `jsonschema`.
- **Constraint:** Do not edit frozen files in `01_FROZEN_RELEASE/v1.0.0/`. Implement corrected copies in `05_IMPLEMENTATION/repos/R01_contracts/schemas/`.

### Item 2: Execution Stage Count Documentation Alignment (17 Normative Stages)
- **Origin:** Forensic Audit ADVISORY-01.
- **Issue:** Historical summaries referenced 11 stages while normative schema (`domain-entities.schema.json`) defines 17 execution stages.
- **R01 Implementation Task:** Ensure all generated TypeScript enums, documentation, and state machine validation tests in R01 strictly reflect the authoritative 17 execution stages.

### Item 3: FlowExecutionResult Strongly-Typed Discriminated Unions
- **Origin:** Forensic Audit ADVISORY-04.
- **Issue:** `flow-execution-result.schema.json` contains an open `result` object.
- **R01 Implementation Task:** In `R01_contracts/types/`, define strongly-typed TypeScript discriminated unions for each of the 10 `FlowExecutionPort` command operations (e.g., `OpenProjectResult`, `CreateSceneResult`, `DownloadVideoResult`).

### Item 4: Automated TypeScript Type Generation
- **Task:** Configure an automated build pipeline in R01 using `json-schema-to-typescript` to compile JSON Schemas into strongly-typed `.d.ts` definitions.

### Item 5: Comprehensive Positive and Negative Fixture Test Suites
- **Task:** Build comprehensive JSON fixture suites for all 6 core schemas:
  - `domain-entities.schema.json`
  - `event-envelope.schema.json`
  - `provider-request.schema.json`
  - `provider-result.schema.json`
  - `browser-command.schema.json`
  - `flow-execution-result.schema.json`
- **Requirement:** Each schema must have $\ge 3$ positive and $\ge 3$ negative test fixtures asserting strict schema rejection on malformed fields or type violations.

### Item 6: Track A & Track B Common FlowExecutionPort Conformance Test Suite
- **Task:** Create a reusable test suite in R01 that can be run identically against both R09 (Browser Worker) and R10 (FlowKit Bridge) to verify semantic equivalence across all 10 operations.

---

## 2. Change Control Rule

If resolving any of these hardening items requires a normative change that would break contract compatibility with downstream specifications, the implementer must open a formal **Change Request (CR)** in `05_IMPLEMENTATION/change-requests/`.
