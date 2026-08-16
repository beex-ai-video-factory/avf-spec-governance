# Risk Register

| ID | Risk | Probability | Impact | Detection | Mitigation | Fallback |
|---|---|---:|---:|---|---|---|
| R1 | Google Flow UI changes | High | High | live regression/smoke | isolate adapter; selector layers | Track B or API provider |
| R2 | FlowKit internal integration breaks | High | High | bridge contract suite | treat as external engine; no core coupling | Track A |
| R3 | Authentication expires | Medium | High | health probe | explicit `AUTH_REQUIRED`; operator workflow | alternate session/provider |
| R4 | Security/anti-abuse challenge | Medium/High | High | normalized blocked state | do not bypass; operator escalation | supported API provider |
| R5 | Provider rate limiting | High | Medium/High | usage metrics | pacing/backoff/budget | provider switch |
| R6 | Duplicate paid generation | Medium | Critical | audit/idempotency tests | persisted idempotency + reconciliation | manual reconcile/compensate |
| R7 | Browser crash | Medium | Medium | heartbeat/lease | isolated worker + durable state | new worker/session |
| R8 | MV3 service worker termination | High | Medium | reconnect telemetry | persist disposable extension state | Native Messaging/worker recovery |
| R9 | LLM invalid structured output | Medium | Medium | schema validation | repair + bounded retry | human/ deterministic fallback |
| R10 | Character drift | High | Medium | semantic QC | references + continuity constraints | regenerate/human review |
| R11 | QC false accept/reject | Medium | Medium | benchmark set | version evaluator + thresholds | human review |
| R12 | Cost/credits exhausted | Medium | High | budget counters | pre-submit budget gate | defer/switch provider |
| R13 | Asset rights/provenance missing | Medium | Critical | ingest validation | rights metadata required | block asset |
| R14 | Vendor lock-in | High | High | architecture review | provider contract | new adapter |
| R15 | Cross-repo contract drift | Medium | High | CI compatibility matrix | version pin + contract tests | block release |
| R16 | Agent introduces architectural divergence | Medium | High | code review/spec tests | bounded build packets; ADR gate | reject implementation |
