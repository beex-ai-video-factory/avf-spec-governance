# C02R PROPONENT REBUTTAL & FORMAL RESPONSE: CLUSTER 11
## QC Pipeline, Media Processing & Dead Letter Queue (DLQ) Architecture

**DOCUMENT_ID:** PROPONENT-RESPONSE-C02R-CL11-R08  
**ROLE:** R08 QA Specialist (QA, Verification & Reliability Architecture) — Proponent Lead  
**DECISION_CLUSTER:** Cluster 11 — QC Pipeline, Media Processing, DLQ & Quarantine Policy  
**TARGET_SPECIFICATIONS:** `03_repo_blueprints/R11_QC.md`, `03_repo_blueprints/R12_MEDIA.md`, `03_repo_blueprints/R02_CORE_STATE.md`, `03_repo_blueprints/R06_ORCHESTRATOR.md`, `02_contracts/qc-result.schema.json`, `02_contracts/provider-result.schema.json`, `02_contracts/dlq-quarantine-event.schema.json`, `02_contracts/STATUS_STATE_MACHINES.md`, `review-session/FREEZE_REMEDIATION_V1/CHANGE_PROPOSALS/CP-013_AUTOMATED_QC_PIPELINE.md`, `review-session/FREEZE_REMEDIATION_V1/CHANGE_PROPOSALS/CP-014_MEDIA_PROCESSING_DLQ_POLICY.md`  
**ADVERSARIAL_INPUT:** `review-session/FREEZE_REMEDIATION_V1/C02R_GENUINE_RAW_PATCH/CLUSTER_11_CHALLENGER_R12.md`  
**DATE:** 2026-08-16  
**STATUS:** FORMAL_PROPONENT_REBUTTAL  

---

## 1. Executive Position & Rebuttal Summary

As the QA and Verification Specialist (`avf-qc` / `avf-integration-harness` / R08) representing the automated quality validation boundary of the AI Video Factory, I formally submit this comprehensive **Proponent Rebuttal and Response** to the adversarial challenge filed by R12 (Media Processing Specialist) in `RED-TEAM-C02R-CL11-R12`.

### 1.1 Acceptance and Concurrence with Physical Media Realities
The adversarial challenge by R12 raises critical, high-impact systems engineering realities regarding:
1. **GPU Head-of-Line (HoL) Blocking:** Synchronously coupling heavy Multimodal LLM (MLLM) evaluation to the ingestion path blocks downstream timeline assembly.
2. **False-Positive Quarantine Poisoning:** Direct WAN/CDN streaming probes using `ffprobe` conflate transient network I/O stalls with genuine container corruption, triggering destructive re-generation loops and double billing.
3. **Quarantine Storage Bloat:** Unbounded raw video retention during provider outages exhausts S3 storage and fragments PostgreSQL MVCC tables.

Rather than invalidating the foundational thesis of **CP-013 (Two-Stage QC Pipeline)** and **CP-014 (Media Processing DLQ & Quarantine Policy)**, R12's cross-examination provides the necessary physical systems clarity to evolve our baseline architecture into a hardened, industrial-grade implementation.

### 1.2 Core Rebuttal Thesis
The Proponent team formally presents the following technical resolutions:
- **Evolved Three-Tier Progressive QC Architecture:** We preserve the strict separation between deterministic technical validation and probabilistic semantic evaluation, but decouple execution into **Tier 0 (Staged Ingestion Guard)**, **Tier 1 (Synchronous Deterministic Ingest, $<100\text{ms}$ CPU)**, and **Tier 2 (Asynchronous Decoupled Multimodal Grading with Lazy Evaluation)**. This unlocks optimistic timeline editing immediately after Tier 1 while eliminating GPU starvation.
- **Strict Transport vs. Bitstream Error Disambiguation:** Ingest workers stage media to local NVMe storage and verify SHA-256 digests before probing. Transient transport drops (`HTTP 429`, `503`, TCP drops) are handled via resumable chunked retries without state alteration, zero DLQ routing, and zero provider re-billing.
- **Compact Forensic Quarantine & 7-Day S3 TTL:** Quarantined media generates lightweight 3x3 JPEG contact sheets ($<150\text{KB}$) and 5-second proxy clips ($<1\text{MB}$) for operator triage. Raw corrupted binaries are automatically purged via a strict **7-Day S3 Lifecycle Configuration**, and PostgreSQL tables are monthly range-partitioned.
- **Retained and Hardened Status of CP-013 and CP-014:** CP-013 and CP-014 are **RETAINED AND AUGMENTED**. Their core invariants—zero defective media downstream, deterministic gate formulas, poison-pill isolation, and DLQ protection—are fully preserved and elevated to production-grade status.

---

## 2. Rebuttal to Attack Vector 1: GPU Queue Choke Points & Ingestion HoL Blocking

```
+---------------------------------------------------------------------------------------------------------+
|                                    THREE-TIER PROGRESSIVE QC PIPELINE                                   |
+---------------------------------------------------------------------------------------------------------+

  [Provider Output URL]
           |
           v
+---------------------------------------------------------------------+
| TIER 0: Staged Ingestion Guard (Resumable NVMe Download + SHA-256)   |  (Transport Retries: No DLQ)
+---------------------------------------------------------------------+
           | Complete File Verified
           v
+---------------------------------------------------------------------+
| TIER 1: Synchronous Deterministic Technical Gate (CPU-Only <100ms)  |  (Bitstream / Codec Check)
+---------------------------------------------------------------------+
           |
           +---------------------------------------------+
           | Technical PASS (<100ms)                     | Technical FAIL
           v                                             v
+------------------------------------+        +------------------------------------+
| OPTIMISTIC ROUGH-CUT PIPELINE      |        | COMPACT FORENSIC QUARANTINE        |
| - Take Status: TECHNICAL_QC_PASSED |        | - 3x3 Contact Sheet (<150KB)       |
| - Timeline Drafting & Proxy Ready  |        | - 5s Diagnostic Proxy (<1MB)       |
| - Zero GPU Blocking                |        | - 7-Day S3 TTL on Raw Binary       |
+------------------------------------+        | - Media DLQ Routing                |
           |                                  +------------------------------------+
           v (Async Event)
+---------------------------------------------------------------------+
| TIER 2: Asynchronous Semantic & MLLM Grading (Decoupled GPU Queue)  |
| - Priority-Weighted Task Queue (avf-qc-evaluators)                  |
| - Batch DINOv2 / CLIP Embeddings                                    |
| - Lazy Evaluation Policy (Primary Candidate Takes Only)             |
| - Final Take State: FULLY_GRADED -> QC_APPROVED / REJECTED          |
+---------------------------------------------------------------------+
```

### 2.1 Mathematical Modeling of Batch Production & Latency Reduction
Challenger R12 demonstrated that evaluating 180 takes (60 shots $\times$ 3 candidates) synchronously with 5.0s MLLM latency creates 900s (15 minutes) of blocking queue depth per project, scaling to $>1.25\text{ hours}$ under multi-project concurrency.

We accept this latency analysis and counter with the **Optimistic Technical Ingest** model:
- **Baseline Synchronous Blocking Latency ($T_{\text{baseline}}$):**
  $$T_{\text{baseline}} = T_{\text{tech}} + T_{\text{sem}} \approx 100\text{ms} + 5,000\text{ms} = 5,100\text{ms per take}$$
- **Three-Tier Progressive QC Critical Path Latency ($T_{\text{progressive}}$):**
  $$T_{\text{progressive}} = T_{\text{tech}} \le 100\text{ms per take}$$
- **Critical Path Speedup:**
  $$\text{Latency Reduction} = \frac{5,100\text{ms} - 100\text{ms}}{5,100\text{ms}} = \mathbf{98.04\%}$$

Upon passing Tier 1, the take immediately transitions to `TECHNICAL_QC_PASSED` in `avf-core-state` (R02). The rough-cut assembly engine and proxy streamer in `avf-media` (R12) can instantly begin timeline concatenation and UI thumbnail rendering. Downstream human operators and automated rough-cut builders are **never blocked by GPU queues**.

### 2.2 Decoupled Asynchronous Tier 2 Architecture & Priority Queuing
Tier 2 semantic grading is executed out-of-band via an asynchronous Celery/Temporal background worker pool (`avf-qc-evaluators`):
1. **Dynamic Priority Weighting:**
   - **Priority 1 (Interactive Director Focus):** Takes currently active on the operator's preview viewport in R13 Console.
   - **Priority 2 (Primary Candidate Takes):** Highest-ranked candidate takes selected by the automated multi-take heuristic selector.
   - **Priority 3 (Batch Background Archive):** Secondary variations and speculative candidates.
2. **Lazy / On-Demand Evaluation Policy:**
   - In standard production runs where $N=3$ candidate variations are generated per shot, only the primary candidate ($k=1$) is automatically submitted to full MLLM grading.
   - Candidates $k \in \{2, 3\}$ undergo lightweight embedding extraction (CLIP/DINOv2) but bypass heavy MLLM visual reasoning unless the director explicitly selects them in R13 Console.
   - **Economic Impact:** Reduces overall VLM/MLLM token consumption by **$66.7\%$** across standard 3-take production batches.

### 2.3 Hardware Resource Isolation & NVDEC / CUDA Concurrency Protection
To address R12's findings on VRAM fragmentation and hardware decoder exhaustion:
1. **Process Boundary Isolation:** Media decoding (FFmpeg with libavcodec) and neural inference (PyTorch / TensorRT) run in separate worker processes with independent memory limits (`cgroups` memory limit 2GB for decode workers; CUDA Unified Memory management for GPU inference workers).
2. **Keyframe Extraction on CPU:** Tier 2 keyframe extraction ($\{t_0, t_{0.25T}, t_{0.50T}, t_{0.75T}, t_T\}$) is executed on CPU workers using `libjpeg-turbo` / `webp` encoders. The GPU receives only compact image tensors ($5 \times 100\text{KB}$ WebP images), completely freeing NVDEC hardware decode chips from video raster buffer pressure.
3. **TensorRT Dynamic Batching:** Vision Transformer embeddings (DINOv2 ViT-L/14) are batched across frames and concurrent takes with dynamic micro-batching (batch size 16–32), maximizing GPU tensor core utilization at $>85\%$ compute efficiency.

---

## 3. Rebuttal to Attack Vector 2: False-Positive Ingest Quarantine & CDN Transport Isolation

### 3.1 Prohibition of Direct WAN Streaming Probes
The Proponent unconditionally agrees with R12 that running `ffprobe` directly over remote HTTP/S3 CDN URLs is an anti-pattern. External video generation APIs (Google Veo, Runway, Kling, Sora) frequently stream non-faststart MP4 containers where the `moov` atom resides at the end of the file, making HTTP range queries fragile.

**Binding Architectural Mandate (Tier 0 Ingest Guard):**
1. **Direct network streaming `ffprobe` is STRICTLY PROHIBITED.**
2. All incoming provider outputs must be fully downloaded to local NVMe scratch storage (`/var/scratch/avf-ingest/{job_id}/`) via a resumable, chunk-aware HTTP/S3 client before any media inspection occurs.
3. Once downloaded, the ingest worker verifies the payload SHA-256 checksum against the manifest and executes `qt-faststart` to ensure atom ordering prior to invoking FFprobe.

### 3.2 Authoritative Error Disambiguation Matrix
To prevent transient CDN packet drops from triggering false-positive take quarantine and expensive re-generation loops, we formalize the following four-tier error classification boundary:

```
+-------------------------------------------------------------------------------------------------------------+
|                                    INGESTION ERROR DISAMBIGUATION TAXONOMY                                  |
+-------------------------------------------------------------------------------------------------------------+
|  CATEGORY             | ERROR SIGNATURES                     | SYSTEM ACTION           | DLQ / BILLING      |
+-----------------------+--------------------------------------+-------------------------+--------------------+
| TRANSPORT_TRANSIENT   | HTTP 429, 502, 503, 504, ECONNRESET,  | Resumable chunk retry   | DLQ: NO            |
|                       | ETIMEDOUT, TCP Window Zero           | Exponential backoff     | Re-bill: NO        |
|                       |                                      | Take: DOWNLOADING       | State: UNCHANGED   |
+-----------------------+--------------------------------------+-------------------------+--------------------+
| TRANSPORT_PERMANENT   | HTTP 401, 403, 404, 410,             | Refresh presigned URL   | DLQ: Ingest Alert  |
|                       | Presigned URL Signature Expired      | Alert ingest worker     | Re-bill: NO        |
|                       |                                      | Take: INGEST_FAILED     | Provider Re-fetch  |
+-----------------------+--------------------------------------+-------------------------+--------------------+
| MEDIA_CONTAINER_      | Missing moov atom on complete file,  | Generate Forensics      | DLQ: MEDIA_DLQ     |
| CORRUPT               | Invalid NAL units, Bitstream Corrupt,| S3 Quarantine Prefix    | Re-bill: CIRCUIT-  |
|                       | FFprobe Exit Code != 0               | Take: FAILED_TECH_QC    |          GATED     |
+-----------------------+--------------------------------------+-------------------------+--------------------+
| MEDIA_CODEC_          | Codec not in whitelist (e.g.         | Isolate binary          | DLQ: MEDIA_DLQ     |
| UNSUPPORTED           | ProRes 4444 XQ instead of 422 HQ)    | Take: FAILED_TECH_QC    | Re-bill: NO        |
|                       |                                      | Compiler Warning        | (Requires fix)     |
+-------------------------------------------------------------------------------------------------------------+
```

### 3.3 Zero Re-Generation Guarantee on Transport Hiccups
Under no circumstances shall a `TRANSPORT_TRANSIENT` or `TRANSPORT_PERMANENT` error:
1. Transition a `Take` entity into `FAILED_TECHNICAL_QC` or `QUARANTINED`.
2. Count toward provider container corruption failure rates.
3. Trigger an automatic generation re-submission to external provider APIs.

The download manager applies bounded exponential backoff with full decorrelated jitter:
$$t_{\text{wait}}(k) = \min\left(30.0, \; \text{Uniform}\left(0, \; 1.5 \cdot 2^{k}\right)\right) \quad \text{for } k \in \{1, 2, 3, 4, 5\}$$

If transport retries are exhausted ($k=5$), the task emits an `INGEST_TRANSPORT_FAILED` diagnostic event and requests a presigned URL refresh from the provider adapter. The original generation job remains preserved, **guaranteeing zero double-billing and zero credit waste**.

---

## 4. Rebuttal to Attack Vector 3: Quarantine Storage Boundedness, Database Health & Forensics

### 4.1 Compact Forensic Extraction Pipeline
When genuine media container corruption occurs (`MEDIA_CONTAINER_CORRUPT`), storing uncompressed 150MB–500MB raw video binaries in operator triage queues is wasteful and creates unnecessary S3 egress overhead.

The Proponent mandates the **Compact Forensic Extraction Pipeline** in `avf-media` (R12):
```bash
# 1. Forensic Contact Sheet: 3x3 Frame Grid (100-150KB JPEG)
ffmpeg -v error -i local_corrupted_take.mp4 \
  -vf "select='not(mod(n\,30))',scale=320:180,tile=3x3" \
  -frames:v 1 -q:v 3 \
  forensic_contact_sheet.jpg

# 2. Diagnostic Proxy: First 5 Seconds Low-Bitrate Stream (<1MB MP4)
ffmpeg -v error -t 5 -i local_corrupted_take.mp4 \
  -vf "scale=640:360" -c:v libx264 -preset ultrafast -crf 32 -an \
  forensic_proxy.mp4

# 3. Structured Probe JSON & Error Diagnostic (<20KB JSON)
ffprobe -v error -show_format -show_streams -show_error -print_format json \
  local_corrupted_take.mp4 > probe_diagnostic.json
```

**Operational Benefits:**
- R13 Operator Console loads lightweight contact sheets ($<150\text{KB}$) and diagnostic JSON ($<20\text{KB}$) instantly, eliminating 99.8% of DLQ dashboard loading bandwidth.
- Operators can visually identify corrupted scanlines, green frames, or aspect ratio distortions without downloading the raw media file.

### 4.2 S3 Object Storage Lifecycle Configuration (Strict 7-Day TTL)
To prevent multi-terabyte storage accumulation during upstream provider outages, object storage buckets enforce a formal lifecycle policy:

```xml
<LifecycleConfiguration>
    <!-- Raw Corrupted Media Binaries: 7-Day Hard Deletion -->
    <Rule>
        <ID>QuarantineRawBinaries7DayTTL</ID>
        <Filter>
            <Prefix>quarantine/raw-binaries/</Prefix>
        </Filter>
        <Status>Enabled</Status>
        <Expiration>
            <Days>7</Days>
        </Expiration>
    </Rule>
    <!-- Lightweight Forensic Artifacts & JSON Logs: 30-Day Retention -->
    <Rule>
        <ID>QuarantineForensics30DayRetention</ID>
        <Filter>
            <Prefix>quarantine/forensics/</Prefix>
        </Filter>
        <Status>Enabled</Status>
        <Expiration>
            <Days>30</Days>
        </Expiration>
    </Rule>
</LifecycleConfiguration>
```

#### Steady-State Storage Boundedness Proof:
Let $R_{\text{fail}}$ be the daily volume of corrupted bytes ingested during an active production campaign ($R_{\text{fail}} = 50\text{ GB/day}$).  
Under the 7-day TTL lifecycle policy, the total quarantine storage footprint $S_{\text{quarantine}}(t)$ reaches steady-state equilibrium at $t \ge 7\text{ days}$:
$$S_{\text{quarantine\_steady}} = \sum_{\tau=0}^{6} R_{\text{fail}} = 7 \times 50\text{ GB} = \mathbf{350\text{ GB (Strictly Bounded)}}$$
Without the 7-day TTL, storage grows linearly ($S_{\text{unbounded}}(90\text{ days}) = 4.5\text{ TB}$). The 7-day TTL bounds cloud storage spend and prevents orphan bucket bloat.

### 4.3 PostgreSQL Relational Table Protection & Monthly Range Partitioning
To safeguard `avf-core-state` (R02) from MVCC table bloat and index fragmentation:
1. **Partitioning Strategy:** The `media_dlq_messages` table is partitioned by range on `created_at` in monthly intervals (`PARTITION BY RANGE (created_at)`).
2. **Log Sanitization:** Raw multi-megabyte FFmpeg stdout/stderr logs are written directly to S3 (`s3://avf-media/quarantine/forensics/{dlq_id}.log`), and only the S3 URI is stored in PostgreSQL.
3. **Project Quota Limits:** A project DLQ storage ceiling is enforced at 25GB. If a project exceeds its quota, an automated Least-Recently-Used (LRU) policy purges the oldest raw binaries while preserving structured JSON metadata.

### 4.4 Automated Provider Circuit Breaking Policy
To halt catastrophic failure cascades when an external provider experiences an encoding regression:
- **Sliding Window:** Rolling 10-minute window (minimum 10 generation takes).
- **Breaker Threshold:** Container corruption rate $>15\%$ ($\frac{\text{Count}(\text{MEDIA\_CONTAINER\_CORRUPT})}{\text{Total Ingest Attempts}} > 0.15$).
- **Action on Trip (`CIRCUIT_OPEN`):**
  1. Orchestrator immediately pauses dispatch to the defective provider.
  2. Active workflows automatically failover to secondary provider adapters (e.g. fallback from Provider A to Provider B).
  3. Emit high-priority PagerDuty/Slack alert `ALERT_PROVIDER_CIRCUIT_TRIPPED`.
  4. Canary probing: Sends 1 test generation every 2 minutes; resets to `CLOSED` after 3 consecutive successful takes.

---

## 5. Status of Change Proposals: CP-013 and CP-014

The Proponent provides the following explicit clarification regarding the status of the change proposals in Decision Cluster 11:

### 5.1 CP-013 (Two-Stage Automated QC Pipeline)
**STATUS: RETAINED, AUGMENTED & HARDENED.**
- **Preserved Invariants:**
  - Strict separation of deterministic container/codec verification from multimodal semantic grading.
  - Zero defective media downstream invariant ($\mathbf{Zero\ Defective\ Media\ Downstream}$).
  - Mathematical formulas for duration tolerance ($\Delta T \le \max(0.25\text{s}, 0.05 \cdot T_{\text{target}})$), black frame ratio ($R_{\text{black}} \le 0.05$), freeze frame detection ($N_{\text{freeze}} \le 1.5\text{s}$), and EBU R128 audio loudness ($-23 \pm 3\text{ LUFS}$).
- **Architectural Augmentation:**
  - Expanded from a synchronous two-stage blocking gate into the **Three-Tier Progressive QC Architecture** (Tier 0 Staged Ingest, Tier 1 Synchronous Technical Gate $<100\text{ms}$ CPU, Tier 2 Asynchronous Multimodal Grading with Lazy Evaluation).
  - Introduction of progressive take states: `PENDING` $\to$ `DOWNLOADING` $\to$ `TECHNICAL_QC_PASSED` $\to$ `SEMANTIC_QC_RUNNING` $\to$ `QC_APPROVED`.

### 5.2 CP-014 (Media Processing DLQ & Quarantine Policy)
**STATUS: RETAINED, AUGMENTED & HARDENED.**
- **Preserved Invariants:**
  - Zero-retry isolation on deterministic poison pills (FFmpeg segfaults, corrupt NAL units, invalid container headers).
  - Subprocess sandbox isolation with strict memory and CPU execution limits.
  - Full diagnostic provenance and operator replay capabilities in R13 Console.
- **Architectural Augmentation:**
  - Implementation of strict **Transport vs. Bitstream Error Disambiguation** to eliminate false-positive quarantine from CDN stalls.
  - Mandatory **Compact Forensic Extraction Pipeline** ($<150\text{KB}$ contact sheets, $<1\text{MB}$ proxies, $<20\text{KB}$ JSON).
  - Enforcement of **7-Day S3 Deletion TTL** on raw quarantined binaries and monthly range partitioning on PostgreSQL `media_dlq_messages`.
  - Addition of automated **Provider Circuit Breakers** (15% failure threshold over 10 minutes).

---

## 6. Formal Contracts, Schemas and DDL Specifications

### 6.1 Schema: `qc-result.schema.json`
Authoritative contract defining technical and semantic evaluation results emitted by `avf-qc` (R11):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.avf.internal/qc-result.schema.json",
  "title": "QCResult",
  "type": "object",
  "required": [
    "qc_result_id",
    "take_id",
    "shot_version_id",
    "evaluator_version",
    "evaluation_tier",
    "technical_metrics",
    "recommendation",
    "evaluated_at"
  ],
  "properties": {
    "qc_result_id": { "type": "string", "format": "uuid" },
    "take_id": { "type": "string", "format": "uuid" },
    "shot_version_id": { "type": "string", "format": "uuid" },
    "evaluator_version": { "type": "string", "pattern": "^v[0-9]+\\.[0-9]+\\.[0-9]+$" },
    "evaluation_tier": {
      "type": "string",
      "enum": ["TIER_1_TECHNICAL_ONLY", "TIER_2_FULL_MULTIMODAL"]
    },
    "technical_metrics": {
      "type": "object",
      "required": [
        "decode_valid",
        "container_format",
        "duration_ms",
        "width",
        "height",
        "fps",
        "video_codec",
        "black_frame_ratio",
        "frozen_frame_duration_ms",
        "audio_sync_drift_ms"
      ],
      "properties": {
        "decode_valid": { "type": "boolean" },
        "container_format": { "type": "string" },
        "duration_ms": { "type": "integer", "minimum": 0 },
        "width": { "type": "integer", "minimum": 1 },
        "height": { "type": "integer", "minimum": 1 },
        "fps": { "type": "number", "minimum": 0 },
        "video_codec": { "type": "string" },
        "audio_codec": { "type": ["string", "null"] },
        "bit_rate_kbps": { "type": "integer" },
        "black_frame_ratio": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "frozen_frame_duration_ms": { "type": "integer", "minimum": 0 },
        "audio_sync_drift_ms": { "type": "number" },
        "moov_atom_position": { "type": "string", "enum": ["START", "END", "UNKNOWN"] }
      }
    },
    "semantic_metrics": {
      "type": "object",
      "required": [
        "character_similarity_score",
        "style_consistency_score",
        "motion_smoothness_score",
        "mllm_artifact_score",
        "composite_score"
      ],
      "properties": {
        "character_similarity_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "style_consistency_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "motion_smoothness_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "mllm_artifact_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
        "composite_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
      }
    },
    "defect_annotations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["metric", "severity", "description"],
        "properties": {
          "metric": { "type": "string" },
          "severity": { "type": "string", "enum": ["FATAL", "MAJOR", "MINOR", "INFO"] },
          "start_frame": { "type": "integer", "minimum": 0 },
          "end_frame": { "type": "integer", "minimum": 0 },
          "description": { "type": "string" }
        }
      }
    },
    "recommendation": {
      "type": "string",
      "enum": [
        "APPROVE",
        "RETRY_TECHNICAL",
        "RETRY_CREATIVE",
        "HUMAN_REVIEW",
        "REJECT"
      ]
    },
    "evaluated_at": { "type": "string", "format": "date-time" }
  }
}
```

---

### 6.2 Schema: `dlq-event.schema.json`
Authoritative contract for messages dispatched to the Media DLQ:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.avf.internal/dlq-event.schema.json",
  "title": "DLQEvent",
  "type": "object",
  "required": [
    "dlq_message_id",
    "project_id",
    "job_id",
    "take_id",
    "failure_category",
    "error_code",
    "attempt_count",
    "max_attempts",
    "forensics",
    "occurred_at"
  ],
  "properties": {
    "dlq_message_id": { "type": "string", "format": "uuid" },
    "project_id": { "type": "string", "format": "uuid" },
    "job_id": { "type": "string", "format": "uuid" },
    "take_id": { "type": "string", "format": "uuid" },
    "provider_id": { "type": "string" },
    "failure_category": {
      "type": "string",
      "enum": [
        "MEDIA_CONTAINER_CORRUPT",
        "MEDIA_CODEC_UNSUPPORTED",
        "TRANSCODE_PROCESS_CRASH",
        "ASSEMBLY_MUX_FAILURE"
      ]
    },
    "error_code": { "type": "string" },
    "error_message": { "type": "string" },
    "attempt_count": { "type": "integer", "minimum": 1 },
    "max_attempts": { "type": "integer", "default": 3 },
    "quarantine_status": {
      "type": "string",
      "enum": ["ACTIVE_RETRY", "PARKED_QUARANTINE", "RESOLVED_REPLAYED", "DISCARDED"]
    },
    "forensics": {
      "type": "object",
      "required": ["contact_sheet_uri", "diagnostic_proxy_uri", "log_uri", "raw_binary_ttl_timestamp"],
      "properties": {
        "contact_sheet_uri": { "type": "string" },
        "diagnostic_proxy_uri": { "type": "string" },
        "log_uri": { "type": "string" },
        "raw_binary_ttl_timestamp": { "type": "string", "format": "date-time" }
      }
    },
    "occurred_at": { "type": "string", "format": "date-time" }
  }
}
```

---

### 6.3 PostgreSQL DDL Specification
Authoritative relational schema for `avf-core-state` (R02):

```sql
-- DDL for Decision Cluster 11: QC Pipeline, Media Processing & DLQ

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. QC Results Table
CREATE TABLE qc_results (
    qc_result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    shot_id UUID NOT NULL,
    shot_version_id UUID NOT NULL,
    take_id UUID NOT NULL,
    evaluator_version VARCHAR(32) NOT NULL,
    evaluation_tier VARCHAR(32) NOT NULL,
    technical_metrics JSONB NOT NULL,
    semantic_metrics JSONB NULL,
    defect_annotations JSONB NOT NULL DEFAULT '[]'::jsonb,
    composite_score NUMERIC(5, 4) NULL,
    recommendation VARCHAR(32) NOT NULL,
    evaluated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_qc_results_tier CHECK (evaluation_tier IN ('TIER_1_TECHNICAL_ONLY', 'TIER_2_FULL_MULTIMODAL')),
    CONSTRAINT ck_qc_results_rec CHECK (recommendation IN ('APPROVE', 'RETRY_TECHNICAL', 'RETRY_CREATIVE', 'HUMAN_REVIEW', 'REJECT')),
    CONSTRAINT fk_qc_results_take FOREIGN KEY (take_id) REFERENCES takes(take_id) ON DELETE RESTRICT
);

CREATE INDEX idx_qc_results_take_tier ON qc_results (take_id, evaluation_tier);
CREATE INDEX idx_qc_results_shot_version ON qc_results (shot_version_id, evaluated_at DESC);

-- 2. Range-Partitioned Media Dead Letter Queue Table
CREATE TABLE media_dlq_messages (
    dlq_message_id UUID NOT NULL DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    job_id UUID NOT NULL,
    take_id UUID NOT NULL,
    provider_id VARCHAR(64) NOT NULL,
    failure_category VARCHAR(64) NOT NULL,
    error_code VARCHAR(128) NOT NULL,
    error_message TEXT NOT NULL,
    attempt_count INTEGER NOT NULL DEFAULT 1,
    max_attempts INTEGER NOT NULL DEFAULT 3,
    quarantine_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE_RETRY',
    contact_sheet_uri TEXT NOT NULL,
    diagnostic_proxy_uri TEXT NOT NULL,
    log_uri TEXT NOT NULL,
    raw_binary_uri TEXT NOT NULL,
    raw_binary_ttl_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ NULL,
    resolved_by VARCHAR(128) NULL,
    resolution_notes TEXT NULL,
    PRIMARY KEY (dlq_message_id, created_at),
    CONSTRAINT ck_dlq_category CHECK (failure_category IN ('MEDIA_CONTAINER_CORRUPT', 'MEDIA_CODEC_UNSUPPORTED', 'TRANSCODE_PROCESS_CRASH', 'ASSEMBLY_MUX_FAILURE')),
    CONSTRAINT ck_dlq_status CHECK (quarantine_status IN ('ACTIVE_RETRY', 'PARKED_QUARANTINE', 'RESOLVED_REPLAYED', 'DISCARDED'))
) PARTITION BY RANGE (created_at);

-- Monthly Partitions for 2026
CREATE TABLE media_dlq_messages_2026_08 PARTITION OF media_dlq_messages
    FOR VALUES FROM ('2026-08-01 00:00:00+00') TO ('2026-09-01 00:00:00+00');

CREATE TABLE media_dlq_messages_2026_09 PARTITION OF media_dlq_messages
    FOR VALUES FROM ('2026-09-01 00:00:00+00') TO ('2026-10-01 00:00:00+00');

CREATE INDEX idx_media_dlq_status_project ON media_dlq_messages (quarantine_status, project_id, created_at DESC);
CREATE INDEX idx_media_dlq_ttl ON media_dlq_messages (raw_binary_ttl_at) WHERE quarantine_status = 'PARKED_QUARANTINE';

-- 3. Take Entity QC Status Constraints in Takes Table
ALTER TABLE takes DROP CONSTRAINT IF EXISTS ck_takes_qc_status;

ALTER TABLE takes ADD CONSTRAINT ck_takes_qc_status CHECK (
    qc_status IN (
        'PENDING', 
        'DOWNLOADING',
        'TECHNICAL_QC_PASSED', 
        'FAILED_TECHNICAL_QC', 
        'SEMANTIC_QC_RUNNING', 
        'QC_APPROVED', 
        'FAILED_SEMANTIC_QC', 
        'QUARANTINED', 
        'OVERRIDDEN'
    )
);
```

---

## 7. Direct Response & Comparative Analysis Matrix

| Challenge Dimension | Challenger R12 Stance | Proponent R08 Formal Position | Resolution & System Impact |
| :--- | :--- | :--- | :--- |
| **Stage 2 MLLM Choke Point** | Synchronous VLM evaluation blocks timeline assembly for 15+ minutes. | **Concur & Resolve:** Restructure into Three-Tier Progressive QC with $<100\text{ms}$ CPU Tier 1 gate. | Optimistic rough-cut editing unlocked instantly; 98.04% latency reduction on critical path. |
| **Lazy MLLM Evaluation** | Evaluating 5 candidate takes per shot wastes 400% excess GPU compute. | **Concur & Resolve:** Implement Lazy Evaluation Policy grading only primary takes automatically. | 66.7% reduction in VLM inference costs across standard 3-take generation batches. |
| **CDN Transport Stalls** | Direct streaming probes misclassify network drops as corrupted containers. | **Concur & Resolve:** Mandate staged NVMe download + SHA-256 validation prior to FFprobe. | Zero false-positive DLQ routings; zero unnecessary provider re-billing. |
| **Non-Faststart MP4s** | Streaming probes fail on trailing `moov` atoms with exit code 1. | **Concur & Resolve:** Run `qt-faststart` box re-indexing on staged local files before probe. | Complete elimination of false `moov atom not found` rejections. |
| **Quarantine Storage Bloat** | Quarantining raw 150MB binaries indefinitely creates multi-terabyte S3 bloat. | **Concur & Resolve:** Enforce 7-Day S3 TTL on raw binaries and 30-Day TTL on forensics. | Steady-state quarantine storage strictly capped; eliminates phantom cloud spend. |
| **Relational Table Health** | Storing raw crash logs in PostgreSQL causes MVCC bloat and query stalls. | **Concur & Resolve:** Range-partition `media_dlq_messages` monthly; offload logs to S3. | Preserves PostgreSQL B-tree index performance and prevents autovacuum lag. |
| **Provider Failure Cascades** | Upstream encoding bugs trigger positive-feedback generation loops. | **Concur & Resolve:** Mandate Automated Provider Circuit Breakers (15% threshold over 10m). | Halts downstream spend bleed; initiates automated fallback to secondary providers. |

---

## 8. Conformance to Architectural Invariants

The remediated Cluster 11 architecture strictly satisfies all canonical AVF invariants:

1. **INV-006 (Content-Addressed Immutability):** Every ingested take is hashed (SHA-256) upon Tier 0 staging. The hash is immutably recorded in `takes.checksum_sha256` and verified before any assembly or transcoding operation.
2. **INV-008 (Payload & Container Integrity):** Media containers must pass Tier 1 deterministic validation ($F_{\text{decode}} = 1$) before entering rough-cut assembly or Tier 2 grading.
3. **INV-009 (QC Models Recommend, Policy Decides):** `avf-qc` emits pure, typed `QCResult` evaluations and recommendation enums. Workflow policy engines (R06) and human operators (R13) own state transitions and re-prompting decisions.
4. **INV-010 (Durable Lineage & Auditability):** All evaluation results, defect annotations, and forensic contact sheet URIs are durably recorded in `qc_results` and `media_dlq_messages`.
5. **INV-014 (Boundary Schema Conformance):** All inter-service communications strictly conform to `qc-result.schema.json`, `dlq-event.schema.json`, and `provider-result.schema.json`.
6. **INV-015 (Continuity Certification):** Final master assembly requires `take.qc_status == 'QC_APPROVED'` or explicit human override (`'OVERRIDDEN'`), ensuring defective takes never enter final 4K renders.

---

## 9. Final Proponent Motion & Spec Freeze Recommendation

The Proponent team confirms that:
1. All adversarial attack vectors raised by Challenger R12 have been rigorously addressed and resolved through concrete, production-ready architectural remediations.
2. The **Three-Tier Progressive QC Architecture**, **Transport Error Disambiguation Matrix**, **Compact Forensic Quarantine**, **7-Day S3 Storage TTL**, and **PostgreSQL Range Partitioning** elevate Decision Cluster 11 into a hardened, high-throughput, cost-efficient subsystem.
3. **CP-013** and **CP-014** are **retained and augmented** to form the definitive specification foundation for `avf-qc` (R11) and `avf-media` (R12).

**FORMAL MOTION:** **FULL CONFIRMATION & SPECIFICATION FREEZE (PASS)** for Decision Cluster 11 under the remediated v1.0 architecture.

---
*Signed by R08 QA Specialist (QA, Verification & Reliability Architect — Proponent Lead)*  
*AI Video Factory Architecture Council — C02R Genuine Adversarial Cross-Examination*  
*Timestamp: 2026-08-16T09:20:00+07:00*
