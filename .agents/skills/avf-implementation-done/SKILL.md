---
name: avf-implementation-done
description: Verify Definition of Done (DoD) criteria, contract conformance, unit and negative test passing, forbidden dependency scans, and implementation signoff before marking a repo complete.
---

# Skill: AVF Implementation Definition of Done (DoD)

## Purpose
Provides the comprehensive checklist and verification procedure for determining when an individual repository (R01–R15) is fully implemented and ready for downstream integration.

## Definition of Done Checklist
Before marking any repository `STATUS = COMPLETED`:
1. **Blueprint Conformance:** All capabilities defined under `OWNS` in the repo blueprint are implemented; no features listed under `DOES NOT OWN` are present.
2. **Schema & Contract Alignment:** Repository types match R01 JSON Schemas. Conformance tests validate 100% of schema positive/negative fixtures.
3. **Automated Test Coverage:**
   - Unit tests pass with zero failures.
   - Negative tests pass with zero failures.
   - Mock integration tests pass using `FakeVideoProvider`.
4. **Static & Security Analysis:**
   - Zero lint errors or TypeScript compilation errors.
   - Zero committed secrets, API keys, or raw credentials.
   - No illegal imports violating `05_IMPLEMENTATION/dependency-gates.yaml`.
5. **Documentation & Handoff:**
   - Repository `README.md` includes local setup, testing instructions, and environment variables.
   - Any technical decisions are recorded in `05_IMPLEMENTATION/decisions/`.
   - Any approved spec variations are linked to formal Change Requests in `05_IMPLEMENTATION/change-requests/`.
