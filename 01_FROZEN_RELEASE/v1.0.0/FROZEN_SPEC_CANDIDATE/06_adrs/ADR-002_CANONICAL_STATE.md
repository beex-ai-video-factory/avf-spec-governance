# ADR-002 — CANONICAL — STATE

## Context
Canonical business state.

## Decision
`avf-core-state` owns PostgreSQL canonical state. Workflow/browser/FlowKit memories are non-canonical.

## Alternatives
Workflow history as source of truth; shared DB access.

## Why
Recoverability and clear ownership.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
