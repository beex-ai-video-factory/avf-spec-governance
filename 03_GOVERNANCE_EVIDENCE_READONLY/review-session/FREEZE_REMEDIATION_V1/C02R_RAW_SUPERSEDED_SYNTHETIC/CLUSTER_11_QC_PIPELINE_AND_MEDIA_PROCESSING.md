# C02R HEARING TRANSCRIPT: CLUSTER 11 — QC PIPELINE, MEDIA PROCESSING & DLQ REPLAY
**CLUSTER_ID:** CLUSTER-11
**FINDINGS_COVERED:** FINDING_013, FINDING_031, FINDING_082
**DATE:** 2026-08-15
**STATUS:** CLOSED_CONFIRMED

## 1. Proponent Brief
- **Proponent:** R08 (QA Specialist) & R02 (Reliability Specialist)
- **Position:** Generated video takes must pass automated Quality Control (R11 QC) before human review or assembly. The QC pipeline validates:
  - Technical parameters: resolution, aspect ratio, frame rate, duration, audio-video sync, container validity (via FFprobe).
  - Visual quality heuristics: black frames, frozen frames, severe artifacting, motion blur.
  - Continuity scoring: CLIP/DINO similarity against character and style references.
  Failed QC takes or unprocessable media files are routed to a Dead Letter Queue (DLQ) with automated alert emission and replay capabilities.
- **Evidence:** `R11_QC.md`, `R12_MEDIA.md`, `STATUS_STATE_MACHINES.md`.
- **Failure Scenario:** A video engine outputs an MP4 file with corrupted moov atom. Without pre-QC inspection, the media pipeline attempts stitching, crashing the video renderer.

## 2. Challenger Attack
- **Challenger:** R14 (Perf/Cost Specialist)
- **Attack Vector:**
  1. *GPU Resource Consumption:* Running heavy neural continuity checks on every single take could double infrastructure compute costs.
  2. *DLQ Poison Messages:* If a video file triggers an FFmpeg segfault, automatic DLQ replay could enter an infinite crash loop.

## 3. Domain Owner Review
- **Domain Owner:** R08 (QA Specialist)
- **Evaluation:**
  - Fast technical checks (FFprobe) run first on CPU (< 100ms). Heavy neural checks run only on candidates passing technical validation.
  - DLQ replay uses exponential backoff and a hard max attempt limit (3 attempts), after which the message moves to a parked quarantine state requiring operator signoff.

## 4. Proponent Response
- **Response:**
  - We formalize the two-stage QC pipeline and DLQ quarantine semantics in `R11_QC.md` and `R12_MEDIA.md`.

## 5. Alternative Hypothesis
- **Alternative (Option B):** Rely solely on manual human review in Operator Console.
- **Why Rejected:** Human review of hundreds of bad takes wastes operator time and breaks automated overnight batch generation.

## 6. Evidence-Based Disposition
- **Disposition:** CONFIRMED
- **Resolution Plan:** CP-013 & CP-014 retained and integrated into `R11_QC.md` and `R12_MEDIA.md`.
