#!/usr/bin/env python3
"""
Generates the 5-prompt pattern for all 15 repositories (75 prompt markdown files)
for AVF_OPERATOR_RUNBOOK_v1.0.0.
"""

import os

RUNBOOK_DIR = "/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0"

REPOS_CONFIG = [
    {
        "id": "R01",
        "prefix": "R01",
        "dir": "02_R01_CONTRACTS",
        "name": "R01_contracts",
        "display_name": "Contracts & Typed Schemas",
        "layer": "Layer 0",
        "phase": "02_R01_CONTRACTS",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R01_CONTRACTS.md",
        "contracts": [
            "02_contracts/domain-entities.schema.json",
            "02_contracts/event-envelope.schema.json",
            "02_contracts/provider-request.schema.json",
            "02_contracts/provider-result.schema.json",
            "02_contracts/browser-command.schema.json",
            "02_contracts/flow-execution-result.schema.json"
        ],
        "allowed_deps": "None (Pure schemas, types, validators)",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, Direct DB",
        "owns": "JSON Schemas, automated TypeScript type generation (json-schema-to-typescript), positive & negative fixture suites (>=3 each), FlowExecutionPort conformance test suite",
        "does_not_own": "Runtime execution, database connections, UI components, external network calls",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/15_R14_OBSERVABILITY/R14_01_PLAN.md",
        "prereq_plan": "PROV-03",
        "specific_guidance": "Read 05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md. Standardize $defs, represent all 17 normative execution stages, strongly-type discriminated unions for FlowExecutionResult 10 operations, produce positive and negative fixture test suites."
    },
    {
        "id": "R14",
        "prefix": "R14",
        "dir": "15_R14_OBSERVABILITY",
        "name": "R14_platform_observability",
        "display_name": "Observability, Telemetry & Security",
        "layer": "Cross-Cutting",
        "phase": "15_R14_OBSERVABILITY",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md",
        "contracts": ["02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "OpenTelemetry tracing SDK wrapper, correlation context propagation, secret & token redaction engine, structured log formatter, Prometheus metrics exporter",
        "does_not_own": "Domain persistence, business logic, workflow execution, provider calls",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/03_R02_CORE_STATE/R02_01_PLAN.md",
        "prereq_plan": "R01-04",
        "specific_guidance": "Zero secrets in logs. Automated redaction filter for Bearer tokens, cookies, passwords. Distributed trace context injection and W3C traceparent propagation."
    },
    {
        "id": "R02",
        "prefix": "R02",
        "dir": "03_R02_CORE_STATE",
        "name": "R02_core_state",
        "display_name": "Core State & Persistence Engine",
        "layer": "Layer 1",
        "phase": "03_R02_CORE_STATE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R02_CORE_STATE.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15",
        "owns": "PostgreSQL schema migrations, Prisma/Drizzle models, GenerationJob state machine, 17 execution stages, Idempotency store, entity CRUD API",
        "does_not_own": "Temporal workflow execution, video generation, browser automation, creative script generation",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/04_R07_PROVIDER_SDK/R07_01_PLAN.md",
        "prereq_plan": "R14-04",
        "specific_guidance": "Enforce INV-001 through INV-012. Deterministic state transitions, idempotency key uniqueness, sole owner of PostgreSQL connection."
    },
    {
        "id": "R07",
        "prefix": "R07",
        "dir": "04_R07_PROVIDER_SDK",
        "name": "R07_provider_sdk",
        "display_name": "Provider Neutral SDK & FakeProvider",
        "layer": "Layer 3",
        "phase": "04_R07_PROVIDER_SDK",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R07_PROVIDER_SDK.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "VideoProvider interface abstraction, capability matrix parser, normalized 9-error taxonomy, FakeVideoProvider with full simulation matrix",
        "does_not_own": "PostgreSQL persistence, Google Flow specific automation, Temporal workflows",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md",
        "prereq_plan": "R02-04",
        "specific_guidance": "FakeVideoProvider must support success(0s), success(30s), fail_transient(2), fail_provider, rate_limit, timeout, status_unknown, corrupt_output."
    },
    {
        "id": "R06",
        "prefix": "R06",
        "dir": "05_R06_WORKFLOW",
        "name": "R06_workflow",
        "display_name": "Temporal Workflow Orchestrator",
        "layer": "Layer 5",
        "phase": "05_R06_WORKFLOW",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R06_WORKFLOW.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json", "02_contracts/provider-request.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state, R03_creative, R04_assets_continuity, R05_prompt_compiler, R07_provider_sdk, R08_google_flow_adapter, R11_qc, R12_media, R14_platform_observability",
        "forbidden_deps": "R09, R10, Direct DB",
        "owns": "Temporal workflow definitions (SingleShot, MultiShot, RenderPipeline), retry policy engine, activity handlers, reconciliation logic",
        "does_not_own": "Database tables directly, browser automation, raw video rendering, UI rendering",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/06_R15_INTEGRATION_HARNESS/R15_01_PLAN.md",
        "prereq_plan": "GATE-00",
        "specific_guidance": "Temporal replay safety, deterministic workflows, exponential backoff with jitter, idempotency token persistence, crash/reconciliation."
    },
    {
        "id": "R15",
        "prefix": "R15",
        "dir": "06_R15_INTEGRATION_HARNESS",
        "name": "R15_integration_harness",
        "display_name": "End-to-End Integration & Scenario Test Harness",
        "layer": "Cross-Cutting",
        "phase": "06_R15_INTEGRATION_HARNESS",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R15_INTEGRATION_HARNESS.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json", "02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json", "02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14",
        "forbidden_deps": "Direct production DB mutation",
        "owns": "16 chaos/fault-injection scenarios, E2E test runner, offline test orchestration, golden test fixture assertions",
        "does_not_own": "Production runtime services, application logic",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Gemini 3.1 Pro High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_01_FAKEPROVIDER_E2E_GATE.md",
        "prereq_plan": "R06-04",
        "specific_guidance": "Implement 16 fault-injection scenarios: worker kill before/after submit, uncertain ack, duplicate delivery, provider timeout, browser disconnect, corrupted video output, budget block."
    },
    {
        "id": "R08",
        "prefix": "R08",
        "dir": "07_R08_GOOGLE_FLOW_ADAPTER",
        "name": "R08_google_flow_adapter",
        "display_name": "Google Flow Provider Adapter",
        "layer": "Layer 3",
        "phase": "07_R08_GOOGLE_FLOW_ADAPTER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/provider-result.schema.json", "02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R07_provider_sdk, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, Direct DB",
        "owns": "Google Flow adapter implementing VideoProvider interface, FlowExecutionPort client caller, prompt/aspect translation",
        "does_not_own": "Direct browser automation code, WebSocket network parsing, database access",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/08_R10_FLOWKIT_BRIDGE/R10_01_PLAN.md",
        "prereq_plan": "GATE-01",
        "specific_guidance": "Decouple provider logic from execution tracks via 10-operation FlowExecutionPort abstraction."
    },
    {
        "id": "R10",
        "prefix": "R10",
        "dir": "08_R10_FLOWKIT_BRIDGE",
        "name": "R10_flowkit_bridge",
        "display_name": "Track B Direct FlowKit Bridge",
        "layer": "Layer 4",
        "phase": "08_R10_FLOWKIT_BRIDGE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md",
        "contracts": ["02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R11, R12, R13, Direct DB",
        "owns": "Direct HTTP/WebSocket protocol client implementing 10-operation FlowExecutionPort",
        "does_not_own": "Browser automation, DOM interaction, database state, workflow logic",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/09_R09_BROWSER_WORKER/R09_01_PLAN.md",
        "prereq_plan": "R08-04",
        "specific_guidance": "10-op port conformance, session maintenance, token refresh, normalized error mapping."
    },
    {
        "id": "R09",
        "prefix": "R09",
        "dir": "09_R09_BROWSER_WORKER",
        "name": "R09_browser_worker",
        "display_name": "Track A Browser Automation Worker",
        "layer": "Layer 4",
        "phase": "09_R09_BROWSER_WORKER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R09_BROWSER_WORKER.md",
        "contracts": ["02_contracts/browser-command.schema.json", "02_contracts/flow-execution-result.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R10, R11, R12, R13, Direct DB",
        "owns": "Playwright/CDP automation implementing 10-operation FlowExecutionPort, 4-tier selector resolution (DOM, A11y, Visual, Agent Recovery), anti-abuse safety",
        "does_not_own": "Direct DB, direct API bridge, workflow state",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.1 Pro High",
        "accept_model": "Claude Opus 4.6 Thinking",
        "accept_conv": "NEW_REQUIRED",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_02_FLOW_EXECUTION_PORT_CONFORMANCE_GATE.md",
        "prereq_plan": "R10-04",
        "specific_guidance": "Strict anti-abuse safety, human gate escalation on CAPTCHA/challenge, session isolation."
    },
    {
        "id": "R03",
        "prefix": "R03",
        "dir": "10_R03_CREATIVE",
        "name": "R03_creative",
        "display_name": "Creative & Script Generation Engine",
        "layer": "Layer 2",
        "phase": "10_R03_CREATIVE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R03_CREATIVE.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R14_platform_observability",
        "forbidden_deps": "R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "LLM-assisted story/scene decomposition service, scene parsing, creative structured outputs",
        "does_not_own": "Database persistence, video rendering, browser execution",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/11_R04_ASSETS_CONTINUITY/R04_01_PLAN.md",
        "prereq_plan": "GATE-02",
        "specific_guidance": "Strict JSON schema enforcement on LLM outputs, deterministic fallback parsers."
    },
    {
        "id": "R04",
        "prefix": "R04",
        "dir": "11_R04_ASSETS_CONTINUITY",
        "name": "R04_assets_continuity",
        "display_name": "Assets & Character Continuity Service",
        "layer": "Layer 2",
        "phase": "11_R04_ASSETS_CONTINUITY",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R04_ASSETS_CONTINUITY.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R14_platform_observability",
        "forbidden_deps": "R03, R05, R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "Asset catalog service, character reference embedding management, continuity token injection",
        "does_not_own": "Database persistence, video generation, workflow orchestration",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/12_R05_PROMPT_COMPILER/R05_01_PLAN.md",
        "prereq_plan": "R03-04",
        "specific_guidance": "Character reference consistency across multi-shot sequences."
    },
    {
        "id": "R05",
        "prefix": "R05",
        "dir": "12_R05_PROMPT_COMPILER",
        "name": "R05_prompt_compiler",
        "display_name": "Provider-Aware Prompt Compiler",
        "layer": "Layer 2",
        "phase": "12_R05_PROMPT_COMPILER",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R05_PROMPT_COMPILER.md",
        "contracts": ["02_contracts/provider-request.schema.json", "02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R04_assets_continuity (API), R14_platform_observability",
        "forbidden_deps": "R06, R07, R08, R09, R10, R11, R12, R13, R15, Direct DB",
        "owns": "Prompt template compiler, dialect transformations (Veo, Luma, Runway syntax), negative prompt rules, safety filters",
        "does_not_own": "Direct video generation, storage, database",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/13_R11_QC/R11_01_PLAN.md",
        "prereq_plan": "R04-04",
        "specific_guidance": "Deterministic prompt compilation, dialect rule engine, token substitution."
    },
    {
        "id": "R11",
        "prefix": "R11",
        "dir": "13_R11_QC",
        "name": "R11_qc",
        "display_name": "Quality Control & Validation Service",
        "layer": "Layer 2",
        "phase": "13_R11_QC",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R11_QC.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R12, R13, Direct DB",
        "owns": "Technical QC (FFprobe container, stream, resolution, framerate, duration check), Semantic QC (LLM/Vision scoring), bounded retry decision output",
        "does_not_own": "Database persistence, video stitching, video generation",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/14_R12_MEDIA/R12_01_PLAN.md",
        "prereq_plan": "R05-04",
        "specific_guidance": "Fast technical inspection before expensive semantic evaluation, quarantine DLQ."
    },
    {
        "id": "R12",
        "prefix": "R12",
        "dir": "14_R12_MEDIA",
        "name": "R12_media",
        "display_name": "Media Processing & Assembly Service",
        "layer": "Layer 2",
        "phase": "14_R12_MEDIA",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R12_MEDIA.md",
        "contracts": ["02_contracts/domain-entities.schema.json"],
        "allowed_deps": "R01_contracts, R14_platform_observability",
        "forbidden_deps": "R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R13, Direct DB",
        "owns": "FFmpeg stitching, audio track overlay, color normalization, video transcoding, final packaging",
        "does_not_own": "Database persistence, generation workflows",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_03_CREATIVE_MEDIA_GATE.md",
        "prereq_plan": "R11-04",
        "specific_guidance": "Safe subprocess invocation, deterministic transcoding parameters."
    },
    {
        "id": "R13",
        "prefix": "R13",
        "dir": "16_R13_OPERATOR_CONSOLE",
        "name": "R13_operator_console",
        "display_name": "Human-in-the-Loop Operator Console",
        "layer": "Layer 5",
        "phase": "16_R13_OPERATOR_CONSOLE",
        "blueprint": "01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R13_OPERATOR_CONSOLE.md",
        "contracts": ["02_contracts/domain-entities.schema.json", "02_contracts/event-envelope.schema.json"],
        "allowed_deps": "R01_contracts, R02_core_state (API), R06_workflow (API), R14_platform_observability",
        "forbidden_deps": "R03, R04, R05, R07, R08, R09, R10, R11, R12, R15, Direct DB, Worker Internals",
        "owns": "Operator UI web application for human approval gates, generation inspection, error triage, DLQ replay triggers",
        "does_not_own": "Direct database mutations, worker execution internals",
        "plan_model": "Gemini 3.7 Flash High",
        "impl_model": "Gemini 3.7 Flash High",
        "review_model": "Gemini 3.7 Flash High",
        "accept_model": "Gemini 3.7 Flash High",
        "accept_conv": "NEW_OR_EXISTING",
        "pass_after_accept": "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_04_SYSTEM_INTEGRATION_GATE.md",
        "prereq_plan": "GATE-03",
        "specific_guidance": "Web UI interacting strictly via R02 Core State REST/gRPC and R06 Temporal client APIs."
    }
]

def generate_repo_suite(repo):
    p_id = repo["id"]
    p_dir = repo["dir"]
    name = repo["name"]
    disp = repo["display_name"]
    layer = repo["layer"]
    phase = repo["phase"]
    bp = repo["blueprint"]
    owns = repo["owns"]
    not_owns = repo["does_not_own"]
    allowed_deps = repo["allowed_deps"]
    forbidden_deps = repo["forbidden_deps"]
    guidance = repo["specific_guidance"]
    
    # 01 PLAN
    plan_id = f"{p_id}-01"
    plan_path = f"{p_dir}/{p_id}_01_PLAN.md"
    next_impl = f"{p_dir}/{p_id}_02_IMPLEMENT.md"
    rec_path = f"{p_dir}/{p_id}_RECOVERY.md"
    
    plan_content = f"""# {p_id} {disp.upper()} — IMPLEMENTATION PLAN
## AI Video Factory — Architectural Specification & Test Plan

**PROMPT_ID:** `{plan_id}`  
**PURPOSE:** Create the complete architectural implementation and test plan for {name} ({disp}) adhering to all 16 blueprint sections without authoring production code.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["plan_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `{repo["prereq_plan"]}`  
**READ_ONLY_INPUTS:**
- `{bp}`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{plan_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`  
**PASS_CRITERIA:**
- PLAN.md covers all 16 blueprint sections from `{bp}`.
- Specific boundaries respected: OWNS: {owns}; DOES NOT OWN: {not_owns}.
- Allowed dependencies: {allowed_deps}; Forbidden dependencies: {forbidden_deps}.
- Test strategy defines >=85% coverage and contract conformance.
- Zero production code authored in this planning step.  
**FAIL_CRITERIA:**
- Missing blueprint sections or production source files written during planning.  
**GIT_EXPECTATION:** Plan committed on feature branch `feature/{p_id.lower()}-scaffold`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{p_dir}/{p_id}_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_impl}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_path}`

---

### Step-by-Step Instructions:

1. **Inspect Blueprint & Contracts:**
   Read `{bp}` and examine referenced schemas.
2. **Review Specific Hardening Requirements:**
   {guidance}
3. **Formulate PLAN.md:**
   Write `05_IMPLEMENTATION/repos/{name}/PLAN.md` detailing:
   - Module architecture and component breakdown
   - TypeScript interfaces / schemas
   - State ownership, persistence, and concurrency models
   - Error taxonomy & retry policy
   - Observability integration (via R14)
   - Comprehensive test plan (unit, contract, negative)
   - Definition of Done checklist
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{plan_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-scaffold"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 0, failed: 0}}
CONTRACT_TESTS: {{passed: 0, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/PLAN.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_impl}"
RECOMMENDED_NEXT_TASK: "Implement {name} application code and unit/contract test suites."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    # 02 IMPLEMENT
    impl_id = f"{p_id}-02"
    impl_path = f"{p_dir}/{p_id}_02_IMPLEMENT.md"
    next_test = f"{p_dir}/{p_id}_03_TEST_AND_REVIEW.md"
    
    impl_content = f"""# {p_id} {disp.upper()} — IMPLEMENTATION & BUILD
## AI Video Factory — Source Code Authoring & Test Suite Implementation

**PROMPT_ID:** `{impl_id}`  
**PURPOSE:** Implement all production source code, build toolchains, unit tests, and contract fixtures for {name} ({disp}) according to the approved PLAN.md.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["impl_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-10 min)`  
**PREREQUISITES:** `{plan_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `{bp}`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Production source code in `05_IMPLEMENTATION/repos/{name}/src/`
- Test suites in `05_IMPLEMENTATION/repos/{name}/tests/`
- Build script passing cleanly (`npm test` / `pytest`).  
**PASS_CRITERIA:**
- All components in PLAN.md fully implemented without placeholder stubs.
- OWNS boundaries strictly enforced: {owns}.
- Zero forbidden dependencies imported: {forbidden_deps}.
- Unit and contract tests execute and pass 100%.  
**FAIL_CRITERIA:**
- Build compilation failure, test failures, or cross-repo file modifications.  
**GIT_EXPECTATION:** Clean commits on feature branch `feature/{p_id.lower()}-impl`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{p_dir}/{p_id}_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_test}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_path}`

---

### Step-by-Step Instructions:

1. **Implement Core Components:**
   Author production modules in `src/` satisfying all architectural responsibilities.
2. **Implement Test Suites:**
   Build unit and contract test suites under `tests/`.
3. **Execute Local Build & Tests:**
   Run test suites and verify 100% pass rate with zero lint/type errors.
4. **Git Commit:**
   Commit all changes to `feature/{p_id.lower()}-impl`.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{impl_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 12, failed: 0}}
CONTRACT_TESTS: {{passed: 6, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/src/"
  - "05_IMPLEMENTATION/repos/{name}/tests/"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_test}"
RECOMMENDED_NEXT_TASK: "Execute independent technical and adversarial review of {name}."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    # 03 TEST AND REVIEW
    test_id = f"{p_id}-03"
    test_path = f"{p_dir}/{p_id}_03_TEST_AND_REVIEW.md"
    next_accept = f"{p_dir}/{p_id}_04_ACCEPT_RELEASE.md"
    
    test_content = f"""# {p_id} {disp.upper()} — INDEPENDENT TECHNICAL REVIEW & AUDIT
## AI Video Factory — Negative Testing, Security & Boundary Conformance

**PROMPT_ID:** `{test_id}`  
**PURPOSE:** Perform an independent technical audit of {name} ({disp}), executing negative test suites, contract compatibility checks, secret redaction validation, and dependency boundary verification.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["review_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (3-5 min)`  
**PREREQUISITES:** `{impl_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `05_IMPLEMENTATION/repos/{name}/src/**`
- `05_IMPLEMENTATION/repos/{name}/tests/**`
- `{bp}`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{test_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`  
**PASS_CRITERIA:**
- Zero forbidden imports detected (scanned against: {forbidden_deps}).
- Branch test coverage >= 85%.
- Negative fixtures correctly trigger normalized error responses.
- Observability and secret redaction verified.  
**FAIL_CRITERIA:**
- Boundary leak, uncovered critical path, secret leakage, or failed contract assertions.  
**GIT_EXPECTATION:** Audit report committed on branch.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{p_dir}/{p_id}_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_accept}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_path}`

---

### Step-by-Step Instructions:

1. **Dependency Boundary Scan:**
   Run static grep search across `05_IMPLEMENTATION/repos/{name}/src/` to confirm zero forbidden imports.
2. **Execute Full Test & Negative Fixture Suite:**
   Run all positive, negative, and edge-case unit and contract tests.
3. **Verify Observability & Redaction:**
   Confirm that all telemetry integration masks sensitive credentials and attaches trace contexts.
4. **Compile AUDIT_REPORT.md:**
   Document test metrics, boundary scan results, and final verification signoff.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{test_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "feature/{p_id.lower()}-impl"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 18, failed: 0}}
CONTRACT_TESTS: {{passed: 8, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{next_accept}"
RECOMMENDED_NEXT_TASK: "Execute formal acceptance and release tagging for {name}."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    # 04 ACCEPT RELEASE
    accept_id = f"{p_id}-04"
    accept_path = f"{p_dir}/{p_id}_04_ACCEPT_RELEASE.md"
    pass_next = repo["pass_after_accept"]
    
    accept_content = f"""# {p_id} {disp.upper()} — ACCEPTANCE & RELEASE
## AI Video Factory — Formal Acceptance, Merge & Version Tagging

**PROMPT_ID:** `{accept_id}`  
**PURPOSE:** Conduct formal acceptance signoff for {name} ({disp}), merge feature branch to main, apply annotated git release tag, and unlock downstream dependency gates.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `{repo["accept_model"]}`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `{repo["accept_conv"]}`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `{test_id}`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/repos/{name}/PLAN.md`
- `{bp}`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( {name} )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{accept_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Released `main` branch with annotated release tag `v1.0.0`
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- All tests pass on `main`.
- Clean merge commit and git tag `{name.lower()}-v1.0.0` applied.
- Repository status marked as `RELEASED` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Merge conflict, uncommitted changes, or failing CI checks.  
**GIT_EXPECTATION:** Tagged release commit on `main`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `{p_dir}/{p_id}_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `{pass_next}`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_path}`

---

### Step-by-Step Instructions:

1. **Verify Audit Signoff:**
   Inspect `05_IMPLEMENTATION/repos/{name}/AUDIT_REPORT.md` and confirm PASS verdict.
2. **Merge to Main Branch:**
   Checkout `main` and merge `feature/{p_id.lower()}-impl` cleanly:
   `git checkout main && git merge --no-ff feature/{p_id.lower()}-impl -m "feat({p_id.lower()}): complete {name} implementation"`
3. **Apply Release Tag:**
   Apply annotated git tag:
   `git tag -a "{name.lower()}-v1.0.0" -m "Release {name} v1.0.0"`
4. **Update System Runtime State:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `{name}.status: "RELEASED"` and record commit SHA and tag.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "{accept_id}"
RESULT: PASS
REPO: "{name}"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {{passed: 18, failed: 0}}
CONTRACT_TESTS: {{passed: 8, failed: 0}}
INTEGRATION_TESTS: {{passed: 0, failed: 0}}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/{name}/ (tagged {name.lower()}-v1.0.0)"
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "{pass_next}"
RECOMMENDED_NEXT_TASK: "Proceed to next scheduled prompt in master execution sequence."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
"""

    # 05 RECOVERY
    rec_id = f"{p_id}-REC"
    rec_file_path = f"{p_dir}/{p_id}_RECOVERY.md"
    
    rec_content = f"""# {p_id} {disp.upper()} — RECOVERY & TRIAGE
## AI Video Factory — Local Repository Defect Triage & Routing

**PROMPT_ID:** `{rec_id}`  
**PURPOSE:** Triage failures occurring within {name} ({disp}), categorize the defect class, and route to local remediation or master system recovery.  
**CURRENT_PHASE:** `{phase}`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `{name}`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/{name}`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/FAILURE_DECISION_TREE.md`  
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/{name}/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{rec_file_path} and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Diagnostic defect analysis and targeted recovery action.  
**PASS_CRITERIA:**
- Defect correctly categorized (IMPLEMENTATION_BUG, CONTRACT_DEFECT, FROZEN_SPEC_DEFECT, ENVIRONMENT, DEPENDENCY, EXTERNAL_PROVIDER).
- Exact remediation command or recovery prompt returned.  
**FAIL_CRITERIA:**
- Unclassified defect.  
**GIT_EXPECTATION:** Worktree preserved for debugging.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human architect.  
**NEXT_PROMPT_IF_PASS:** Dynamic routing based on defect class.  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md`

---

### Defect Classification & Dispatch Matrix:

1. **Category A: Local Implementation Bug (Syntax, Logic, Local Unit Test)**
   - **Action:** Fix code within `05_IMPLEMENTATION/repos/{name}/src/` and re-run `{impl_path}`.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/{impl_path}`
2. **Category B: Schema Incompatibility / Contract Break**
   - **Action:** Open contract change triage.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md`
3. **Category C: Frozen Spec Contradiction**
   - **Action:** Open formal Change Request.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md`
4. **Category D: Upstream Dependency Missing or Broken**
   - **Action:** Verify upstream repository release.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md`
5. **Category E: Git Conflict / Branch State Issue**
   - **Action:** Run git state reconciliation.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`
6. **Category F: Environment / Toolchain Failure**
   - **Action:** Re-run environment doctor.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`
"""

    return {
        plan_path: plan_content,
        impl_path: impl_content,
        test_path: test_content,
        accept_path: accept_content,
        rec_file_path: rec_content
    }

total_written = 0
for repo in REPOS_CONFIG:
    suite = generate_repo_suite(repo)
    for rel_path, content in suite.items():
        full_path = os.path.join(RUNBOOK_DIR, rel_path)
        with open(full_path, "w") as f:
            f.write(content.strip() + "\n")
        total_written += 1

print(f"Successfully generated {total_written} repo prompt files across 15 repositories.")
