# SECURITY MODEL & CREDENTIAL HYGIENE
## AI Video Factory — Trust Boundaries & Data Protection
**VERSION:** 1.0.0

---

## 1. Trust Boundaries
1. **Core State Database:** Isolated inside private VPC; accessible strictly by R02 service instances via TLS and IAM authentication.
2. **Worker Nodes & Browser Execution:**
   - Chrome user data directory protected with OS permissions (`chmod 700`).
   - Native Messaging host communicates over OS standard I/O pipes (restricted to local process user).
3. **Provider Secrets & Session Cookies:**
   - Secrets injected at startup via OS environment variables or secure Secret Manager (AWS/GCP/Vault).
   - In-memory credentials managed in Node.js `Buffer` / `Uint8Array` structures and wiped with `buf.fill(0)` after request execution.
   - Zero hardcoded secrets in repositories or Docker images.
4. **Telemetry Redaction:**
   - R14 Observability SDK automatically masks `Authorization`, `Cookie`, `set-cookie`, and bearer tokens from logs, traces, and metrics.
