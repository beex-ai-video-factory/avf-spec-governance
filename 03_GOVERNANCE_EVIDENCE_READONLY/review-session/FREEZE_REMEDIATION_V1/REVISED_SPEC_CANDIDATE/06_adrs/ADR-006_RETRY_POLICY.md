# ADR-006 — RETRY — POLICY

## Context
Deterministic retry policy.

## Decision
QC/LLMs provide scores/reasons; software policy owns retries and budgets.

## Alternatives
Agent decides retry until satisfied.

## Why
Bounded cost and predictable behavior.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
