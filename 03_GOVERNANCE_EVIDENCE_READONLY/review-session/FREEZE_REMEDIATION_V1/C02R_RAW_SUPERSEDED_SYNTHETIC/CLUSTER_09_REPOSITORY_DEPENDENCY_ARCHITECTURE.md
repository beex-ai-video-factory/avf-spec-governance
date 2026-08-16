# C02R HEARING TRANSCRIPT: CLUSTER 09 — REPOSITORY DEPENDENCY ARCHITECTURE & DAG
**CLUSTER_ID:** CLUSTER-09
**FINDINGS_COVERED:** FINDING_010, FINDING_028, FINDING_070, TECH-010, TECH-009
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R01 (Domain DDD Specialist) & R11 (Platform Specialist)
- **Position:** The repository dependency graph previously had missing edges (e.g. R15 Integration Harness consuming all components, R14 Observability telemetry ingestion from Track A/B workers, and Workflow activity dependencies on media/qc). We must establish a complete, mathematically acyclic Dependency Directed Acyclic Graph (DAG) across all 15 repositories:
  - Layer 0 (Foundation): R01 Contracts
  - Layer 1 (State & Storage): R02 Core State
  - Layer 2 (Domain Engines): R03 Creative, R04 Assets/Continuity, R05 Prompt Compiler, R11 QC, R12 Media
  - Layer 3 (Provider Infrastructure): R07 Provider SDK, R08 Google Flow Adapter
  - Layer 4 (Execution Workers): R09 Browser Worker, R10 FlowKit Bridge
  - Layer 5 (Orchestration & Operations): R06 Workflow, R13 Operator Console
  - Cross-Cutting: R14 Platform Observability (imported by all), R15 Integration Harness (consumes all)
- **Evidence:** `DEPENDENCY_GRAPH.md` vs `REPOSITORY_STRATEGY.md` and individual repo blueprints.
- **Failure Scenario:** A developer in R08 Google Flow Adapter directly imports a database repository from R02 Core State, violating layer boundaries and causing circular dependency build failures.

## 2. Challenger Attack
- **Challenger:** R10 (DX Specialist) & R15 (Red Team Specialist)
- **Attack Vector:**
  1. *Observability Circularity:* If R14 Platform Observability is imported by R01 Contracts, does R14 depend on R01?
  2. *Forbidden Dependencies:* How is forbidden dependency enforcement verified during CI/CD?

## 3. Domain Owner Review
- **Domain Owner:** R11 (Platform Specialist)
- **Evaluation:**
  - R01 Contracts is pure TypeScript interfaces/schemas and has zero runtime dependencies (does not import R14).
  - All other repositories import R01 Contracts and R14 Observability SDK.
  - Forbidden dependencies must be explicitly codified:
    - No repo except R02 may access the canonical database.
    - R08/R09/R10 may not import R03/R04/R05 domain engines.
    - R09 and R10 may not depend on each other.
    - No repo may have circular dependencies.
  - CI tooling (`dependency-cruiser` / ESLint rules) in R15 will enforce the DAG rules.

## 4. Proponent Response
- **Response:**
  - We reconstruct `DEPENDENCY_GRAPH.md` with the complete 15-repo matrix, explicit layer definitions, and automated verification rules.
  - We update all 15 repo blueprints to ensure their "Dependencies" and "Forbidden Dependencies" sections match the master graph 100%.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Merge all 15 repos into a single monorepo with internal packages.
- **Why Rejected:** The Council explicitly evaluated monorepo vs polyrepo in ADR-001 and selected modular polyrepo with standalone agent build packets to allow parallel AI agent development.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-010 amended to:
  1. Rebuild `DEPENDENCY_GRAPH.md` with complete layers, telemetry edges, harness edges, and forbidden matrix.
  2. Update all 15 repo blueprints in `03_repo_blueprints/`.
