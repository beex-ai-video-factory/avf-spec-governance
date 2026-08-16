# RULE: Contract-First Architecture & Conformance
# Trigger: Always On (applies to all repo implementation and interfaces)

## Objective
Enforce schema-first and contract-driven development across all AI Video Factory repositories.

## Mandatory Directives
1. **R01 Contracts Precede Consumers:** Repository R01 (`repos/R01_contracts/`) is the root dependency for all inter-service contracts. R01 JSON Schemas, TypeScript interfaces, and validation fixtures must be implemented and tested before dependent repositories (R02–R15) begin implementation.
2. **Normative Typed Schemas:** JSON Schemas defined in the frozen baseline (`01_FROZEN_RELEASE/v1.0.0/02_contracts/`) are the single source of truth for:
   - `domain-entities.schema.json`
   - `event-envelope.schema.json`
   - `provider-request.schema.json`
   - `provider-result.schema.json`
   - `browser-command.schema.json`
   - `flow-execution-result.schema.json`
3. **Producer/Consumer Conformance Testing:** Any change or creation of API endpoints, message envelopes, or provider payloads requires both positive and negative fixture tests validating against the frozen schemas.
4. **Frozen Contract Changes Require CR:** If a contract schema is found to lack necessary fields or types during implementation, a formal Change Request (CR) must be submitted and approved before any schema alteration is permitted.
