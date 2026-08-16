# CHANGE PROPOSAL: CP-001 (AMENDED)
**CHANGE_ID:** CP-001
**TITLE:** Canonical Domain Model Provenance & Entity Completeness
**STATUS:** PROPOSED_FOR_VOTE
**DISPOSITION:** AMENDED
**SOURCE_FINDINGS:** TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, TECH-017
**MATERIALLY_AFFECTED_ROLES:** R01 (Domain DDD), R04 (Contracts), R05 (Data), R09 (AI), R02 (Reliability)
**MANDATORY_SIGNOFF_ROLES:** R01 (Domain DDD), R04 (Contracts), R05 (Data)

## 1. Rationale & Problem Description
The domain schema inverted the ShotVersion/PromptVersion lineage, omitted GenerationJob provenance (prompt_version_id, attempt_index, timestamps, normalized_error), dropped ShotVersion creative intent fields, lacked AssetVersion rights metadata, and enforced rigid technology choices (mandatory LoRA/face embeddings). This proposal establishes the true immutable hierarchy: ShotVersion -> PromptVersion -> GenerationJob -> Take.

## 2. Exact Specification Changes
1. `02_contracts/domain-entities.schema.json`:
   - `ShotVersion`: Remove `prompt_version_id` requirement. Add `duration_ms`, `action_description`, `camera_motion`, `environment_settings`, `character_refs`, `style_refs`, `asset_refs`, `constraints`, `continuity_refs`.
   - `PromptVersion`: Require `shot_id` and `shot_version_id`.
   - `GenerationJob`: Require `shot_id`, `shot_version_id`, `prompt_version_id`, `provider_id`, `attempt_index`, `status`, `idempotency_key`. Include `execution_stage`, `provider_job_id`, `lease_token`, `lease_expires_at`, `estimated_cost_credits`, `actual_cost_credits`, `normalized_error`, `requested_at`, `submitted_at`, `completed_at`.
   - `AssetVersion`: Add `source_type`, `license_type`, `rights_attribution`, `origin_uri`, `mime_type`, `byte_size`, `checksum_sha256`.
   - `CharacterVersion` & `StyleVersion`: Make `face_embedding_hash` and `lora_weights_uri` optional under `custom_attributes`.
   - UUID validation: Update `/UUID` to use `format: uuid` and RFC 4122 regex.
2. `01_master/DATA_MODEL.md`: Update entity relationship diagrams and table schemas to match.
3. `03_repo_blueprints/R01_CONTRACTS.md`, `R02_CORE_STATE.md`, `R05_PROMPT_COMPILER.md`: Update entity contracts.

## 3. Capability Preservation Proof
Preserves CAP-01 (Canonical Core State), CAP-05 (Prompt Compiler), and CAP-06 (Assets & Continuity). No capability regression.
