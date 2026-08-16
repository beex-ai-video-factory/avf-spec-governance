# DOMAIN OWNER ARCHITECTURAL REVIEW & VERDICT
## Cluster 01: Canonical Domain Provenance & Entity Model
**DOMAIN_OWNER:** R05 (Data Architect)  
**AFFILIATION:** AI Video Factory Architecture Council — C02R Genuine Adversarial Cross-Examination  
**TARGET_SPEC_VERSION:** v1.0.0 Freeze Candidate  
**DOCUMENT_STATUS:** AUTHORITATIVE_VERDICT  
**DATE:** 2026-08-15  
**CORRESPONDING_FINDINGS:** FINDING_001, FINDING_004, FINDING_018, FINDING_042, TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, TECH-017  

---

## 1. Executive Summary & Domain Authority Statement

As the Data Architect and designated Domain Owner for **Cluster 01 (Canonical Domain Provenance & Entity Model)**, I have completed an exhaustive review of the proposals submitted by Proponent **R01 (Domain DDD Specialist)** and the challenges levied by **R15 (Red Team Specialist)** and **R04 (Contracts Specialist)**.

The canonical state layer (`avf-core-state` / PostgreSQL) serves as the immutable spine of the entire AI Video Factory. Any defect, inversion, or ambiguity in domain entity lineage at this layer cascades into catastrophic downstream failures: non-reproducible generation runs, corrupted revision histories, orphaned media takes, broken billing attribution, and impossible audit trails.

The prior v1.0.0-rc draft exhibited critical relational errors, most notably the inverted lineage where `ShotVersion` attempted to capture `prompt_version_id`, while `PromptVersion` lacked direct parent version binding to `shot_version_id`, and `GenerationJob` was stripped of its relational coordinates.

This document delivers the formal Domain Owner evaluation across five core architectural dimensions, confirms the relational mappings and compound foreign key integrity, resolves technology coupling, defends data integrity against challenger attacks, and issues binding directives for freeze implementation.

---

## 2. Canonical Lineage & Relational Mapping Review

### 2.1 The Five-Tier Production Hierarchy
In professional digital film and AI video production, creative state evolves across five distinct lifecycle phases:

```
+-------------------------------------------------------------------------+
|                                  SHOT                                   |
| (Logical Identity & Timeline Position: e.g., SC01_SH001)               |
+-------------------------------------------------------------------------+
                                    | 1
                                    | N
+-------------------------------------------------------------------------+
|                              SHOT_VERSION                               |
| (Immutable Creative Intent: duration, action, camera, lighting, chars)  |
+-------------------------------------------------------------------------+
                                    | 1
                                    | N
+-------------------------------------------------------------------------+
|                             PROMPT_VERSION                              |
| (Compiled Engine Instruction: positive/negative text, seed, AST, model) |
+-------------------------------------------------------------------------+
                                    | 1
                                    | N
+-------------------------------------------------------------------------+
|                             GENERATION_JOB                              |
| (Physical Execution Attempt: provider, lease, status, cost, attempt_no) |
+-------------------------------------------------------------------------+
                                    | 1
                                    | N
+-------------------------------------------------------------------------+
|                                  TAKE                                   |
| (Candidate Rendered Media: storage URI, SHA-256 hash, QC metrics)       |
+-------------------------------------------------------------------------+
```

### 2.2 Relational Entity Semantics
1. **`shots` (Logical Identity):**
   - Represents the persistent narrative element in a project timeline (e.g., Scene 1, Shot 4).
   - Retains stable `shot_id` (UUIDv4), `project_id`, `scene_id`, and `sequence_order`.
   - Does *not* store mutable creative prompts or duration targets directly; it is the anchor for version history.
2. **`shot_versions` (Immutable Creative Intent):**
   - Represents a specific human/director revision of how the shot should look and feel.
   - Contains narrative action description, camera kinematics, duration target, scene environment constraints, style profile bindings, and character references.
   - **Immutability Invariant:** Once committed, a `ShotVersion` is never updated in place. Director changes yield a new `shot_version_id` with an incremented `version_number`.
3. **`prompt_versions` (Compiled Generation Instructions):**
   - Represents the deterministic realization of a `ShotVersion` targeting a specific AI engine (e.g., Google Veo, Runway Gen-3, Luma Dream Machine, Kling, or local ComfyUI).
   - Produced exclusively by `avf-prompt-compiler` (R05).
   - Captures `shot_version_id`, compiler version, provider profile, compiled positive/negative prompt texts, model parameter mappings, and an exact `input_hash` representing the AST state.
   - **Crucial Provenance Rule:** Multiple `PromptVersion` records can be compiled for a single `ShotVersion` (e.g., prompt variant A vs. variant B, or target provider X vs. provider Y), but each `PromptVersion` strictly references exactly one `ShotVersion`.
4. **`generation_jobs` (Physical Execution Attempt Boundary):**
   - Represents an operational attempt to execute a `PromptVersion` on a designated provider track.
   - Owned transactionally by `avf-core-state` (R02), operated via leases by workers (`avf-workflow` R06 / provider adapters).
   - Encapsulates execution state (`QUEUED`, `RESERVED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `RECONCILED`), provider-assigned transaction keys (`provider_job_id`), dispatch track, lease tokens, attempt index, credit reservation, and structured `normalized_error` if terminated.
5. **`takes` (Produced Candidate Artifact):**
   - Represents the concrete digital video/media asset resulting from a `GenerationJob`.
   - Captures object storage URI, SHA-256 binary digest, MIME type, frame count, byte size, resolution, and downstream QC evaluation linkage (`qc_status`, `qc_score`).
   - **Immutability Invariant:** A `Take` is permanently retained for historical lineage and audit, even when rejected by QC or discarded by the operator. Re-running generation yields a new `GenerationJob` and a new `Take`.

---

## 3. Compound Foreign Key Integrity & Relational Proof

### 3.1 The Redundant Denormalization Dilemma
Challenger R15 raised the concern that including `shot_id` alongside `shot_version_id` in downstream tables (`prompt_versions`, `generation_jobs`, `takes`) introduces denormalization risks where a corrupted or malicious write could pair `shot_id = A` with `shot_version_id = B` (where Version B actually belongs to Shot C).

### 3.2 Relational Proof of Consistency via Compound Foreign Keys
To guarantee absolute referential consistency without sacrificing analytical query performance, PostgreSQL composite unique constraints and compound foreign keys are mandatory.

Let:
- Table $S$ (`shots`) have Primary Key $(shot\_id)$.
- Table $SV$ (`shot_versions`) have Primary Key $(shot\_version\_id)$ and Unique Constraint $(shot\_id, shot\_version\_id)$.
- Table $PV$ (`prompt_versions`) have Primary Key $(prompt\_version\_id)$ and Foreign Key $(shot\_id, shot\_version\_id) \to SV(shot\_id, shot\_version\_id)$.
- Table $GJ$ (`generation_jobs`) have Primary Key $(job\_id)$ and Compound Foreign Keys:
  - $(shot\_id, shot\_version\_id) \to SV(shot\_id, shot\_version\_id)$
  - $(prompt\_version\_id) \to PV(prompt\_version\_id)$
- Table $T$ (`takes`) have Primary Key $(take\_id)$ and Compound Foreign Keys:
  - $(shot\_id, shot\_version\_id) \to SV(shot\_id, shot\_version\_id)$
  - $(job\_id) \to GJ(job\_id)$

**Theorem (Referential Non-Drift):**  
If $GJ$ references $SV$ via $(shot\_id, shot\_version\_id)$, then no record in $GJ$ can reference a `shot_version_id` under a different `shot_id` than the one defined in $SV$.

**Proof:**  
By relational engine enforcement in PostgreSQL:
1. $SV$ enforces $(shot\_id, shot\_version\_id)$ uniqueness.
2. An `INSERT` or `UPDATE` into $GJ$ requires that the tuple $(shot\_id, shot\_version\_id)$ exists identically in $SV$.
3. If an insertion attempts to write $(shot\_id = A, shot\_version\_id = B)$ where $(shot\_id = C, shot\_version\_id = B)$ exists in $SV$, PostgreSQL immediately aborts the transaction with foreign key violation code `23503` (`foreign_key_violation`).
4. Therefore, relational cross-shot corruption is mathematically impossible at the engine storage level. $\blacksquare$

### 3.3 Query Performance & Indexing Benefit
By storing `shot_id` directly in `generation_jobs` and `takes` under compound constraints, dashboard queries (such as fetching all generation jobs or takes for a given shot timeline) execute in $O(\log N)$ time using a single index scan on `idx_generation_jobs_shot_lookup (shot_id, created_at DESC)` without requiring an expensive multi-table inner join across `shot_versions` and `prompt_versions`.

---

## 4. PostgreSQL DDL Specification & Constraints

The authoritative schema for R02 `avf-core-state` is defined below. All constraints use `ON DELETE RESTRICT` to enforce the absolute immutability and audit-preservation requirements of System Invariant #6 and #17.

```sql
-- PostgreSQL 15+ Schema Definition: Canonical Provenance Model

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- 1. Logical Shot Entity
CREATE TABLE shots (
    shot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    scene_id UUID NOT NULL,
    shot_code VARCHAR(64) NOT NULL,
    sequence_order INTEGER NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(128) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    CONSTRAINT uq_shots_project_code UNIQUE (project_id, shot_code),
    CONSTRAINT ck_shots_status CHECK (status IN ('DRAFT', 'ACTIVE', 'LOCKED', 'ARCHIVED'))
);

CREATE INDEX idx_shots_project ON shots (project_id, sequence_order);

-- 2. Immutable Shot Version (Creative Direction)
CREATE TABLE shot_versions (
    shot_version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shot_id UUID NOT NULL REFERENCES shots(shot_id) ON DELETE RESTRICT,
    version_number INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    action_description TEXT NOT NULL,
    camera_motion JSONB NOT NULL DEFAULT '{}'::jsonb,
    environment_settings JSONB NOT NULL DEFAULT '{}'::jsonb,
    character_version_ids UUID[] NOT NULL DEFAULT '{}',
    style_version_id UUID NULL,
    asset_ids UUID[] NOT NULL DEFAULT '{}',
    constraints TEXT[] NOT NULL DEFAULT '{}',
    continuity_refs JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(128) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    CONSTRAINT uq_shot_versions_shot_num UNIQUE (shot_id, version_number),
    CONSTRAINT uq_shot_versions_compound UNIQUE (shot_id, shot_version_id),
    CONSTRAINT ck_shot_versions_duration CHECK (duration_ms > 0 AND duration_ms <= 600000),
    CONSTRAINT ck_shot_versions_version_pos CHECK (version_number >= 1)
);

CREATE INDEX idx_shot_versions_lookup ON shot_versions (shot_id, version_number DESC);

-- 3. Compiled Prompt Version
CREATE TABLE prompt_versions (
    prompt_version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    version_number INTEGER NOT NULL,
    target_provider VARCHAR(64) NOT NULL,
    compiler_version VARCHAR(32) NOT NULL,
    positive_prompt TEXT NOT NULL,
    negative_prompt TEXT NULL,
    model_parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    ast_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    input_hash CHAR(64) NOT NULL, -- SHA-256 digest of input parameters
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(128) NOT NULL,
    CONSTRAINT uq_prompt_versions_shot_ver_num UNIQUE (shot_version_id, version_number),
    CONSTRAINT uq_prompt_versions_compound UNIQUE (shot_version_id, prompt_version_id),
    CONSTRAINT fk_prompt_versions_shot_version 
        FOREIGN KEY (shot_id, shot_version_id) 
        REFERENCES shot_versions(shot_id, shot_version_id) 
        ON DELETE RESTRICT,
    CONSTRAINT ck_prompt_versions_input_hash CHECK (input_hash ~ '^[a-f0-9]{64}$')
);

CREATE INDEX idx_prompt_versions_hash ON prompt_versions (input_hash);
CREATE INDEX idx_prompt_versions_shot_ver ON prompt_versions (shot_version_id, version_number DESC);

-- 4. Generation Job (Execution Attempt Boundary)
CREATE TABLE generation_jobs (
    job_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    prompt_version_id UUID NOT NULL,
    provider_id VARCHAR(64) NOT NULL,
    flow_track VARCHAR(32) NOT NULL, -- 'TRACK_A' or 'TRACK_B'
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    status VARCHAR(32) NOT NULL DEFAULT 'QUEUED',
    execution_stage VARCHAR(64) NOT NULL DEFAULT 'DISPATCH_QUEUED',
    attempt_index INTEGER NOT NULL DEFAULT 1,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    provider_job_id VARCHAR(256) NULL,
    lease_token UUID NULL,
    lease_expires_at TIMESTAMPTZ NULL,
    estimated_cost_credits NUMERIC(10, 4) NOT NULL DEFAULT 0.0000,
    actual_cost_credits NUMERIC(10, 4) NULL,
    normalized_error JSONB NULL,
    requested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMPTZ NULL,
    completed_at TIMESTAMPTZ NULL,
    entity_version INTEGER NOT NULL DEFAULT 1, -- Optimistic locking
    CONSTRAINT fk_gen_jobs_shot_version 
        FOREIGN KEY (shot_id, shot_version_id) 
        REFERENCES shot_versions(shot_id, shot_version_id) 
        ON DELETE RESTRICT,
    CONSTRAINT fk_gen_jobs_prompt_version 
        FOREIGN KEY (prompt_version_id) 
        REFERENCES prompt_versions(prompt_version_id) 
        ON DELETE RESTRICT,
    CONSTRAINT ck_gen_jobs_status CHECK (status IN ('QUEUED', 'RESERVED', 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED', 'RECONCILED')),
    CONSTRAINT ck_gen_jobs_flow_track CHECK (flow_track IN ('TRACK_A', 'TRACK_B', 'DIRECT_API'))
);

CREATE INDEX idx_generation_jobs_shot_lookup ON generation_jobs (shot_id, created_at DESC);
CREATE INDEX idx_generation_jobs_lease ON generation_jobs (status, lease_expires_at) WHERE status IN ('RESERVED', 'RUNNING');
CREATE INDEX idx_generation_jobs_provider ON generation_jobs (provider_id, provider_job_id);

-- 5. Candidate Rendered Take
CREATE TABLE takes (
    take_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    prompt_version_id UUID NOT NULL,
    job_id UUID NOT NULL REFERENCES generation_jobs(job_id) ON DELETE RESTRICT,
    take_number INTEGER NOT NULL,
    storage_uri TEXT NOT NULL,
    mime_type VARCHAR(64) NOT NULL,
    byte_size BIGINT NOT NULL,
    checksum_sha256 CHAR(64) NOT NULL,
    duration_ms INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    fps NUMERIC(6, 3) NOT NULL,
    qc_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    qc_score NUMERIC(5, 4) NULL,
    is_selected_master BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_takes_shot_take_num UNIQUE (shot_id, take_number),
    CONSTRAINT fk_takes_shot_version 
        FOREIGN KEY (shot_id, shot_version_id) 
        REFERENCES shot_versions(shot_id, shot_version_id) 
        ON DELETE RESTRICT,
    CONSTRAINT fk_takes_prompt_version 
        FOREIGN KEY (prompt_version_id) 
        REFERENCES prompt_versions(prompt_version_id) 
        ON DELETE RESTRICT,
    CONSTRAINT ck_takes_qc_status CHECK (qc_status IN ('PENDING', 'PASSED', 'REJECTED', 'QUARANTINED', 'OVERRIDDEN')),
    CONSTRAINT ck_takes_checksum CHECK (checksum_sha256 ~ '^[a-f0-9]{64}$')
);

CREATE INDEX idx_takes_shot ON takes (shot_id, take_number);
CREATE INDEX idx_takes_checksum ON takes (checksum_sha256);
CREATE INDEX idx_takes_job ON takes (job_id);
```

---

## 5. Creative Intent Semantics in `ShotVersion`

### 5.1 The Root Cause of Compilation Breakdown
In earlier discarded revisions of `domain-entities.schema.json`, `ShotVersion` was reduced to a generic container stripped of concrete creative fields, erroneously expecting `PromptVersion` or external workflow payloads to supply camera, lighting, and action instructions.

This broke the fundamental architectural principle: **The Prompt Compiler (R05) is a pure, deterministic compiler, not a creative hallucinator.**

To compile a target prompt for Google Veo or Runway, R05 must ingest structured creative intent from `ShotVersion`. If `ShotVersion` lacks these fields, prompt compilation is non-deterministic and unreproducible across runs.

### 5.2 Mandatory Creative Intent Fields
Every `ShotVersion` payload and database row MUST contain the following typed structures:

```json
{
  "shot_version_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "shot_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "version_number": 2,
  "duration_ms": 4500,
  "action_description": "Detective Vance walks slowly through the rain-soaked alley, turning head sharply toward the sound of broken glass on screen right.",
  "camera_motion": {
    "shot_type": "MEDIUM_CLOSE_UP",
    "angle": "LOW_ANGLE",
    "movement": "TRACKING_BACKWARD",
    "lens_focal_length_mm": 50,
    "speed": "SLOW",
    "stabilization": "CINEMATIC_STEADICAM"
  },
  "environment_settings": {
    "time_of_day": "NIGHT",
    "weather": "HEAVY_RAIN",
    "lighting_style": "NEO_NOIR_HIGH_CONTRAST",
    "primary_light_source": "FLICKERING_NEON_SIGN_CYAN",
    "fill_light": "WET_ASPHALT_REFLECTIONS"
  },
  "character_version_ids": [
    "c1a2b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c"
  ],
  "style_version_id": "s9a8b7c6-d5e4-3f2a-1b0c-9d8e7f6a5b4c",
  "asset_ids": [
    "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  ],
  "constraints": [
    "NO_DAYLIGHT",
    "CHARACTER_MUST_WEAR_FEDORA",
    "NO_DIRECT_CAMERA_STARE"
  ],
  "continuity_refs": {
    "preceding_shot_version_id": "8f3c7e4d-1a2b-3c4d-5e6f-7a8b9c0d1e2f",
    "eye_line_vector": [0.75, 0.15, -0.64],
    "spatial_anchor_character_position": "SCREEN_LEFT_MOVING_CENTER"
  }
}
```

---

## 6. Comprehensive Metadata Model for `AssetVersion` & IP Governance

### 6.1 Requirements for Enterprise IP & Storage Integrity
In an industrial production pipeline, raw media assets, character reference sheets, style LoRAs, and generated video takes are subject to strict copyright, retention, and storage verification rules.

`AssetVersion` represents the immutable physical snapshot of a digital asset. It cannot merely be a bare URL; it must guarantee bitwise verification, storage locality, and legal rights attribution.

### 6.2 Schema & Field Specification for `AssetVersion`

```json
{
  "asset_version_id": "d3b07384-d113-40f7-8739-9d5a57041f12",
  "asset_id": "e2a1b0c9-8d7e-6f5a-4b3c-2d1e0f9a8b7c",
  "version_number": 1,
  "storage": {
    "storage_uri": "s3://avf-production-assets/projects/proj-101/characters/vance_headshot_v1.png",
    "storage_provider": "S3_COMPLIANT",
    "bucket": "avf-production-assets",
    "region": "us-east-1",
    "storage_tier": "HOT"
  },
  "content_attributes": {
    "mime_type": "image/png",
    "byte_size": 4194304,
    "checksum_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "dimensions": {
      "width": 2048,
      "height": 2048,
      "aspect_ratio": "1:1"
    },
    "color_space": "REC709"
  },
  "source_provenance": {
    "source_type": "HUMAN_UPLOAD",
    "uploaded_by": "lead_character_artist_01",
    "source_job_id": null,
    "upstream_asset_version_id": null
  },
  "rights_metadata": {
    "license_type": "PROPRIETARY_WORK_FOR_HIRE",
    "rights_holder": "Studio Operations LLC",
    "attribution_text": "Original character design by Studio Team A",
    "expiration_date": null,
    "commercial_use_allowed": true,
    "model_training_permitted": false
  },
  "created_at": "2026-08-15T12:00:00Z"
}
```

---

## 7. Decoupling Model-Specific Artifacts into `custom_attributes`

### 7.1 The Architectural Trap of Hardcoded LoRA/Embedding Fields
The frozen blueprint v0.9.0 contained a severe abstraction leak:
- `CharacterVersion` declared a mandatory `face_embedding_hash` (assuming an InsightFace 512-d float array).
- `StyleVersion` declared a mandatory `lora_weights_uri` (assuming a Stable Diffusion `.safetensors` file).

**Why this breaks multi-provider architecture:**
1. Contemporary foundation video models (Google Veo, Runway Gen-3, OpenAI Sora) operate via multi-modal reference image URLs or internal identity tokens rather than exposing custom fine-tuned LoRA weight injection endpoints.
2. Forcing clients or test harnesses to supply dummy SHA-256 hashes or fictitious S3 paths for models that do not use LoRAs violates Domain-Driven Design and corrupts data truth.
3. Different embedding architectures (InsightFace vs. CLIP vs. DINOv2 vs. FaceNet) have incompatible dimensionalities and distance metrics. Storing a bare hash without algorithm context is functionally useless for continuity verification.

### 7.2 The Extensible Namespaced `custom_attributes` Solution
Technology-specific descriptors are moved into an extensible, structured `custom_attributes` JSONB map on `CharacterVersion` and `StyleVersion`.

#### `CharacterVersion` Specification:
```json
{
  "character_version_id": "c1a2b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "character_id": "b0a1b2c3-d4e5-6f7a-8b9c-0d1e2f3a4b5c",
  "name": "Detective Vance",
  "visual_traits": {
    "gender_presentation": "MALE",
    "apparent_age": 42,
    "hair_color_style": "DARK_BROWN_RECEDING",
    "facial_hair": "HEAVY_STUBBLE",
    "distinguishing_features": ["SCAR_LEFT_CHEEK", "PIERCING_GRAY_EYES"]
  },
  "reference_asset_ids": [
    "d3b07384-d113-40f7-8739-9d5a57041f12",
    "e4c18495-e224-51a8-9840-0e6b68152a23"
  ],
  "custom_attributes": {
    "face_embeddings": {
      "insightface_antelopev2_512d": {
        "embedding_vector_ref": "s3://avf-embeddings/chars/vance_antelopev2.bin",
        "checksum_sha256": "4a5e1e5f8f9d0c2b1a3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c"
      }
    },
    "provider_specific_tokens": {
      "google_flow_identity_token": "id_token_vance_98472",
      "runway_actor_id": "act_88301"
    }
  }
}
```

#### `StyleVersion` Specification:
```json
{
  "style_version_id": "s9a8b7c6-d5e4-3f2a-1b0c-9d8e7f6a5b4c",
  "style_profile_id": "p1a2b3c4-d5e6-7f8a-9b0c-1d2e3f4a5b6c",
  "style_name": "Neo-Noir 35mm Gritty",
  "art_direction": {
    "film_stock": "KODAK_VISION3_500T",
    "color_grading": "TEAL_AND_ORANGE_MUTED",
    "grain_level": "HEAVY_ANALOG",
    "aspect_ratio": "2.39:1"
  },
  "custom_attributes": {
    "diffusion_weights": {
      "lora_weights_uri": "s3://avf-models/loras/neo_noir_v2.safetensors",
      "lora_multiplier": 0.75,
      "base_model": "SDXL_1.0"
    }
  }
}
```

This guarantees 100% provider generality: R04 (Assets Continuity) and R05 (Prompt Compiler) inspect `custom_attributes` only when targeting compatible providers, while text-only and multi-modal reference pipelines operate seamlessly without dummy data.

---

## 8. Evaluation of Challenger (R15 / R04) Arguments & Counter-Defense

| Challenge Raised by R15 / R04 | Domain Owner Evaluation & Technical Counter-Defense |
|---|---|
| **1. Denormalization Hazard:** Storing `shot_id` alongside `shot_version_id` in downstream tables violates 3NF and invites data corruption. | **REJECTED.** As proven in §3.2, PostgreSQL compound foreign keys (`FOREIGN KEY (shot_id, shot_version_id) REFERENCES shot_versions(shot_id, shot_version_id)`) make cross-shot data corruption impossible. The inclusion of `shot_id` provides vital query performance for high-frequency dashboard indexing without join overhead. |
| **2. UUID Format Rigidity:** Strict RFC 4122 UUID regex validation in JSON Schemas will break test harnesses using string prefixes (e.g. `mock-shot-001`). | **REJECTED.** Relaxing canonical ID validation across distributed message buses invites corrupted state and broken DB UUID conversions. Test fixtures and mocks MUST use standard, reproducible UUIDv4 strings (e.g., `00000000-0000-4000-8000-000000000001` or deterministic UUIDv5 namespaces). Core contracts must never be compromised for test convenience. |
| **3. Junction Table Proposal (Option B):** Decouple `ShotVersion` and `PromptVersion` into independent entities connected via a junction table `ShotPromptBinding`. | **REJECTED.** A prompt compiled for a video factory is never a generic, floating entity; it is a compilation artifact generated specifically to fulfill the creative intent of a concrete `ShotVersion`. An extra junction table adds needless join overhead, breaks deterministic AST compilation traceability, and provides zero production benefit. |
| **4. LoRA / Face Embedding Coupling:** Hardcoded fields break provider neutrality. | **UPHELD & REMEDIATED.** Challenger was entirely correct. As detailed in §7, these fields are now fully decoupled into namespaced `custom_attributes` dictionaries. |

---

## 9. Formal Domain Owner Verdict & Binding Directives

### 9.1 Authoritative Verdict
**STATUS: CONFIRMED_WITH_DIRECTIVES**  
The proposed canonical domain provenance model (`Shot` -> `ShotVersion` -> `PromptVersion` -> `GenerationJob` -> `Take`) is mathematically sound, robust against distributed concurrency hazards, and satisfies all requirements of TECH-004, TECH-013, TECH-014, TECH-015, TECH-016, and TECH-017.

### 9.2 Binding Implementation Directives for C03R / C04R

1. **Directive to R01 (`avf-contracts`):**
   - Update `domain-entities.schema.json` to reflect the corrected lineage.
   - Restore all creative intent fields to `$defs/shotVersion`.
   - Add `$defs/assetVersion` containing complete storage, content, provenance, and rights metadata.
   - Move LoRA and facial embedding properties into optional `$defs/customAttributes` on `characterVersion` and `styleVersion`.
   - Enforce strict `format: "uuid"` with RFC 4122 regex patterns across all entity ID definitions.

2. **Directive to R02 (`avf-core-state`):**
   - Implement the exact PostgreSQL DDL defined in §4 of this review.
   - Enforce compound foreign keys: `FOREIGN KEY (shot_id, shot_version_id) REFERENCES shot_versions(shot_id, shot_version_id) ON DELETE RESTRICT`.
   - Ensure all take and generation job state transitions adhere to strict optimistic concurrency via `entity_version`.

3. **Directive to R04 (`avf-assets-continuity`):**
   - Align asset ingestion, reference set resolution, and character/style registries with the extensible `custom_attributes` structure.
   - Implement rights validation checks prior to emitting `ResolvedAssetSet` payloads.

4. **Directive to R05 (`avf-prompt-compiler`):**
   - Ingest `ShotVersion` creative intent structures as the primary compilation input.
   - Generate deterministic `PromptVersion` records referencing `shot_id` and `shot_version_id`, with verifiable SHA-256 `input_hash` digests.

---
**DOMAIN OWNER SIGN-OFF:**  
*R05 — Lead Data Architect, AI Video Factory Architecture Council*  
*Timestamp: 2026-08-15T21:30:00Z*
