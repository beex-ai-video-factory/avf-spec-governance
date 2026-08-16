# C01 Independent Specialist Review — R09_AI (AI Agent / LLM Systems Architect)

**Reviewer Role:** R09_AI — AI Agent / LLM Systems Architect  
**Review Round:** C01 Independent Blind Review  
**Execution Mode:** Independent Subagent Execution (Isolated)  
**Session ID:** `563742cd-476f-4cd8-9729-563e7f5bc389`  
**Timestamp:** `2026-08-15T11:30:00+07:00`  
**Model & Engine:** Antigravity / DeepMind Advanced Reasoning Engine (`flash` / `pro` architecture)  
**Active Skills & Tools:** `view_file`, `list_dir`, `grep_search`, `write_to_file`, `replace_file_content`, `run_command`  
**Assigned Gap Seed:** GAP-005 (Fallback commercial API provider integration)

---

## 1. Assigned and Inspected Specification Files

The following primary specification files, blueprints, ADRs, contracts, and baseline registers were inspected in detail for this review:

1. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R03_CREATIVE.md` (avf-creative blueprint)
2. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md` (avf-prompt-compiler blueprint)
3. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md` (avf-provider-sdk blueprint)
4. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-005_LLM_STATE_MUTATION.md` (LLM State Mutation ADR)
5. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md` (Canonical architecture, LLM boundaries, execution classification)
6. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md` (Contract families, error taxonomy)
7. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json` (ShotVersion, PromptVersion schemas)
8. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json` (ProviderGenerationRequest schema)
9. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-result.schema.json` (ProviderGenerationResult schema)
10. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md` (GenerationJob state machine transitions)
11. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R04_ASSETS_CONTINUITY.md` (Asset & continuity resolution)
12. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R06_WORKFLOW.md` (Durable orchestration & retry coordination)
13. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md` (Multimodal QC evaluation & scoring)
14. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-003_PROVIDER_ABSTRACTION.md` (Provider Abstraction ADR)
15. `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-006_RETRY_POLICY.md` (Retry Policy ADR)
16. `review-session/C00_FINAL/C00_GAP_TO_C01_SEED_REGISTER.md` (Baseline gap register; GAP-005 seed)
17. `review-session/C00_FINAL/PROTECTED_CAPABILITY_REGISTER.md` (C-01 through C-19)
18. `review-session/C00_FINAL/SYSTEM_INVARIANT_INVENTORY.md` (INV-001 through INV-020)

---

## 2. Invariants and Contracts Relevant to AI / LLM Systems

The following architectural invariants and protected capabilities govern the AI, LLM, prompt compilation, and provider gateway domains:

- **INV-002 (`R02_CORE_STATE` / `R05_PROMPT_COMPILER`):** A `GenerationJob` references immutable `ShotVersion` and `PromptVersion` identifiers.
- **INV-003 (`R06_WORKFLOW` / `R07_PROVIDER_SDK`):** Every external side effect has a deterministic idempotency key (`gen:{project_id}:{shot_version_id}:{prompt_version_id}:{provider}:{attempt_no}`).
- **INV-004 (`R02_CORE_STATE` / `R03_CREATIVE` / `R05_PROMPT_COMPILER` / `R11_QC` / `ADR-005`):** LLMs and agents may propose state changes but cannot directly mutate canonical project state.
- **INV-006 (`R04_ASSETS_CONTINUITY` / `R02_CORE_STATE`):** Every generated artifact preserves provenance and content checksum.
- **INV-008 (`R07_PROVIDER_SDK` / `ADR-003`):** Provider adapters cannot directly modify Project/Shot records.
- **INV-009 (`R11_QC` / `R06_WORKFLOW` / `ADR-006`):** QC models recommend; deterministic policy decides retry/approval escalation.
- **INV-010 (`R06_WORKFLOW` / `R05_PROMPT_COMPILER`):** Technical retries do not create new PromptVersions.
- **INV-011 (`R03_CREATIVE` / `R05_PROMPT_COMPILER` / `R06_WORKFLOW`):** Creative retries create a new attempt and create a new PromptVersion when prompt semantics changed.
- **INV-018 (`R06_WORKFLOW` / `R07_PROVIDER_SDK`):** Budget limits are enforced by deterministic policy before external generation requests.
- **Protected Capabilities:**
  - **C-02 (Immutable creative artifacts):** Append-only versioning for ScriptVersion, ShotVersion, PromptVersion.
  - **C-03 (Provenance & reproducibility):** Lineage tracing from Take -> PromptVersion -> ShotVersion -> Compiler Version -> Provider.
  - **C-04 (Provider abstraction):** Isolation behind `VideoGenerationProvider` interface.
  - **C-10 (Deterministic fake provider):** FakeVideoProvider supporting delay, simulated failure, corrupt output, rate limits.
  - **C-16 (Automated + human QC):** Technical checks + MLLM semantic checks.
  - **C-17 (Future provider extensibility):** Seamless integration of commercial video APIs.
  - **C-18 (Future agent/model extensibility):** Hot-swappable LLM models without core pipeline mutation.

---

## 3. Executive Summary & Specialist Assessment

As the **AI Agent / LLM Systems Architect (R09_AI)**, I have audited the specification against the core principles of bounded autonomy, deterministic compilation, structured output validation/repair, LLM hallucination containment, and provider capability isolation.

### Key Architectural Findings:
1. **Resolution of GAP-005 (Commercial Fallback Provider Adapter Architecture):** The blueprint mentions future commercial APIs in diagrams and ADR-003, but `R07_PROVIDER_SDK` and `R05_PROMPT_COMPILER` completely lack a concrete HTTP/REST provider adapter blueprint and a Capability Negotiation Protocol. If Google Flow is blocked by CAPTCHA/auth challenges, the system has no specified mechanism to translate prompt/asset parameters to a commercial fallback API (e.g. Runway Gen-3 / Veo 2 / Kling).
2. **Elimination of Non-Determinism in Prompt Compiler (`R05`):** `R05_PROMPT_COMPILER` introduces an architectural contradiction by claiming to support "optional bounded LLM enrichment" while asserting `input_hash` immutability and idempotency. LLM enrichment inside the compiler breaks deterministic replay and provenance (INV-002, INV-006). All LLM enrichment must be strictly quarantined in `avf-creative` (R03) as an explicit, versioned upstream proposal stage, keeping `avf-prompt-compiler` (R05) 100% pure deterministic string/template compilation.
3. **Contract Gap in `promptVersion` (`domain-entities.schema.json`):** The schema stores only `prompt_text: string`, dropping negative constraints, asset reference bindings (first frame vs character ref), aspect ratios, duration, and camera parameters. This breaks take reproducibility (C-03).
4. **Formalization of Structured Output Repair & Entity Whitelisting in `R03`:** Structured JSON repair in `avf-creative` lacks an explicit multi-turn bounding protocol and referential validation against project entity IDs, risking unhandled foreign key crashes when LLMs hallucinate UUIDs.
5. **Confidence-Gated MLLM QC Escalation in `R11`:** Multimodal QC models must output explicit confidence scores that deterministic policy engines (`ADR-006`) evaluate to prevent noisy scores from triggering expensive, wasteful automatic retry loops.

---

## 4. Evidence-Backed Findings (Council Finding Format)

### Finding F-R09-001: Missing Concrete Commercial Fallback Provider Adapter Blueprint and Capability Negotiation Protocol (GAP-005)

```yaml
FINDING_ID: F-R09-001
ROLE: R09_AI
SEVERITY: HIGH
CATEGORY: ARCHITECTURE / CONTRACTS / CAPABILITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/MASTER_BLUEPRINT.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json
AFFECTED_CONTRACTS:
  - provider-request.schema.json
  - provider-result.schema.json
  - CONTRACTS_OVERVIEW.md
  - C-04 (Provider abstraction)
  - C-17 (Future provider extensibility)
  - INV-008 (Provider adapters boundary)
  - GAP-005 (Fallback commercial API provider integration)
EVIDENCE:
  - MASTER_BLUEPRINT.md Section 3 diagram includes "Future API Providers (APIX)", and Section 8 states Google Flow is one adapter.
  - R07_PROVIDER_SDK.md Section "MVP VERSION" specifies only "Interfaces + FakeVideoProvider + Google Flow capability profile contract", deferring real API adapters to "PRODUCTION VERSION".
  - provider-request.schema.json defines capability as a coarse enum ["text_to_video", "image_to_video", "frames_to_video", "reference_to_video", "image_generation"], but contains no structured schema for provider capability negotiation (aspect ratios, duration steps, token limits, reference image count limits, negative prompt support).
  - R05_PROMPT_COMPILER.md lists `RecompileForProvider` in PUBLIC API, but defines no capability mapping or syntax degradation rules when switching from Google Flow to a commercial API provider.
FAILURE_SCENARIO: |
  In production, Google Flow automation encounters a blocking CAPTCHA challenge (`BLOCKED_SECURITY`) or breaking DOM redesign (`BLOCKED_UI_CHANGE`).
  The workflow attempts to fall back to an external commercial API provider (e.g. Runway Gen-3 or Google Veo API) to complete an urgent commercial project.
  Because R07 has no concrete commercial REST adapter blueprint, and R05 has no capability matrix defining how Google Flow camera instructions and multi-asset references map into the commercial API's parameters (e.g. Runway Gen-3 only supports 5s/10s fixed durations and single first-frame/last-frame image inputs), the prompt recompilation fails with `UNSUPPORTED_CAPABILITY` or sends a malformed payload.
  The video factory experiences an unrecoverable full pipeline stall.
WHY_IT_MATTERS: |
  The core value proposition of AVF is vendor replaceability and business continuity when browser automation is disrupted.
  Without a concrete reference commercial API adapter and a formal Capability Negotiation Engine in R07 and R05, provider replaceability is purely aspirational, leaving the system dangerously vulnerable to Google Flow downtime.
PROPOSED_SOLUTION: |
  1. Update R07_PROVIDER_SDK.md to specify a standardized `HttpVideoProviderAdapter` base class with concrete lifecycle methods (asynchronous job polling, webhook callback handling, signed URL upload, exponential backoff, and error taxonomy translation).
  2. Implement a reference commercial API adapter (e.g. `CommercialApiVideoProvider` targeting Runway Gen-3 or Veo API / Fal.ai gateway) in Phase 1 alongside `FakeVideoProvider` to validate multi-provider interchangeability.
  3. Define a formal `ProviderCapabilityDescriptor` schema in `avf-contracts` specifying:
     - `provider_family`: string (e.g. "google_flow", "runway_gen3", "veo_2", "luma_ray2")
     - `supported_modalities`: array of enums
     - `supported_aspect_ratios`: array of strings (e.g. ["16:9", "9:16", "1:1"])
     - `duration_increments_sec`: array of numbers (e.g. [5, 10])
     - `max_prompt_length_chars`: integer
     - `supports_negative_prompt`: boolean
     - `max_reference_images`: integer
     - `camera_motion_control_type`: enum ["DIRECT_TEXT", "VECTOR_JSON", "UNSUPPORTED"]
  4. In R05_PROMPT_COMPILER.md, specify a deterministic `CapabilityDegradationPolicy` that automatically adapts a semantic shot plan to the target provider's capabilities (e.g. appending negative constraints into main prompt text if the provider lacks a native negative prompt field; degrading multi-image references to primary subject image).
ALTERNATIVES_CONSIDERED: |
  - Alternative A: Keep commercial API providers deferred entirely to Phase 3/4. Rejected because without a reference API adapter, contract tests cannot prove that `VideoGenerationProvider` interface is truly provider-neutral.
  - Alternative B: Hardcode provider-specific branches in workflow orchestration. Rejected because it violates C-04 and pollutes core workflow logic with vendor-specific rules.
CAPABILITY_IMPACT: Preserves and strengthens C-04 (Provider abstraction) and C-17 (Future provider extensibility). Resolves GAP-005.
COMPATIBILITY_IMPACT: Fully backward-compatible; extends `avf-contracts` with capability descriptor schema.
MIGRATION_IMPACT: Zero breaking schema changes; adds new capability metadata structures.
TEST_OR_BENCHMARK_REQUIRED: Conformance test suite running identical test vectors across `FakeVideoProvider`, `CommercialApiVideoProvider`, and `GoogleFlowAdapter`.
RESIDUAL_RISK: Commercial video provider APIs change rapidly; adapter requires periodic maintenance.
CONFIDENCE: 95%
```

---

### Finding F-R09-002: Contradiction Between LLM Enrichment and Prompt Compilation Determinism in R05

```yaml
FINDING_ID: F-R09-002
ROLE: R09_AI
SEVERITY: CRITICAL
CATEGORY: DETERMINISM / PROVENANCE / LLM_BOUNDARY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R03_CREATIVE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-005_LLM_STATE_MUTATION.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json ($defs.promptVersion)
  - C-02 (Immutable creative artifacts)
  - C-03 (Provenance and reproducibility)
  - INV-002 (GenerationJob references immutable versions)
  - INV-006 (Artifact provenance and checksums)
  - INV-010 (Technical retries do not create new PromptVersions)
EVIDENCE:
  - R05_PROMPT_COMPILER.md states under "Execution Type": "Deterministic-first with optional bounded LLM enrichment".
  - R05_PROMPT_COMPILER.md states under "IDEMPOTENCY": "Same normalized inputs + compiler version => same input_hash; output expected semantically repeatable."
  - R05_PROMPT_COMPILER.md states under "FAILURE MODES": "LLM enrichment invalid".
  - domain-entities.schema.json defines `promptVersion` with `input_hash: string` and `compiler_version: string`.
FAILURE_SCENARIO: |
  A generation job fails due to an intermittent network disconnect during video download (`TRANSIENT_TRANSPORT`).
  According to INV-010, the technical retry must reuse the exact same `PromptVersion` without re-generating creative content.
  However, in a workflow replay or recovery where `CompilePrompt` is re-evaluated, if R05 invokes an LLM for enrichment, the non-deterministic LLM generation produces different prompt wording ("dramatic cinematic lighting with soft mist" vs "moody film noir with volumetric haze").
  If `input_hash` was calculated from inputs before enrichment, the same `input_hash` now corresponds to different prompt text, silently breaking cryptographic immutability and provenance tracking.
  If `input_hash` is calculated after enrichment, a technical retry generates a new `input_hash`, violating INV-010 and triggering an invalid creative retry cycle.
WHY_IT_MATTERS: |
  Non-determinism inside a compiler destroys reproducibility (C-03) and state machine invariants (INV-002, INV-010).
  A compiler MUST be a pure deterministic function: `f(inputs, version) = output`.
  Embedding stochastic LLM calls inside a component labeled "Stateless service/library" corrupts the audit trail and makes debugging generation failures impossible.
PROPOSED_SOLUTION: |
  1. Enforce a strict architectural boundary: `avf-prompt-compiler` (R05) MUST be 100% pure deterministic string templating, syntax normalization, and capability mapping with ZERO LLM dependencies.
  2. Move all semantic prompt enrichment, stylistic descriptor expansion, and creative prose generation into `avf-creative` (R03).
  3. In `avf-creative` (R03), prompt enrichment produces an immutable `EnrichedShotPlan` or `CreativePromptProposal` with explicit model provenance (`model_id`, `temperature=0`, `seed`, `template_version`).
  4. R05 takes this structured, already-enriched shot specification and deterministically compiles it into provider-specific syntax templates (`google_flow_syntax_v1`, `runway_gen3_syntax_v1`).
  5. Calculate `input_hash = SHA256(canonical_json(ShotVersion, ResolvedAssetSet, ProviderCapabilities, CompilerVersion))`.
ALTERNATIVES_CONSIDERED: |
  - Alternative A: Allow LLM enrichment in R05 but pin temperature=0 and random seed. Rejected because closed commercial LLM APIs (e.g. OpenAI/Gemini/Anthropic) do not guarantee bitwise reproducible output across backend model versions even at temperature=0.
  - Alternative B: Store LLM outputs in an ephemeral cache inside R05. Rejected because R05 is stateless and cannot own persistent state; caching violates C-01.
CAPABILITY_IMPACT: Protects C-02, C-03, and INV-002 with 100% mathematical determinism.
COMPATIBILITY_IMPACT: None on external contracts; clarifies internal responsibility boundary between R03 and R05.
MIGRATION_IMPACT: Refactors LLM enrichment tasks into R03; simplifies R05 implementation and testing.
TEST_OR_BENCHMARK_REQUIRED: Golden test suite in R05 asserting 1,000 iterations of `CompilePrompt` over identical inputs produce 100% identical byte-for-byte `prompt_text` and `input_hash`.
RESIDUAL_RISK: None.
CONFIDENCE: 99%
```

---

### Finding F-R09-003: Incomplete `promptVersion` Schema in Domain Entities Contract Failing Multi-Modal Parameter Capture

```yaml
FINDING_ID: F-R09-003
ROLE: R09_AI
SEVERITY: HIGH
CATEGORY: CONTRACTS / DATA_MODEL / REPRODUCIBILITY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/domain-entities.schema.json
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/provider-request.schema.json
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R05_PROMPT_COMPILER.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json ($defs.promptVersion)
  - provider-request.schema.json
  - C-02 (Immutable creative artifacts)
  - C-03 (Provenance and reproducibility)
  - INV-002 (GenerationJob references immutable PromptVersion)
EVIDENCE:
  - domain-entities.schema.json defines `promptVersion` with properties:
    `prompt_version_id`, `shot_version_id`, `version`, `provider_family`, `compiler_version`, `prompt_text`, `input_hash`.
  - provider-request.schema.json requires:
    `prompt`, `negative_constraints` (array of strings), `asset_refs` (array of `{ asset_id, role }`), and `generation_options` (object).
  - domain-entities.schema.json completely omits negative constraints, asset reference role bindings, aspect ratios, durations, and camera parameters from the `promptVersion` definition.
FAILURE_SCENARIO: |
  A user configures a shot with reference assets (e.g. `character_face_asset_id` as subject reference, `environment_asset_id` as background), a 9:16 aspect ratio, and negative constraints ("blurry, extra limbs, watermark").
  R05 compiles these into a `ProviderGenerationRequest`.
  However, Core State persists the `PromptVersion` in PostgreSQL according to `domain-entities.schema.json`, which only saves `prompt_text`.
  Three weeks later, an operator chooses "Regenerate from PromptVersion" to produce a second take.
  Core State constructs the new request from the stored `PromptVersion`. Because negative constraints, asset role bindings, and aspect ratios were never stored in `PromptVersion`, the regenerated job runs without negative prompts or asset references, producing a completely inconsistent video that fails QC.
WHY_IT_MATTERS: |
  Modern video generation models are multi-modal and parameter-driven; prompt text is only one part of the input.
  An entity named `PromptVersion` that only stores a text string cannot satisfy C-03 (Full chain of custody: every Take traces to exact PromptVersion and assets) or INV-006.
PROPOSED_SOLUTION: |
  Update `domain-entities.schema.json` to expand `$defs.promptVersion` to capture all compiled multi-modal parameters:
  ```json
  "promptVersion": {
    "type": "object",
    "required": [
      "prompt_version_id",
      "shot_version_id",
      "version",
      "provider_family",
      "compiler_version",
      "prompt_text",
      "input_hash"
    ],
    "properties": {
      "prompt_version_id": { "type": "string", "format": "uuid" },
      "shot_version_id": { "type": "string", "format": "uuid" },
      "version": { "type": "integer", "minimum": 1 },
      "provider_family": { "type": "string" },
      "compiler_version": { "type": "string" },
      "prompt_text": { "type": "string" },
      "negative_prompt": { "type": ["string", "null"] },
      "compiled_asset_bindings": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["asset_id", "role"],
          "properties": {
            "asset_id": { "type": "string", "format": "uuid" },
            "role": { "type": "string" }
          }
        }
      },
      "generation_parameters": {
        "type": "object",
        "properties": {
          "aspect_ratio": { "type": "string" },
          "duration_sec": { "type": "number" },
          "camera_motion": { "type": "object" },
          "seed": { "type": ["integer", "null"] }
        },
        "additionalProperties": true
      },
      "input_hash": { "type": "string" }
    }
  }
  ```
ALTERNATIVES_CONSIDERED: |
  - Alternative A: Encode all negative constraints and asset IDs into a single JSON-serialized string inside `prompt_text`. Rejected because it ruins searchability, lints, and provider-specific syntax compilation.
CAPABILITY_IMPACT: Ensures 100% reproducibility of generated takes (C-03).
COMPATIBILITY_IMPACT: Minor additive schema extension in `domain-entities.schema.json`.
MIGRATION_IMPACT: Trivial update to PostgreSQL schema in `avf-core-state`.
TEST_OR_BENCHMARK_REQUIRED: Round-trip serialization test converting `PromptVersion` entity to `ProviderGenerationRequest` and validating schema equality.
RESIDUAL_RISK: None.
CONFIDENCE: 98%
```

---

### Finding F-R09-004: Underspecified Structured Output Repair Protocol and Referential Integrity Validation in Creative Service (R03)

```yaml
FINDING_ID: F-R09-004
ROLE: R09_AI
SEVERITY: HIGH
CATEGORY: LLM_RELIABILITY / VALIDATION / BOUNDED_AUTONOMY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R03_CREATIVE.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/CONTRACTS_OVERVIEW.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-005_LLM_STATE_MUTATION.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json ($defs.shotVersion)
  - CONTRACTS_OVERVIEW.md (Error taxonomy)
  - ADR-005 (LLM State Mutation)
  - INV-004 (LLM proposal validation before state mutation)
EVIDENCE:
  - R03_CREATIVE.md states under "RETRY STRATEGY": "Schema repair then max bounded model retry; never infinite creative loop."
  - R03_CREATIVE.md states under "DONE WHEN": "invalid output reaches explicit failure after bounded repair."
  - The blueprint specifies no concrete bounding constant (e.g. `MAX_REPAIR_ATTEMPTS = 2`), no repair prompt feedback contract, and no referential validation rule for foreign keys generated by LLMs (e.g. `character_version_ids`, `style_version_id`, `asset_ids`).
FAILURE_SCENARIO: |
  During `GenerateShotPlan`, an LLM transforms a creative brief into structured `ShotVersion` proposals.
  The LLM generates valid JSON matching the schema, but hallucinates a random UUID `a8f9c42b-...` in `character_version_ids`.
  Syntactic JSON Schema validation passes because the field is a valid UUID string format.
  The proposal is sent to `avf-core-state` to be committed.
  When `avf-core-state` executes the database insert, PostgreSQL throws a foreign key constraint violation error.
  Because R03 did not catch this semantic violation or attempt repair, the workflow crashes with an unhandled database exception (`INTERNAL_ERROR`) instead of a graceful creative retry or operator escalation.
WHY_IT_MATTERS: |
  LLMs frequently hallucinate identifiers or generate near-miss JSON structures.
  If structured output validation only checks syntax without validating referential integrity against the project's active entity whitelist, invalid proposals escape the service boundary, crashing downstream relational databases.
  Furthermore, without an explicit repair loop budget and repair error taxonomy, LLM workers can either loop unpredictably or fail silently.
PROPOSED_SOLUTION: |
  1. Specify a mandatory 2-Stage Output Validation Pipeline in `R03_CREATIVE.md`:
     - **Stage 1 (Syntactic Validation):** Strict validation against `avf-contracts` JSON Schema / Pydantic models (using structured output / constrained grammar decoding where available).
     - **Stage 2 (Semantic Referential Validation):** Whitelist validation asserting that all UUIDs in `character_version_ids`, `style_version_id`, and `asset_ids` exist in the provided input context.
  2. Formalize the Bounded Repair Protocol in `R03_CREATIVE.md`:
     - Constant: `MAX_SCHEMA_REPAIR_ATTEMPTS = 2`.
     - Repair prompt structure: Injection of original prompt + malformed JSON output + exact JSON Schema / referential validation error diff with instruction to fix ONLY the schema/foreign key errors.
  3. Add normalized error class `CREATIVE_REPAIR_EXHAUSTED` (or sub-code under `VALIDATION_ERROR`) in `CONTRACTS_OVERVIEW.md`. When repair attempts exceed limit, R03 returns this typed error, allowing `R06_WORKFLOW` to route to `HUMAN_REVIEW` or fallback template without process crash.
ALTERNATIVES_CONSIDERED: |
  - Alternative A: Let Core State reject invalid foreign keys with HTTP 422. Rejected because R03 is the owner of LLM structured output validation and must repair errors before sending proposals over the wire.
CAPABILITY_IMPACT: Strengthens INV-004, ADR-005, and C-18.
COMPATIBILITY_IMPACT: Backward-compatible contract refinement.
MIGRATION_IMPACT: Adds semantic validator in `avf-creative`.
TEST_OR_BENCHMARK_REQUIRED: Unit tests with mock LLM emitting invalid JSON and hallucinated UUIDs, verifying exact 2 repair cycles and graceful `CREATIVE_REPAIR_EXHAUSTED` error.
RESIDUAL_RISK: None.
CONFIDENCE: 96%
```

---

### Finding F-R09-005: Undefined Confidence Gating and Semantic Score Drift Protection in Multimodal QC (R11)

```yaml
FINDING_ID: F-R09-005
ROLE: R09_AI
SEVERITY: MEDIUM
CATEGORY: AI_EVALUATION / QUALITY_CONTROL / RETRY_POLICY
AFFECTED_FILES:
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R11_QC.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-006_RETRY_POLICY.md
  - AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/02_contracts/STATUS_STATE_MACHINES.md
AFFECTED_CONTRACTS:
  - domain-entities.schema.json ($defs.qcResult)
  - ADR-006 (Retry Policy)
  - INV-009 (QC models recommend; deterministic policy decides)
  - INV-018 (Budget limits enforced by deterministic policy)
  - C-16 (Automated + human QC)
EVIDENCE:
  - R11_QC.md states: "Hybrid deterministic + MLLM ... low confidence can recommend HUMAN_REVIEW."
  - R11_QC.md states: "Technical and semantic failures separated; recommendation is typed and policy-neutral."
  - ADR-006_RETRY_POLICY.md states: "Final retry decision is made by deterministic policy engine, not LLM."
  - However, neither R11_QC nor ADR-006 defines the numeric threshold for `confidence` or how the deterministic policy engine handles low-confidence scores vs outright failure scores.
FAILURE_SCENARIO: |
  A generated video take features stylized low-key lighting.
  The MLLM semantic evaluator in R11 evaluates character consistency and assigns a borderline low score of `0.58` (pass threshold = `0.60`), but with a very low confidence score of `0.35` due to dark shadows.
  Because the deterministic retry policy engine in R06 only inspects `score < 0.60`, it blindly triggers an automated `CREATIVE_RETRY`.
  The workflow compiles a new prompt and submits a costly second generation job.
  The second take also receives an ambiguous score, rapidly burning through the project's generation budget (`BLOCKED_BUDGET`) without ever consulting an operator.
WHY_IT_MATTERS: |
  Multimodal LLMs are susceptible to perceptual ambiguity, lighting changes, and scoring hallucinations.
  Without confidence gating, borderline or uncertain MLLM evaluation scores cause spurious automated re-generation loops, wasting money and provider credits.
PROPOSED_SOLUTION: |
  1. Define a standardized `QCResult` structure in `avf-contracts`:
     ```json
     {
       "qc_result_id": "uuid",
       "generation_job_id": "uuid",
       "take_id": "uuid",
       "technical_qc": {
         "passed": true,
         "duration_sec": 5.02,
         "black_frame_ratio": 0.0,
         "freeze_frame_max_sec": 0.0,
         "audio_loudness_lufs": -14.1
       },
       "semantic_qc": {
         "overall_score": 0.58,
         "confidence": 0.35,
         "dimension_scores": {
           "character_consistency": 0.55,
           "motion_naturalness": 0.70,
           "prompt_adherence": 0.65
         },
         "detected_issues": ["POOR_LIGHTING_AMBIGUITY"]
       },
       "evaluator_provenance": {
         "model_id": "gemini-1.5-pro",
         "evaluator_version": "qc-semantic@1.1.0",
         "sampled_frame_count": 8
       }
     }
     ```
  2. Update `ADR-006` and `avf-workflow` deterministic policy engine with a **Confidence Gating Rule**:
     - IF `technical_qc.passed == false` => `TECHNICAL_RETRY` (up to tech budget).
     - IF `semantic_qc.overall_score >= PASS_THRESHOLD` (e.g. 0.70) => `APPROVED`.
     - IF `semantic_qc.overall_score < PASS_THRESHOLD` AND `semantic_qc.confidence >= CONFIDENCE_THRESHOLD` (e.g. 0.75) => `CREATIVE_RETRY` (up to creative budget).
     - IF `semantic_qc.overall_score < PASS_THRESHOLD` AND `semantic_qc.confidence < CONFIDENCE_THRESHOLD` (0.75) => `HUMAN_REVIEW` (halt automation, alert operator with explanation).
  3. Require golden labeled evaluation benchmark sets in `R11_QC` to calibrate confidence scores across model versions.
ALTERNATIVES_CONSIDERED: |
  - Alternative A: Re-run semantic evaluation with a second MLLM. Rejected for MVP/V1 due to cost and latency overhead; human escalation is safer.
CAPABILITY_IMPACT: Protects C-16, C-09, and INV-018 from wasteful retry runaway.
COMPATIBILITY_IMPACT: Additive schema clarification in contracts.
MIGRATION_IMPACT: None.
TEST_OR_BENCHMARK_REQUIRED: Unit tests in R06 policy engine validating confidence routing matrix.
RESIDUAL_RISK: Minor tuning required for confidence calibration across different video styles.
CONFIDENCE: 92%
```

---

## 5. Architectural Deep-Dive & Evaluation Across Assigned Focus Areas

### 5.1 Prompt Compilation Determinism & Compiler Versioning
- **Current State:** R05 mixes template compilation with "optional bounded LLM enrichment".
- **Analysis:** In high-throughput media pipelines, prompt compilation must be completely deterministic and idempotent. If two identical requests yield two different compiled prompts, cache invalidation, golden test validation, and cross-attempt comparison break down.
- **Verdict:** LLM enrichment must be quarantined in `avf-creative` (R03). `avf-prompt-compiler` (R05) must remain a pure, deterministic compiler versioned semantically (`google_flow@1.0.0`, `runway_gen3@1.0.0`) and covered by regression-proof golden prompt fixtures.

### 5.2 Structured Output Repair & Hallucination Containment
- **Current State:** R03 states outputs are validated proposals, but lacks multi-turn bounds and referential validation.
- **Analysis:** Schema validation alone is insufficient for AI agents that generate domain graphs. If an LLM hallucinates an entity ID, it passes syntax parsing but violates database foreign keys.
- **Verdict:** Two-tier validation (Syntactic Schema -> Referential Whitelist) paired with a bounded 2-turn error feedback reflection loop (`MAX_SCHEMA_REPAIR_ATTEMPTS = 2`) is required before proposals are emitted.

### 5.3 Bounded Autonomy & Containment of "Magical Agents"
- **Current State:** ADR-005 establishes that LLMs propose while Core State commits.
- **Analysis:** This is a sound, critical architectural invariant (INV-004). However, R03 mentions "agent only for explicitly approved multi-step research".
- **Verdict:** We must strictly specify that any research subagent runs in a sandboxed, read-only environment without credentials to mutation APIs or external side-effect execution ports, operating under hard step and timeout limits (e.g. max 5 tool calls, 30s timeout).

### 5.4 Provider Capability Adapters & Commercial Fallback (GAP-005)
- **Current State:** Gap seed GAP-005 correctly flagged the lack of a commercial fallback API adapter blueprint.
- **Analysis:** Relying solely on Google Flow browser automation creates an unacceptable single point of failure. A commercial API adapter (e.g. Runway / Veo API) must be architected in R07 with a formal Capability Descriptor Schema in `avf-contracts` and degradation policies in R05.
- **Verdict:** Finding F-R09-001 completely resolves GAP-005 with a concrete technical specification.

---

## 6. Proven Defects vs. Uncertainties Needing an Empirical Spike

| Item | Classification | Rationale | Recommended Action |
|---|---|---|---|
| **R05 LLM Enrichment Non-Determinism** | **PROVEN DEFECT** | Violates mathematical determinism, INV-002, and INV-006. | Enforce 100% deterministic R05; quarantine LLM enrichment in R03. |
| **`promptVersion` Schema Missing Parameters** | **PROVEN DEFECT** | Drops negative constraints, aspect ratios, and asset role bindings, breaking take reproducibility. | Update `domain-entities.schema.json` with multi-modal fields. |
| **Lack of Commercial Fallback Adapter (GAP-005)** | **PROVEN DEFECT** | Blueprint lacks concrete API adapter architecture and capability negotiation schema. | Add `HttpVideoProviderAdapter` and `ProviderCapabilityDescriptor` contract. |
| **R03 Hallucinated Foreign Keys** | **PROVEN DEFECT** | Syntactic validation allows invalid UUIDs that crash PostgreSQL inserts. | Mandate Stage 2 Referential Validation and 2-turn repair bounding. |
| **MLLM Semantic QC Confidence Calibration** | **UNCERTAINTY / SPIKE** | Optimal confidence threshold varies by video aesthetic and lighting conditions. | Execute a Phase 1 calibration spike with 100 labeled video clips to establish baseline confidence curves. |

---

## 7. Residual Risks and Uncertainties

1. **Third-Party Commercial API Volatility:** Commercial video generation APIs (Runway, Luma, Veo, Sora) frequently change request schemas, rate limits, and pricing. While `ProviderCapabilityDescriptor` isolates the core from these changes, adapter maintenance in R07 will require ongoing monitoring.
2. **MLLM Frame Sampling Tradeoffs:** In R11, sampling 8 frames vs 16 frames per 5-second video affects evaluation latency and cost. Empirical benchmarking is required during Phase 2 to optimize frame selection algorithms.

---

## 8. Formal Signature & Review Declaration

I hereby certify that this review was conducted independently in accordance with the Council Governance Charter and Role Charter for **R09_AI**. I have not consulted other specialist reviews prior to submitting this raw review.

- **Role:** R09_AI — AI Agent / LLM Systems Architect
- **Model:** Antigravity Reasoning System (`flash` / `pro` dual reasoning profile)
- **Review Round:** C01 Independent Blind Review
- **Session ID:** `563742cd-476f-4cd8-9729-563e7f5bc389`
- **Timestamp:** `2026-08-15T11:30:00+07:00`
- **Submission Path:** `review-session/C01/ROLE_REVIEWS/RAW/R09_RAW.md`
- **Declaration:** *I do not approve my own proposed changes; findings are submitted to the Council for cross-examination and formal voting.*
