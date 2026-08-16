# Final Architecture Risk Register (v1.0.0 Frozen)

| RISK_ID | RISK_CATEGORY | DESCRIPTION | SEVERITY | MITIGATION & CONTINGENCY STRATEGY | OWNER |
|---|---|---|---|---|---|
| RSK-001 | Third-Party Mock Drift | Containerized mock provider simulators in R15 may diverge from live vendor API updates. | MEDIUM | Scheduled bi-weekly automated live integration canary runs with bounded test credits. | R08 / R15 |
| RSK-002 | MV3 Keepalive Policy Evolution | Future Chrome browser updates could throttle offscreen document keepalive audio channels. | LOW | Native Messaging Host daemon provides secondary direct CDP pipe; Playwright fallback ready. | R06 / R09 |
| RSK-003 | V8 Heap Secret Remanence | Immutable JS strings in V8 engine could persist in heap before garbage collection. | LOW | Strict Buffer / Uint8Array binary allocation with explicit sodium.memzero memory wiping. | R07 / R15 |
| RSK-004 | Worker Lease Contention | Long GC pauses or synchronous I/O could cause worker lease expiration during provider call. | LOW | Fencing tokens + provider-side idempotency keys prevent duplicate billing on retry. | R02 / R06 |
