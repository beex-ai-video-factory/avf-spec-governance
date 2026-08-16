# ADR-001 — MODULAR — POLYREPO

## Context
Independent repository boundaries with controlled deployment composition.

## Decision
Use separately versioned repositories for bounded components and an integration repo; do not require each repo to become a separate runtime service.

## Alternatives
One giant monorepo; dozens of network microservices.

## Why
AI-agent build isolation and replaceability without operational microservice theater.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
