# C02R HEARING TRANSCRIPT: CLUSTER 01 — CANONICAL DOMAIN PROVENANCE & ENTITY MODEL
**CLUSTER_ID:** CLUSTER-01
**FINDINGS_COVERED:** FINDING_001, FINDING_004, FINDING_018, FINDING_042, TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, TECH-017
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R01 (Domain DDD Specialist) & R05 (Data Architect)
- **Position:** The canonical domain entities in `domain-entities.schema.json` previously inverted the primary creative lineage. In film/video production, a `ShotVersion` represents immutable creative direction (duration, camera movement, scene action, character/style constraints). A `PromptVersion` is a compiled realization of a `ShotVersion` tailored for an AI generation engine. Therefore, `PromptVersion` must capture `shot_version_id` (and `shot_id`). When a generation attempt runs, `GenerationJob` must record the immutable tuple: `shot_id`, `shot_version_id`, `prompt_version_id`, plus execution metadata (`provider_id`, `attempt_index`, `provider_job_id`, `flow_track`, timestamps, `normalized_error`). When finished, `Take` references the resulting output media linked back to `job_id`, `shot_version_id`, and `prompt_version_id`.
- **Evidence:** `DATA_MODEL.md` §2.1-2.4 vs `domain-entities.schema.json` lines 120-210.
- **Failure Scenario:** If `ShotVersion` requires `prompt_version_id`, you cannot define a shot before compiling a prompt, and compiling multiple candidate prompts for one shot requires mutating or duplicating shot versions, destroying shot revision history.

## 2. Challenger Attack
- **Challenger:** R15 (Red Team Specialist) & R04 (Contracts Specialist)
- **Attack Vector:**
  1. *Schema Bloat & Circular References:* If `ShotVersion` contains detailed arrays for character, style, and asset references while `GenerationJob` also redundantly holds `shot_id`, `shot_version_id`, and `prompt_version_id`, how do we prevent denormalized data corruption in R02 Core State PostgreSQL?
  2. *Strict UUID Rigidity:* Enforcing strict RFC 4122 UUID v4 regex validation could break compatibility with external systems or legacy mock identifiers during testing if test runners use prefixed string IDs.
  3. *Technology Leakage:* The original schema forced `CharacterVersion` to require `face_embedding_hash` and `StyleVersion` to require `lora_weights_uri`. For text-only or non-LoRA diffusion pipelines, this forces clients to inject dummy hashes or fail schema validation.

## 3. Domain Owner Review
- **Domain Owner:** R05 (Data Specialist)
- **Evaluation:**
  - In PostgreSQL relational mapping (`DATA_MODEL.md`), foreign keys flow naturally: `shots` (1) -> `shot_versions` (N) -> `prompt_versions` (N) -> `generation_jobs` (N) -> `takes` (N).
  - Redundant fields like `shot_id` on `GenerationJob` provide high-performance aggregate querying without multi-table joins, but must be enforced via compound foreign keys: `FOREIGN KEY (shot_id, shot_version_id) REFERENCES shot_versions(shot_id, shot_version_id)`.
  - Creative intent fields in `ShotVersion` (`duration_ms`, `action_description`, `camera_motion`, `environment_settings`, `character_refs`, `style_refs`, `asset_refs`, `constraints`, `continuity_refs`) are essential for compiler reproducibility.
  - `face_embedding_hash` and `lora_weights_uri` must be moved into optional metadata dictionaries (`attributes` / `embedding_metadata`) to preserve model generality.

## 4. Proponent Response
- **Response:**
  - We agree to compound foreign key constraints in R02 and explicit schema typing.
  - For UUIDs, RFC 4122 compliance is mandatory for canonical state safety across distributed message buses. Test suites must generate valid UUIDs rather than weak strings.
  - We accept removing hardcoded LoRA and facial embedding requirements from the base entities, making them optional extension fields under `custom_attributes`.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Keep `PromptVersion` independent of `ShotVersion`, mapping them only at the `GenerationJob` junction table.
- **Why Rejected:** In video production, a prompt is never standalone; it is specifically generated to fulfill the creative intent and constraints of a given shot revision. Decoupling them destroys the semantic compilation trace needed for prompt optimization loops.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-001 amended + CP-016/CP-017 to:
  1. Fix `domain-entities.schema.json` and `DATA_MODEL.md` to establish `ShotVersion` -> `PromptVersion` -> `GenerationJob` -> `Take` lineage.
  2. Restore all creative intent fields to `ShotVersion`.
  3. Expand `AssetVersion` with rights, license, source, and storage metadata.
  4. Make technology-specific fields optional in `CharacterVersion` and `StyleVersion`.
  5. Enforce strict RFC 4122 UUID regex and document JSON Schema fragment entrypoints.
