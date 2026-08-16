---
name: avf-repo-boundaries
description: Enforce domain boundaries, extract OWNS and DOES NOT OWN constraints from repository blueprints, and detect forbidden cross-repository imports or dependency DAG violations.
---

# Skill: AVF Repo Boundaries & DAG Enforcement

## Purpose
Guarantees that repositories maintain clean domain boundaries according to ADR-001 (Modular Polyrepo) and ADR-002 (Canonical State).

## Core Responsibilities & Invariants
- **R01 Contracts:** OWNS schemas and contract types. DOES NOT OWN business logic or runtime services.
- **R02 Core State:** OWNS PostgreSQL schema, state machine persistence, domain entity tables, state mutation logic. DOES NOT OWN workflow orchestration or provider communication.
- **R03 Creative:** OWNS ideation, script generation, and scene planning. DOES NOT OWN raw provider calls or video rendering.
- **R04 Assets & Continuity:** OWNS asset catalog, prompt continuity, character profiles, visual consistency. DOES NOT OWN DB persistence.
- **R05 Prompt Compiler:** OWNS template rendering, negative prompt injection, provider dialect formatting. DOES NOT OWN state storage.
- **R06 Workflow:** OWNS Temporal workflow definitions, activity dispatch, and saga coordination. DOES NOT OWN domain entity tables.
- **R07 Provider SDK:** OWNS provider-neutral interface definitions, capability matrices, and mock fake provider. DOES NOT OWN Google Flow specifics.
- **R08 Google Flow Adapter:** OWNS translation between Provider SDK and Google Flow execution engines. DOES NOT OWN browser CDP details.
- **R09 Browser Worker:** OWNS Track A browser automation, Playwright/CDP execution, resilient selectors. DOES NOT OWN Track B or direct APIs.
- **R10 FlowKit Bridge:** OWNS Track B direct HTTP protocol bridge to Google Flow backend. DOES NOT OWN browser sessions.
- **R11 QC:** OWNS technical QC (FFprobe, container verification) and semantic QC (LLM/Vision assessment).
- **R12 Media:** OWNS FFmpeg stitching, audio overlay, transcoding, asset packaging.
- **R13 Operator Console:** OWNS human-in-the-loop review UI, gate approvals, audit inspection.
- **R14 Platform Observability:** OWNS OpenTelemetry traces, metrics collection, structured logging, cost tracking.
- **R15 Integration Harness:** OWNS E2E test suites, fake provider simulation, scenario test runner.
