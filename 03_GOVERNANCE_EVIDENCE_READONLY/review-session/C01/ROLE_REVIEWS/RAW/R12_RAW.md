# Independent Blind Review — R12_PRODUCT_OPS
**Role:** Product / Operator / Human-in-the-loop Architect  
**Review Round:** C01  
**Timestamp:** 2026-08-15T11:30:00+07:00  
**Session ID:** `f1bb45a2-477d-4761-a47b-634853b99730`  
**Review Target Version:** AI Video Factory Specification v0.9.0 Candidate for v1.0 Freeze  

---

## 1. Enumeration of Inspected Specification Files

The following files from `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0` and baseline artifacts from `review-session/C00_FINAL/` were systematically inspected:

1. `03_repo_blueprints/R13_OPERATOR_CONSOLE.md` (Primary assigned blueprint)
2. `01_master/MASTER_BLUEPRINT.md` (Primary master architecture)
3. `02_contracts/STATUS_STATE_MACHINES.md` (Primary state machine contract)
4. `02_contracts/CONTRACTS_OVERVIEW.md` (Contract families, error taxonomy, forward compatibility)
5. `02_contracts/domain-entities.schema.json` (ShotVersion, PromptVersion schemas)
6. `02_contracts/provider-request.schema.json` (Generation request schema)
7. `02_contracts/provider-result.schema.json` (Generation result schema)
8. `03_repo_blueprints/R02_CORE_STATE.md` (Core state, commands, persistence, audit ledger)
9. `03_repo_blueprints/R06_WORKFLOW.md` (Durable orchestration, human gates, signaling)
10. `03_repo_blueprints/R11_QC.md` (Technical and semantic QC evaluation)
11. `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md` (Telemetry, audit logs, correlation)
12. `04_integration/SECURITY_MODEL.md` (Trust zones, credentials, screenshot access control)
13. `04_integration/COMMAND_EVENT_CATALOG.md` (Core commands, domain events, outbox delivery)
14. `04_integration/E2E_INTEGRATION_PROTOCOL.md` (Release manifest, deterministic suites)
15. `05_phases/PHASE_ROADMAP.md` & `05_phases/BUILD_ORDER.md` (Phase sequencing)
16. `06_adrs/ADR-005_LLM_STATE_MUTATION.md` (Proposal vs commit boundary)
17. `06_adrs/ADR-006_RETRY_POLICY.md` (Deterministic software policy vs LLM retries)
18. `06_adrs/ADR-007_BROWSER_SECURITY.md` (Security challenges & operator intervention)
19. `review-session/C00_GAP_TO_C01_SEED_REGISTER.md` (Assigned seeds: GAP-007, GAP-010)
20. `review-session/C00_FINAL/SYSTEM_INVARIANT_INVENTORY.md` (System Invariants INV-001 through INV-020)
21. `review-session/C00_FINAL/REQUIREMENT_TRACEABILITY_MATRIX.md` (Requirements REQ-001 through REQ-055)

---

## 2. Invariants and Contracts Relevant to Product / Operator Role

| Invariant / Contract ID | Name / Summary | Operational Relevance & Constraint |
|---|---|---|
| **INV-001** | `Take` belongs to 1 `Shot` & 1 `GenerationJob` | Manual takes cannot be re-parented across shots arbitrarily; must preserve 1:1 job linkage. |
| **INV-002** | `GenerationJob` references immutable `ShotVersion` & `PromptVersion` | Operator prompt edits MUST generate a new `PromptVersion`, never mutate in-place. |
| **INV-003** | Idempotency keys on all external side-effects | All operator actions (approvals, prompt overrides, retries) must carry deterministic `command_id` to prevent double-execution. |
| **INV-004** | LLMs propose; software commands commit state | Operator console is the human interface for reviewing LLM proposals and executing validated mutation commands. |
| **INV-005** | Browser/worker state is non-canonical | Operator actions must target Core API / Workflow API, never write directly to worker memory or browser state. |
| **INV-006** | Artifact provenance & content checksum | Operator approvals and manual asset uploads must calculate and record SHA-256 and operator identity. |
| **INV-009** | QC models recommend; deterministic policy decides | Operator must have visibility into raw QC scores and deterministic policy thresholds; can manually override recommendation. |
| **INV-010** | Technical retries reuse `PromptVersion` | Operator triggering technical retry must not inadvertently trigger prompt recompilation. |
| **INV-011** | Creative retries create new `PromptVersion` | Manual operator prompt refinement must create a new `PromptVersion` with `origin: HUMAN_OPERATOR`. |
| **INV-012** | No security bypass automation | Authentication/CAPTCHA halts automation immediately, emitting `BLOCKED_AUTH`/`BLOCKED_SECURITY` requiring human recovery. |
| **INV-015** | Correlation IDs propagate everywhere | Operator console actions must attach `trace_id`, `operator_id`, `project_id`, `shot_id`, `generation_job_id`. |
| **INV-016** | Completed `Take` cannot be overwritten | Rejecting a take creates a new Take/Job; does not destructively modify or delete the prior take record. |
| **INV-018** | Budget limits enforced before generation | Budget exhaustion transitions to `BLOCKED_BUDGET`; operator can grant budget overrides with explicit audit justification. |
| **REQ-013** | R13_OPERATOR_CONSOLE ownership | Owns operator views, action UX, approval/retry/edit flows, browser session health visualization. |
| **REQ-020** | ADR-005 LLM State Mutation | Enforces proposal-command pattern across all UI interactions. |
| **REQ-021** | ADR-006 Retry Policy | Deterministic policy governs automatic retries; escalates to `HUMAN_REVIEW` on threshold exhaustion. |
| **REQ-022** | ADR-007 Browser Security | Operator intervention workflow must cleanly handle manual browser unblocking. |
| **GAP-007** | Technical QC pass/fail scoring thresholds | Operator usability of QC scoring, defect categorization, and tri-state routing. |
| **GAP-010** | Operator override authentication & audit log schema | Auditability, schemas, and immutability of manual operator actions. |

---

## 3. Executive Summary & Lens Analysis

As the **Product / Operator / Human-in-the-loop Architect (R12)**, the primary mandate is ensuring that the AI Video Factory is **controllable, transparent, recoverable, auditable, and resilient to operational failures** without imposing unnecessary cognitive or procedural friction on human operators.

### Key Architectural Strengths of v0.9.0:
1. **Separation of Non-Canonical Worker/Browser State from Core Truth (ADR-002, INV-005):** The principle that browser workers are disposable peripherals protects against catastrophic state loss during browser crashes.
2. **Deterministic-First Automation with Human Fallback (ADR-007, INV-012):** Explicitly forbidding brittle, unauthorized CAPTCHA/anti-abuse bypass automation protects provider accounts and provides clear boundaries for human escalation.
3. **Immutable Artifact Versioning (INV-002, INV-016):** Strict append-only versioning ensures full reproducibility of past creative work.

### Critical Gaps and Vulnerabilities Identified in C01 Review:
1. **GAP-007 (QC Threshold Usability & Tri-State Escalation):** QC is specified as a binary or opaque evaluation without a standardized schema or tri-state routing policy (`AUTO_APPROVE` vs `HUMAN_REVIEW` vs `AUTO_RETRY`). This risks either severe operator approval fatigue or runaway automated costs.
2. **GAP-010 (Operator Override Audit Logs & Schema Absence):** There are no defined JSON schemas for operator commands, mutations, or audit log records in `avf-contracts`, violating the core contract-first principle.
3. **Blocked State Recovery Deadlocks:** `STATUS_STATE_MACHINES.md` lists 8 blocked/error states but specifies **zero transition rules or operator exit signals** for recovering from them.
4. **Roadmap Staging Hazard (Phase 6 vs MVP Need):** Operator console is scheduled for Phase 6, yet blocked states and human gates occur in Phases 0, 1, and 2. Operators and QA in early phases will be forced to perform unsafe direct DB mutations (violating INV-013).
5. **Operator Prompt Intervention Lineage Breakage:** The specification lacks an explicit flow for how an operator refines a prompt during human review while maintaining immutability and provenance.
6. **Optimistic Concurrency Missing in Operator UX:** No version-checking mechanism prevents concurrent operators from clobbering each other's decisions on shared shots or project queues.

---

## 4. Evidence-Backed Council Findings

```markdown
# Finding

FINDING_ID: F-R12-001
ROLE: R12_PRODUCT_OPS
SEVERITY: HIGH
CATEGORY: SPEC_GAP
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md
- review-session/C00_GAP_TO_C01_SEED_REGISTER.md
AFFECTED_CONTRACTS:
- domain-entities.schema.json
- STATUS_STATE_MACHINES.md
- COMMAND_EVENT_CATALOG.md
EVIDENCE:
- R11_QC.md lines 33-39 states outputs include "QCResult proposal", "technical findings", "semantic scores/issues", and "recommendation", but defines no structured schema.
- R11_QC.md line 124-126 states "technical and semantic failures separated" and "recommendation is typed and policy-neutral", but provides no concrete metric ranges, weightings, or threshold definitions.
- STATUS_STATE_MACHINES.md lines 14-16, 21, 26 only lists `QC_PENDING -> QC_RUNNING -> APPROVED`, `FAILED_QC`, `HUMAN_REVIEW` without threshold-based transition criteria.
- C00_GAP_TO_C01_SEED_REGISTER.md GAP-007 explicitly seeds this gap: "What minimum technical QC metrics (black frame %, freeze frame duration, audio loudness) constitute a blocking failure?"
FAILURE_SCENARIO:
A generated video take has a minor 0.5-second freeze frame at the tail end but perfect character likeness and motion. Because the QC engine lacks a multi-tier threshold policy, it issues an opaque `FAILED_QC`. The workflow engine automatically burns a second expensive generation attempt, which produces a worse result. Conversely, if all failures default to `HUMAN_REVIEW`, an operator managing a 100-shot project is bombarded with dozens of minor notifications, creating massive cognitive overload and approval fatigue.
WHY_IT_MATTERS:
Without a standardized, granular QC result schema and a tri-state escalation model (Green: Auto-Pass, Amber: Human Review, Red: Auto-Retry), the factory cannot achieve autonomous operation or predictable unit economics. Operators cannot see actionable defect timestamps or override specific QC sub-scores.
PROPOSED_SOLUTION:
1. Define a concrete `QCResult` schema in `avf-contracts` (`qc-result.schema.json`) with distinct objects for `technical_metrics` and `semantic_metrics`:
   - `technical_metrics`: `black_frame_ratio` (float [0..1]), `freeze_frame_max_sec` (float), `audio_loudness_lufs` (float), `decode_error` (boolean), `resolution_valid` (boolean), `fps_valid` (boolean).
   - `semantic_metrics`: `character_consistency_score` (float [0..1]), `style_match_score` (float [0..1]), `motion_quality_score` (float [0..1]), `prompt_adherence_score` (float [0..1]), `confidence` (float [0..1]).
   - `defect_annotations`: array of `{ metric: string, start_frame: int, end_frame: int, severity: "FATAL"|"WARNING"|"INFO", description: string }`.
2. Standardize baseline technical thresholds for auto-blocking:
   - `black_frame_ratio > 0.05` => Fatal technical failure (Red).
   - `freeze_frame_max_sec > 1.5` => Fatal technical failure (Red).
   - `decode_error == true` => Fatal technical failure (Red).
3. Implement Tri-State Policy in Workflow RetryPolicyEngine:
   - **PASS (Green):** Technical checks pass AND Semantic Score >= `pass_threshold` (default 0.80) => Auto-transition to `APPROVED` (if project policy allows auto-approval).
   - **AMBER (Human Review Required):** Technical checks pass AND (`review_threshold` (default 0.60) <= Semantic Score < `pass_threshold` OR `confidence < 0.70`) => Transition to `HUMAN_REVIEW` with visual defect overlay in Operator Console.
   - **RETRY / FAIL (Red):** Fatal technical check OR Semantic Score < `review_threshold` => Automatic retry if `attempt_no < max_attempts` and budget permits; otherwise escalate to `HUMAN_REVIEW`.
ALTERNATIVES_CONSIDERED:
- Binary Pass/Fail threshold: Rejected because it causes extreme retry cost inflation or severe approval fatigue.
- LLM decides approval dynamically: Rejected as a direct violation of ADR-006 and INV-009.
CAPABILITY_IMPACT:
Greatly enhances operational autonomy and operator efficiency while providing clear visual diagnostics for borderline takes.
COMPATIBILITY_IMPACT:
Additive schema in `avf-contracts`. No breaking changes to upstream core entities.
MIGRATION_IMPACT:
None for MVP; establishes required contracts prior to Phase 5 build.
TEST_OR_BENCHMARK_REQUIRED:
Unit tests in R11 testing metric calculation against synthetic corrupt video clips (black frames, frozen frames, audio spikes) and Contract tests validating `qc-result.schema.json`.
RESIDUAL_RISK:
Semantic scoring calibration will require tuning against real provider outputs in Phase 5; the tri-state thresholds must remain project-configurable.
CONFIDENCE:
VERY HIGH (Proven defect; concrete solution provided).
```

```markdown
# Finding

FINDING_ID: F-R12-002
ROLE: R12_PRODUCT_OPS
SEVERITY: HIGH
CATEGORY: CONTRACT
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md
- review-session/C00_GAP_TO_C01_SEED_REGISTER.md
AFFECTED_CONTRACTS:
- CONTRACTS_OVERVIEW.md
- domain-entities.schema.json
- event-envelope.schema.json
EVIDENCE:
- R13_OPERATOR_CONSOLE.md line 71 lists "operator action audit", line 113 states "all mutations auditable", but R13 specifies no concrete command or audit schema.
- R02_CORE_STATE.md lines 41-53 lists public commands (`ApproveTake`, `BlockGeneration`, etc.) but does not define operator-specific payload envelopes or mutation audit tables.
- `02_contracts/` contains schemas for provider requests, provider results, and browser commands, but has ZERO schemas for operator mutations or audit logs.
- C00_GAP_TO_C01_SEED_REGISTER.md GAP-010 explicitly identifies this omission: "How are manual operator approvals, prompt overrides, and budget increases authenticated and audited in the canonical log?"
FAILURE_SCENARIO:
An operator manually overrides a prompt on a high-visibility brand project and increases the project budget by $500 to push a deadline. Two days later, executive stakeholders discover unexpected spend and unintended prompt wording. When checking system logs, they find generic service-level database updates without operator identity, timestamp, session ID, justification reason, or diff of the prompt changes. Compliance and forensic audits fail completely.
WHY_IT_MATTERS:
Commercial studio and enterprise production require immutable auditability for every human intervention, especially financial budget increases, safety overrides, and creative prompt mutations. Lacking an operator command contract invites ad-hoc, unauthenticated mutations and breaks INV-004.
PROPOSED_SOLUTION:
1. Create `operator-command.schema.json` in `avf-contracts` with standard fields:
   - `schema_version`: "1.0"
   - `command_id`: UUIDv4 (Idempotency key)
   - `operator_id`: UUIDv4 / string (Authenticated user identity)
   - `operator_roles`: array of string (e.g. `["OPERATOR", "STUDIO_LEAD", "ADMIN"]`)
   - `action`: enum (`APPROVE_TAKE_OVERRIDE`, `REJECT_TAKE`, `PROMPT_OVERRIDE`, `BUDGET_INCREASE`, `UNBLOCK_SESSION`, `RETRY_SHOT`, `CANCEL_JOB`, `FORCE_STATE_TRANSITION`)
   - `target_entity_type`: enum (`Project`, `Shot`, `Take`, `GenerationJob`, `BrowserSession`)
   - `target_entity_id`: UUIDv4
   - `expected_version`: integer (Optimistic concurrency lock)
   - `reason`: string (Mandatory justification; minLength: 5)
   - `payload`: object (Action-specific parameters, e.g. `budget_increment_usd`, `new_prompt_text`, `unblock_action`)
   - `correlation`: `{ trace_id, workflow_run_id, project_id, shot_id }`
2. Create `operator-audit-log.schema.json` and mandate an append-only `operator_audit_log` table in `avf-core-state`.
3. Require `avf-core-state` to atomically write the business state mutation and the `operator_audit_log` entry in the same PostgreSQL transaction.
ALTERNATIVES_CONSIDERED:
- Relying solely on unstructured OpenTelemetry log spans: Rejected because log aggregation systems have retention expirations and cannot guarantee transactional consistency with relational business records.
- Storing audit fields inside entity metadata columns: Rejected because historical mutation sequences would be overwritten by latest entity states.
CAPABILITY_IMPACT:
Guarantees enterprise-grade compliance, security auditability, and tamper-proof change tracking.
COMPATIBILITY_IMPACT:
Additive contracts in `avf-contracts`; mandatory implementation in `avf-core-state` and `avf-operator-console`.
MIGRATION_IMPACT:
None if introduced prior to v1.0 contract freeze.
TEST_OR_BENCHMARK_REQUIRED:
Contract tests verifying rejection of unauthenticated/reason-less commands, and integration tests verifying atomic commit of state and audit log records.
RESIDUAL_RISK:
RBAC identity provider integration (OIDC/SAML) is production-scope; for MVP, simple API key/session header propagation is sufficient.
CONFIDENCE:
VERY HIGH (Proven defect; standard architectural pattern).
```

```markdown
# Finding

FINDING_ID: F-R12-003
ROLE: R12_PRODUCT_OPS
SEVERITY: HIGH
CATEGORY: STATE_MACHINE
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
AFFECTED_CONTRACTS:
- STATUS_STATE_MACHINES.md
- COMMAND_EVENT_CATALOG.md
EVIDENCE:
- STATUS_STATE_MACHINES.md lines 18-28 lists recoverable/error states (`FAILED_TRANSIENT`, `FAILED_PROVIDER`, `FAILED_QC`, `BLOCKED_AUTH`, `BLOCKED_SECURITY`, `BLOCKED_UI_CHANGE`, `BLOCKED_BUDGET`, `HUMAN_REVIEW`, `CANCELLED`).
- STATUS_STATE_MACHINES.md lines 30-36 gives transition rules only for `SUBMITTING -> SUBMITTED` and `APPROVED`, but specifies ZERO transition rules, valid trigger signals, or target states for the 8 blocked/error states!
- R06_WORKFLOW.md lines 44-46 only exposes `SignalApprove`, `SignalResume`, `CancelWorkflow` without specifying which signal applies to which blocked state or how data is passed.
FAILURE_SCENARIO:
A browser worker encounters a Google account re-authentication prompt. It detects the challenge and transitions `GenerationJob` to `BLOCKED_AUTH`. The operator opens Chrome, completes OAuth/2FA, and returns to the Operator Console. The operator clicks "Resume". However, because `STATUS_STATE_MACHINES.md` does not specify whether `BLOCKED_AUTH` transitions back to `SUBMITTING`, `GENERATING`, or `READY`, the workflow worker rejects the signal as invalid state transition, leaving the job permanently hung in `BLOCKED_AUTH`.
WHY_IT_MATTERS:
State machine ambiguity causes workflow deadlocks, unrecoverable jobs, and divergent implementations between `avf-workflow`, `avf-core-state`, and `avf-operator-console`. Human recovery is a core architectural pillar; without explicit transition rules, recovery workflows cannot function.
PROPOSED_SOLUTION:
Amend `STATUS_STATE_MACHINES.md` to include an explicit, authoritative State Transition Matrix for all blocked and recoverable states:

| Source State | Trigger Signal / Action | Precondition / Validation | Target State | Description |
|---|---|---|---|---|
| `BLOCKED_AUTH` | `SignalUnblockAuth` | Operator completes browser login; worker confirms `ENSURE_SESSION` OK | `SUBMITTING` (if not submitted) or `GENERATING` (if generation was in flight) | Resumes generation after re-authentication. |
| `BLOCKED_SECURITY` | `SignalUnblockSecurity` | Operator solves CAPTCHA; worker confirms page interactive | `SUBMITTING` or `GENERATING` | Resumes after manual CAPTCHA clearance. |
| `BLOCKED_UI_CHANGE` | `SignalRerouteTrack` or `SignalRetrySubmit` | Operator acknowledges selector update or switches Track A -> Track B | `READY` | Retries job with updated execution configuration. |
| `BLOCKED_BUDGET` | `SignalIncreaseBudget` | Operator adds budget allocation or authorizes override | `READY` | Releases budget hold and proceeds to submission. |
| `HUMAN_REVIEW` | `SignalApproveOverride` | Operator manually accepts take despite QC warnings | `APPROVED` | Creates approved Take record and advances workflow. |
| `HUMAN_REVIEW` | `SignalRejectAndRetry` | Operator rejects take and optionally submits modified prompt | `READY` (New Job) / `REJECTED` (Old Job) | Spawns new `GenerationJob` with incremented attempt / version. |
| `HUMAN_REVIEW` | `SignalCancel` | Operator abandons shot | `CANCELLED` | Terminates workflow for this shot. |
| `FAILED_QC` | Deterministic Policy (`AutoRetry`) | `attempt_no < max_attempts` AND Budget available | `READY` (New Attempt) | Automated creative retry. |
| `FAILED_QC` | Deterministic Policy (`Escalate`) | `attempt_no >= max_attempts` OR Budget exhausted | `HUMAN_REVIEW` | Escalates to operator when automated retries fail. |
| `FAILED_PROVIDER` | Deterministic Policy / `SignalRetry` | Error class is retryable (`PROVIDER_RATE_LIMIT`, etc.) | `READY` | Re-submits with exponential backoff. |

ALTERNATIVES_CONSIDERED:
- Treating all blocked states as fatal and restarting entire workflows from scratch: Rejected because restarting wastes already generated upstream assets and burned compute/credits.
CAPABILITY_IMPACT:
Provides deterministic, reliable manual recovery for every category of automation blockage.
COMPATIBILITY_IMPACT:
Clarifies and completes `STATUS_STATE_MACHINES.md` and aligns signal methods in `R06_WORKFLOW.md`.
MIGRATION_IMPACT:
None prior to contract freeze.
TEST_OR_BENCHMARK_REQUIRED:
Workflow integration tests simulating each of the 8 blocked states and validating successful resumption to `APPROVED` or `CANCELLED` upon receiving the designated signal.
RESIDUAL_RISK:
Re-verifying browser session health before state resumption is critical to avoid immediate re-blocking; worker must validate session health during the unblock activity.
CONFIDENCE:
VERY HIGH (Proven defect; explicit specification provided).
```

```markdown
# Finding

FINDING_ID: F-R12-004
ROLE: R12_PRODUCT_OPS
SEVERITY: HIGH
CATEGORY: PROVENANCE
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json
AFFECTED_CONTRACTS:
- domain-entities.schema.json
- COMMAND_EVENT_CATALOG.md
EVIDENCE:
- R13_OPERATOR_CONSOLE.md line 15 lists "approval/retry/edit flows" and line 100 lists "prompt/asset diff", but nowhere describes how manual prompt edits interact with immutability rules.
- domain-entities.schema.json lines 90-126 defines `promptVersion` with required fields `compiler_version` and `input_hash`, but has no fields indicating human authorship, parent prompt linkage, or manual override notes.
- MASTER_BLUEPRINT.md §12 requires: "Creative artifacts are append-only versions, never overwritten. Prompt v1 -> Prompt v2. Take always references the exact PromptVersion."
- Invariant INV-002 and INV-011 require that prompt changes create a new `PromptVersion`.
FAILURE_SCENARIO:
During `HUMAN_REVIEW`, an operator notices that the prompt is missing a crucial lighting cue ("golden hour cinematic rim light"). The operator edits the prompt text directly in the console and clicks "Retry". If the console simply updates the existing `PromptVersion` record in Postgres, it silently destroys the provenance of Take 1 (violating INV-002 and INV-016). If the console sends raw prompt text directly to the provider adapter without creating a `PromptVersion`, Take 2 is created without a valid `prompt_version_id`, breaking database foreign keys and lineage.
WHY_IT_MATTERS:
Full creative reproducibility requires that any human prompt modification is recorded as a first-class, immutable `PromptVersion` with complete parentage. Without explicit schema support and workflow mechanics, implementers will create unversioned prompt hacks.
PROPOSED_SOLUTION:
1. Extend `promptVersion` in `domain-entities.schema.json` to include:
   - `origin`: enum (`"AI_COMPILED"`, `"HUMAN_OPERATOR"`, `"HYBRID"`) - default `"AI_COMPILED"`
   - `parent_prompt_version_id`: string (UUIDv4, optional/nullable)
   - `created_by_operator_id`: string (UUIDv4, optional/nullable)
   - `operator_notes`: string (optional)
2. Specify the Operator Prompt Override Flow in `R13_OPERATOR_CONSOLE.md`:
   - Step 1: Operator edits prompt text / negative constraints / reference image weights in the Console.
   - Step 2: Console dispatches `RegisterPromptVersion` command to `avf-core-state` (or calls `avf-prompt-compiler`) with `origin: "HUMAN_OPERATOR"`, `parent_prompt_version_id: current_id`, and `input_hash: sha256(new_prompt_content)`.
   - Step 3: `avf-core-state` atomically creates `PromptVersion` (v_next).
   - Step 4: Console issues `SignalRetryAndGenerate` to `avf-workflow` referencing `new_prompt_version_id`.
   - Step 5: Workflow creates a new `GenerationJob` linking `shot_version_id`, `new_prompt_version_id`, and increments `attempt_no`.
ALTERNATIVES_CONSIDERED:
- Creating a separate `ShotVersion` for every prompt tweak: Rejected as overly coarse; prompt adjustments for the same camera/action plan should increment `PromptVersion` under the same `ShotVersion`.
CAPABILITY_IMPACT:
Preserves 100% provenance lineage while empowering human operators to refine AI-generated prompts.
COMPATIBILITY_IMPACT:
Additive properties to `domain-entities.schema.json` ($defs.promptVersion).
MIGRATION_IMPACT:
None prior to v1.0 freeze.
TEST_OR_BENCHMARK_REQUIRED:
Integration test executing operator prompt edit, verifying that `PromptVersion v2` is created with correct parent pointer, and verifying Take 2 references `v2` while Take 1 still references `v1`.
RESIDUAL_RISK:
Prompt compiler provider-specific syntax normalization should still run on human-edited prompts to ensure provider formatting constraints are respected.
CONFIDENCE:
VERY HIGH (Proven defect; directly preserves System Invariants INV-002, INV-004, INV-011).
```

```markdown
# Finding

FINDING_ID: F-R12-005
ROLE: R12_PRODUCT_OPS
SEVERITY: MEDIUM
CATEGORY: PRODUCT_POLICY
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md
AFFECTED_CONTRACTS:
- domain-entities.schema.json
- STATUS_STATE_MACHINES.md
EVIDENCE:
- MASTER_BLUEPRINT.md §6 states approval gates are "Human or policy-driven", and §9 depicts workflow with "Approve / Regenerate / HumanReview".
- Neither `MASTER_BLUEPRINT.md`, `R02_CORE_STATE.md`, nor `domain-entities.schema.json` defines a configurable `ApprovalPolicy` structure on the Project or Shot entity.
- Charter R12 explicitly mandates: "Avoid approvals everywhere; require them where automation risk justifies them."
FAILURE_SCENARIO:
A production studio creates a 60-shot social media video campaign. The system default requires human approval before prompt submission AND after QC for every single shot. Operators are forced to manually click "Approve" 120 times per project, creating severe operational latency, bottlenecking throughput, and causing operators to blindly click "Approve" without inspecting outputs (rubber-stamping). Conversely, on a high-stakes commercial TV ad, a team wants strict mandatory human sign-off on all shots, but the system has no way to enforce pre-generation gates.
WHY_IT_MATTERS:
Fixed, hardcoded approval gating either destroys automation velocity for high-volume pipelines or introduces unacceptable quality risk for high-touch productions. Studio operators must be able to configure governance policies per project.
PROPOSED_SOLUTION:
1. Introduce a formal `ApprovalPolicy` object into the Project and Shot entities in `domain-entities.schema.json`:
   ```json
   "approval_policy": {
     "type": "object",
     "properties": {
       "mode": {
         "type": "string",
         "enum": ["FULLY_AUTONOMOUS", "ASSISTED_REVIEW", "STRICT_HUMAN_GATE"],
         "default": "ASSISTED_REVIEW"
       },
       "pre_generation_approval": { "type": "boolean", "default": false },
       "qc_auto_approve_threshold": { "type": "number", "minimum": 0, "maximum": 1, "default": 0.85 },
       "qc_auto_retry_max_attempts": { "type": "integer", "minimum": 0, "maximum": 5, "default": 2 },
       "high_cost_threshold_usd": { "type": "number", "default": 10.0 },
       "require_approval_on_high_cost": { "type": "boolean", "default": true }
     }
   }
   ```
2. Policy Execution Rules in `avf-workflow`:
   - `FULLY_AUTONOMOUS`: Skips human review if QC score >= `qc_auto_approve_threshold` and within budget; auto-assembles final cut.
   - `ASSISTED_REVIEW` (Default): Auto-approves Green QC passes; routes Amber/Borderline QC scores or low-confidence assessments to `HUMAN_REVIEW`.
   - `STRICT_HUMAN_GATE`: Halts at `HUMAN_REVIEW` before generation submit AND after take generation, regardless of QC scores.
ALTERNATIVES_CONSIDERED:
- Hardcoding `ASSISTED_REVIEW` globally: Rejected because it restricts studio pipeline flexibility and enterprise multi-tier workflows.
CAPABILITY_IMPACT:
Allows seamless scaling from lights-out automated batch video generation to fine-grained artistic control.
COMPATIBILITY_IMPACT:
Additive property to Project/Shot schemas with backward-compatible defaults.
MIGRATION_IMPACT:
Default to `ASSISTED_REVIEW` for existing schemas.
TEST_OR_BENCHMARK_REQUIRED:
Workflow unit tests validating that each of the three policy modes routes through or bypasses `HUMAN_REVIEW` state as configured.
RESIDUAL_RISK:
Studios setting `FULLY_AUTONOMOUS` without adequate budget caps could incur cost overruns; project-level hard budget caps (INV-018) remain unconditionally enforced.
CONFIDENCE:
VERY HIGH (Proven product requirement).
```

```markdown
# Finding

FINDING_ID: F-R12-006
ROLE: R12_PRODUCT_OPS
SEVERITY: HIGH
CATEGORY: ROADMAP
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/PHASE_ROADMAP.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/05_phases/BUILD_ORDER.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
AFFECTED_CONTRACTS:
- API_COMPATIBILITY_POLICY.md
EVIDENCE:
- PHASE_ROADMAP.md line 67 places "Phase 6 — Operator control: Add dashboard, approvals, retries, prompt/asset intervention, browser-session health."
- MASTER_BLUEPRINT.md line 249 requires: "Every blocked auth/security challenge must surface operator action, never silently loop."
- PHASE_ROADMAP.md line 10-15 specifies that Phase 0 spikes must "measure disconnect/recovery" and "document authentication/security challenge behavior."
- R13_OPERATOR_CONSOLE.md lines 94-96 defines: "MVP VERSION: Projects, Shots, GenerationJobs, blocked states, approve/retry/resume, browser session health."
FAILURE_SCENARIO:
In Phase 1 and Phase 2, developers and QA engineers test multi-shot durable workflows with real browser workers. The browser hits an expired cookie or CAPTCHA (`BLOCKED_AUTH`/`BLOCKED_SECURITY`). Because R13 Operator Console is deferred until Phase 6, there is no standardized UI, CLI, or administrative endpoint to view the blocked state, review the failure, or issue an unblock signal. Engineers are forced to manually update database rows with raw SQL (`UPDATE generation_jobs SET status = 'READY'`), violating INV-013 and bypassing state machine validation.
WHY_IT_MATTERS:
Sequencing operator controls at the very end of the roadmap (Phase 6) creates an unworkable operational deadlock during Phases 0–5. Human-in-the-loop is not an afterthought UI feature—it is the foundational safety and recovery net for the entire platform.
PROPOSED_SOLUTION:
Restructure the Operator Control delivery across phases:
1. **Phase 1-2 (MVP Operator Control Surface & Admin CLI):**
   - Ship a lightweight Operator CLI / Admin API in `avf-core-state` and `avf-workflow` that supports:
     - `avf-admin job list --status BLOCKED_*`
     - `avf-admin session unblock --session-id <id>`
     - `avf-admin take approve --take-id <id>`
     - `avf-admin prompt override --shot-id <id> --prompt-file <path>`
   - Implement basic REST endpoints in Core API for operator commands with full audit logging.
2. **Phase 6 (Production Operator Web Console):**
   - Deliver the rich React/TypeScript Single Page Application with timeline scrubbing, side-by-side video compare, interactive QC overlays, bulk operations, and RBAC dashboards.
ALTERNATIVES_CONSIDERED:
- Building the full React Operator Console in Phase 1: Rejected because UI visual polish and dashboard widgets would delay core pipeline verification.
CAPABILITY_IMPACT:
Enables clean, contract-compliant human intervention and testing from Day 1 of development without delaying the core pipeline.
COMPATIBILITY_IMPACT:
None. Aligns implementation milestones with operational reality.
MIGRATION_IMPACT:
Updates `PHASE_ROADMAP.md` and `BUILD_ORDER.md`.
TEST_OR_BENCHMARK_REQUIRED:
E2E integration test in Phase 1 verifying that an operator can unblock a simulated `BLOCKED_AUTH` job via the Admin CLI / API.
RESIDUAL_RISK:
Low. CLI tooling leverages existing core API endpoints.
CONFIDENCE:
VERY HIGH (Proven operational dependency).
```

```markdown
# Finding

FINDING_ID: F-R12-007
ROLE: R12_PRODUCT_OPS
SEVERITY: MEDIUM
CATEGORY: UI_SPEC
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R13_OPERATOR_CONSOLE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md
AFFECTED_CONTRACTS:
- CONTRACTS_OVERVIEW.md
EVIDENCE:
- R13_OPERATOR_CONSOLE.md line 13-17 mentions "operator views", "action UX", "browser session health presentation", but contains zero specifications for media playback, frame-accurate inspection, or QC visual overlays.
- SECURITY_MODEL.md line 38 states "diagnostics screenshot retention is configurable and access-controlled", but specifies no interaction pattern for how operators securely view diagnostic screenshots or VNC streams when browser automation is blocked.
FAILURE_SCENARIO:
An operator reviews Take 1, which was flagged by QC for visual artifacting. The console only displays a small static thumbnail and an overall score of "0.72". The operator cannot scrub through frames, zoom in to inspect face fidelity, compare Take 1 side-by-side with Take 2, or jump directly to the defect timestamp. The operator is forced to download the raw MP4 file locally and open external video editing tools, adding 3-5 minutes of friction per shot.
WHY_IT_MATTERS:
Operator productivity and review fidelity depend on specialized media inspection tools tailored to AI video artifacts (morphing, temporal jitter, frame freezing, limb hallucination).
PROPOSED_SOLUTION:
Specify core operator inspection view capabilities in `R13_OPERATOR_CONSOLE.md`:
1. **Frame-Accurate Video Player Component:**
   - Transport controls: Play/pause, step forward/backward 1 frame (hotkeys: J/K/L, arrow keys).
   - Timecode display: SMPTE format (`HH:MM:SS:FF`) and frame counter.
   - Synchronized audio waveform visualizer.
2. **Side-by-Side Take Comparator:**
   - Synchronized multi-take playback (Take A vs Take B) with split-screen slider or side-by-side view.
   - Prompt/parameter difference viewer highlighting what changed between attempts.
3. **QC Defect Timeline Overlay:**
   - Visual color-coded bands on the video scrub bar corresponding to QC defect intervals (e.g. Red for black frame, Yellow for semantic jitter).
   - Click-to-seek functionality jumping directly to flagged defect frames.
4. **Secure Diagnostic Session Viewer:**
   - Ephemeral pre-signed URLs with short TTL (e.g. 5 minutes) for diagnostic screenshots stored in object storage.
   - Token and cookie redaction overlay masking sensitive auth headers in screenshot previews.
ALTERNATIVES_CONSIDERED:
- Standard browser `<video>` tag with default controls: Rejected because native HTML5 video controls lack frame-by-frame stepping, timecode synchronization, and timeline defect markers.
CAPABILITY_IMPACT:
Dramatically increases operator review speed and accuracy, reducing triage time per shot from minutes to seconds.
COMPATIBILITY_IMPACT:
Frontend UI specifications only; consumes standard streaming URLs and `QCResult` annotations.
MIGRATION_IMPACT:
None.
TEST_OR_BENCHMARK_REQUIRED:
UI unit tests verifying frame stepping precision and keyboard shortcut responsiveness.
RESIDUAL_RISK:
Video streaming formats must be compatible with standard browser codecs (H.264/MP4 and WebM); transcoding is owned by `R12_MEDIA`.
CONFIDENCE:
HIGH (Standard best practice for video production tools).
```

```markdown
# Finding

FINDING_ID: F-R12-008
ROLE: R12_PRODUCT_OPS
SEVERITY: MEDIUM
CATEGORY: COST_CONTROL
AFFECTED_FILES:
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R02_CORE_STATE.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md
- AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md
AFFECTED_CONTRACTS:
- domain-entities.schema.json
- STATUS_STATE_MACHINES.md
EVIDENCE:
- MASTER_BLUEPRINT.md §10 and §11 describe budget exhaustion and idempotency.
- Invariant INV-018 states: "Budget limits are enforced by deterministic policy before external generation requests."
- STATUS_STATE_MACHINES.md line 25 lists `BLOCKED_BUDGET`.
- The specifications provide no tiered alert model (e.g. 80% soft warning, 100% hard block) or operator override bounds, meaning projects simply hard-fail upon hitting the ceiling without advance notice.
FAILURE_SCENARIO:
A 20-shot video generation workflow is running overnight. At shot 16, the project crosses its $50 budget limit by $0.50. The workflow immediately halts all remaining shots into `BLOCKED_BUDGET`. The next morning, the operator arrives to find the deadline missed because 4 shots were blocked. If the system had emitted a soft warning at 80% ($40), the operator could have topped up the budget before leaving. Furthermore, when the operator tops up by $10, there is no guardrail preventing an accidental $1,000 top-up due to a typo.
WHY_IT_MATTERS:
Cost control must balance financial protection with production continuity. Abrupt hard stops without pre-warning cause avoidable delivery delays, while unconstrained manual overrides create financial risk.
PROPOSED_SOLUTION:
1. Define a Multi-Tier Budget Control Model in `avf-core-state` and `avf-workflow`:
   - `budget_limit_usd`: Absolute hard ceiling.
   - `budget_warning_threshold_ratio`: Default 0.80 (80%).
   - `accumulated_spend_usd`: Real-time ledger sum.
2. Operational Escalation Rules:
   - **Soft Warning (Spend >= 80% of Limit):** Core state emits `ProjectBudgetWarning` event; Operator Console displays prominent amber banner with estimated spend to complete remaining shots. Workflow continues uninterrupted.
   - **Hard Block (Spend + Estimated Next Job Cost > Limit):** Workflow halts generation before provider submission and transitions `GenerationJob` to `BLOCKED_BUDGET`. Emits `ProjectBudgetExhausted` event.
3. Structured Operator Override:
   - Operator command `IncreaseProjectBudget` requires:
     - `additional_amount_usd`: numeric > 0
     - `max_permitted_override_usd`: capped by operator role tier (e.g. Operator: up to $100, Studio Lead: up to $500, Admin: unlimited).
     - `reason`: mandatory string.
4. Auto-Resumption: Upon budget increase commit in `avf-core-state`, `avf-workflow` automatically wakes pending `BLOCKED_BUDGET` jobs in priority order.
ALTERNATIVES_CONSIDERED:
- Uncapped post-paid billing with no hard blocks: Rejected as unacceptable financial risk with expensive commercial video models.
CAPABILITY_IMPACT:
Prevents avoidable deadline misses while maintaining strict, auditable financial governance.
COMPATIBILITY_IMPACT:
Additive fields in Project schema and budget check activities.
MIGRATION_IMPACT:
None prior to freeze.
TEST_OR_BENCHMARK_REQUIRED:
Workflow integration test validating soft warning emission at 80%, hard blocking at 100%, and automatic job queue resumption upon authorized budget increment.
RESIDUAL_RISK:
Accurate pre-flight cost estimation for dynamic providers (e.g. per-second billing); worst-case maximum cost must be used for pre-flight budget reservation.
CONFIDENCE:
VERY HIGH (Proven financial control pattern).
```

---

## 5. Concrete Failure Scenarios & Operator Walkthroughs

### Scenario A: CAPTCHA / Browser Challenge Deadlock
- **Context:** Track A browser worker is generating a video via Google Flow. Google displays an interactive security challenge.
- **Flaw in Current Spec:** Worker detects challenge and sets `BLOCKED_SECURITY`. However, because there is no defined unblock signal or interactive session protocol, the operator has no documented way to take over the browser, solve the challenge, and signal the worker to verify and resume.
- **Target Resolution with Proposed Fixes:**
  1. Worker emits `GenerationBlocked(SECURITY_CHALLENGE, details={ worker_id, session_id })`.
  2. Workflow transitions job to `BLOCKED_SECURITY` and halts timeout clock.
  3. Operator Console displays a prominent "Security Challenge Detected" card with worker host and session ID.
  4. Operator clicks "Open Interactive Session" (spawning an authenticated VNC / remote browser tab to the worker).
  5. Operator completes the CAPTCHA manually.
  6. Operator clicks "Challenge Resolved & Resume" in the Console.
  7. Console dispatches `operator-command` (`action: UNBLOCK_SESSION`).
  8. Worker runs `ENSURE_SESSION` health check. If session is valid and DOM is interactive, worker returns OK.
  9. Workflow transitions job from `BLOCKED_SECURITY -> SUBMITTING` and proceeds smoothly.

### Scenario B: Concurrent Operator Double-Approval Race Condition
- **Context:** Two operators, Alice and Bob, are collaborating on a shared project queue containing Shot #7 in `HUMAN_REVIEW`.
- **Flaw in Current Spec:** R13 notes that commands must carry `command_id`, but does not specify entity versioning or optimistic locking.
- **Failure Execution:**
  1. Alice reviews Take 1 and decides to approve it. She clicks "Approve Take".
  2. Simultaneously, Bob reviews Take 1, thinks the lighting is flat, edits the prompt, and clicks "Regenerate Shot".
  3. If Bob's command arrives 100ms after Alice's approval, it could either overwrite Alice's approved take or spawn an unwanted second generation while the workflow is already assembling the video.
- **Target Resolution with Proposed Fixes:**
  1. Alice's client sends `ApproveTake` with `expected_version: 1` and `expected_status: "HUMAN_REVIEW"`.
  2. Core state commits Alice's approval, increments Shot status to `APPROVED`, and bumps `version: 2`.
  3. Bob's client sends `RegenerateShot` with `expected_version: 1`.
  4. Core state rejects Bob's command with HTTP `409 CONFLICT` (`CONFLICT_STATE_MODIFIED`).
  5. Bob's console immediately displays a toast: *"Shot #7 was already approved by Alice at 11:22 AM. Current status: APPROVED."* Bob's UI refreshes to show the updated state without data corruption.

### Scenario C: Operator Prompt Lineage Corruption
- **Context:** Operator Bob refines an AI-generated prompt during `HUMAN_REVIEW` by changing the camera angle from "wide shot" to "close up on face".
- **Flaw in Current Spec:** Lack of operator prompt override contract means an implementation might overwrite the original `PromptVersion` record in PostgreSQL or send raw text without registering a version.
- **Failure Execution:** Downstream stakeholders ask why Take 1 looks wide while the prompt record says "close up". Traceability and auditability are broken (violating INV-002 and INV-006).
- **Target Resolution with Proposed Fixes:**
  1. Bob edits prompt in Console.
  2. Console dispatches `RegisterPromptVersion` with `parent_prompt_version_id: prompt_v1_uuid`, `origin: "HUMAN_OPERATOR"`, and `operator_id: bob_uuid`.
  3. Core state creates `PromptVersion v2`.
  4. Workflow starts `GenerationJob #2` pointing to `PromptVersion v2` (attempt #2).
  5. The console diff viewer clearly shows:
     - `Prompt v1` (AI-compiled) => Take 1 (QC: 0.65, Rejected)
     - `Prompt v2` (Edited by Bob) => Take 2 (QC: 0.92, Approved).
  6. Provenance is 100% complete and audit-compliant.

---

## 6. Proposed Schema & Contract Additions

### A. `operator-command.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://avf.local/contracts/operator-command/1.0",
  "title": "OperatorCommandEnvelope",
  "type": "object",
  "required": [
    "schema_version",
    "command_id",
    "occurred_at",
    "operator_id",
    "action",
    "target_entity_type",
    "target_entity_id",
    "expected_version",
    "reason",
    "correlation"
  ],
  "properties": {
    "schema_version": { "const": "1.0" },
    "command_id": { "type": "string", "format": "uuid" },
    "occurred_at": { "type": "string", "format": "date-time" },
    "operator_id": { "type": "string" },
    "operator_roles": {
      "type": "array",
      "items": { "type": "string" }
    },
    "action": {
      "type": "string",
      "enum": [
        "APPROVE_TAKE_OVERRIDE",
        "REJECT_TAKE",
        "PROMPT_OVERRIDE",
        "BUDGET_INCREASE",
        "UNBLOCK_SESSION",
        "RETRY_SHOT",
        "CANCEL_JOB",
        "FORCE_STATE_TRANSITION"
      ]
    },
    "target_entity_type": {
      "type": "string",
      "enum": ["Project", "Shot", "Take", "GenerationJob", "BrowserSession", "WorkflowRun"]
    },
    "target_entity_id": { "type": "string", "format": "uuid" },
    "expected_version": { "type": "integer", "minimum": 1 },
    "reason": { "type": "string", "minLength": 5 },
    "payload": {
      "type": "object",
      "additionalProperties": true
    },
    "correlation": {
      "type": "object",
      "required": ["trace_id"],
      "properties": {
        "trace_id": { "type": "string" },
        "workflow_run_id": { "type": "string", "format": "uuid" },
        "project_id": { "type": "string", "format": "uuid" },
        "shot_id": { "type": "string", "format": "uuid" }
      }
    }
  },
  "additionalProperties": false
}
```

### B. `operator-audit-log.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://avf.local/contracts/operator-audit-log/1.0",
  "title": "OperatorAuditLogRecord",
  "type": "object",
  "required": [
    "audit_id",
    "command_id",
    "occurred_at",
    "operator_id",
    "action",
    "target_entity_type",
    "target_entity_id",
    "previous_state",
    "new_state",
    "reason",
    "trace_id"
  ],
  "properties": {
    "audit_id": { "type": "string", "format": "uuid" },
    "command_id": { "type": "string", "format": "uuid" },
    "occurred_at": { "type": "string", "format": "date-time" },
    "operator_id": { "type": "string" },
    "action": { "type": "string" },
    "target_entity_type": { "type": "string" },
    "target_entity_id": { "type": "string", "format": "uuid" },
    "previous_state": { "type": "object" },
    "new_state": { "type": "object" },
    "changes_diff": { "type": "object" },
    "reason": { "type": "string" },
    "trace_id": { "type": "string" }
  },
  "additionalProperties": false
}
```

### C. `qc-result.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://avf.local/contracts/qc-result/1.0",
  "title": "QCResultProposal",
  "type": "object",
  "required": [
    "schema_version",
    "qc_result_id",
    "take_id",
    "evaluator_version",
    "evaluator_profile_hash",
    "evaluated_at",
    "technical_passed",
    "overall_score",
    "recommendation"
  ],
  "properties": {
    "schema_version": { "const": "1.0" },
    "qc_result_id": { "type": "string", "format": "uuid" },
    "take_id": { "type": "string", "format": "uuid" },
    "evaluator_version": { "type": "string" },
    "evaluator_profile_hash": { "type": "string" },
    "evaluated_at": { "type": "string", "format": "date-time" },
    "technical_passed": { "type": "boolean" },
    "technical_metrics": {
      "type": "object",
      "properties": {
        "black_frame_ratio": { "type": "number", "minimum": 0, "maximum": 1 },
        "freeze_frame_max_sec": { "type": "number", "minimum": 0 },
        "audio_loudness_lufs": { "type": ["number", "null"] },
        "decode_error": { "type": "boolean" },
        "resolution_valid": { "type": "boolean" },
        "fps_valid": { "type": "boolean" },
        "duration_sec": { "type": "number" }
      }
    },
    "semantic_metrics": {
      "type": "object",
      "properties": {
        "character_consistency_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "style_match_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "motion_quality_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "prompt_adherence_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "defect_annotations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["metric", "severity", "description"],
        "properties": {
          "metric": { "type": "string" },
          "start_frame": { "type": "integer" },
          "end_frame": { "type": "integer" },
          "severity": { "type": "string", "enum": ["FATAL", "WARNING", "INFO"] },
          "description": { "type": "string" }
        }
      }
    },
    "overall_score": { "type": "number", "minimum": 0, "maximum": 1 },
    "recommendation": {
      "type": "string",
      "enum": ["APPROVE", "HUMAN_REVIEW", "RETRY_TECHNICAL", "RETRY_CREATIVE", "REJECT"]
    }
  },
  "additionalProperties": false
}
```

---

## 7. Proven Defects vs Uncertainties Needing Spikes

### Proven Defects (Must be fixed in Specification prior to v1.0 Freeze):
1. **Missing Operator Command and Audit Log Schemas (F-R12-002, GAP-010):** The absence of formal contracts for operator actions is an architectural defect violating contract-first design.
2. **Undefined Blocked State Transition Matrix (F-R12-003):** The state machine lists blocked states but provides no transition mechanics or unblocking signals, leading to deadlocks.
3. **Roadmap Staging Gap for Early Phase Human Recovery (F-R12-006):** Placing all operator controls in Phase 6 makes Phases 0–5 untestable without manual database tampering.
4. **Missing Operator Prompt Versioning Lineage (F-R12-004):** The domain entity schemas lack fields for recording human authorship and parent prompt linkage.

### Uncertainties Needing Architecture Spikes (Phase 0 Spikes):
1. **Interactive Session Latency & VNC Integration for CAPTCHA Resolution:**
   - *Question:* What is the operator experience and latency when opening a remote VNC session or DevTools port to a headless browser worker in a Docker container to solve a CAPTCHA?
   - *Spike Required:* Spike in `avf-integration-harness` to measure operator unblock turnaround time and verify that `ENSURE_SESSION` reliably detects solved CAPTCHAs without page reloads.
2. **Semantic QC Threshold Calibration across Diverse Visual Styles:**
   - *Question:* Do fixed thresholds (e.g. 0.80 Pass, 0.60 Review) produce consistent false-positive/false-negative rates across photorealistic vs anime vs 3D stylized models?
   - *Spike Required:* Benchmark spike in Phase 5 comparing MLLM evaluator scores across 100 labeled test videos to establish default calibration curves per style profile.

---

## 8. Residual Uncertainties & Open Risks

1. **High-Concurrency Multi-Operator Project Queues:** If a studio scales to 20+ operators triaging a shared 1,000-shot queue simultaneously, optimistic locking (`expected_version`) prevents data corruption but may cause frequent `409 CONFLICT` retries for operators unless client-side WebSockets broadcast real-time lock/lease states.
   - *Mitigation:* In Phase 6, implement ephemeral shot-leasing in the Operator Console backend (e.g. "Operator Bob is currently reviewing Shot #4").
2. **Diagnostic Screenshot Data Privacy & Compliance:** Diagnostic screenshots captured during `BLOCKED_AUTH` or `BLOCKED_SECURITY` may contain operator PII or Google account details.
   - *Mitigation:* Enforce strict TTL (default 24 hours), automated client-side redaction of known auth selector bounding boxes, and encryption at rest in object storage as specified in `SECURITY_MODEL.md`.

---

## 9. Review Signature & Metadata

- **Reviewer Role:** `R12_PRODUCT_OPS` (Product / Operator / Human-in-the-loop Architect)
- **Model / Agent:** DeepMind Advanced Agentic Coding Assistant (Antigravity v2.0)
- **Review Round:** C01 Independent Blind Review
- **Session Timestamp:** `2026-08-15T11:30:00+07:00`
- **Conversation ID:** `f1bb45a2-477d-4761-a47b-634853b99730`
- **Submission Status:** Complete, Evidence-Backed, Self-Contained Review
- **Formal Recommendation:** **CONDITIONAL PASS** — Pass subject to adoption of Change Proposals resolving findings `F-R12-001` through `F-R12-008` before v1.0 specification freeze.
