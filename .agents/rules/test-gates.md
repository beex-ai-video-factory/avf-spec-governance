# RULE: Verification & Test Gates
# Trigger: Glob on 05_IMPLEMENTATION/repos/** and test executions

## Objective
Guarantee software quality, schema compliance, and system reliability by prohibiting fake passes, incomplete stubs, or unverified implementation handoffs.

## Mandatory Directives
1. **Comprehensive Test Pyramid:** Every repository implementation must provide:
   - Unit tests covering domain logic and error paths.
   - Negative tests validating boundary conditions, malformed payloads, and timeout handling.
   - Contract conformance tests validating against frozen JSON Schemas.
   - Mock/Fake provider integration tests verifying end-to-end execution without external network calls.
2. **Zero Fake Passes:** Tests must genuinely execute code under test and assert invariants. Stubs returning hardcoded `true` or skipping assertions are strictly prohibited.
3. **Pre-Handoff Integration Gate:** A repository cannot be marked `STATUS = COMPLETED` or handed off to downstream dependencies until all tests pass cleanly in the local environment and are verified by `04_TOOLING/validation/` scripts.
4. **Offline Reproducibility:** Tests must execute deterministically in offline environments using the `FakeVideoProvider` and local emulators without requiring live API keys or external subscriptions.
