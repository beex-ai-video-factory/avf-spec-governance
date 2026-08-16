# ADR-003 — PROVIDER — ABSTRACTION

## Context
Provider abstraction mandatory.

## Decision
All video generation goes through `VideoGenerationProvider`; Google Flow is one adapter.

## Alternatives
Direct Flow calls from workflow/creative modules.

## Why
Replaceability and contract testing.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
