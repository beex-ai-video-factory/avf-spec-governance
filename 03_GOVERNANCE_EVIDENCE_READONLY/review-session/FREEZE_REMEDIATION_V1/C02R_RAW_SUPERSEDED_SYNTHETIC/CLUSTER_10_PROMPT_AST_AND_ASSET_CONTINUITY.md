# C02R HEARING TRANSCRIPT: CLUSTER 10 — PROMPT AST LAYERING & ASSET CONTINUITY
**CLUSTER_ID:** CLUSTER-010
**FINDINGS_COVERED:** FINDING_011, FINDING_029, FINDING_075
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R09 (AI Specialist) & R01 (Domain DDD Specialist)
- **Position:** Prompt generation for complex video generation requires a 3-layer compilation pipeline:
  1. *Layer 1 (Semantic AST):* High-level scene description, character identities, camera trajectories, mood, lighting.
  2. *Layer 2 (Engine IR):* Provider-neutral intermediate representation with parameter mapping, aspect ratio formatting, token weights.
  3. *Layer 3 (Target String/Payload):* Engine-specific optimized prompt string (e.g. Veo2 / Sora / Google Flow syntax) with negative prompts and asset reference tokens.
  Asset continuity (R04) ensures consistent character facial embeddings, style vectors, and color grading across shots.
- **Evidence:** `R05_PROMPT_COMPILER.md`, `R04_ASSETS_CONTINUITY.md`.
- **Failure Scenario:** A prompt engineer tweaks a camera motion string directly, inadvertently wiping out character continuity tokens because there is no structured AST preserving entity references.

## 2. Challenger Attack
- **Challenger:** R04 (Contracts Specialist)
- **Attack Vector:**
  1. *AST Complexity:* Does the 3-layer AST add latency to the critical path?
  2. *Schema Rigidity:* Will new video models with novel input modalities (e.g. 3D bounding boxes or audio-driven motion) break the AST contract?

## 3. Domain Owner Review
- **Domain Owner:** R09 (AI Specialist)
- **Evaluation:**
  - The AST compiles in < 5ms in Node.js, representing negligible overhead compared to 30-120 second video generation.
  - The AST uses an extensible node dictionary (`custom_directives`) allowing new modalities without breaking base compiler interfaces.

## 4. Proponent Response
- **Response:**
  - We formalize the AST interfaces in `R05_PROMPT_COMPILER.md` and ensure clean integration with `domain-entities.schema.json`.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Simple string template interpolation (e.g. Mustache/Jinja).
- **Why Rejected:** String templates cannot enforce continuity constraint validation, token length limits, or automated multi-provider prompt transpilation.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-011 & CP-012 retained and integrated into `R05_PROMPT_COMPILER.md` and `R04_ASSETS_CONTINUITY.md`.
