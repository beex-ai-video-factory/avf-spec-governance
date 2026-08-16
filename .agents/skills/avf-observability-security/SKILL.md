---
name: avf-observability-security
description: Implement end-to-end distributed tracing, correlation IDs, automated secret redaction, audit logging, and provider cost/retry telemetry in R14.
---

# Skill: AVF Observability & Security Engineering

## Purpose
Governs distributed tracing, security logging, and metrics aggregation across all repositories (R14 Platform Observability).

## Mandatory Practices
1. **Trace Context Propagation:**
   - Every incoming user request, webhook, or trigger must generate or propagate a `trace_id` and `correlation_id` formatted in accordance with W3C TraceContext standards.
   - All logs, Temporal workflow activities, and downstream provider requests must include these IDs.
2. **Automated Secret Redaction:**
   - Any log output, exception message, or telemetry event must pass through automated secret redaction masks for:
     - API keys (e.g., `AIza*`, bearer tokens)
     - Session cookies (`SAPISID`, `SSID`, `__Secure-*`)
     - User credentials / passwords
     - Private cloud URLs with SAS tokens.
3. **Cost & Retry Telemetry:**
   - Track per-project, per-scene provider generation costs, token usage, retry counts, and latency percentiles (p50, p95, p99).
