# ADR-004 — DUAL — FLOW — EXECUTION

## Context
Dual Google Flow execution tracks.

## Decision
Freeze `FlowExecutionPort`; support Track A controlled browser implementation and Track B FlowKit compatibility bridge.

## Alternatives
Fork FlowKit into core; single custom browser route only.

## Why
Speed now without long-term coupling.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
