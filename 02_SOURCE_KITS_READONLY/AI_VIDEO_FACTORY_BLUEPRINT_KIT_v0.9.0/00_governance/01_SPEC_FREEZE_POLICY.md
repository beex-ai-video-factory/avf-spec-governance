# Specification Freeze Policy

## Freeze unit

The freeze unit is not a document; it is a **contract set** consisting of:

- architecture boundaries;
- canonical entities;
- API/command/event schemas;
- state machines;
- repository ownership;
- acceptance criteria;
- compatibility/versioning policy;
- security invariants.

## Frozen baseline

A release tagged `v1.0.0` means implementation teams may assume:

1. Entity IDs and relationships will not change incompatibly inside v1.
2. Published JSON schemas are authoritative.
3. A repo may evolve internally without coordinating with other repos if contracts remain compatible.
4. No repo may directly read another repo's private database tables.
5. FlowKit-specific fields cannot leak into core contracts.

## Change classes

### Patch
Documentation clarification; no semantic contract change.

### Minor
Backward-compatible optional fields, new enum values only when consumers are required to tolerate unknown values, new endpoints/events.

### Major
Breaking field semantics, removed fields, changed state transitions, ownership changes, altered idempotency semantics.

Major changes require an ADR and integration migration plan.

## Freeze gate

Before tagging `v1.0.0`, all items in `04_integration/FREEZE_CHECKLIST.md` must be signed off.
