# C03R SOLUTION PACKAGE 01: CANONICAL PROVENANCE & DATA MODEL
**SOLUTION_ID:** SOL-01
**FINDINGS_ADDRESSED:** TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, TECH-017
**DATE:** 2026-08-15
**STATUS:** DESIGN_COMPLETE

---

## 1. Problem Statement
The prior frozen specification suffered from five major data model defects:
1. Inverted/muddled provenance: `ShotVersion` required `prompt_version_id`, while `PromptVersion` only referenced `shot_id` instead of `shot_version_id`.
2. Missing `GenerationJob` provenance: `GenerationJob` omitted `prompt_version_id`, `shot_id`, timestamps, attempt index, and normalized error fields.
3. Loss of `ShotVersion` creative intent fields (duration, camera motion, action, constraints).
4. Incomplete `AssetVersion` metadata (rights, source type, attribution).
5. Over-coupled technology specifics (hardcoded mandatory LoRA and face embedding fields).

---

## 2. Options Analysis

### Option A: Unified Hierarchical Immutable Provenance (Recommended)
- **Architecture:** 
  - `ShotVersion` represents creative intent. Schema contains: `shot_version_id`, `shot_id`, `version_number`, `duration_ms`, `action_description`, `camera_motion`, `environment_settings`, `character_refs`, `style_refs`, `asset_refs`, `constraints`, `continuity_refs`, `created_at`. It does **not** contain `prompt_version_id`.
  - `PromptVersion` represents compiled prompt for an AI engine. Schema contains: `prompt_version_id`, `shot_id`, `shot_version_id`, `version_number`, `target_provider`, `positive_prompt`, `negative_prompt`, `parameters`, `ast_snapshot`, `created_at`.
  - `GenerationJob` represents an execution attempt. Schema contains: `job_id`, `project_id`, `shot_id`, `shot_version_id`, `prompt_version_id`, `provider_id`, `flow_track`, `idempotency_key`, `status`, `execution_stage`, `attempt_index`, `max_attempts`, `provider_job_id`, `lease_token`, `lease_expires_at`, `estimated_cost_credits`, `actual_cost_credits`, `normalized_error`, `requested_at`, `submitted_at`, `completed_at`, `entity_version`.
  - `Take` represents generated output asset. Schema contains: `take_id`, `shot_id`, `shot_version_id`, `prompt_version_id`, `job_id`, `take_number`, `storage_uri`, `mime_type`, `byte_size`, `checksum_sha256`, `duration_ms`, `qc_status`, `qc_score`, `created_at`.
  - Decouple LoRA and face embeddings into optional attributes under `CharacterVersion` and `StyleVersion`.
  - Stricten UUID format using RFC 4122 pattern and JSON Schema `format: uuid`.
- **Exact Normative Files to Change:**
  - `02_contracts/domain-entities.schema.json`
  - `01_master/DATA_MODEL.md`
  - `02_contracts/CONTRACTS_OVERVIEW.md`
  - `03_repo_blueprints/R01_CONTRACTS.md`
  - `03_repo_blueprints/R02_CORE_STATE.md`
  - `03_repo_blueprints/R05_PROMPT_COMPILER.md`
- **Migration & Compatibility:** Fully backwards-compatible with Master Blueprint v0.9.0 intent. Replaces flawed v1.0.0-rc draft schema.
- **Producer / Consumer Impact:** R01 exports updated TypeScript types. R02 implements compound foreign keys. R05 compiles prompts referencing `shot_version_id`.
- **Idempotency & Recovery:** `GenerationJob` idempotency key incorporates `shot_version_id`, `prompt_version_id`, `provider_id`, and `attempt_index`.
- **Capability Delta:** 100% preservation of CAP-01 (Canonical Core State), CAP-05 (Prompt Compiler), and CAP-06 (Assets & Continuity).

### Option B: Flat Execution Junction Model
- **Architecture:** Keep `ShotVersion` and `PromptVersion` completely unlinked; create a junction entity `ShotPromptBinding` that links them only at execution time.
- **Drawbacks:** Requires an extra entity and database table for every prompt revision, adds complexity to R05 Prompt Compiler query paths, and makes timeline visualization in R13 Operator Console unintuitive.

---

## 3. Decision
**Selected: Option A.** Option A directly reflects domain truth, provides bulletproof provenance, and fulfills all requirements of TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, and TECH-017.
