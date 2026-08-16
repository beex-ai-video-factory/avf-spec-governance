# Independent Blind Review Report — Round C01

**Role:** `R13_OSS` (OSS / Dependency / Licensing Reviewer)  
**Session ID:** `1df69d95-cadb-43c4-9b5e-c2b6f237217e`  
**Review Target Version:** AI Video Factory Blueprint Kit v0.9.0  
**Baseline Reference:** `review-session/C00_FINAL/`  
**Date / Timestamp:** 2026-08-15T11:30:00+07:00  

---

## 1. Executive Summary & Review Scope

As `R13_OSS`, my primary mandate is to enforce robust open-source software (OSS) reuse strategies, verify intellectual property and licensing boundaries (MIT/Apache vs. GPL/AGPL), audit third-party dependency supply-chain risks, mandate version pinning and lockfile governance, and guarantee strict external codebase isolation.

### The Foundational Axiom
> **"No external repo may silently define our canonical contract."**

The AVF architecture must preserve full capability and replaceability. Third-party engines, external OSS repositories (specifically FlowKit), and third-party media or AI frameworks are untrusted or disposable peripherals. They must never dictate canonical database schemas, command envelopes, domain models, or lifecycle invariants.

### Mandated Review Inputs
1. **Primary Assigned Specifications:**
   - [`DEPENDENCY_GRAPH.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md)
   - [`SOURCE_LEDGER.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/08_evidence/SOURCE_LEDGER.md)
   - [`R10_FLOWKIT_BRIDGE.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md)
2. **Assigned Gap Seed:**
   - **`GAP-008`**: FlowKit bridge process supervision, crash recovery, IPC lifecycle, and licensing boundaries.
3. **Cross-Referenced System Blueprints & Governance:**
   - [`MASTER_BLUEPRINT.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md)
   - [`SECURITY_MODEL.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md)
   - [`R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md)
   - [`R08_GOOGLE_FLOW_ADAPTER.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md)
   - [`R09_BROWSER_WORKER.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md)
   - [`R11_QC.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md)
   - [`R12_MEDIA.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R12_MEDIA.md)
   - [`ADR-004_DUAL_FLOW_EXECUTION.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-004_DUAL_FLOW_EXECUTION.md)
   - [`ADR-007_BROWSER_SECURITY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-007_BROWSER_SECURITY.md)
   - [`ADR-008_WORKFLOW_ENGINE.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-008_WORKFLOW_ENGINE.md)
   - [`PHASE_0_BENCHMARK.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/PHASE_0_BENCHMARK.md)
   - Baseline Registers: [`SYSTEM_INVARIANT_INVENTORY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/C00_FINAL/SYSTEM_INVARIANT_INVENTORY.md), [`C00_GAP_TO_C01_SEED_REGISTER.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md), [`CONTRACT_INVENTORY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/C00_FINAL/CONTRACT_INVENTORY.md).

---

## 2. Invariant & Contract Inventory (R13 Lens)

| INVARIANT_ID | INVARIANT RULE | ENFORCEMENT & OSS / DEPENDENCY BOUNDARY |
|---|---|---|
| **INV-005** | Browser / extension / FlowKit state is never canonical business state. | R10 / FlowKit SQLite treated as ephemeral worker cache; canonical truth is strictly owned by `avf-core-state` (PostgreSQL). |
| **INV-007** | Google Flow-specific fields do not appear in core contracts unless represented as namespaced provider metadata. | External FlowKit internal structures, schemas, and endpoint responses must not bleed into `avf-contracts`. |
| **INV-008** | Provider adapters cannot directly modify Project / Shot records. | `avf-flowkit-bridge` and `avf-google-flow-adapter` communicate via typed contracts only. |
| **INV-012** | Authentication / security challenges do not trigger automated bypass behavior. | FlowKit bypass/anti-bot hacks must not be copied or invoked; bridge must map challenges to normalized `AUTH_REQUIRED` / `SECURITY_CHALLENGE`. |
| **INV-013** | A repo cannot read another repo's private database schema directly. | Prohibits `avf-flowkit-bridge` from reading core DB or core services from accessing FlowKit SQLite. |
| **INV-014** | Contract consumers must validate schema versions at boundaries. | Boundary schema validators (e.g. Ajv / Pydantic) validate all IPC inputs/outputs. |
| **INV-020** | Switching between Track A and Track B does not change upstream generation contracts. | Strict contract conformance on `FlowExecutionPort` (`browser-command.schema.json`). |

---

## 3. Concrete Failure Scenarios

To anchor the review in concrete engineering realities, the following failure scenarios demonstrate what occurs if OSS, licensing, process supervision, and dependency isolation boundaries are inadequately specified:

### Scenario 1: The Zombie FlowKit Subprocess & Deadlock Cascade (GAP-008)
- *Trigger:* `avf-flowkit-bridge` spawns FlowKit as an un-supervised raw OS child process. During generation of Shot #4, the Chrome tab hosting Google Flow crashes due to an out-of-memory error. FlowKit’s Python process hangs indefinitely waiting on an unclosed WebSocket connection.
- *Cascade:* `avf-flowkit-bridge` has no health supervisor, PID tracking, or process lease timeout. It continues holding the execution lease. `avf-workflow` times out after 15 minutes and retries the job. The bridge attempts to spawn another FlowKit instance on port 8000, which crashes with `EADDRINUSE`. The system deadlocks, holding locks on local media and exhausting worker resources.
- *Root Cause:* Absence of an explicit process supervision topology (Sidecar / Daemon with health endpoint vs. Supervised Subprocess with strict reaping and port allocation).

### Scenario 2: FFmpeg GPL Copyleft Contamination Lawsuit
- *Trigger:* An engineering agent implementing `avf-media` or `avf-qc` imports a Python binding (such as `PyAV` or C-FFI wrapper) that statically or dynamically links against a standard FFmpeg distribution built with `--enable-gpl` (utilizing `libx264`/`libx265`).
- *Cascade:* The AVF proprietary codebase incorporates GPL copyleft code into its runtime address space. During enterprise due diligence or a compliance audit, the system is found to violate GPL v2/v3 terms by distributing proprietary binaries/containers without open-sourcing the entire AVF application layer.
- *Root Cause:* Lack of an explicit architectural policy mandating FFmpeg execution strictly via decoupled CLI subprocesses (`exec`/`spawn` or containerized sidecar) rather than linked C-bindings.

### Scenario 3: Upstream FlowKit Repository Tampering / Deletion
- *Trigger:* The external OSS author of `crisng95/flowkit` deletes the GitHub repository, re-licenses the repository to AGPLv3/commercial, or pushes a compromised commit with a malicious dependency in its `requirements.txt`.
- *Cascade:* CI/CD builds for `avf-flowkit-bridge` dynamically pull from upstream GitHub `main`. Production deployments fail immediately, or worse, execute unverified third-party code in the privileged local execution zone.
- *Root Cause:* Failure to enforce an immutable Git commit pin, internal mirror repository, cryptographic checksum verification, and Software Bill of Materials (SBOM).

### Scenario 4: AI Framework State Leakage & Churn (LangGraph / LangChain)
- *Trigger:* `avf-creative` or `avf-prompt-compiler` uses LangGraph for structured prompt generation. An agent implements prompt compilation by passing LangGraph's internal `StateGraph` object directly across repository boundaries into `avf-workflow`.
- *Cascade:* LangGraph releases a breaking version update (e.g. v0.1 to v0.2), altering state serialization keys. The entire workflow engine breaks, and canonical entities in PostgreSQL cannot deserialize historical prompt records.
- *Root Cause:* Lack of an encapsulation firewall around AI orchestration frameworks.

---

## 4. Formal Findings (Council Finding Format)

### Finding F-R13-001: FlowKit Process Supervision Topology, IPC Lifecycle, and Crash Recovery Underspecified (GAP-008 Resolution)

FINDING_ID: F-R13-001
ROLE: R13_OSS
SEVERITY: CRITICAL
CATEGORY: ARCHITECTURE
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-004_DUAL_FLOW_EXECUTION.md
AFFECTED_CONTRACTS:
  - FlowExecutionPort (browser-command.schema.json)
  - STATUS_STATE_MACHINES.md
EVIDENCE:
  - R10_FLOWKIT_BRIDGE.md (Lines 14, 52, 89) mentions "FlowKit process health adapter", "local process/HTTP/WS integration", and "FlowKit unavailable/restart tests", but provides no concrete specification for process management:
    1. Is FlowKit spawned and reaped as a child subprocess by avf-flowkit-bridge, or run as an external systemd/Docker daemon?
    2. How are port conflicts (e.g. 127.0.0.1:8000) avoided when running concurrent worker instances?
    3. How does the bridge detect an unresponsive FlowKit instance (hung WebSocket vs. crash vs. Chrome disconnect)?
    4. What is the exact teardown, SIGTERM/SIGKILL escalation sequence, and zombie-reaping mechanism?
FAILURE_SCENARIO:
  - A browser tab crashes while FlowKit is awaiting DOM generation completion. FlowKit's Python process hangs indefinitely without closing its WebSocket connection. The bridge times out, but FlowKit remains running as a zombie process holding port 8000 and locking its SQLite database. Subsequent generation requests fail with port collision or database locked errors, causing an unrecoverable worker outage.
WHY_IT_MATTERS:
  - Without a deterministic process supervision model, Track B (FlowKit bridge) cannot satisfy INV-005 and INV-019 (worker crash recoverability without canonical queue loss).
PROPOSED_SOLUTION:
  - Adopt a Supervised Sidecar Daemon Architecture for Track B:
    1. Standard Execution Model: FlowKit is managed as an isolated sidecar process/container managed via a dedicated Process Supervisor abstraction (supporting both Docker Compose sidecar in production/CI and a Managed Subprocess Controller in local development).
    2. Dynamic Port & Profile Isolation: The bridge assigns dynamic ephemeral loopback ports (or Unix domain sockets) and isolated temporary Chrome profile directories (`--user-data-dir=/tmp/avf-flowkit-$JOB_ID`) per worker instance.
    3. Active Liveness & Readiness Probing: The bridge implements a strict 5-second polling health check against FlowKit's `/health` endpoint and WebSocket ping/pong.
    4. Controlled Lifecycle Sequence:
       - On Job Start: Probe `/health`; if dead, spawn with PID registration and lease deadline.
       - On Hang / Timeout: Bridge sends `SIGTERM`, waits 5 seconds, escalates to `SIGKILL`, reaps PID, removes stale socket/lock files, and emits normalized `TRANSIENT_BROWSER` error.
       - On Teardown: Clean up ephemeral SQLite and temporary Chrome cache.
ALTERNATIVES_CONSIDERED:
  - Option 1 (Embedded In-Process Python): Embed FlowKit directly inside the bridge process. (Rejected: Fatal memory corruption or unhandled exception in FlowKit would crash the bridge; violates boundary isolation).
  - Option 2 (Unmanaged External OS Daemon): Assume FlowKit is manually launched by the operator before starting AVF. (Rejected: Unreliable for automated CI/CD and multi-worker execution).
CAPABILITY_IMPACT:
  - Preserves 100% of Track B acceleration capability while converting an unreliable prototype integration into an enterprise-grade resilient service.
COMPATIBILITY_IMPACT:
  - Upstream `FlowExecutionPort` remains completely unchanged (INV-020 preserved).
MIGRATION_IMPACT:
  - Requires implementing the Process Supervisor controller in `avf-flowkit-bridge` during Phase 0/Phase 1.
TEST_OR_BENCHMARK_REQUIRED:
  - Chaos injection test: SIGKILL FlowKit process mid-generation and assert bridge recovers within 10 seconds, reports `TRANSIENT_BROWSER`, and successfully handles next command.
RESIDUAL_RISK:
  - OS-specific differences in process signal handling (macOS vs. Linux vs. Windows).
CONFIDENCE:
  - High (99%) — standard site reliability engineering pattern for legacy/third-party process bridging.

---

### Finding F-R13-002: Upstream FlowKit Supply-Chain Risk, Vendoring, Mirroring, and License Attribution Governance

FINDING_ID: F-R13-002
ROLE: R13_OSS
SEVERITY: HIGH
CATEGORY: SUPPLY_CHAIN
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/08_evidence/SOURCE_LEDGER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
AFFECTED_CONTRACTS:
  - API_COMPATIBILITY_POLICY.md
EVIDENCE:
  - SOURCE_LEDGER.md (Lines 18-20) cites `https://github.com/crisng95/flowkit` as MIT license.
  - R10_FLOWKIT_BRIDGE.md (Line 51) lists "FlowKit pinned release/commit" as a dependency.
  - However, no formal specification exists governing:
    1. Upstream repo mirroring and immutability (what happens if the GitHub repo is deleted or re-licensed?).
    2. Transitive dependency license compliance (FlowKit's Python and NPM packages may contain copyleft or non-commercial licenses).
    3. Mandatory MIT copyright notice preservation and attribution bundling in AVF distributions.
    4. Clean-room boundary ensuring reverse-engineered Google private endpoint schemas in FlowKit do not create legal/contractual liability in AVF.
FAILURE_SCENARIO:
  - Upstream maintainer pushes a malicious update or re-licenses FlowKit to AGPLv3. During automated CI container builds, unpinned dependency fetching pulls the new version, triggering compliance violations and security vulnerabilities.
WHY_IT_MATTERS:
  - Supply-chain poisoning or license contamination in privileged local execution components threatens the commercial viability and security of the entire platform.
PROPOSED_SOLUTION:
  - Implement an Immutable OSS Ingestion and Compliance Policy:
    1. Internal Mirror & Pinning: FlowKit source must be cloned into an internal organizational mirror repository (`avf-vendor/flowkit`) and pinned to an exact immutable commit SHA-256 hash.
    2. Automated License & CVE Gate: Run FOSSA / `pip-licenses` / `license-checker` against FlowKit and all transitive dependencies to guarantee 100% MIT/Apache/BSD/ISC license compatibility.
    3. Legal Attribution Pack: Include FlowKit's MIT license notice in `THIRD_PARTY_LICENSES.md` generated during container builds.
    4. Clean-Room Protocol Isolation: `avf-flowkit-bridge` communicates exclusively over localhost HTTP/WS; zero FlowKit source code or Python modules may be imported directly into other AVF repositories.
ALTERNATIVES_CONSIDERED:
  - Direct Git Submodule from upstream GitHub: (Rejected: Vulnerable to upstream deletion, forced force-pushes, or commit rewrites).
CAPABILITY_IMPACT:
  - Zero loss of capability; establishes supply-chain sovereignty and reproducibility.
COMPATIBILITY_IMPACT:
  - Fully transparent to all upstream services.
MIGRATION_IMPACT:
  - Create `avf-vendor/flowkit` mirror repository and add license validation script to CI.
TEST_OR_BENCHMARK_REQUIRED:
  - CI verification test that blocks builds if upstream commit SHA does not match pinned hash in `COMPATIBILITY.yaml` or if unauthorized licenses are detected.
RESIDUAL_RISK:
  - Upstream FlowKit changes may diverge from our pinned fork, requiring manual maintenance if Track B is retained long-term.
CONFIDENCE:
  - High (95%).

---

### Finding F-R13-003: FFmpeg Copyleft / GPL Viral Licensing Risk in Media and QC Processing Services

FINDING_ID: F-R13-003
ROLE: R13_OSS
SEVERITY: HIGH
CATEGORY: LEGAL_LICENSING
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R12_MEDIA.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json
  - DEPENDENCY_GRAPH.md
EVIDENCE:
  - R12_MEDIA.md (Lines 16, 57) specifies "FFmpeg wrappers" and dependency on "FFmpeg/ffprobe".
  - R11_QC.md (Lines 56, 105) specifies "media decoding tools" and "ffprobe/decode/duration/resolution checks".
  - The specification does not define whether FFmpeg is invoked via external CLI binary execution or via linked runtime libraries (e.g. `libavcodec`, `PyAV`, C-FFI bindings).
  - FFmpeg compiled with `libx264`, `libx265`, or `--enable-gpl` falls under GPL v2.0+ or GPL v3.0+. Linking against GPL FFmpeg shared/static libraries dynamically infects the hosting application with GPL copyleft requirements.
FAILURE_SCENARIO:
  - An engineering agent writes `avf-media` using Python `PyAV` or Node.js native C++ addons linked against a system GPL FFmpeg library. Under GPL terms, `avf-media` and any statically/dynamically coupled AVF services become derivative works subject to mandatory GPL open-sourcing.
WHY_IT_MATTERS:
  - Unintended GPL contamination creates legal and IP risks for commercial deployment of AVF.
PROPOSED_SOLUTION:
  - Formalize FFmpeg Integration & Licensing Architectural Standard:
    1. Decoupled CLI Subprocess Execution Only: Mandate that `avf-media` and `avf-qc` interact with FFmpeg/ffprobe strictly via CLI process invocation (`execFile`/`subprocess.run` with parameterized argument arrays) over standard OS process boundaries. Prohibit direct C-linkage, FFI, or in-process shared library loading (`libav*`).
    2. Base Image Build Standard: Container base images must use standard FFmpeg builds where CLI binaries execute in independent process memory spaces.
    3. Update `DEPENDENCY_GRAPH.md`: Add explicit forbidden dependency rule: `avf-media / avf-qc -> GPL in-process linked C-libraries`.
ALTERNATIVES_CONSIDERED:
  - Pure LGPL-only FFmpeg build without GPL codecs: (Considered, but limits support for advanced codecs like H.264/H.265 encoding in postproduction; CLI process separation solves the legal constraint without sacrificing codec capability).
CAPABILITY_IMPACT:
  - Full FFmpeg video processing, probe, normalization, and assembly capabilities are preserved without legal risk.
COMPATIBILITY_IMPACT:
  - None. Internal implementation detail of `R11_QC` and `R12_MEDIA`.
MIGRATION_IMPACT:
  - Enforce subprocess execution pattern in repository agent implementation rules.
TEST_OR_BENCHMARK_REQUIRED:
  - Unit/Integration test validating FFmpeg CLI wrapper timeout, error capture, and process exit code normalization.
RESIDUAL_RISK:
  - Slight CLI process spawn overhead (typically <10ms per probe/transcode invocation), negligible compared to video processing durations.
CONFIDENCE:
  - High (99%) — standard industry practice for compliant FFmpeg integration.

---

### Finding F-R13-004: Lack of System-Wide Dependency Pinning, Cryptographic Lockfiles, and SBOM Policy

FINDING_ID: F-R13-004
ROLE: R13_OSS
SEVERITY: MEDIUM
CATEGORY: SECURITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/00_governance/
AFFECTED_CONTRACTS:
  - API_COMPATIBILITY_POLICY.md
EVIDENCE:
  - Blueprints across R01-R15 specify technologies (PostgreSQL, Redis, Temporal, Playwright, OpenTelemetry, React, FastAPI, etc.) but lack a mandatory policy for:
    1. Strict version pinning and lockfile enforcement (`package-lock.json`, `poetry.lock`, `requirements.txt` with SHA-256 hashes).
    2. Mandatory Software Bill of Materials (SBOM) generation (CycloneDX / SPDX).
    3. Automated CVE / vulnerability scanning in CI.
    4. Prohibited license policy (e.g. AGPLv3, SSPL, Commons Clause, Non-Commercial CC-BY-NC).
FAILURE_SCENARIO:
  - A transient dependency of an NPM or Python package is compromised (supply-chain attack) or releases a breaking minor version on package registries. Unpinned builds fetch the compromised package during automated CI/CD deployment, resulting in credential exfiltration or broken production builds.
WHY_IT_MATTERS:
  - Polyrepo architectures multiply supply-chain exposure across 15 repositories. Without uniform governance, dependencies drift rapidly.
PROPOSED_SOLUTION:
  - Establish a Canonical Supply Chain & Dependency Governance Standard in `04_integration/SECURITY_MODEL.md`:
    1. Lockfile Immutability: Every repository must commit an exact lockfile. CI builds must run `npm ci` or `poetry install --frozen` (or equivalent) and fail if lockfiles are missing or out of sync.
    2. Hash Verification: Python requirements must enforce `--require-hashes` or poetry hash verification.
    3. Automated Vulnerability Gate: CI pipelines must execute automated dependency audits (`pip-audit`, `npm audit`, Trivy/Trivy-operator) with zero-tolerance for unresolved Critical/High CVEs.
    4. Automated License Linter: CI must enforce an allowlist: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, PostgreSQL, PSF. Build must fail on AGPL, SSPL, or unapproved copyleft licenses.
    5. SBOM Generation: Every release build must generate a CycloneDX JSON SBOM artifact.
ALTERNATIVES_CONSIDERED:
  - Ad-hoc per-repo dependency management. (Rejected: Inevitably leads to version drift and supply chain vulnerabilities).
CAPABILITY_IMPACT:
  - Significantly improves system stability and operational security with zero reduction in functionality.
COMPATIBILITY_IMPACT:
  - None on public contracts.
MIGRATION_IMPACT:
  - Add standard GitHub Actions / CI workflow templates for lockfile and vulnerability checking to `09_agent_packets`.
TEST_OR_BENCHMARK_REQUIRED:
  - CI test verifying dependency check failure when a dummy vulnerable or AGPL-licensed package is introduced.
RESIDUAL_RISK:
  - Maintenance overhead of periodic security patch bumps.
CONFIDENCE:
  - High (99%).

---

### Finding F-R13-005: AI Orchestration Framework Encapsulation Boundary (LangGraph / LangChain Dependency Churn)

FINDING_ID: F-R13-005
ROLE: R13_OSS
SEVERITY: MEDIUM
CATEGORY: ARCHITECTURE
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-008_WORKFLOW_ENGINE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R03_CREATIVE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json
  - event-envelope.schema.json
EVIDENCE:
  - ADR-008 states: "Use a Temporal-class durable workflow engine for operational sequencing; LangGraph only for bounded AI workflows."
  - Python AI orchestration packages (LangChain, LangGraph, LlamaIndex) have frequent breaking changes, high dependency bloat, and rapid API churn.
  - The blueprint kit does not explicitly mandate that AI framework internal data structures must be strictly encapsulated within `avf-creative` and `avf-prompt-compiler`.
FAILURE_SCENARIO:
  - An implementation agent models prompt generation by returning LangGraph `BaseMessage` or graph state dictionaries directly as payload fields in workflow activities. An upstream LangGraph upgrade changes message serialization, causing persistent workflow replay failures in Temporal and schema rejection in `avf-core-state`.
WHY_IT_MATTERS:
  - Violates the core principle that external libraries must not dictate canonical AVF domain contracts.
PROPOSED_SOLUTION:
  - Add Strict AI Framework Encapsulation Rule to `R03_CREATIVE`, `R05_PROMPT_COMPILER`, and `R06_WORKFLOW`:
    1. Zero Framework Leakage: LangGraph / LangChain types must never cross repository boundaries, be stored in PostgreSQL, or appear in event payloads.
    2. Boundary Translation: All outputs from LangGraph chains must be parsed and strictly validated into released `avf-contracts` (e.g. `PromptVersion`, `ScriptVersion`, `CreativeSpecVersion`) using Pydantic / Ajv before leaving the service.
    3. Direct SDK Fallback: For simple deterministic prompt compilation, prefer direct vendor SDKs (e.g. `google-genai`, `anthropic`, `openai`) over heavyweight orchestrators to minimize dependency bloat.
ALTERNATIVES_CONSIDERED:
  - Permitting LangGraph state persistence in workflow memory. (Rejected: Violates INV-004 and INV-014).
CAPABILITY_IMPACT:
  - Full support for multi-step creative generation while ensuring bulletproof contract isolation.
COMPATIBILITY_IMPACT:
  - Guarantees strict compatibility across all versions.
MIGRATION_IMPACT:
  - Standardized boundary mapping classes in `R03` and `R05`.
TEST_OR_BENCHMARK_REQUIRED:
  - Contract serialization tests ensuring no third-party framework classes exist in exported JSON schemas.
RESIDUAL_RISK:
  - Internal refactoring required if LangGraph APIs change, but isolated strictly inside R03/R05.
CONFIDENCE:
  - High (95%).

---

### Finding F-R13-006: Playwright & Browser Automation Binary Ingestion, Hermetic CI, and Sandboxing Governance

FINDING_ID: F-R13-006
ROLE: R13_OSS
SEVERITY: MEDIUM
CATEGORY: SUPPLY_CHAIN
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09A_R10_GOOGLE_FLOW_EXECUTION_OPTIONS.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/PHASE_0_BENCHMARK.md
AFFECTED_CONTRACTS:
  - FlowExecutionPort (browser-command.schema.json)
EVIDENCE:
  - R09_BROWSER_WORKER.md and Option A3 in R09A rely on Playwright and persistent browser automation contexts.
  - Playwright downloads arbitrary binary browser builds from public Microsoft CDNs during package installation (`npx playwright install`).
  - In air-gapped CI, containerized production environments, or secure developer environments, unpinned dynamic binary downloads can fail or present supply-chain risks.
FAILURE_SCENARIO:
  - A CI runner or worker container spins up in an environment with restricted external CDN access. `playwright install` fails, or pulls a new Chromium major version that alters DOM rendering / selector behaviour, breaking benchmark runs unexpectedly.
WHY_IT_MATTERS:
  - Reproducibility of browser automation depends directly on pinning exact browser binary versions and ensuring hermetic deployment.
PROPOSED_SOLUTION:
  - Specify Browser Binary & Environment Isolation Standards:
    1. Pre-Baked Container Images: Production and CI container images for `avf-browser-worker` must use official, verified base images (e.g. `mcr.microsoft.com/playwright:vX.Y.Z-focal`) with pre-installed, checksummed browser binaries.
    2. Pinned Browser Revision: `COMPATIBILITY.yaml` in `avf-browser-worker` must explicitly pin the exact Chromium/Chrome revision and Playwright driver version.
    3. User Data Directory Sandboxing: Ensure persistent context directories are created in isolated temporary mounts (`/tmp/playwright-profiles/$JOB_ID`) with secure POSIX permissions (0700) to protect session credentials.
ALTERNATIVES_CONSIDERED:
  - Runtime dynamic browser installation. (Rejected: Flaky in production and CI).
CAPABILITY_IMPACT:
  - Reliable, deterministic browser execution across Track A options.
COMPATIBILITY_IMPACT:
  - None.
MIGRATION_IMPACT:
  - Standardized Dockerfile for `avf-browser-worker`.
TEST_OR_BENCHMARK_REQUIRED:
  - Hermetic CI build test verifying container starts and executes automation without external network access for binary downloads.
RESIDUAL_RISK:
  - Chrome version drift relative to live Google Flow web changes (addressed by Phase 0 benchmark and selector abstraction layers).
CONFIDENCE:
  - High (95%).

---

### Finding F-R13-007: Incomplete Forbidden Dependency Matrix for External OSS Engines in DEPENDENCY_GRAPH.md

FINDING_ID: F-R13-007
ROLE: R13_OSS
SEVERITY: MEDIUM
CATEGORY: ARCHITECTURE
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/DEPENDENCY_GRAPH.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md
AFFECTED_CONTRACTS:
  - DEPENDENCY_GRAPH.md
EVIDENCE:
  - DEPENDENCY_GRAPH.md (Lines 40-48) enumerates 7 forbidden dependencies:
    - Creative -> Google Flow Adapter
    - Asset Service -> Browser Worker
    - Prompt Compiler -> FlowKit model/database
    - QC -> browser selectors
    - Browser Worker -> Core database
    - FlowKit Bridge -> Core database
    - Operator Console -> provider-specific database
  - While these 7 are correct, the matrix omits several critical OSS/third-party isolation rules that are essential to enforce our foundational axiom.
FAILURE_SCENARIO:
  - A developer connects `avf-operator-console` directly to FlowKit's local WebSocket for diagnostic monitoring, or links `avf-core-state` directly to third-party provider SDKs, bypassing `avf-provider-sdk`. The system suffers architectural degradation and tight coupling to external tools.
WHY_IT_MATTERS:
  - `DEPENDENCY_GRAPH.md` is the primary architectural linting rulebook for automated dependency scanners and coding agents.
PROPOSED_SOLUTION:
  - Expand the "Forbidden dependencies" section in `04_integration/DEPENDENCY_GRAPH.md` to include:
    - `FlowKit Bridge -> Core database` (Already listed)
    - `Prompt Compiler -> FlowKit model/database` (Already listed)
    - `Operator Console -> FlowKit / Browser Worker direct connection` (Must route via Core API / Observability)
    - `Core API / State -> FlowKit / Browser Worker / Provider SDK direct connection` (Must route via Workflow Orchestrator)
    - `Workflow Orchestrator -> FlowKit Bridge direct dependency` (Must route via Provider SDK -> Google Flow Adapter)
    - `Media / QC Services -> GPL in-process linked dynamic C-libraries` (Must use CLI subprocess or network boundary)
    - `Core Contracts -> Third-party framework proprietary classes` (Must be pure JSON Schema / Pydantic models)
ALTERNATIVES_CONSIDERED:
  - Rely on code review alone. (Rejected: Architectural rules must be explicitly codified in the specification).
CAPABILITY_IMPACT:
  - Enforces rock-solid architectural hygiene with zero negative impact on system capabilities.
COMPATIBILITY_IMPACT:
  - Strengthens system modularity and multi-repo decoupling.
MIGRATION_IMPACT:
  - Update `DEPENDENCY_GRAPH.md` text and add corresponding dependency-cruiser / ESLint / import-linter rules.
TEST_OR_BENCHMARK_REQUIRED:
  - Automated CI dependency-cruiser rule verification in `R15_INTEGRATION_HARNESS`.
RESIDUAL_RISK:
  - None.
CONFIDENCE:
  - High (99%).

---

## 5. Classification: Proven Defects vs. Uncertainties Needing Spikes

To maintain rigorous distinction between immediate architectural requirements and items requiring Phase 0 empirical testing:

| ITEM / TOPIC | CLASSIFICATION | RATIONALE & RECOMMENDED ACTION |
|---|---|---|
| **FlowKit Process Supervision Architecture (F-R13-001 / GAP-008)** | **PROVEN SPECIFICATION DEFECT** | Must be formally defined before v1.0 freeze. The blueprint cannot leave process spawning, PID tracking, port allocation, and crash recovery unstated. |
| **FFmpeg GPL Copyleft Separation (F-R13-003)** | **PROVEN SPECIFICATION DEFECT** | Must be codified in blueprints before implementation agents write code linking GPL C-libraries. |
| **Supply Chain & Lockfile Governance (F-R13-004)** | **PROVEN SPECIFICATION DEFECT** | System-wide policy required in `04_integration/SECURITY_MODEL.md` before Phase 1 build. |
| **Forbidden Dependency Matrix Expansion (F-R13-007)** | **PROVEN SPECIFICATION DEFECT** | Codify all OSS and external isolation boundaries in `DEPENDENCY_GRAPH.md`. |
| **FlowKit WebSocket Reconnect Latency vs. Track A** | **UNCERTAINTY NEEDING SPIKE** | Phase 0 benchmark protocol must measure control-plane latency and reconnection overhead between Track A and Track B under simulated worker crashes. |
| **FlowKit SQLite Lock Contention under Concurrency** | **UNCERTAINTY NEEDING SPIKE** | Phase 0 spike to measure whether FlowKit SQLite encounters database locking when multiple browser commands are queued. |
| **Playwright Dedicated Profile Session Longevity** | **UNCERTAINTY NEEDING SPIKE** | Phase 0 benchmark to verify how long Google Flow authentication persists in dedicated Playwright profiles vs. MV3 Chrome extension profiles. |

---

## 6. Protection of System Capabilities

A key principle of the Council Charter is to **avoid reducing system capability solely to avoid hard engineering**:

1. **Retaining Dual-Track Capability (Track A & Track B):**
   - The dual-track strategy (ADR-004) must NOT be abandoned to simplify integration. Track B (FlowKit bridge) provides immediate acceleration and reference baseline capabilities for Phase 0, while Track A provides long-term platform ownership and packaging control.
   - The solutions proposed in `F-R13-001` and `F-R13-002` solve the supervision and licensing challenges of FlowKit cleanly without removing Track B.
2. **Preserving Full FFmpeg Media Capabilities:**
   - Rather than crippling `avf-media` by banning advanced video codecs (H.264, H.265, AAC), `F-R13-003` utilizes standard decoupled CLI process invocation, enabling full codec support while maintaining 100% legal compliance.
3. **Preserving AI Creative Exploration:**
   - Rather than forbidding modern AI orchestration tools, `F-R13-005` establishes clear encapsulation boundaries, allowing rich multi-agent creative reasoning in `avf-creative` while shielding the workflow core and database from dependency churn.

---

## 7. Residual Uncertainties

1. **Upstream FlowKit Longevity:**
   - As an independent OSS repository, FlowKit maintainers may cease updating the project as Google Flow web UI evolves.
   - *Mitigation:* The clean boundary on `FlowExecutionPort` guarantees that Track B can be deprecated and decommissioned at any time without impacting any core contracts or workflows.
2. **Google Flow Terms of Service & Web Evolution:**
   - Any browser-based automation is subject to provider UI changes and anti-abuse updates.
   - *Mitigation:* Handled via ADR-007 (treating challenges as blocked operator states) and Phase 0 failure criteria (switching to supported commercial API providers if UI automation reliability drops below agreed thresholds).

---

## 8. Official Review Sign-Off

- **Reviewer Role:** `R13_OSS` (OSS / Dependency / Licensing Reviewer)
- **Model:** `gemini-2.5-pro` (DeepMind Agentic Engine)
- **Round:** C01 Independent Blind Review
- **Skill Versions:**
  - `modern-web-guidance`: v1.0.0
  - `chrome-extensions`: v1.0.0
  - `chrome-devtools`: v1.0.0
- **Session / Conversation ID:** `1df69d95-cadb-43c4-9b5e-c2b6f237217e`
- **Timestamp:** `2026-08-15T11:30:00+07:00`
- **Approval Status:** Review Submitted (I do not approve my own proposed changes; submitted to Council Consolidation).
