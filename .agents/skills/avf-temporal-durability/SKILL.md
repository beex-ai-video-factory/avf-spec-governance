---
name: avf-temporal-durability
description: Design and verify Temporal workflows and activities for deterministic execution, replay safety, exponential retry policies, idempotency keys, and state reconciliation before resubmissions.
---

# Skill: AVF Temporal Durability & Workflow Determinism

## Purpose
Ensures that all orchestration in R06 Workflow and asynchronous activities adhere to strict Temporal durability and determinism standards (ADR-008).

## Key Principles
1. **Workflow Determinism:**
   - Never use non-deterministic functions (e.g., `Math.random()`, `Date.now()`, direct UUID generation, or network I/O) directly inside workflow definitions.
   - Use Temporal workflow APIs (e.g., `workflow.currentTime()`, `workflow.uuid4()`) or execute I/O inside Activities.
2. **Activity Idempotency:**
   - Every activity must accept an `idempotency_key` (typically `scene_id` + `attempt_count` or `generation_request_id`).
   - Prior to re-submitting a generation request to a provider, activities must check if an active or completed generation already exists for that idempotency key.
3. **Replay Safety & Versioning:**
   - Any workflow logic modification must use Temporal workflow versioning (`workflow.patched()`) to avoid breaking running instances during replay.
4. **Exponential Backoff & Retries:**
   - Configure bounded retry intervals with jitter to prevent thundering herds on downstream providers.
