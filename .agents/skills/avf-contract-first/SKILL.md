---
name: avf-contract-first
description: Validate JSON Schemas, generate TypeScript types, build positive and negative test fixtures, and verify producer/consumer contract compatibility across all AVF services.
---

# Skill: AVF Contract-First Engineering

## Purpose
Provides procedures for validating JSON Schema definitions, generating strongly typed interfaces, and implementing rigorous producer-consumer conformance test suites.

## Core Procedures
1. **Schema Validation:**
   - Ensure all schemas use JSON Schema Draft-07 / 2020-12 valid syntax.
   - Verify `$id`, `$schema`, and `$defs` references resolve locally without internet fetching.
2. **Type Generation:**
   - Generate TypeScript types directly from JSON Schema definitions using `json-schema-to-typescript` or equivalent CLI tools.
   - Store generated types in `05_IMPLEMENTATION/repos/R01_contracts/types/`.
3. **Fixture Generation:**
   - Create at least 3 positive fixtures representing valid payload variants for each schema.
   - Create at least 3 negative fixtures validating:
     - Missing mandatory fields
     - Extra forbidden properties (when `additionalProperties: false`)
     - Type mismatches (e.g., string vs number)
     - Value constraints (e.g., regex pattern, enum value violation, range violation).
4. **Producer-Consumer Verification:**
   - Both producer services (e.g., R05 Prompt Compiler) and consumer services (e.g., R08 Google Flow Adapter) must link against R01 schemas for payload validation.
