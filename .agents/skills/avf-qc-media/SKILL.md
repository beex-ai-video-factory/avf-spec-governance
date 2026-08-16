---
name: avf-qc-media
description: Implement multi-stage quality control (fast technical FFprobe inspection before semantic LLM/Vision assessment), bounded retry loops, quarantine DLQ, and media processing.
---

# Skill: AVF Quality Control & Media Processing

## Purpose
Specifies the inspection pipeline and processing rules for R11 QC and R12 Media.

## Pipeline Architecture
1. **Stage 1: Fast Technical QC (FFprobe / Container Inspection)**
   - Validate container integrity (MP4/MOV).
   - Check stream headers (video codec: H.264/HEVC, resolution matches request, frame rate $> 24\text{ fps}$, duration within tolerance $\pm 0.5\text{s}$).
   - Detect blank/black frames or audio silence.
   - Cost: $\sim 10\text{ms}$ CPU time.
2. **Stage 2: Semantic QC (LLM / Vision Model)**
   - Only executed if Stage 1 Technical QC passes.
   - Assess prompt adherence, visual artifacts, character continuity, and safety.
3. **Failure Quarantine & Dead Letter Queue (DLQ):**
   - Retries are bounded to a maximum of 3 attempts per scene.
   - Failed renders that exhaust retries are routed to the DLQ with full diagnostic bundle and quarantined for operator review.
