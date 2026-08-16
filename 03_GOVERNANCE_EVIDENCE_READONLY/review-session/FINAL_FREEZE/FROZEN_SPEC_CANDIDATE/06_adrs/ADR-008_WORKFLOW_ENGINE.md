# ADR-008 — WORKFLOW — ENGINE

## Context
Durable workflow runtime.

## Decision
Use a Temporal-class durable workflow engine for operational sequencing; LangGraph only for bounded AI workflows.

## Alternatives
Use LangGraph as total system orchestrator.

## Why
Correct long-running retries/resume and side-effect handling.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
