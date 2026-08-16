# C03R SOLUTION PACKAGE 04: EVENT ENVELOPE & CATALOG NAMING STANDARDS
**SOLUTION_ID:** SOL-04
**FINDINGS_ADDRESSED:** TECH-007, FINDING_006, FINDING_023
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
Event envelope definition in `CONTRACTS_OVERVIEW.md` conflicted with `event-envelope.schema.json`, and event names in `COMMAND_EVENT_CATALOG.md` failed the schema's lowercase dotted regex pattern.

---

## 2. Options Analysis

### Option A: Unified OTel-Compliant Dotted Event Contract (Recommended)
- **Architecture:**
  - Standardize `event-envelope.schema.json` with:
    - `event_id` (UUID)
    - `event_type` (regex `^avf\.[a-z0-9_-]+(\.[a-z0-9_-]+)+$`)
    - `aggregate_id` (string/UUID)
    - `aggregate_version` (integer >= 1)
    - `timestamp_utc` (date-time)
    - `correlation_id` (UUID)
    - `trace_id` (32-hex or UUID string for OpenTelemetry)
    - `span_id` (16-hex string for OpenTelemetry)
    - `workflow_run_id` (optional string)
    - `schema_version` (semver string e.g. "1.0.0")
    - `payload` (object)
  - Update `COMMAND_EVENT_CATALOG.md` to list both the canonical dotted event string (e.g. `avf.project.created`, `avf.generation.job_created`, `avf.take.registered`, `avf.qc.completed`) and the TypeScript event class name (`ProjectCreatedEvent`, etc.).
  - Update `CONTRACTS_OVERVIEW.md` to match `event-envelope.schema.json` exactly.
- **Exact Normative Files to Change:**
  - `02_contracts/event-envelope.schema.json`
  - `02_contracts/CONTRACTS_OVERVIEW.md`
  - `04_integration/COMMAND_EVENT_CATALOG.md`
  - `03_repo_blueprints/R01_CONTRACTS.md`
  - `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`

### Option B: Dual Envelope Model (Internal vs External)
- **Drawbacks:** Requires transformation middleware between internal services and event bus, increasing latency and bug surface.

---

## 3. Decision
**Selected: Option A.** Single unambiguous event contract across the entire system.
