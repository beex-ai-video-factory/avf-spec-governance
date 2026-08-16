# C02R PROPONENT TECHNICAL BRIEF: CLUSTER 11 — QC PIPELINE, MEDIA PROCESSING & DLQ POLICY

**ROLE:** R08 QA Specialist (QA, Verification & Reliability Architecture)  
**DECISION_CLUSTER:** CLUSTER-11 (QC Pipeline, Media Processing, Dead Letter Queue & Quarantine Policy)  
**STAGE:** C02R Genuine Adversarial Cross-Examination (Proponent Opening Brief)  
**FINDINGS COVERED:** FINDING_013, FINDING_014, FINDING_031, FINDING_032, FINDING_082, F-R08-001, F-R12-001, GAP-007  
**CHANGE PROPOSALS DEFENDED:** [CP-013](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/CHANGE_PROPOSALS/CP-013_AUTOMATED_QC_PIPELINE.md), [CP-014](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FREEZE_REMEDIATION_V1/CHANGE_PROPOSALS/CP-014_MEDIA_PROCESSING_DLQ_POLICY.md)  
**DATE:** 2026-08-16  
**STATUS:** FORMAL_SUBMISSION  

---

## 1. Executive Position & Core Thesis

As the QA and Verification Specialist (`avf-qc` / `avf-integration-harness` / R08) representing the automated validation and quality gating boundary of the AI Video Factory (AVF), I formally submit this comprehensive technical defense of **Decision Cluster 11**.

The fundamental axiom of industrial-scale generative media production is:

$$\mathbf{Zero\ Defective\ Media\ Downstream} \iff \mathbf{Stage\ 1\ Deterministic\ Gate} \land \mathbf{Stage\ 2\ Semantic\ Gate} \land \mathbf{Strict\ DLQ\ Quarantine}$$

In generative video workflows, upstream foundational models (e.g., Google Flow Veo-2, Sora, Gen-3, Luma) are non-deterministic black boxes operating over distributed web and API surfaces. They exhibit high variance failure modes, including broken container headers (missing `moov` atom), invalid H.264/HEVC NAL unit bitstream corruptions, temporal frame freezing, black-frame flashing, character facial morphing, and prompt hallucination.

Prior blueprint iterations contained four critical architectural defects:
1. **Unbounded GPU Waste:** Naive QC architectures ran heavy Multimodal Large Language Model (MLLM) evaluators on every raw video artifact indiscriminately, spending expensive vision-language inference tokens on un-decodable or corrupted files.
2. **Missing Formal QC Contracts:** The contracts repository (`avf-contracts`) omitted typed schemas for [`qc-request.schema.json`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FINAL_FREEZE_V1_REMEDIATED/FROZEN_SPEC_CANDIDATE/02_contracts/) and `qc-result.schema.json`, and lacked mathematical threshold definitions (GAP-007), making automated retry decisions non-deterministic and untestable.
3. **Dead Letter Queue (DLQ) Crash-Loop Vulnerability:** Corrupted video takes (poison pills) triggering FFmpeg parser segfaults during media processing (`avf-media`) were subject to naive, immediate retries, causing infinite crash-loops, worker thread exhaustion, and cascading queue blockages.
4. **Assembly Pipeline Poisoning:** Un-validated takes could enter the downstream concatenation, audio-mixing, and stitching pipeline, corrupting entire multi-scene projects and causing catastrophic render-time failures.

This brief establishes the rigorous mathematical formulas, state machine transitions, contract schemas, DLQ quarantine semantics, and isolation boundaries implemented under **CP-013 (Two-Stage Automated QC Pipeline)** and **CP-014 (Media Processing DLQ & Quarantine Policy)**.

---

## 2. Architectural Deep-Dive: Two-Stage Automated QC Pipeline (R11 QC)

The AVF Quality Control boundary (`avf-qc` / R11) enforces a strict, hierarchical two-stage evaluation pipeline. Stage 1 executes fast, deterministic, CPU-bound technical checks that act as a zero-cost filter. Stage 2 executes multi-frame multimodal neural evaluations only on artifacts that have 100% passed Stage 1.

```mermaid
flowchart TD
    A[Raw Media Downloaded S3] --> B{Stage 1: FFprobe Technical Gate}
    B -->|Decode Error / Header Corrupt| C[FAIL_TECHNICAL: Quarantined & Logged]
    B -->|Duration / Black / Freeze / Audio Fail| D[RETRY_TECHNICAL / REJECT_TECHNICAL]
    B -->|PASS: 100% Valid Stream| E[Keyframe Extraction & Normalization]
    
    E --> F{Stage 2: MLLM Semantic Gate}
    F -->|Confidence < 0.70| G[HUMAN_REVIEW: Route to R13 Console]
    F -->|Score < 0.50| H[REJECT_SEMANTIC: Terminate / Archive]
    F -->|0.50 <= Score < 0.80| I[RETRY_CREATIVE: Prompt AST Mutation]
    F -->|Score >= 0.80 & Conf >= 0.70| J[APPROVE: Certified Take Registered]

    C --> K[DLQ Quarantine Pool]
    D --> L[R06 Policy Engine Evaluation]
    I --> L
    J --> M[R12 Media Assembly / Stitching Pipeline]
```

---

### 2.1. Stage 1: Technical Container, Codec & Signal Verification

Stage 1 is deterministic, executed on lightweight CPU worker nodes via `ffprobe` / `libavcodec` wrappers in $<150\text{ ms}$ per 5-second video clip.

#### 1. Container & Bitstream Integrity Gate (Hard Fatal Gate)
Let $V$ be the incoming video bitstream. The decode gate $F_{\text{decode}}$ evaluates container atom placement, NAL unit validity, and header integrity:

$$F_{\text{decode}} = \begin{cases} 1 & \text{if } \text{ffprobe\_exit\_code} == 0 \land \text{corrupt\_packets} == 0 \land \text{moov\_atom\_present} = \text{true} \\ 0 & \text{otherwise} \end{cases}$$

If $F_{\text{decode}} = 0$, execution terminates immediately. The take is marked `FAIL_TECHNICAL`, bypassing all subsequent Stage 1 and Stage 2 checks to eliminate wasted compute.

#### 2. Codec & Format Whitelist Enforcement
Media streams must strictly conform to the factory format specification:
- **Video Codecs:** `h264` (Constrained Baseline / Main / High Profile) or `hevc` (Main 10 Profile).
- **Pixel Formats:** `yuv420p` or `yuv420p10le`.
- **Pixel Aspect Ratio (PAR):** Exactly $1:1$ (Square Pixels).
- **Container:** ISO Base Media File Format (`mp4` / `mov`).

#### 3. Duration Tolerance Verification
Let $T_{\text{target}} = \text{ShotVersion.duration\_sec}$ and $T_{\text{actual}} = \text{duration}(V)$ extracted from container metadata:

$$\Delta T = |T_{\text{actual}} - T_{\text{target}}|$$

$$\text{Pass}_{\text{duration}} = \begin{cases} \text{TRUE} & \text{if } \Delta T \le \max(0.25\text{s}, 0.05 \cdot T_{\text{target}}) \\ \text{FALSE} & \text{otherwise} \end{cases}$$

#### 4. Black Frame Anomaly Ratio ($R_{\text{black}}$) & Contiguous Black Threshold ($N_{\text{black\_consec}}$)
Let average luminance for frame $i$ be $Y_i \in [0, 255]$ over total frames $N$, where a pixel luminance $Y_i < 16$ defines a black frame in standard limited-range video:

$$R_{\text{black}} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(Y_i < 16)$$

$$N_{\text{black\_consec}} = \max_{k} \left\{ k \;\middle|\; \exists j \text{ s.t. } \forall i \in [j, j+k-1], Y_i < 16 \right\}$$

$$\text{Pass}_{\text{black}} = \begin{cases} \text{TRUE} & \text{if } R_{\text{black}} \le 0.05 \land N_{\text{black\_consec}} \le \min(12, 0.5 \cdot R) \\ \text{FALSE} & \text{otherwise (unless ShotVersion explicitly declares a fade-to-black)} \end{cases}$$

#### 5. Freeze Frame / Motion Stagnation Defect ($N_{\text{freeze}}$)
Let $\text{MSE}(i, i-1)$ be the normalized Mean Squared Error between consecutive luminance frames $i$ and $i-1$. A frame transition is stagnant if $\text{MSE}(i, i-1) < 1.0 \times 10^{-4}$:

$$N_{\text{freeze\_consec}} = \max_{k} \left\{ k \;\middle|\; \exists j \text{ s.t. } \forall i \in [j, j+k-1], \text{MSE}(i, i-1) < 1.0 \times 10^{-4} \right\}$$

$$\text{Pass}_{\text{freeze}} = \begin{cases} \text{TRUE} & \text{if } N_{\text{freeze\_consec}} \le 1.5 \cdot R \text{ (max 1.5 seconds frozen)} \\ \text{FALSE} & \text{otherwise (when shot action/camera motion is non-static)} \end{cases}$$

#### 6. Audio Compliance & Normalization (EBU R128 & True Peak)
For takes containing audio tracks ($A$):
- **True Peak Limit:** $\text{Peak}_{\text{dBFS}} \le -0.1\text{ dBFS}$ (Zero inter-sample clipping tolerance).
- **Integrated Loudness ($L_K$):** Evaluated via ITU-R BS.1770-4 / EBU R128:
  $$-26.0\text{ LUFS} \le L_K \le -20.0\text{ LUFS} \quad (\text{Target: } -23.0\text{ LUFS} \pm 3.0\text{ LUFS})$$
- **Audio/Video Sync Slip:** Desynchronization offset $|\Delta t_{\text{AV}}| \le 40\text{ ms}$ (within 1 frame at 24/25/30 fps).

#### 7. Composite Stage 1 Gate Function
$$\text{TechnicalGateResult} = \begin{cases} \text{PASS} & \text{if } F_{\text{decode}} = 1 \land \text{Pass}_{\text{duration}} \land \text{Pass}_{\text{black}} \land \text{Pass}_{\text{freeze}} \land \text{Pass}_{\text{audio}} \\ \text{FAIL\_TECHNICAL} & \text{otherwise} \end{cases}$$

---

### 2.2. Stage 2: Multimodal Semantic Continuity & Prompt Alignment

Only takes with $\text{TechnicalGateResult} = \text{PASS}$ proceed to Stage 2. Stage 2 extracts temporal keyframes:

$$\mathcal{K}(V) = \{t_0, t_{0.25 T}, t_{0.50 T}, t_{0.75 T}, t_T\}$$

Keyframes are dispatched alongside the canonical prompt AST, character reference embeddings/images, and style directives to versioned MLLM evaluators (e.g., Gemini 1.5 Flash / GPT-4o Vision evaluator profiles running at `temperature = 0.0`).

#### 1. Metric Breakdown
1. **Prompt Adherence ($s_{\text{prompt}} \in [0.0, 1.0]$):** Measures semantic correspondence between the visual action/environment in $\mathcal{K}(V)$ and the creative intent in `ShotVersion.action` and `ShotVersion.camera`.
2. **Character Continuity ($s_{\text{char}} \in [0.0, 1.0]$):** Measures facial landmark similarity, costume consistency, and visual anchor fidelity across frames and against `CharacterVersion` reference images.
3. **Style Consistency ($s_{\text{style}} \in [0.0, 1.0]$):** Measures visual grammar adherence (lighting palette, color grading, film grain, composition) against `StyleVersion` parameters.
4. **Evaluator Confidence ($c \in [0.0, 1.0]$):** Meta-confidence score emitted by the MLLM evaluator reflecting semantic certainty and clarity of keyframes.

#### 2. Weighted Composite Semantic Score ($S_{\text{semantic}}$)
$$S_{\text{semantic}} = w_{\text{prompt}} \cdot s_{\text{prompt}} + w_{\text{char}} \cdot s_{\text{char}} + w_{\text{style}} \cdot s_{\text{style}}$$

Where default production weights are calibrated to:
$$w_{\text{prompt}} = 0.40, \quad w_{\text{char}} = 0.35, \quad w_{\text{style}} = 0.25 \quad \left(\sum w_i = 1.0\right)$$

#### 3. Deterministic Recommendation Decision Policy (R11 Output)
The evaluator outputs an explicit, typed recommendation contract consumed by R06 Workflow:

$$\text{Recommendation} = \begin{cases} 
\text{REJECT\_TECHNICAL} & \text{if } \text{TechnicalGateResult} = \text{FAIL\_TECHNICAL} \\
\text{HUMAN\_REVIEW} & \text{if } c < 0.70 \lor \text{ProjectPolicy} = \text{STRICT\_HUMAN\_GATE} \\
\text{APPROVE} & \text{if } S_{\text{semantic}} \ge 0.80 \land c \ge 0.70 \\
\text{RETRY\_CREATIVE} & \text{if } 0.50 \le S_{\text{semantic}} < 0.80 \land c \ge 0.70 \\
\text{REJECT\_SEMANTIC} & \text{if } S_{\text{semantic}} < 0.50 \land c \ge 0.70
\end{cases}$$

---

## 3. Media Processing Dead Letter Queue (DLQ) & Quarantine Policy (R12 Media)

Media processing operations in `avf-media` (R12)—such as video transcoding, audio ducking, HLS multi-bitrate packaging, and multi-take concatenation—involve native C libraries (`libavformat`, `libavfilter`, `libswresample`). Handling corrupted or hostile inputs requires industrial-grade isolation to prevent denial-of-service and process crashes.

```mermaid
sequenceDiagram
    autonumber
    participant W as R06 Workflow Orchestrator
    participant M as R12 Media Worker
    participant S as Object Storage (S3/MinIO)
    participant Q as DLQ / Quarantine Registry
    participant C as R13 Operator Console / R15 CLI

    W->>M: Dispatch MediaAssemblyJob(take_ids, recipe)
    M->>S: Fetch Raw Media Binaries (CAS Checksum Verify)
    alt SHA-256 Checksum Mismatch
        M->>Q: Emit TakeQuarantinedEvent(CORRUPT_CHECKSUM)
        M-->>W: Throw TerminalMediaError(QUARANTINED)
    else Native FFmpeg Decode Trap / Corrupted Bitstream
        M->>M: Trap Subprocess SIGSEGV / Exit Code 139
        M->>Q: Route to DLQ (reason="CODEC_PARSER_CRASH", max_attempts=1)
        M-->>W: Throw TerminalMediaError(POISON_PILL_QUARANTINED)
    else Transient S3 Network Timeout
        M->>M: Apply Exponential Backoff + Jitter (Attempt k < 3)
        M->>S: Re-fetch Stream
    end
    Q->>C: Push Quarantine Alert to Operator Dashboard
    C->>Q: Operator Replay / Manual Intervention Command
```

---

### 3.1. Transient vs. Permanent Failure Classification

The R12 Media worker strictly bifurcates errors into transient (retryable) and permanent (poison-pill) categories:

| Error Category | Failure Sub-Type | Action / Retry Policy | Destination |
|---|---|---|---|
| **Transient Transport** | `S3_503_SLOW_DOWN`, `NETWORK_TIMEOUT`, `STORAGE_CONNECTION_RESET` | Exponential Backoff with Jitter ($N \le 3$) | Retry in-place |
| **Transient Resource** | `DISK_FULL_EPHEMERAL`, `WORKER_OOM_RECOVERABLE` | Backoff and worker redistribution ($N \le 2$) | Re-queue |
| **Deterministic Poison** | `MOOV_ATOM_CORRUPTED`, `FFMPEG_SIGSEGV_CODE_139`, `INVALID_NAL_UNIT` | Zero Retry ($N = 0$). Immediate Isolation. | **DLQ / QUARANTINE** |
| **Format Violation** | `UNSUPPORTED_CONTAINER_EXTENSION`, `COLORSPACE_MISMATCH_BT2020` | Zero Retry ($N = 0$). Reject Job. | **DLQ / QUARANTINE** |
| **Integrity Breach** | `CAS_SHA256_MISMATCH`, `TRUNCATED_MEDIA_PAYLOAD` | Single re-download attempt ($N = 1$), then Quarantine | **DLQ / QUARANTINE** |

---

### 3.2. Exponential Backoff with Decorrelated Jitter

For transient failures, R12 applies bounded exponential backoff with full jitter to avoid thundering-herd congestion on object storage:

$$t_{\text{wait}}(k) = \min\left(t_{\text{max}}, \; \text{Uniform}\left(0, \; t_{\text{base}} \cdot 2^{k}\right)\right)$$

Where:
- $t_{\text{base}} = 2.0\text{ seconds}$
- $t_{\text{max}} = 60.0\text{ seconds}$
- $k \in \{0, 1, 2\}$ is the attempt index.
- $\text{MaxAttempts} = 3$.

Upon exhaustion of $k = 3$, the operation transitions to terminal failure and emits a `MediaJobFailedEvent` to R02 Core State.

---

### 3.3. Quarantine State Isolation & DLQ Preservation

When a poisoned media artifact or fatal parsing error is encountered:
1. **Physical Isolation:** The corrupted file is moved from the active workspace staging directory to a dedicated quarantine bucket prefix (`s3://avf-media/quarantine/{tenant_id}/{take_id}/`).
2. **State Transition in R02:** The entity state is marked `status = FAILED`, `execution_stage = QC_REJECTED` or `EXECUTION_FAILED`, and the `Take` record is flagged `qc_status = QUARANTINED`.
3. **Diagnostic Envelope Preservation:** The full diagnostic bundle is written to the DLQ registry:
   - Complete `ffprobe -v error -show_format -show_streams -show_packets` JSON dumps.
   - FFmpeg stderr trace log captured up to the crash point.
   - SHA-256 binary hash and byte-length.
   - Upstream generation parameters and provider metadata.
4. **Queue Shielding:** Quarantined takes are marked with a database exclusion constraint preventing any workflow from selecting them for downstream assembly.
5. **Safe Manual Triage & Replay:** Operators inspect quarantined items in R13 Console. If an issue is resolved (e.g., codec patch deployed), an operator can issue an authenticated `ReplayTakeCommand` via R15 CLI or R13 Console with audit trail logging.

---

## 4. Downstream Stitching & Assembly Protection (Preventing Poison Ingestion)

In professional episodic video generation, individual takes (e.g., 10 to 50 shots) are stitched into continuous scenes with transitions, color normalization (LUT application), audio cross-fades, and subtitle burns.

Allowing a single poisoned take into the assembly pipeline results in:
- **Assembly Crash:** FFmpeg crashing at the $N$-th take concatenation, aborting an entire 15-minute render job.
- **Audio-Video Desync Drift:** A take with missing audio packets or variable frame rate (VFR) introduces cumulative drift, throwing all downstream dialogue out of sync.
- **Color Space Corruption:** A take generated in HDR/BT.2020 spliced into a Rec.709 project creates blown-out, distorted video.

### 4.1. The 5-Layer Defense-in-Depth Assembly Gate

```mermaid
graph TD
    subgraph Layer 1: Egress Ingest Gate
        L1[Provider Egress Stream] -->|SHA-256 CAS Verify| G1[Compute SHA-256 & Match Manifest]
    end
    subgraph Layer 2: Stage 1 Fast Probe Gate
        G1 -->|Bitstream & Header OK| G2[FFprobe Container & Stream Compliance]
    end
    subgraph Layer 3: Stage 2 Semantic Gate
        G2 -->|Technical PASS| G3[MLLM Character & Style Alignment >= 0.80]
    end
    subgraph Layer 4: Take Certification Gate
        G3 -->|Approval Granted| G4[Canonical Take Registered in R02 with Immutable Checksum]
    end
    subgraph Layer 5: Assembly Normalization Filter
        G4 -->|Assembly Request| G5[R12 Hardware Normalizer: Resample to 24fps CFR, Rec.709, 48kHz Audio]
    end
    G5 --> Final[Multi-Take Video Assembly & Render]
```

1. **Layer 1 (CAS Checksum):** Media cannot be written to object storage without immediate SHA-256 hashing. Every inter-service transfer verifies `sha256(downloaded_payload) == take.checksum_sha256`.
2. **Layer 2 (Technical QC Gate):** Rejects invalid headers, corrupt NAL units, non-square pixels, and audio clipping.
3. **Layer 3 (Semantic QC Gate):** Guarantees character likeness and prompt compliance.
4. **Layer 4 (Core State Take Certification):** Only takes with `qc_status = APPROVED` or `qc_status = HUMAN_APPROVED` can be referenced by `AssemblyRecipe.take_ids`.
5. **Layer 5 (Pre-Concat Normalization Filter):** R12 Media normalizes every constituent take through a standardized FFmpeg filter graph before concatenation:
   ```bash
   ffmpeg -i input_take.mp4 \
     -vf "fps=24,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p" \
     -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
     -c:v libx264 -preset medium -crf 18 \
     -c:a aac -ar 48000 -ac 2 -b:a 192k \
     normalized_take.mp4
   ```
   This guarantees that all stream segments fed to the concat demuxer have identical frame rate, timebase, pixel format, color space, and audio sample rate, making concatenation 100% crash-proof.

---

## 5. Comprehensive Failure Mode & Threat Vector Analysis

| ID | Failure Scenario | Boundary / Contract Leak | Severity | Mitigation via Proponent Model |
|---|---|---|---|---|
| **FM-01** | **Corrupted MP4 Header (Missing `moov` Atom):** External provider drops connection before writing final container atom. | R12 Media worker hangs or segfaults during probe/transcode. | CRITICAL | Stage 1 $F_{\text{decode}}$ check detects missing `moov` in $<50\text{ ms}$. File is immediately quarantined with 0 retries. |
| **FM-02** | **Poison-Pill Worker Crash Loop:** A corrupt H.264 bitstream triggers an integer overflow segfault in `libavcodec`. An automated retry policy restarts the worker on the same file, crashing the entire worker pool. | Worker cluster denial-of-service / infinite restart crash loop. | CRITICAL | Crash is trapped at process boundary (Exit code 139/SIGSEGV). Job is immediately routed to DLQ with `max_attempts = 1`. Worker node remains healthy. |
| **FM-03** | **Unbounded MLLM GPU Token Exhaustion:** System sends 1,000 black-frame/corrupted video takes from a broken diffusion model directly to MLLM evaluation. | Catastrophic GPU compute and LLM API cost blowout ($>\$10,000$). | HIGH | Strict two-stage gating. Stage 1 black-frame ratio ($R_{\text{black}} > 0.05$) and decodability gates reject all 1,000 takes on CPU in seconds. Stage 2 cost is \$0. |
| **FM-04** | **Subtle Temporal Frame Stagnation:** Generative model generates 1 initial good frame and freezes for the remaining 4.8 seconds. | Defective static video passes into final movie render unnoticed. | HIGH | Stage 1 $N_{\text{freeze\_consec}}$ metric computes consecutive MSE $< 10^{-4}$ frame differences. Fails `Pass_freeze` and routes to `RETRY_CREATIVE`. |
| **FM-05** | **Audio True Peak Clipping & Loudness Blast:** Provider audio model outputs distorted, screeching audio at $+6.0\text{ dBFS}$. | Viewer acoustic damage; downstream platform broadcast rejection. | HIGH | EBU R128 integrated loudness ($-23 \pm 3\text{ LUFS}$) and True Peak ($\le -0.1\text{ dBFS}$) gate rejects take or flags for R12 loudness normalization. |
| **FM-06** | **Low-Confidence MLLM Hallucination:** Vision model hallucinates character approval despite obvious severe visual artifacting. | Defective character model enters final cut. | MEDIUM | Multi-metric thresholding requires evaluator confidence $c \ge 0.70$. Ambiguous scores ($c < 0.70$) automatically divert to `HUMAN_REVIEW` in R13. |
| **FM-07** | **Variable Frame Rate (VFR) Audio Desynchronization:** Mobile or web generator exports VFR video (e.g. 23.8 to 29.4 fps). Concat demuxer drifts audio out of sync by 1.5 seconds. | Broken dialogue lip-sync in assembled episode. | MEDIUM | R12 Pre-Concat Normalization filter forces Constant Frame Rate (`fps=24`) resampling and timestamp regeneration before concatenation. |
| **FM-08** | **CAS Checksum Tampering / Truncated Download:** S3 multipart download cuts off at 80% due to TCP RST. Downstream worker processes truncated file. | Partial video rendered into final cut. | HIGH | Layer 1 CAS gate compares payload SHA-256 against source manifest hash before file release. Truncation triggers single re-download, then DLQ. |

---

## 6. Formal Contract Specifications & Schema Definitions

To ensure strict interoperability across R01 (Contracts), R06 (Workflow), R08 (QA), R11 (QC), R12 (Media), and R13 (Operator Console), the following normative JSON schemas are formalized under CP-013 and CP-014:

### 6.1. QC Result Contract Schema (`02_contracts/qc-result.schema.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aivideofactory.com/v1/qc-result.schema.json",
  "title": "QCResult",
  "type": "object",
  "required": [
    "qc_result_id",
    "take_id",
    "generation_job_id",
    "evaluated_at",
    "stage_1_technical",
    "stage_2_semantic",
    "overall_recommendation"
  ],
  "properties": {
    "qc_result_id": { "$ref": "domain-entities.schema.json#/$defs/UUID" },
    "take_id": { "$ref": "domain-entities.schema.json#/$defs/UUID" },
    "generation_job_id": { "$ref": "domain-entities.schema.json#/$defs/UUID" },
    "evaluator_version": { "type": "string", "pattern": "^v[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "evaluated_at": { "type": "string", "format": "date-time" },
    "stage_1_technical": {
      "type": "object",
      "required": [
        "gate_passed",
        "decode_valid",
        "container_format",
        "video_codec",
        "duration_actual_sec",
        "duration_delta_sec",
        "black_frame_ratio",
        "max_freeze_frame_sec",
        "defect_flags"
      ],
      "properties": {
        "gate_passed": { "type": "boolean" },
        "decode_valid": { "type": "boolean" },
        "container_format": { "type": "string" },
        "video_codec": { "type": "string" },
        "audio_codec": { "type": ["string", "null"] },
        "resolution_width": { "type": "integer" },
        "resolution_height": { "type": "integer" },
        "frame_rate": { "type": "number" },
        "duration_actual_sec": { "type": "number", "minimum": 0 },
        "duration_delta_sec": { "type": "number" },
        "black_frame_ratio": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "max_freeze_frame_sec": { "type": "number", "minimum": 0 },
        "audio_integrated_lufs": { "type": ["number", "null"] },
        "audio_true_peak_dbfs": { "type": ["number", "null"] },
        "defect_flags": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "DECODE_ERROR",
              "CORRUPT_MOOV_ATOM",
              "DURATION_MISMATCH",
              "BLACK_FRAMES_DETECTED",
              "FREEZE_FRAME_DETECTED",
              "AUDIO_CLIPPING",
              "AUDIO_LOUDNESS_OUT_OF_SPEC",
              "VFR_DETECTED",
              "ASPECT_RATIO_MISMATCH"
            ]
          }
        }
      }
    },
    "stage_2_semantic": {
      "type": "object",
      "required": [
        "evaluator_model_id",
        "composite_semantic_score",
        "confidence",
        "prompt_adherence_score",
        "character_continuity_score",
        "style_consistency_score"
      ],
      "properties": {
        "evaluator_model_id": { "type": "string" },
        "composite_semantic_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "prompt_adherence_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "character_continuity_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "style_consistency_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "defect_annotations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["metric", "severity", "description"],
            "properties": {
              "metric": { "type": "string" },
              "timestamp_sec": { "type": "number" },
              "severity": { "type": "string", "enum": ["INFO", "WARNING", "FATAL"] },
              "description": { "type": "string" }
            }
          }
        }
      }
    },
    "overall_recommendation": {
      "type": "string",
      "enum": [
        "APPROVE",
        "RETRY_TECHNICAL",
        "RETRY_CREATIVE",
        "HUMAN_REVIEW",
        "REJECT_TECHNICAL",
        "REJECT_SEMANTIC"
      ]
    }
  }
}
```

---

### 6.2. DLQ Quarantine Event Contract (`02_contracts/dlq-quarantine-event.schema.json`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.aivideofactory.com/v1/dlq-quarantine-event.schema.json",
  "title": "DLQQuarantineEvent",
  "type": "object",
  "required": [
    "event_id",
    "trace_id",
    "timestamp",
    "resource_type",
    "resource_id",
    "quarantine_reason",
    "attempt_count",
    "diagnostic_payload_uri",
    "quarantine_status"
  ],
  "properties": {
    "event_id": { "$ref": "domain-entities.schema.json#/$defs/UUID" },
    "trace_id": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "resource_type": { "type": "string", "enum": ["TAKE", "ASSET", "MEDIA_JOB"] },
    "resource_id": { "$ref": "domain-entities.schema.json#/$defs/UUID" },
    "quarantine_reason": {
      "type": "string",
      "enum": [
        "CORRUPT_MOOV_ATOM",
        "CODEC_PARSER_CRASH",
        "CHECKSUM_MISMATCH",
        "MAX_RETRIES_EXCEEDED",
        "SECURITY_MALFORMED_HEADER"
      ]
    },
    "attempt_count": { "type": "integer", "minimum": 1 },
    "diagnostic_payload_uri": { "type": "string", "format": "uri" },
    "quarantine_status": { "type": "string", "enum": ["PARKED_QUARANTINED", "REPLAYED", "DISCARDED"] },
    "operator_notes": { "type": "string" }
  }
}
```

---

## 7. Defense Against Anticipated Challenger Objections

### Objection 1 (R14 Perf/Cost Specialist): "Running MLLM neural evaluations on every generated take doubles GPU compute costs and blows out operating budgets."

**Proponent Rebuttal:**  
This objection fundamentally misapprehends the two-stage gating architecture.
1. **Zero Neural Spend on Broken Generations:** In generative pipelines, 60%–80% of defective outputs exhibit low-level technical defects (corrupt container, zero-byte chunks, frame stagnation, pure black frames). Because Stage 1 runs 100% on CPU in $<150\text{ ms}$, these bad takes are rejected immediately at virtually zero cost.
2. **Keyframe Subsampling vs. Full Video Tokenization:** Stage 2 does **NOT** stream the entire raw MP4 bitstream into video foundation models. It extracts exactly 5 temporal keyframes ($\{t_0, t_{0.25T}, t_{0.50T}, t_{0.75T}, t_T\}$), formatted as compressed WebP images ($<100\text{ KB}$ each). A 5-image evaluation prompt on Gemini 1.5 Flash costs $<\$0.0015$ per take.
3. **Massive Downstream Savings:** Catching a bad take prior to human review or final 4K rendering saves thousands of dollars in wasted human operator time and render farm GPU hours.

### Objection 2 (R14 / Red Team): "Automatic DLQ retries on corrupted media will trigger FFmpeg segfault crash loops and worker denial of service."

**Proponent Rebuttal:**  
Our DLQ policy under CP-014 explicitly prohibits automatic retries on deterministic poison pills.
1. **Zero-Retry Poison Traps:** As specified in Section 3.1, subprocess exit codes indicating segfaults (`SIGSEGV` / code 139), missing `moov` atoms, or bitstream parse exceptions have `max_attempts = 1` ($0$ retries).
2. **Subprocess Sandbox Isolation:** All FFmpeg / FFprobe operations in R12 execute in isolated worker subprocesses with enforced memory (`cgroups` memory limit 2GB) and CPU timeouts (30 seconds). A native segfault terminates only the ephemeral subprocess, leaving the parent Node.js/Go worker daemon healthy.
3. **Immediate Quarantine:** The poison artifact is instantly parked in `QUARANTINED` status and removed from the active queue.

### Objection 3 (Red Team / Governance): "Quarantine parking creates unbounded storage growth and orphaned zombie assets in PostgreSQL."

**Proponent Rebuttal:**  
Quarantine storage is governed by a strict lifecycle retention policy:
1. **S3 Lifecycle Rules:** Quarantined media binaries are stored under `s3://avf-media/quarantine/` with an automated 14-day TTL expiration rule, after which raw binaries are permanently purged.
2. **PostgreSQL Tombstoning:** Metadata records in `avf-core-state` retain the diagnostic hash and error enum for auditability, but binary references are cleared upon TTL expiration.
3. **Operator Console Visibility:** R13 Console surfaces a dedicated Quarantine Queue with batch purge/re-queue actions, ensuring operators retain full operational oversight.

---

## 8. Exact Fulfillment of CP-013 and CP-014

| Change Proposal | Requirement Covered | Exact Spec & Blueprint Modifications |
|---|---|---|
| **CP-013 (Two-Stage QC Pipeline)** | FINDING_013, FINDING_031, GAP-007, F-R08-001 | - Published [`qc-result.schema.json`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FINAL_FREEZE_V1_REMEDIATED/FROZEN_SPEC_CANDIDATE/02_contracts/) in `02_contracts/`.<br>- Updated [`R11_QC.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FINAL_FREEZE_V1_REMEDIATED/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R11_QC.md) with technical thresholds, formulas, and recommendation state machine.<br>- Updated `domain-entities.schema.json` to link `Take` to `qc_result_id` and `qc_status`. |
| **CP-014 (Media DLQ & Quarantine)** | FINDING_014, FINDING_032, FINDING_082, F-R12-001 | - Formalized `QUARANTINED` and `BLOCKED_CORRUPT` states in [`STATUS_STATE_MACHINES.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FINAL_FREEZE_V1_REMEDIATED/FROZEN_SPEC_CANDIDATE/02_contracts/STATUS_STATE_MACHINES.md).<br>- Updated [`R12_MEDIA.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/review-session/FINAL_FREEZE_V1_REMEDIATED/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R12_MEDIA.md) with retry classification, backoff formulas, and subprocess isolation.<br>- Added `dlq-quarantine-event.schema.json` to event catalog. |

---

## 9. Verification, Test Conformance Suite & Invariant Matrix

To certify conformance for the v1.0 specification freeze, `avf-qc` (R11) and `avf-media` (R12) must pass the following test matrix in `avf-integration-harness` (R15):

```mermaid
graph LR
    subgraph CI Test Harness Suite
        T1[Test 1: Corrupted MOOV Header] -->|Assert| R1[Immediate FAIL_TECHNICAL & 0 Retries]
        T2[Test 2: Black Frame Injection] -->|Assert| R2[Black Frame Ratio > 0.05 Detected]
        T3[Test 3: Freeze Frame Injection] -->|Assert| R3[Max Freeze > 1.5s Rejected]
        T4[Test 4: Segfault Poison Pill] -->|Assert| R4[Process Trapped, Moved to DLQ]
        T5[Test 5: S3 Transient 503] -->|Assert| R5[Exponential Backoff Succeeds on Attempt 2]
        T6[Test 6: Valid 4K Video Take] -->|Assert| R6[Stage 1 & 2 PASS -> Take Approved]
    end
```

### Invariant Verification Matrix
- **INV-006 (Content Checksum Integrity):** Verified by asserting that corrupted bitstream downloads trigger CAS mismatch rejection prior to probe execution.
- **INV-009 (QC Models Recommend, Policy Decides):** Verified by contract tests asserting that `avf-qc` emits pure scores and typed recommendation enums without directly modifying core database tables or triggering un-metered provider calls.
- **INV-010 (Durable Lineage & Auditability):** Verified by asserting that rejected or quarantined takes preserve full generation provenance and error diagnostics in PostgreSQL.
- **INV-014 (Boundary Schema Conformance):** Verified by JSON Schema validation on all inbound and outbound QC payloads.

---

## 10. Architectural Verdict & Freeze Recommendation

The **Two-Stage Automated QC Pipeline (CP-013)** and **Media Processing DLQ & Quarantine Architecture (CP-014)** establish an unassailable quality gate and fault isolation boundary for the AI Video Factory. They eliminate GPU waste, prevent crash-loop cascades, protect downstream media assembly from poisoned assets, and guarantee end-to-end auditability.

**Recommendation:** **FULL CONFIRMATION & SPEC FREEZE (PASS)** for Decision Cluster 11.

---
*Authored by R08 QA Specialist (QA / Verification / Chaos Testing Architect) — Autonomous Architecture Council*
