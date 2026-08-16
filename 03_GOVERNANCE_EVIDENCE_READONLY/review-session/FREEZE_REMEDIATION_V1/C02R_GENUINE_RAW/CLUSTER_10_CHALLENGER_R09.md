# C02R GENUINE CHALLENGER ATTACK: DECISION CLUSTER 10
**DOMAIN:** Prompt AST Layering & Asset Continuity  
**ROLE:** R09 (AI Specialist / Challenger)  
**TARGET PROPOSALS:** CP-011 (3-Layer Prompt Compilation AST & Extensible Directives), CP-012 (Asset Versioning & Character/Style Continuity Scoring Invariants)  
**TARGET SPECIFICATIONS:** `03_repo_blueprints/R05_PROMPT_COMPILER.md`, `03_repo_blueprints/R04_ASSETS_CONTINUITY.md`, `03_repo_blueprints/R03_CREATIVE.md`, `03_repo_blueprints/R07_PROVIDER_SDK.md`, `03_repo_blueprints/R08_GOOGLE_FLOW_ADAPTER.md`, `03_repo_blueprints/R11_QC.md`, `02_contracts/provider-request.schema.json`, `02_contracts/domain-entities.schema.json`  
**STATUS:** ACTIVE_ADVERSARIAL_CHALLENGE  
**DATE:** 2026-08-16  

---

## 1. Executive Summary & Adversarial Stance

The proponent architecture for Decision Cluster 10 (CP-011 and CP-012) proposes a centralized **3-layer compilation pipeline** (`Semantic AST` $\to$ `Engine IR` $\to$ `Target Payload`) managed by `avf-prompt-compiler` (R05), combined with an abstract asset continuity resolver (`avf-assets-continuity`, R04). The proponent claims this design ensures cross-provider portability, prevents prompt corruption, and enforces character and style consistency across scene cuts.

**As R09 AI Specialist, I formally challenge this design as an over-engineered, leaky abstraction that fails fundamental realities of generative video AI:**

1. **The 3-Layer AST Semantic Bottleneck & Latent Optimization Erasure:** The 3-layer intermediate representation (IR) imposes a lowest-common-denominator schema that strips away model-specific latent space optimizations (e.g., token position saliency, attention masks, negative prompt weighting, CFG scheduling, and ControlNet/IP-Adapter graphs). Furthermore, it introduces uncontrolled token limit truncation risks and CPU/LLM latency overhead on the generation critical path.
2. **Dynamic Prompt Mutation Collapse Under Creative Retries:** In-flight creative intent adjustments and automated QC-driven retries break the system's lineage model. The architecture lacks generational snapshot isolation, causing AST cache poisoning, idempotency key collisions, and race conditions where Takes are evaluated against desynchronized shot versions.
3. **Continuity Scoring Breakdown on Multi-Character Cuts & LoRA Stacks:** The asset continuity model relies on naive scalar embeddings and ungrounded token insertion. It catastrophically fails during multi-character scene cuts (attribute bleeding, occlusion false-positives) and multi-LoRA style blending, while leaking proprietary engine internals across trust boundaries.

This challenge dissects these critical failure modes and provides concrete, mathematically rigorous alternative hypotheses to replace the fragile 3-layer AST compiler and scalar continuity resolver before v1.0 freeze.

---

## 2. Attack Vector 1: 3-Layer AST Compiler Breakdown (Latency, Token Limits & Latent Optimization Erasure)

```
[Layer 1: Semantic AST]  -->  [Layer 2: Engine IR]  -->  [Layer 3: Target Payload]
(High-Level Scene Tree)       (Provider-Neutral IR)      (Provider-Specific String)
         |                             |                            |
         v                             v                            v
   LLM Latency &              Lowest Common Denom.          Silent Token Truncation &
 Context Explosion            Strips Latent Weights        Position Saliency Destruction
```

### 2.1 The "Lowest Common Denominator" Trap & Loss of Model-Specific Latent Optimizations

Modern text-to-video (T2V) and image-to-video (I2V) architectures (e.g., Google Veo 2, OpenAI Sora, Runway Gen-3 Alpha, Kling 1.5, HunyuanVideo, Wan2.1, ComfyUI/Diffusers pipelines) do not interpret natural language prompts or conditioning tokens uniformly. They operate on fundamentally different latent spaces, text encoders (CLIP ViT-L vs T5-XXL vs dual-encoder blends), and conditioning mechanisms:

- **Token Position Saliency & Attention Decay:** Transformer-based diffusion backbones exhibit positional bias. Tokens placed in the initial 20–30 token window receive substantially higher self-attention weights. The proponent's Layer 2 Engine IR normalizes scene components into a fixed structural hierarchy (e.g., `Scene -> Camera -> Characters -> Lighting -> Style -> Quality Boosters`). When serialized into Layer 3, this static ordering moves crucial subject tokens past the attention threshold of models that prioritize the front of the prompt.
- **Syntactic Weighting & Emphasis Markers:** Open-source and advanced engines rely on syntax-level token emphasis:
  $$\text{Prompt Token Weighting: } ((\text{Alice}:1.35)),\quad [\text{cinematic lighting}:0.8],\quad \text{BREAK}$$
  The proponent's Engine IR strips these syntax markers into abstract numerical weights (`{"token": "Alice", "weight": 1.35}`). When compiling to providers that do not natively parse weighted syntax (such as standard Google Flow or Sora web endpoints), the compiler either silently drops the weight or attempts ad-hoc natural language expansion (e.g., prepending "highly detailed Alice"), causing prompt bloat and unpredictable latent drift.
- **Negative Conditioning Incompatibilities:** Commercial APIs (e.g., Google Flow / VideoFX, Sora) do not accept negative prompt strings or CFG scale overrides; open/semi-open APIs (Kling, ComfyUI, SDXL-based backbones) depend heavily on negative embeddings to suppress spatial distortions, morphing, and text rendering artifacts. The 3-layer AST either forces negative prompts into irrelevant providers (which reject or ignore them) or forces leaky `custom_directives` into every node, completely invalidating the claim of a provider-neutral Engine IR.

### 2.2 Token Budget Truncation & The Priority Inversion Defect

External AI video providers enforce hard token, byte, or character limits at their API boundaries:
- **Runway Gen-3 Alpha:** Strict ~512 character limit.
- **CLIP ViT-L Encoders:** Fixed 77-token maximum context window (75 usable tokens + `BOS`/`EOS`).
- **T5-XXL Encoders:** 256 or 512 token context window with quadratic attention cost.
- **Google Flow / Veo 2 Web Interface:** Hard character limits on input form fields.

When the 3-layer AST serializes a rich scene description (containing action beats, camera trajectory, character appearance descriptors, environment details, style tokens, and negative constraints), the resulting payload frequently exceeds provider token boundaries:

```
[Character Descriptors (120 chars)] + [Action Blocking (180 chars)] + [Environment (150 chars)] 
+ [Camera Trajectory (90 chars)] + [Style Modifiers (110 chars)] = 650 chars (EXCEEDS 512 LIMIT!)
```

#### The Failure Mechanics:
1. **Naive End-Truncation:** In standard serialization, the tail of the compiled string is cut off:
   ```text
   Original: "Alice wearing red leather jacket walking through rainy neon Tokyo street, 35mm lens, dolly forward --ar 16:9 --camera-speed fast"
   Truncated: "Alice wearing red leather jacket walking through rainy neon Tokyo street, 35mm lens, dolly forw"
   ```
   The camera direction, aspect ratio parameters, and speed directives are silently mutilated.
2. **The Priority Inversion Defect:** The 3-layer compiler lacks a **token-budget-aware knapsack solver**. It treats all AST nodes equally during IR generation. When truncation occurs, mission-critical identity tokens or camera constraints are dropped while non-essential decorative adjectives (e.g., "photorealistic, hyper-detailed, 8k, volumetric") in the environment node are preserved.
3. **Downstream Execution Failure:** The provider API receives a truncated string missing closing syntax or critical formatting flags, resulting in generic visual output that fails downstream QC (R11) while still consuming non-refundable generation credits.

### 2.3 Compilation Latency & Critical Path Bottlenecks

The proponent claims the AST compiles in $< 5\text{ ms}$ in Node.js. This claim is fundamentally deceptive because it considers only static string templating and ignores the blueprint specifications in `03_repo_blueprints/R05_PROMPT_COMPILER.md`:

- **LLM Enrichment Overhead:** `R05_PROMPT_COMPILER.md` line 4 specifies *"Deterministic-first with optional bounded LLM enrichment"*. When a complex shot requires prompt enrichment (e.g., expanding abstract script beats into visual descriptors or repairing semantic syntax), an LLM API call is injected directly into the critical compilation path:
  $$t_{\text{compile}} = t_{\text{AST\_parse}} (3\text{ms}) + t_{\text{LLM\_enrichment}} (1200\text{ms} - 3500\text{ms}) + t_{\text{schema\_validate}} (15\text{ms})$$
- **High-Concurrency Batch Rendering Bottleneck:** In a standard 30-shot commercial or scene sequence, triggering 30 sequential or semi-parallel LLM enrichments introduces 45–90 seconds of latency *before a single generation job can be submitted to provider workers*.
- **Multi-Layer Validation Tax:** Validating three separate schemas (`Semantic AST` schema $\to$ `Engine IR` schema $\to$ `ProviderRequest` schema) using JSON Schema validators (Ajv) across dozens of shots creates significant event-loop CPU starvation in Node.js worker processes.

---

## 3. Attack Vector 2: Dynamic Prompt Mutation, Creative Retries & In-Flight State Desynchronization

```
[Timeline of In-Flight Intent Mutation Race]
T0: User edits Shot V1 -> Creates Shot V2 (Camera: "DOLLY_IN")
T1: R05 compiles Prompt V2.1 for Shot V2
T2: Worker completes Generation Job #101 (Dispatched at T-30 for Shot V1, Camera: "PAN_LEFT")
T3: Worker writes Take #101 (References Shot V1, Prompt V1.1)
T4: R11 QC Evaluator awakens -> Reads current Shot record (Shot V2!)
T5: QC Evaluator compares Take #101 against Shot V2 rules -> REJECTS (Camera Mismatch!)
```

### 3.1 Creative Retries vs Prompt Lineage & Idempotency Collisions

System Invariant 11 (`01_master/SYSTEM_INVARIANTS.md`) mandates:
> *"Creative retries create a new attempt and create a new PromptVersion when prompt semantics changed."*

The interaction between R03 (Creative), R05 (Prompt Compiler), and R02 (Core State) during an automated QC retry loop exhibits severe architectural flaws:

1. **The Semantic Equivalence Ambiguity:** When R11 QC fails a take due to visual artifacting (e.g., `SCORE_TEMPORAL_FLICKER = 0.42`), R06 Workflow requests a retry.
   - If R05 adjusts only the random seed or adds a mild negative weight, did prompt semantics change?
   - If R05 creates `PromptVersion V2`, it violates the requirement that technical parameter shifts should remain within the same prompt lineage.
   - If R05 reuses `PromptVersion V1`, the calculated `idempotency_key` (defined in `02_contracts/provider-request.schema.json` as `hash(shot_version_id, prompt_version_id, attempt_no)`) collides with previous attempts if `attempt_no` tracking is desynchronized across distributed retries.
2. **Provider Cache Poisoning:** In headless browser workers (`avf-browser-worker`, R09) interacting with web-based platforms (Google Flow), the browser UI caches previous prompt inputs. If a creative retry submits a mutated prompt string without explicit DOM form invalidation, the browser worker inadvertently re-submits the old prompt text from form state, generating duplicate takes with identical visual defects.

### 3.2 In-Flight Creative Intent Mutation & Lack of Generational Snapshot Isolation

In a collaborative video production workflow, an operator in R13 Operator Console frequently edits scene blocking, lighting, or camera angles while generation jobs are actively rendering:

1. **The State Desynchronization Race:**
   - Generation Job #204 is executing at Runway for `ShotVersion V1` (Prompt: *"Alice sitting in coffee shop, static wide shot"*).
   - Operator revises the shot in R13, committing `ShotVersion V2` (Prompt: *"Alice running from explosion in coffee shop, tracking shot"*).
   - Job #204 completes successfully, delivering `Take 204`.
   - `avf-qc` (R11) evaluates `Take 204`. However, `R11_QC.md` line 28 lists `ShotVersion` as an input without specifying that QC must bind to the *originating* `ShotVersion V1` rather than the project's *current head* `ShotVersion V2`.
   - QC loads `ShotVersion V2` as context, evaluates the peaceful wide shot against the action-packed tracking shot spec, assigns a semantic adherence score of $0.12$, and marks the take as `REJECTED_SEMANTIC_MISMATCH`.
   - An automated workflow trigger immediately spawns an unnecessary retry for `ShotVersion V2`, wasting API budget.
2. **AST Cache Invalidation Failure:** R05 prompt compiler maintains an in-memory or Redis AST compilation cache keyed by `input_hash`. If a sub-entity (e.g., `CharacterVersion` face reference image) is modified without bumping the parent `ShotVersion` number, R05 serves a stale compiled prompt payload from cache, completely ignoring the updated character assets.

---

## 4. Attack Vector 3: Continuity Scoring Breakdown on Multi-Character Scene Cuts & Engine Leakage

```
[Shot 1: Wide Two-Shot]                    [Shot 2: Reverse-Angle Close-Up]
+-------------------------------+          +-------------------------------+
|   [Alice]           [Bob]     |   --->   |    (Alice)           [BOB]    |
| (Blonde/Red)    (Black/Blue)  |          | (Occluded/Blurs)  (Main Face) |
+-------------------------------+          +-------------------------------+
       |                 |                        |                 |
       v                 v                        v                 v
  Face Vector A     Face Vector B           Face Vector ?     Face Vector B'
                                           (Low Sim to A)   (Matches Bob)
                                                  |
                                                  v
                                     QC Evaluates Alice against ?
                                     --> FALSE POSITIVE REJECTION!
```

### 4.1 Multi-Character Scene Cuts, Spatial Binding & Occlusion Failures

The asset continuity model in CP-012 and `03_repo_blueprints/R04_ASSETS_CONTINUITY.md` relies on assigning an array of character UUIDs (`character_version_ids: [UUID_A, UUID_B]`) to a `ShotVersion`. This model breaks down completely in multi-character scenes:

#### Failure Mode 1: The Token Binding Problem (Attribute Bleeding)
Diffusion and autoregressive video backbones cannot reliably associate adjectives with specific subjects when multiple characters appear in the same unstructured prompt string:
- **Compiled Prompt Payload:** *"Alice, a woman with blonde hair in a red leather jacket, talking to Bob, a man with black hair in a sharp blue suit, in a dimly lit restaurant."*
- **Generative Model Artifact:** The model renders Alice with black hair in a blue suit and Bob in a red jacket (cross-attention cross-talk / attribute bleeding).
- **Architectural Defect:** The 3-layer AST provides no spatial grounding representation (e.g., bounding boxes, regional prompt masks, or layout conditioning tokens) to bind character identity tokens to distinct spatial coordinates.

#### Failure Mode 2: Multi-Face Continuity Scoring False-Positives in R11
When evaluating a generated take containing multiple characters:
- In Shot 2 (a reverse-angle shot), Bob is in sharp focus facing the camera, while Alice appears as an out-of-focus shoulder/hair silhouette in the foreground.
- The automated QC pipeline (R11) runs face detection (e.g., RetinaFace / InsightFace) on sampled frames.
- RetinaFace detects one high-confidence face (Bob) and one distorted/low-confidence boundary (Alice's ear/hair).
- R11 attempts to score both `CharacterVersion(Alice)` and `CharacterVersion(Bob)`.
- The extracted embedding for the blurred silhouette yields a cosine similarity score of $0.38$ against Alice's ground-truth embedding ($S_C < 0.85$).
- Because R04/R11 lacks **role-aware screen-presence semantics** (`PRIMARY_FOCUS`, `OVER_SHOULDER_OCCLUDED`, `BACKGROUND_EXTRA`), R11 marks the entire Take as a `CONTINUITY_FAILURE`, rejecting an aesthetically perfect shot.

### 4.2 LoRA Style Stacking, Non-Linear Blending & Proprietary Engine Leaks

Modern AI video pipelines rely on Low-Rank Adaptation (LoRA) stacks to enforce character identity and artistic style:
$$\Delta W_{\text{total}} = \alpha_{\text{char}} \Delta W_{\text{char}} + \alpha_{\text{style}} \Delta W_{\text{style}} + \alpha_{\text{lighting}} \Delta W_{\text{lighting}}$$

The proponent's attempt to abstract this inside `StyleVersion` and `ResolvedAssetSet` introduces severe cross-boundary leaks and functional collapse:

```
[Local ComfyUI Worker]                [Commercial API (Google Flow / Sora)]
Accepts: safetensors LoRA weights     Accepts: Text prompt + Reference Images ONLY
         Alpha scaling (0.75)                  Rejects raw model weights!
         Block-weight masks                    Cannot load .safetensors!
```

#### The Architectural Dilemma:
1. **Engine Leakage into Core Contracts:** If `02_contracts/domain-entities.schema.json` and `provider-request.schema.json` include LoRA tensor paths, trigger phrases, network ranks ($r$), and alpha scalings ($\alpha$), the contracts leak local open-weight engine implementations into the core domain model, violating System Invariant 7.
2. **Functional Collapse on Commercial Providers:** When a project configured with LoRA styles is routed to a commercial cloud provider (Google Flow, Sora, Runway), the provider adapter cannot load LoRA safetensors. R05 is forced to transpile the LoRA into descriptive prompt text (*"in the style of artist X"*). This transpilation produces severe stylistic divergence:
   - Text-only style descriptions fail to capture complex lighting, grain, and color palettes.
   - Downstream style continuity scoring in R11 (using CLIP image-to-image or DINOv2 feature distance) drops below acceptance thresholds ($S_{\text{style}} < 0.78$), causing the shot to fail QC repeatedly.
3. **Multi-LoRA Rank Collapse:** When multiple LoRAs are combined (e.g., Character A LoRA + Character B LoRA + Cinematic Style LoRA), their weight deltas interfere destructively in latent space, causing severe visual artifacting (clipping, saturated colors, facial deformation). The 3-layer AST has no mechanism to calculate weight orthogonality or predict multi-LoRA interference prior to execution.

---

## 5. Alternative Hypotheses & Concrete Architectural Counter-Proposals

To resolve these fatal flaws, I propose two concrete architectural alternatives to replace the 3-layer AST compiler and loose asset resolver:

```
PROPOSED ALTERNATIVE ARCHITECTURE:
+-----------------------------------------------------------------------------------+
| 1. Dispatched Transpiler Plugins with Token Budget Knapsack Solvers                |
|    [ShotVersion + Context] -> [@avf/transpiler-veo2]    -> [Veo2 Payload + Knapsack]|
|                            -> [@avf/transpiler-comfyui] -> [Comfy Graph + Weights] |
+-----------------------------------------------------------------------------------+
| 2. Unified Multimodal Conditioning Packet (UMCP)                                 |
|    - Identity Spec: InsightFace 512-d embeddings + Multi-View Reference Sheet     |
|    - Spatial Grounding: Bounding Boxes + Screen Presence Roles (FOCUS / OCCLUDED)|
|    - Engine Adapter: Discriminated Union (LoRA vs Reference Images vs Text Trigger) |
+-----------------------------------------------------------------------------------+
```

### 5.1 Alternative A: Plugin-Based Transpiler Pipeline with Token Budget Knapsack Optimization

Instead of a monolithic 3-layer AST compiler with an artificial "Engine IR", replace R05 with **Isolated Transpiler Plugins** implementing deterministic **Token Budget Knapsack Solvers**:

```typescript
// Proposed Transpiler Plugin Interface in avf-contracts
export interface IProviderTranspiler {
  readonly providerId: string;
  readonly maxContextTokens: number;
  readonly capabilities: ProviderCapabilityFlags;

  transpile(
    shot: ImmutableShotSnapshot,
    conditioning: UnifiedConditioningPacket
  ): TranspilationResult;
}

export interface TranspilationResult {
  readonly primaryPrompt: string;
  readonly negativePrompt?: string;
  readonly referenceAssets: TranspiledAssetRef[];
  readonly engineOptions: Record<string, unknown>;
  readonly tokenBudgetUsage: {
    readonly allocatedTokens: number;
    readonly maxTokens: number;
    readonly prunedNodes: string[]; // Explicit audit of dropped non-essential tokens
  };
}
```

#### Key Advantages of Alternative A:
1. **Zero Intermediate Abstraction Loss:** Each provider plugin directly transpiles the normalized shot intent into the target engine's native syntax (e.g. ComfyUI JSON node graphs with exact LoRA weights; Google Flow natural language strings; Runway image-to-video multipart payloads).
2. **Deterministic Token Knapsack Solver:** When prompt components exceed token limits, the transpiler executes a prioritized knapsack algorithm:
   $$\text{Priority: } \text{Identity Tokens} (w=10) > \text{Primary Action} (w=8) > \text{Camera Motion} (w=7) > \text{Environment} (w=4) > \text{Aesthetic Adjectives} (w=1)$$
   Non-essential adjectives are cleanly pruned, and pruned tokens are recorded in `compile_diagnostics` for full observability.
3. **Sub-Millisecond Execution:** Eliminating intermediate AST layer transformations and LLM enrichment loops reduces compilation latency to $< 1.5\text{ ms}$, entirely removing R05 as a critical path bottleneck.

---

### 5.2 Alternative B: Unified Multimodal Conditioning Packets (UMCP) with Spatial Grounding

Replace the unstructured `character_version_ids` array and loose metadata with a strongly typed **Unified Multimodal Conditioning Packet (UMCP)** in `domain-entities.schema.json`:

```json
{
  "$id": "https://avf.local/contracts/unified-multimodal-conditioning/1.0",
  "title": "UnifiedMultimodalConditioningPacket",
  "type": "object",
  "required": ["characters", "style", "spatial_grounding"],
  "properties": {
    "characters": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["character_id", "character_version_id", "presence_role", "conditioning_mode"],
        "properties": {
          "character_id": { "type": "string", "format": "uuid" },
          "character_version_id": { "type": "string", "format": "uuid" },
          "presence_role": {
            "type": "string",
            "enum": ["PRIMARY_FOCUS", "SECONDARY", "OVER_SHOULDER_OCCLUDED", "BACKGROUND_EXTRA"]
          },
          "conditioning_mode": {
            "type": "string",
            "enum": ["FACIAL_EMBEDDING_VECTOR", "MULTI_VIEW_REFERENCE_SHEET", "LORA_WEIGHTS", "TEXT_PROMPT_ONLY"]
          },
          "embedding_vector": {
            "type": "object",
            "properties": {
              "model": { "type": "string", "enum": ["InsightFace_AntelopeV2", "ArcFace_r100"] },
              "dimensions": { "type": "integer", "enum": [512, 1024] },
              "vector_uri": { "type": "string", "format": "uri" },
              "checksum": { "type": "string", "pattern": "^sha256:[a-f0-9]{64}$" }
            }
          },
          "reference_sheet": {
            "type": "object",
            "properties": {
              "front_url": { "type": "string", "format": "uri" },
              "profile_url": { "type": "string", "format": "uri" },
              "three_quarter_url": { "type": "string", "format": "uri" }
            }
          },
          "adapter_spec": {
            "type": "object",
            "properties": {
              "lora_uri": { "type": "string", "format": "uri" },
              "trigger_phrase": { "type": "string" },
              "recommended_alpha": { "type": "number", "minimum": 0.0, "maximum": 2.0 }
            }
          }
        }
      }
    },
    "spatial_grounding": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["character_id", "normalized_bounding_box"],
        "properties": {
          "character_id": { "type": "string", "format": "uuid" },
          "normalized_bounding_box": {
            "type": "object",
            "required": ["x_min", "y_min", "x_max", "y_max"],
            "properties": {
              "x_min": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
              "y_min": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
              "x_max": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
              "y_max": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
            }
          }
        }
      }
    },
    "style": {
      "type": "object",
      "required": ["style_id", "style_version_id", "color_palette", "lighting_key"],
      "properties": {
        "style_id": { "type": "string", "format": "uuid" },
        "style_version_id": { "type": "string", "format": "uuid" },
        "color_palette": { "type": "array", "items": { "type": "string" } },
        "lighting_key": { "type": "string" },
        "reference_frame_url": { "type": "string", "format": "uri" }
      }
    }
  }
}
```

#### Key Advantages of Alternative B:
1. **Solves the Multi-Character Binding Problem:** Provides spatial grounding bounding boxes enabling regional prompting / ControlNet attention masking on supporting engines, and spatial prompt separation on commercial APIs.
2. **Eliminates False-Positive QC Failures:** R11 QC evaluators use `presence_role` to apply weighted scoring:
   $$S_{\text{overall}} = \sum_{c \in \text{Characters}} w(c.\text{presence\_role}) \cdot S_{\text{face}}(c)$$
   Where $w(\text{PRIMARY\_FOCUS}) = 0.85$, $w(\text{SECONDARY}) = 0.15$, and $w(\text{OVER\_SHOULDER\_OCCLUDED}) = 0.00$. Occluded characters no longer trigger spurious QC rejections.
3. **Engine-Agnostic Polymorphism:** Allows seamless fallback: an open worker uses `embedding_vector` or `adapter_spec`, while a closed commercial API (Google Flow) uses `reference_sheet` or `trigger_phrase`, without leaking private provider schemas.

---

## 6. Detailed Comparison Matrix

| Architectural Dimension | Proponent Model (CP-011 / CP-012) | Alternative A + B (Transpilers + UMCP) | Challenger Verdict |
| :--- | :--- | :--- | :--- |
| **AST Compilation Model** | 3-layer AST (`Semantic -> Engine IR -> Target Payload`) | Direct Transpiler Plugins per Provider Family | **Alternative A** eliminates abstraction loss & $O(N \times M)$ IR complexity. |
| **Token Limit Handling** | Uncontrolled string serialization / tail truncation | Prioritized Token Budget Knapsack Solver | **Alternative A** guarantees critical identity tokens are never pruned. |
| **Compilation Latency** | High (5ms - 3500ms with LLM enrichment on critical path) | Sub-millisecond ($< 1.5\text{ ms}$ deterministic execution) | **Alternative A** removes generation startup bottlenecks. |
| **Multi-Character Continuity** | Unindexed UUID list; suffers attribute bleeding & false QC fails | Spatial Grounding BBoxes + Role-Aware Scoring Weights | **Alternative B** resolves occlusion errors & attention cross-talk. |
| **LoRA / Adapter Handling** | Loose JSON attributes; breaks on commercial APIs | Discriminated Multimodal Conditioning Packet | **Alternative B** enforces typed fallbacks between open/closed engines. |
| **In-Flight Intent Mutation** | Desynchronized state; QC compares Takes against new shot versions | Immutable Generational Snapshots tied to Job ID | **Alternative A** guarantees audit integrity and prevents retry storms. |

---

## 7. Concrete Red Team Hardening Requirements for Freeze

Before Decision Cluster 10 can be safely closed and certified for v1.0 freeze, the following mandatory remediations must be applied to the specification:

1. **Repeal Monolithic 3-Layer AST in CP-011:** Replace the 3-layer compiler in `03_repo_blueprints/R05_PROMPT_COMPILER.md` with modular provider transpiler plugins and a normative **Token Budget Knapsack Pruning Specification**.
2. **Adopt Unified Multimodal Conditioning Packet (UMCP) in CP-012:** Upgrade `03_repo_blueprints/R04_ASSETS_CONTINUITY.md` and `02_contracts/domain-entities.schema.json` to include typed `presence_role`, `embedding_vector`, and `spatial_grounding` schemas.
3. **Mandate Generational Snapshot Isolation:** Enforce in `03_repo_blueprints/R02_CORE_STATE.md` and `03_repo_blueprints/R06_WORKFLOW.md` that all generation jobs, prompt compilations, and QC evaluations bind exclusively to an immutable `(ShotVersion, PromptVersion, ConditioningSnapshot)` tuple that cannot be desynchronized by in-flight edits.
4. **Harden QC Multi-Character Evaluation Rules in R11:** Update `03_repo_blueprints/R11_QC.md` to mandate role-weighted continuity scoring, explicitly exempting `OVER_SHOULDER_OCCLUDED` and `BACKGROUND_EXTRA` characters from facial similarity thresholds.

---

**FILED BY:** R09 AI Specialist (Challenger)  
**STATUS:** FORMAL CHALLENGE SUBMITTED TO ARCHITECTURE COUNCIL
