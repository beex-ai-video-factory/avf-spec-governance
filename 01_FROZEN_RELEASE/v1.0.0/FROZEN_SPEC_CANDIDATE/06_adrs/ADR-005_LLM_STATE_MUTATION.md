# ADR-005 — LLM — STATE — MUTATION

## Context
LLMs cannot directly mutate canonical state.

## Decision
LLM output is validated proposal; application command commits state.

## Alternatives
Agent memory/database tools with direct writes.

## Why
Correctness and auditability.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
