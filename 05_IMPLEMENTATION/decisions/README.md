# IMPLEMENTATION DECISION RECORDS (IDR)
## AI Video Factory — Technical Implementation Choices

**Purpose:** Implementation Decision Records document concrete technical, framework, library, and algorithm choices made during implementation where the frozen architecture and ADRs are intentionally silent.

---

## Non-Negotiable Boundaries

1. **Subordinate to Frozen ADRs:** IDRs are strictly subordinate to frozen Architecture Decision Records (`01_FROZEN_RELEASE/v1.0.0/06_adrs/ADR-001` through `ADR-008`).
2. **No Contract Contradiction:** An IDR may **NEVER** contradict a frozen contract, schema, or system invariant.
3. **Scope:** IDRs govern library selections (e.g., Fastify vs Express for R02 API, Zod vs Ajv for internal validation, specific Temporal SDK idioms), internal data structures, and algorithmic details.

---

## IDR Template

Every IDR must follow this structure:

```markdown
# IDR-XXX: [TITLE]

**Status:** PROPOSED | ACCEPTED | SUPERSEDED
**Date:** YYYY-MM-DD
**Author:** [Agent / Engineer]
**Affected Repo:** [e.g., R02_core_state]
**Relevant Frozen ADR:** [e.g., ADR-002 Canonical State]

## Context & Problem Statement
*Describe the technical implementation detail requiring a decision where the frozen spec is silent.*

## Decision Drivers
- Driver 1
- Driver 2

## Considered Options
1. Option 1
2. Option 2

## Decision Outcome
*Chosen option and detailed technical rationale.*

## Consequences & Invariant Compliance
*Verify that no frozen schemas or contracts are altered.*
```

---

## Registered IDRs

| IDR | Title | Repo | Status | Date |
|---|---|---|---|---|
| *(None - Baseline Initialized)* | - | - | - | - |
