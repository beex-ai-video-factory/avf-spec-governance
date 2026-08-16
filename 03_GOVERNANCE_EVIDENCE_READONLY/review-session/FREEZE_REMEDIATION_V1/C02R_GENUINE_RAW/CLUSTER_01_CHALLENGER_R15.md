# C02R RED TEAM CHALLENGE: CLUSTER 01 — CANONICAL DOMAIN PROVENANCE & ENTITY MODEL

**DOCUMENT_ID:** RED-TEAM-C02R-CL01-R15  
**ROLE:** R15 Red Team Specialist (Challenger)  
**DECISION_CLUSTER:** Cluster 01 — Canonical Domain Provenance & Entity Model  
**TARGET_SPECIFICATIONS:** `01_master/DATA_MODEL.md`, `02_contracts/domain-entities.schema.json`, `03_repo_blueprints/R01_CONTRACTS.md`, `03_repo_blueprints/R02_CORE_STATE.md`, `03_repo_blueprints/R04_ASSETS_CONTINUITY.md`, `03_repo_blueprints/R05_PROMPT_COMPILER.md`, `03_repo_blueprints/R15_INTEGRATION_HARNESS.md`, `review-session/FREEZE_REMEDIATION_V1/C03R/SOL_01_CANONICAL_PROVENANCE_DATA_MODEL.md`  
**DATE:** 2026-08-15  
**STATUS:** ACTIVE_ADVERSARIAL_CHALLENGE  

---

## 1. Executive Summary & Adversarial Stance

The proponent team (R01 Domain DDD & R05 Data Architect) and Solution Package `SOL-01` propose remediating the inverted provenance between `ShotVersion` and `PromptVersion` by establishing a strict hierarchical immutable lineage:
$$\text{Shot} \longrightarrow \text{ShotVersion} \longrightarrow \text{PromptVersion} \longrightarrow \text{GenerationJob} \longrightarrow \text{Take} \longrightarrow \text{QCResult}$$

While this directionally fixes the fatal cyclic dependency of the v1.0.0-rc draft (where `ShotVersion` required `prompt_version_id`), the proposed schema changes introduce severe latent vulnerabilities, architectural debt, and operational risks across:
1. **PostgreSQL Relational Integrity vs Denormalization Anarchy:** Excessive multi-level foreign key denormalization without enforceable compound integrity constraints creates silent divergence between shot versions and compiled prompts.
2. **Schema Bloat and Unindexed MVCC Overhead:** Open-ended JSONB columns (`action`, `camera`, `environment`, `constraints`) with unconstrained typing create massive write amplification and break query performance.
3. **Rigid RFC 4122 UUID Enforcement:** Over-zealous schema validation breaks deterministic testing harnesses, prevents human-readable integration tracing, and misaligns with external AI provider identifier semantics.
4. **Continuity Degradation via LoRA & Face Embedding Decoupling:** Relegating facial embeddings and LoRA weights to unstructured attributes degrades character continuity guarantees from hard architectural invariants to best-effort prompt suggestions, directly violating core product requirements.
5. **Inflight Version Mutation Races in Prompt Compilers:** High-concurrency generation workflows suffer from AST cache poisoning, idempotency key collision, and orphaned take attribution when shot revisions occur while jobs are in flight.

This challenge dissects each failure mode with concrete code and schema examples, proving that the proposed data model cannot be frozen in its current form without critical architectural mitigations.

---

## 2. Attack Vector 1: PostgreSQL Schema Bloat, JSONB Trap & Denormalization Inconsistencies

### 2.1 The Compound Foreign Key Bypass & Inflight Data Corruption

The proponent model proposes storing `shot_id`, `shot_version_id`, and `prompt_version_id` redundantly on `GenerationJob` and `Take` to avoid multi-table JOINs during high-throughput state lookups and dashboard rendering.

```sql
-- PROPOSED SCHEMA SNIPPET (GenerationJob)
CREATE TABLE generation_jobs (
    job_id UUID PRIMARY KEY,
    project_id UUID NOT NULL,
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    prompt_version_id UUID NOT NULL,
    provider_id VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL,
    -- ... other fields ...
    FOREIGN KEY (shot_version_id) REFERENCES shot_versions(shot_version_id),
    FOREIGN KEY (prompt_version_id) REFERENCES prompt_versions(prompt_version_id)
);
```

#### The Exploit / Failure Mode:
Because standard relational foreign keys only validate individual scalar keys, the database allows an incoherent state where `prompt_version_id` actually belongs to `shot_version_id = 'v1'`, but `generation_jobs.shot_version_id` is set to `'v2'`.

```text
[Shot V1] <--- [Prompt V1 (shot_version_id = V1)]
    ^
    | (Desynchronized Insert / Race)
    v
[Shot V2] <------------------------------------+
    ^                                          |
    +---- [GenerationJob (shot_version_id = V2, prompt_version_id = V1)]
```

When an upstream orchestrator (R06 Workflow or R13 Operator Console) fires a retry or re-generation during a shot edit, a race condition allows `GenerationJob` to bind a Prompt compiled for Shot V1 against Shot V2. 
- The generation succeeds at the provider level.
- The resulting `Take` is labeled as Shot V2, but visually depicts the prompt and constraints of Shot V1.
- Audit trails and QC evaluation pipelines (R11) evaluate the Take against V2 rules (e.g. 10-second duration target) when the prompt was compiled for V1 (5-second duration target), generating spurious QC failures and cost waste.

#### Red Team Hardening Requirement:
Simple scalar foreign keys MUST be banned in R02 Core State. PostgreSQL composite foreign keys and composite unique constraints MUST be strictly enforced:

```sql
-- MANDATORY HARDENING
ALTER TABLE prompt_versions 
    ADD CONSTRAINT uq_prompt_shot_lineage UNIQUE (shot_id, shot_version_id, prompt_version_id);

ALTER TABLE generation_jobs 
    ADD CONSTRAINT fk_job_strict_lineage 
    FOREIGN KEY (shot_id, shot_version_id, prompt_version_id) 
    REFERENCES prompt_versions(shot_id, shot_version_id, prompt_version_id)
    ON DELETE RESTRICT;
```

---

### 2.2 The Open JSONB Anti-Pattern & PostgreSQL MVCC Write Amplification

In `02_contracts/domain-entities.schema.json` lines 52-60, creative intent properties are defined as untyped JSON objects:
```json
"action": { "type": "object" },
"camera": { "type": "object" },
"environment": { "type": "object" }
```

#### Failure Mechanics:
1. **Schema Rot & Contract Dissolution:** Defining `"action": { "type": "object" }` provides zero contract safety. Clients in R03 Creative or R13 Operator Console can write arbitrary schemas (`{"action_text": "..."}` vs `{"description": "...", "blocking": []}` vs `{"beats": {}}`). The schema validation layer becomes a toothless pass-through.
2. **PostgreSQL TOAST & Heap Fragmentation:** `ShotVersion` records with large JSONB payloads (storing rich scene blocking, continuity references, and nested prompt ASTs) exceed PostgreSQL's 2KB page inline threshold and are pushed to TOAST storage.
3. **HOT (Heap-Only Tuple) Update Invalidation on GenerationJob:** `GenerationJob` rows are updated 5 to 15 times per generation cycle (`PENDING` -> `QUEUED` -> `SUBMITTED_TO_PROVIDER` -> `LEASE_ACQUIRED` -> `POLLING` -> `COMPLETED`/`FAILED`). When `GenerationJob` embeds JSONB diagnostics, metadata, or normalized error payloads, PostgreSQL cannot perform Heap-Only Tuple (HOT) optimizations. Every state transition forces a new heap tuple allocation and B-Tree index pointer update across all indexes (`idx_job_status`, `idx_job_provider`, `idx_job_shot`), triggering massive write amplification, buffer pool churn, and autovacuum freeze lag under production loads (>100 concurrent renders).

---

## 3. Attack Vector 2: Strict RFC 4122 UUID Rigidity vs Real-World Test & Provider Ecosystem

### 3.1 Breakdown of R15 Integration Harness and Deterministic Mocks

`02_contracts/domain-entities.schema.json` and SOL-01 mandate strict RFC 4122 UUID validation:
```json
"shot_version_id": {
  "type": "string",
  "format": "uuid"
}
```

#### Failure Scenarios in Testing & Orchestration:
1. **Human-Legible Debugging in Complex Tracing:** In multi-service E2E tests (R15 Integration Harness, FlowKit Bridge, FakeProvider), engineers and automated fault-injection harnesses rely on structured, human-readable synthetic identifiers:
   - `shot-hero-intro-v01`
   - `job-mock-timeout-attempt-02`
   - `proj-perf-benchmark-100k`
   Enforcing strict UUID format instantly rejects all human-readable deterministic fixtures at the API boundary, forcing test suites to adopt random or opaque v4 UUIDs.
2. **Loss of Deterministic Test Reproducibility:** When tests use randomized UUIDs, log correlation across R02, R06, R08, and R14 becomes non-deterministic. If a test fails on attempt 3 of `9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d`, replicating that exact failure across parallel test runs requires passing complete UUID seeds.
3. **Nil UUID & Sentinel Value Rejection:** RFC 4122 v4/v5 validators frequently reject the Nil UUID (`00000000-0000-0000-0000-000000000000`) or special sentinel IDs used for system-level default styles, global fallback styles, or root project templates.

---

### 3.2 Provider Foreign Identifier Ingestion Leaks

External AI video generators do not utilize RFC 4122 UUIDs for their internal tasks:
- Google Flow / VideoFX: `task_alphanumeric_64`
- Kling AI: `task_kling_984128491`
- Runway Gen-3: `uuid-like but prefixed or alphanumeric string`
- ComfyUI / Local Worker: `prompt_id` (custom string or hash)

If `provider_job_id` or upstream task correlation fields are mistakenly constrained or coerced into UUID columns, adapter ingestion crashes. Furthermore, mapping external IDs into internal UUIDs requires maintaining bidirectional translation tables in R07/R08, introducing distributed state synchronization bugs when external providers return asynchronous webhook callbacks.

---

## 4. Attack Vector 3: Decoupling Facial Embeddings & LoRAs Weakens Cross-Cut Continuity

### 4.1 The "Silent Drift" Failure Mode: Loss of Type-Checked Identity Contracts

In SOL-01 / TECH-017, the proponent removes `face_embedding_hash` from `CharacterVersion` and `lora_weights_uri` from `StyleVersion`, arguing that they represent "technology leakage" and should be moved to optional metadata dictionaries (`custom_attributes`).

#### The Red Team Attack:
Character continuity across scene cuts is **the single most critical value proposition of an automated AI video factory**. AI video generation models suffer notoriously from visual identity drift, where a character's facial features, age, and ethnicity morph between Shot 1 (close-up) and Shot 2 (medium shot).

By moving facial embeddings and model adaptations out of the normative entity schema:
1. **Contract Invisibility:** Neither JSON Schema nor PostgreSQL schema can enforce that a `CharacterVersion` has valid embedding vectors before being passed to R05 Prompt Compiler.
2. **Silent Failure in Ingestion:** If an asset ingestion pipeline fails to extract ArcFace/InsightFace embeddings or provides an incompatible 512-d vector instead of a 1024-d vector, the error is swallowed into an opaque JSONB attribute.
3. **Downstream Pipeline Blindness:**
   - R05 (Prompt Compiler) cannot determine whether to compile a text-prompt fallback or a reference-image conditioning payload.
   - R04 (Assets & Continuity Resolver) cannot execute deterministic nearest-neighbor ranking or cosine-similarity checks across shot candidate frames.
   - R11 (QC Pipeline) cannot calculate identity consistency scores because the canonical ground-truth embedding is unindexed, untyped, or missing.

```text
[Asset Ingestion] 
   | (Fails to write 'face_embedding' to JSONB or writes corrupted 256-d float array)
   v
[CharacterVersion] (Passes schema validation because face_embedding is optional JSONB!)
   v
[R05 Prompt Compiler] (Compiles pure text prompt: "Alice walking in rain")
   v
[R08 Provider Adapter] (Renders generic woman with zero facial resemblance)
   v
[R11 QC Pipeline] (Cannot assert facial delta because character ground truth is null/untyped)
   v
[CRITICAL CONTINUITY FAILURE DELIVERED TO USER]
```

---

### 4.2 LoRA Weight Poisoning & Model Incompatibility

A LoRA weight is not merely a string URI; it is deeply tied to:
- `base_model_family` (e.g. `SDXL_v1.0`, `Flux.1_dev`, `Wan2.1_T2V`, `HunyuanVideo`)
- `network_dim` (rank) & `network_alpha`
- `trigger_words` (mandatory prompt tokens required to activate the weights)
- `recommended_weight` / `clip_weight`

When `lora_weights_uri` is demoted to unstructured metadata, R05 (Prompt Compiler) cannot validate model compatibility. If an operator assigns an `SDXL` LoRA style to a shot targeted for a `Flux.1` or Google Flow generation pipeline, R05 generates a prompt referencing incompatible weights, causing worker execution crashes or severe visual artifacting at runtime.

#### Red Team Hardening Requirement:
Facial identity representations and model adapters MUST NOT be dumped into arbitrary JSONB. They must be formalized into explicit, typed polymorphic contract components:

```json
"identity_conditioning": {
  "type": "object",
  "required": ["method", "reference_asset_ids"],
  "properties": {
    "method": { "type": "string", "enum": ["FACIAL_EMBEDDING", "IP_ADAPTER", "LORA", "REFERENCE_SHEET", "PROMPT_ONLY"] },
    "embedding_spec": {
      "type": "object",
      "required": ["model_tag", "dimensions", "vector_checksum"],
      "properties": {
        "model_tag": { "type": "string" },
        "dimensions": { "type": "integer" },
        "vector_checksum": { "type": "string" }
      }
    },
    "adapter_spec": {
      "type": "object",
      "required": ["target_base_model", "adapter_uri", "trigger_words", "default_scale"],
      "properties": {
        "target_base_model": { "type": "string" },
        "adapter_uri": { "type": "string", "format": "uri" },
        "trigger_words": { "type": "array", "items": { "type": "string" } },
        "default_scale": { "type": "number", "minimum": 0.0, "maximum": 2.0 }
      }
    }
  }
}
```

---

## 5. Attack Vector 4: Inflight Shot Version Mutation & Prompt Compiler Failure Edge Cases

### 5.1 Inflight Retry Mismatch & Franken-Prompt Compilation

In a distributed video production pipeline, video generations take between 30 seconds and 10 minutes. During this execution window, creative directors frequently edit shot action descriptions, adjust camera movements, or replace character costumes in the UI (R13 Operator Console).

#### Failure Timeline:
1. **$T_0$:** Operator creates Shot 1, Version 1 (`SV_1`). Duration = 4.0s, Camera = "Static Close-Up", Prompt = `PV_1`.
2. **$T_1$:** Generation Job `JOB_1` is created for `(SV_1, PV_1)` and submitted to Google Flow / Kling provider.
3. **$T_2$:** While `JOB_1` is executing, Operator updates Shot 1 to Version 2 (`SV_2`): Duration = 8.0s, Camera = "Dynamic Orbital Pan", Action = "Explosion in background".
4. **$T_3$:** `JOB_1` suffers a transient network disconnection from the provider (`PROVIDER_HTTP_504_GATEWAY_TIMEOUT`).
5. **$T_4$:** R06 Workflow orchestrator catches the transient failure and triggers an automatic retry policy.
6. **$T_5$ (The Defect):** If R06 or R05 queries Core State for the "current shot version" rather than the immutable pinned `shot_version_id` on `JOB_1`, it compiles a new prompt using `SV_2` parameters but attaches it to `JOB_1`'s attempt context, or re-dispatches `PV_1` with `SV_2` duration limits.
7. **$T_6$:** The resulting video is 4 seconds long (from `PV_1`) but registered against `SV_2` which expects an 8-second timeline slice, creating audio-video desynchronization in timeline assembly (R12 Media Processing).

```text
Time Line:
T0: Shot V1 Created (4s) ---> Prompt V1 Compiled
T1: Job 1 Dispatched [V1, PV1] ------------------------+ (Running at Provider...)
T2: Operator Edits Shot ---> Shot V2 Created (8s)      |
T3: Provider 504 Timeout on Job 1 <--------------------+
T4: Workflow Initiates Retry Attempt 2
T5: ERROR: Retry resolves Shot V2, but uses Prompt V1 or creates Frankenstein Prompt!
```

---

### 5.2 R05 Prompt Compiler Cache Poisoning

R05 (Prompt Compiler) optimizes compilation throughput by caching compiled sub-trees of the Prompt AST (e.g. style prefixes, character appearance descriptions, negative prompt blocks) keyed by entity ID.

#### Cache Invalidation Defect:
- If the cache key is constructed as `hash(shot_id + style_id + character_id)` instead of `hash(shot_version_id + style_version_id + character_version_id + compiler_version)`:
- When a user modifies a Character's costume in `CharacterVersion` 2 without changing the base `character_id`, R05 returns the cached prompt AST from `CharacterVersion` 1.
- The prompt sent to the diffusion model contains the old costume description, while the asset resolver attached the new costume reference image. The AI generation engine experiences cross-conditioning conflict, resulting in visual hallucinations.

---

### 5.3 Idempotency Key Collision Across Shot Versions

`01_master/DATA_MODEL.md` and SOL-01 state that `GenerationJob` idempotency key is computed from:
$$\text{idempotency\_key} = \text{HMAC-SHA256}(\text{shot\_id}, \text{prompt\_version\_id}, \text{provider\_id}, \text{attempt\_index})$$

#### The Vulnerability:
Notice that `shot_version_id` is omitted from this naive formulation under the assumption that `prompt_version_id` uniquely determines `shot_version_id`.
However:
1. If a prompt compiler produces an identical prompt text for both Shot V1 and Shot V2 (e.g., the shot edit only changed an internal non-prompt constraint such as post-processing color grading target or editor notes):
2. `PromptVersion` input hash may evaluate to the same value, reusing `prompt_version_id`.
3. When `GenerationJob` is submitted for Shot V2 with Attempt Index 1, the idempotency key collides with the previously completed Job from Shot V1!
4. R02 Core State rejects the new generation job as a duplicate request (`HTTP 409 Conflict`), blocking generation of Shot V2.

---

## 6. Red Team Concrete Demands for Specification Freeze

To allow Decision Cluster 01 to be safely frozen for v1.0 release, the following non-negotiable architectural remediations MUST be incorporated into the normative contracts:

| Requirement ID | Target Document | Mandatory Change |
|---|---|---|
| **REQ-CL01-01** | `DATA_MODEL.md`, `R02_CORE_STATE.md` | Mandate composite foreign keys `(shot_id, shot_version_id)` and `(shot_id, shot_version_id, prompt_version_id)` across `prompt_versions`, `generation_jobs`, and `takes` to guarantee referential lineage integrity. |
| **REQ-CL01-02** | `domain-entities.schema.json` | Replace unconstrained `"type": "object"` in `action`, `camera`, `environment` with explicit sub-schemas specifying required fields (`type`, `description`, `parameters`). |
| **REQ-CL01-03** | `domain-entities.schema.json` | Introduce typed `identity_conditioning` and `style_adapter_spec` contracts rather than burying facial embeddings and LoRA weights in untyped JSONB dictionaries. |
| **REQ-CL01-04** | `R05_PROMPT_COMPILER.md` | Define normative AST cache key specification: MUST include `shot_version_id`, `character_version_ids`, `style_version_id`, `compiler_version`, and `asset_fingerprint_sha256`. |
| **REQ-CL01-05** | `DATA_MODEL.md`, `R02_CORE_STATE.md` | Define canonical `idempotency_key` algorithm incorporating `project_id`, `shot_id`, `shot_version_id`, `prompt_version_id`, `provider_id`, and `attempt_index`. |
| **REQ-CL01-06** | `02_contracts/domain-entities.schema.json`, `R15_INTEGRATION_HARNESS.md` | Permit both RFC 4122 UUID v4/v5 format AND structured test-prefixed identifiers (e.g. `pattern: "^([0-9a-fA-F-]{36}|[a-z0-9_-]{3,64})$"`) in development/test profiles to maintain testability without compromising production rigor. |

---

## 7. Conclusion

The proposed provenance hierarchy (`ShotVersion` -> `PromptVersion` -> `GenerationJob` -> `Take`) is logically necessary and addresses the historical circular dependency defect. However, without the database-level composite foreign key constraints, typed continuity sub-schemas, AST cache isolation, and deterministic test identifier patterns outlined above, the data model remains vulnerable to data corruption, silent continuity failure, and production deadlock.

**Red Team Verdict:** CHALLENGE SUSTAINED. Proceed to remediation with mandatory inclusion of REQ-CL01-01 through REQ-CL01-06.
