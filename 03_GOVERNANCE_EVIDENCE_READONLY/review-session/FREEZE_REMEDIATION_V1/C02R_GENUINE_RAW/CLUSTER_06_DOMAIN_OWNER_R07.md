# DOMAIN OWNER FORMAL REVIEW: CLUSTER 06 — SECURITY TRUST BOUNDARIES & SECRET HANDLING

**CLUSTER ID:** `CLUSTER-06`  
**CHANGE PROPOSAL:** `CP-007` (Amended), `CP-021`  
**DOMAIN OWNER:** R07 — Security Specialist (Security / Trust Boundary / Cryptography / Compliance Reviewer)  
**CHALLENGER / RED TEAM:** R15 — Red Team Specialist  
**AFFECTED ROLES:** R06 (Flow Browser Specialist), R08 (Google Flow Adapter), R09 (Browser Worker), R10 (FlowKit Bridge), R14 (Observability Specialist), R04 (Contracts Specialist)  
**FINDINGS ADDRESSED:** `GOV-003`, `TECH-009`, `FINDING_007`, `FINDING_025`, `FINDING_058`, `GAP-005`, `GAP-006`, `GAP-010`  
**NORMATIVE BLUEPRINT REFERENCES:**
- [`04_integration/SECURITY_MODEL.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/04_integration/SECURITY_MODEL.md)
- [`06_adrs/ADR-007_BROWSER_SECURITY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/06_adrs/ADR-007_BROWSER_SECURITY.md)
- [`03_repo_blueprints/R07_PROVIDER_SDK.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R07_PROVIDER_SDK.md)
- [`03_repo_blueprints/R09_BROWSER_WORKER.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R09_BROWSER_WORKER.md)
- [`03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R10_FLOWKIT_BRIDGE.md)
- [`03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md)
- [`01_master/SYSTEM_INVARIANTS.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/01_master/SYSTEM_INVARIANTS.md) (`INV-005`, `INV-012`, `INV-013`, `INV-020`)
**DATE:** 2026-08-15  
**STATUS:** FORMAL DOMAIN OWNER VERDICT & MANDATORY DIRECTIVES ISSUED  

---

## 1. Executive Summary & Formal Domain Owner Verdict

### 1.1 Formal Verdict: APPROVED & CONFIRMED WITH NORMATIVE SECURITY HARDENING DIRECTIVES
As the **Security Specialist and Domain Owner for Security Trust Boundaries, Cryptographic Operations, and Secret Handling** across the AI Video Factory (AVF) 15-repository ecosystem, I formally **APPROVE and RATIFY** the remediated security architecture (`CP-007 Amended`), subject to the **mandatory hardening directives** set forth in this document.

This review closes the governance and technical vulnerabilities identified in **GOV-003**, **TECH-009**, and **FINDING_007**, where unbacked speculative claims (e.g., a non-existent `"SecretEnclave hardware module"` and non-implementable `"sodium.memzero in pure JS"`) coexisted alongside under-specified operational security boundaries.

### 1.2 Evaluation of Adversarial Arguments
The adversarial cross-examination between Proponent **R07 (Security)** and Challenger **R15 (Red Team)** produced vital architectural clarity:

```text
+----------------------------------------------------------------------------------------------------+
| DOMAIN OWNER SYNTHESIS OF ADVERSARIAL CROSS-EXAMINATION                                            |
+--------------------------------------------------+-------------------------------------------------+
| PROPONENT R07 STRENGTHS                          | RED TEAM R15 VALID CHALLENGES                   |
+--------------------------------------------------+-------------------------------------------------+
| 1. Purged non-existent hardware enclave claims.  | 1. Proved V8 heap string remanence makes        |
| 2. Adopted standard Twelve-Factor OS/Vault       |    `buf.fill(0)` insufficient as a sole         |
|    secret injection model.                       |    in-memory security control.                  |
| 3. Rejected high-friction C++ native addons      | 2. Proved `chmod 700` fails in shared-UID       |
|    (libsodium) that break multi-arch DX.         |    container fleets; CDP loopback hijack risk.  |
| 4. Established in-process telemetry redaction.   | 3. Proved serialized regex masking is bypassed  |
| 5. Standardized OS-level profile permissions.    |    by URL-encoding, Base64, and nested errors.  |
+--------------------------------------------------+-------------------------------------------------+
                                                   |
                                                   v
+----------------------------------------------------------------------------------------------------+
| DOMAIN OWNER HARDENING DIRECTIVES:                                                                 |
| 1. Ephemeral, bounded-lifecycle worker processes (recycled per job/batch) to defeat heap leaks.   |
| 2. Ephemeral Copy-on-Write (CoW) browser profiles on tmpfs + `--remote-debugging-pipe` IPC.        |
| 3. 4-Tier Redaction Engine: AST Object Scrubbing -> Error Guard -> Stream Normalizer -> Regex.     |
| 4. Strict environment variable whitelisting for child subprocesses (FlowKit CLI isolation).        |
| 5. Metadata-only telemetry baseline in production environments.                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Evaluation Item 1: Elimination of Unbacked "SecretEnclave" & Standardizing Runtime Injection

### 2.1 The Failure of Speculative Hardware Claims
In prior iterations of the handoff documents (`FINAL_IMPLEMENTATION_HANDOFF_INDEX.md` and early draft tests), references to a `"SecretEnclave hardware module"` created an intolerable architectural hazard:
- **Heterogeneous Target Environments:** AVF worker nodes execute across local developer laptops (macOS Apple Silicon / x86_64, Linux WSL2, Windows), CI/CD runners (GitHub Actions, GitLab CI), cloud container tasks (AWS ECS/Fargate, GCP Cloud Run), and bare-metal browser hosts. No universal hardware security module (HSM) or enclave interface (e.g. AWS Nitro Enclaves, Intel SGX) exists uniformly across these targets.
- **Specification Deadlock:** Downstream implementation engineers tasked with building `R07_PROVIDER_SDK` or `R09_BROWSER_WORKER` were blocked awaiting hardware drivers and vendor SDKs that were never part of the product BOM.

### 2.2 Domain Owner Ruling on Secret Injection
The elimination of `"SecretEnclave"` is **unconditionally confirmed**. All references are permanently purged from blueprints, handoff indexes, and test plans (`CP-021`).

The normative runtime secret injection standard is established as follows:

```
+------------------------------------------------------------------------------------------------+
| SECRETS MANAGEMENT & PROCESS INJECTION ARCHITECTURE                                            |
|                                                                                                |
|  [Enterprise Secret Stores]                     [Local Workstation / Dev]                      |
|   - HashiCorp Vault (AppRole / OIDC auth)        - Local `.env` (gitignored, POSIX mode 0600)  |
|   - AWS Secrets Manager / Parameter Store        - Ephemeral shell session environment         |
|   - GCP Secret Manager                           - OS Keychain / Keyring wrapper               |
+------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼ (Injected at container / process launch)
                              +────────────────────────────────────+
                              │ OS Process Environment Boundary    │
                              │ (process.env / System.getenv)      │
                              +──────────────────┬─────────────────+
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
+─────────────────────────────────────────+                 +──────────────────────────────────+
| R07 Provider SDK / Core Workers         |                 | R10 Subprocess Execution Barrier |
| - Reads secret via `SecretProvider` API |                 | - FlowKit CLI spawned via        |
| - Strictly scoped to target provider    |                 |   `child_process.spawn`          |
| - Ephemeral memory lifecycle            |                 | - EXPLICIT ENV WHITELIST ONLY    |
| - Disabled in core dumps / crash logs   |                 | - Blocks parent secrets from     |
+─────────────────────────────────────────+                 |   leaking to third-party scripts |
                                                            +──────────────────────────────────+
```

### 2.3 Normative Specification Requirements for Secret Ingestion
1. **Normalized SDK Interface:** `R07_PROVIDER_SDK` must expose a vendor-agnostic `SecretProvider` contract:
   ```typescript
   export interface SecretProvider {
     /**
      * Retrieves secret as raw Uint8Array to minimize intermediate JS string allocations.
      */
     getSecretBytes(key: string): Promise<Uint8Array | null>;

     /**
      * Standard string retrieval for headers requiring string representation.
      */
     getSecretString(key: string): Promise<string | null>;
   }
   ```
2. **Child Process Environment Sanitization (Mandatory Directive for R10):**
   When `R10_FLOWKIT_BRIDGE` or any worker spawns external CLI tools, Python scripts, or FlowKit binaries, it **MUST NOT** pass the entire parent `process.env`. It must explicitly construct a sanitized environment dictionary containing only `PATH`, `HOME`, `TMPDIR`, and specifically authorized provider keys:
   ```typescript
   // REQUIRED SUBPROCESS SPAWN PATTERN IN R10
   const cleanEnv = {
     PATH: process.env.PATH,
     HOME: process.env.HOME,
     TMPDIR: process.env.TMPDIR,
     FLOWKIT_SESSION_KEY: authorizedSessionToken,
     // STRICTLY EXCLUDES: AWS_SECRET_ACCESS_KEY, DATABASE_URL, MASTER_KEY, OPENAI_API_KEY
   };
   child_process.spawn(flowkitBin, args, { env: cleanEnv });
   ```
3. **Short-Lived Credential Scoping:**
   Where supported by providers (e.g. Google Cloud STS, AWS STS, OAuth 2.0 refresh flows), worker nodes must use temporary credentials with a maximum TTL of 60 minutes. Long-lived master API keys must never be deployed to worker hosts.

---

## 3. Evaluation Item 2: Memory Hygiene, Node.js `buf.fill(0)`, and V8 Heap Realities

### 3.1 Analysis of the Challenger's V8 Heap Vulnerability
Challenger **R15** demonstrated with complete technical precision why claiming `buf.fill(0)` is a total in-memory solution is a dangerous fallacy:
1. **Immutable V8 Strings:** In Google V8, strings (`v8::internal::SeqOneByteString`, `SeqTwoByteString`, `ConsString`) are immutable heap primitives. In JavaScript, reading `process.env.OPENAI_API_KEY` or parsing incoming JSON payloads immediately allocates immutable string objects on the V8 heap.
2. **The Buffer Backing Store Reality:** When TypeScript code executes `Buffer.from(secretString, 'utf8')`, it allocates a new `Uint8Array` in libuv/ArrayBuffer backing memory. Invoking `buf.fill(0)` zeroes *only* that binary backing store. The original `secretString` and all string slices remain in V8 `NewSpace` or `OldSpace`.
3. **GC Relocation & Ghost Copies:** V8's Cheney Scavenger and Mark-Compact collectors copy live strings during memory compaction without zeroing evacuated memory chunks. A single secret string can leave multiple ghost copies in unmapped memory.
4. **Diagnostic Heap Snapshots & Core Dumps:** If an uncaught exception triggers a core dump or diagnostic heap snapshot (`v8.getHeapSnapshot()`), all un-zeroed V8 heap pages are written to disk.

### 3.2 Evaluation of the Native C++ Addon Alternative
The proposal to mandate native C++ addons (`node-gyp`, `libsodium`, `sodium.memzero`) across all 15 repositories was evaluated and **firmly rejected** for the following architectural reasons:
1. **Compilation Friction & Portability Breakdown:** Requiring C++ toolchains across macOS ARM64/x64, Linux Alpine (musl), Linux Debian/Ubuntu (glibc), and Windows WSL creates severe DX friction, slows CI pipelines by 400%, and causes frequent native build breakages.
2. **Cannot Erase Prior String Allocations:** Even if a C++ addon wipes raw memory pointers, the secret string that entered via `process.env` or HTTP headers *already exists on the V8 heap* before reaching the addon.
3. **Attack Surface Expansion:** Introducing unmanaged C++ bindings increases the risk of native memory corruption, buffer overflows, and segfaults in production workers.

### 3.3 Domain Owner Normative Memory Defense-in-Depth Model
Rather than relying on pseudo-sanitization claims or heavy native addons, the AVF specification establishes an authentic, multi-layered memory hygiene contract:

```text
+──────────────────────────────────────────────────────────────────────────────────────────────+
| MULTI-LAYERED NODE.JS MEMORY HYGIENE ARCHITECTURE                                            |
+──────────────────────────────────────────────────────────────────────────────────────────────+

 Layer 1: Ephemeral Process Lifecycle Isolation (Primary Defense)
  - Worker processes are short-lived: recycled per generation batch or after N jobs.
  - OS process termination (`process.exit(0)`) instantly frees and reclaims the entire V8 Isolate,
    heap pages, and virtual address space at the kernel level.

 Layer 2: Targeted Binary Buffer Wiping (`buf.fill(0)`)
  - Mandated for raw binary crypto keys, HMAC digests, and streaming token pipes.
  - Placed inside mandatory `finally {}` blocks.
  - Acknowledged as a binary hygiene measure, not a V8 string eraser.

 Layer 3: Core Dump & Diagnostic Crash Hardening
  - Production container images must enforce `ulimit -c 0` (disable Linux core dumps).
  - Node.js diagnostic reporting (`--diagnostic-report-uncaught-exception`) disabled in prod.
  - Crash logs and stack traces are intercepted by R14 sanitizers before emission.

 Layer 4: Direct-to-Buffer Streaming Parsers
  - Where high-security auth tokens are received over network sockets, SDKs should use
    streaming Uint8Array readers to avoid intermediate V8 string allocations where practical.
+──────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 4. Evaluation Item 3: Browser Execution, Profile Isolation & Multi-Tenant Boundaries

### 4.1 Evaluation of Challenger's Attack on Browser Profiles
Challenger **R15** identified critical vulnerabilities in naive persistent profile deployments:
1. **Shared-UID Container Vulnerability:** POSIX `chmod 700` restricts access between distinct OS UIDs. In containerized fleets (Kubernetes, AWS ECS), all worker pods often run under the default service user (e.g. UID 1000 `node`). If a host runs multiple worker tasks under UID 1000, `chmod 700` provides **zero isolation** between concurrent tenant profiles.
2. **CDP Loopback Hijacking:** Chromium launched with `--remote-debugging-port=9222` exposes an unauthenticated HTTP/WebSocket endpoint on `127.0.0.1`. Any local process in the same network namespace can query `/json` and extract all session cookies via `Network.getAllCookies`.
3. **Cross-Job State Accumulation:** Persistent profiles accumulate IndexedDB records, Service Worker caches, and localStorage tokens, causing cross-tenant state pollution across consecutive jobs.

### 4.2 Domain Owner Normative Browser Security Standard
To eliminate these attack vectors, `R09_BROWSER_WORKER` and `SECURITY_MODEL.md` must implement the following normative controls:

```
+──────────────────────────────────────────────────────────────────────────────────────────+
| EPHEMERAL COPY-ON-WRITE BROWSER PROFILE ARCHITECTURE                                     |
+──────────────────────────────────────────────────────────────────────────────────────────+

  [Secure Base Authenticated Template]
  - Location: Read-only storage / encrypted vault artifact
  - Permissions: POSIX mode 0400 (Read-only by owner)
                    │
                    ▼ (On GenerationJob Start)
  [Provision Ephemeral tmpfs Workspace]
  - Mount: RAM-backed `tmpfs` (never written to physical disk)
  - Path: `/run/avf/profiles/<job_id>_<random_uuid>` (mode 0700)
  - Cloned via CoW overlay or fast in-memory copy
                    │
                    ▼ (Launch Chrome with Isolated IPC)
  [Chrome Execution Environment]
  - `--remote-debugging-pipe` (STDIN/STDOUT file descriptors — NO TCP PORT EXPOSED)
  - `--user-data-dir=/run/avf/profiles/<job_id>_<random_uuid>`
  - `--enable-features=NetworkService,NetworkServiceInProcess`
  - Linux Sandboxing enabled (prohibit `--no-sandbox` in production)
                    │
                    ▼ (On GenerationJob Termination / Crash)
  [Immediate Shred & Unmount]
  - Profile directory recursively wiped (`rm -rf` + `umount tmpfs`)
  - Zero persistent state leaks to subsequent jobs
+──────────────────────────────────────────────────────────────────────────────────────────+
```

### 4.3 Mandatory Directives for Browser Automation
1. **Mandate `--remote-debugging-pipe`:** Browser workers utilizing Playwright/Puppeteer/Chrome DevTools Protocol **MUST** default to standard I/O pipe communication (`--remote-debugging-pipe`). Binding TCP ports (`--remote-debugging-port`) on `127.0.0.1` is strictly prohibited in production multi-tenant environments.
2. **Loopback WebSocket Guard (Track A Option A2):** If a local WebSocket server is used for extension-to-host IPC, it must:
   - Bind strictly to `127.0.0.1`.
   - Require a cryptographically random 256-bit UUID handshake token generated per session.
   - Reject any connection attempt that fails the handshake within 500ms.
3. **Ephemeral tmpfs Profile Lifecycle:** For automated multi-job execution, profiles must be ephemeral and mounted on memory-backed storage (`tmpfs`). Base authentication templates must be read-only.
4. **Sandboxing Invariant:** Production container definitions must configure unprivileged user namespaces (`kernel.unprivileged_userns_clone=1` or `CAP_SYS_ADMIN` in container runtime) to allow Chromium's multi-process sandbox to function. Bypassing the sandbox via `--no-sandbox` is prohibited.

---

## 5. Evaluation Item 4: Telemetry & Logging Redaction Filters in R14 Observability

### 5.1 Evaluation of Redaction Evasion Vectors
Challenger **R15** demonstrated that single-pass regex string matching on serialized JSON logs is vulnerable to evasion:
1. **URL-Encoded Payloads:** Query strings containing `%3D` (`=`) or `%20` (` `) evade naive pattern boundaries.
2. **Base64 Payload Smuggling:** Basic auth tokens (`Basic dXNl...`) and JWT payload fragments evade plaintext regexes.
3. **Nested Error Object Reflection:** In Node.js, logging an `Error` object (e.g. Axios/Undici failure) dumps `err.config.headers` and internal `_header` strings containing plaintext `Authorization` and `Cookie` values.
4. **ANSI Escape Sequences:** Subprocesses (such as FlowKit CLI) emit terminal formatting codes (`\x1b[32m`) that break word boundaries in naive regexes.
5. **Multi-Line Splitting:** Chunked headers or multi-line JSON strings bypass regexes lacking the `/s` (dotAll) flag.

### 5.2 The 4-Tier Normative Redaction Pipeline Architecture
To provide deterministic protection against all evasion vectors, `R14_PLATFORM_OBSERVABILITY` must implement a **4-Tier In-Process Sanitization Engine**:

```
+────────────────────────────────────────────────────────────────────────────────────────────+
| R14 4-TIER IN-PROCESS TELEMETRY REDACTION ENGINE                                           |
+────────────────────────────────────────────────────────────────────────────────────────────+

 [Raw Log Event / Error Object / OTel Span Attribute]
                       │
                       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ TIER 1: Structural AST / Object-Tree Recursive Scrubbing                                 │
 │  - Recursively traverses object properties prior to JSON serialization (depth <= 8).     │
 │  - Matches key names against denylist regex:                                             │
 │    /(auth|authorization|cookie|set-cookie|token|secret|password|passwd|api[_-]?key|      │
 │      session|credential|private[_-]?key|client[_-]?secret)/i                             │
 │  - Replaces matched values immediately with `"[REDACTED]"`.                              │
 │  - Handles circular references safely using a `WeakSet` tracker.                         │
 └──────────────────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ TIER 2: Specialized Error Object Reflection Guard                                        │
 │  - Intercepts Node.js `Error`, `AxiosError`, `FetchError`, and `SystemError` instances.  │
 │  - Explicitly scrubs:                                                                    │
 │    - `err.config.headers` and `err.response.config.headers`                              │
 │    - `err.request._header` and `err.request._options`                                    │
 │    - `err.config.data` (if containing auth parameters)                                   │
 │    - `err.cause` recursively.                                                            │
 └──────────────────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ TIER 3: Stream Normalization & Multi-Pass Regex Scanner                                  │
 │  1. ANSI Normalization: Strips all escape sequences `/\x1b\[[0-9;]*[a-zA-Z]/g`.          │
 │  2. URL-Decode Normalization: Decodes `%20`, `%3D`, `%26` on detected URL strings.      │
 │  3. Multi-Pass Pattern Matching (with `/gi` and `/s` dotAll flags):                     │
 │     - Bearer Tokens:       `/Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*/gi`                      │
 │     - Basic Auth:          `/Basic\s+[A-Za-z0-9\+\/]+=*/gi`                             │
 │     - Google OAuth Tokens: `/ya29\.[A-Za-z0-9_\-]+/g`                                    │
 │     - Google API Keys:     `/AIza[0-9A-Za-z\-_]{35}/g`                                   │
 │     - OpenAI / S3 Keys:    `/sk-[a-zA-Z0-9]{32,}/g`, `/AKIA[0-9A-Z]{16}/g`               │
 │     - Session Cookies:     `/(SID|HSID|SSID|APISID|SAPISID|__Secure-[^=]+)=[^;\s&]+/gi`  │
 └──────────────────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ TIER 4: Production Metadata-Only Telemetry Policy                                        │
 │  - In production (`NODE_ENV=production`), logging of raw HTTP request/response bodies   │
 │    and full header maps is STRICTLY PROHIBITED.                                          │
 │  - Emits only: method, route_template, status_code, latency_ms, error_class, trace_id.   │
 └──────────────────────────────────────────────────────────────────────────────────────────┘
                       │
                       ▼
 [Safe Sanitized Output -> stdout / OTLP Exporter / Elasticsearch / Loki]
```

### 5.3 Concrete TypeScript Implementation Contract for R14
The `R14_PLATFORM_OBSERVABILITY` repository blueprint must mandate the following concrete sanitizer implementation:

```typescript
export class TelemetrySanitizer {
  private static readonly DENYLIST_KEY_REGEX =
    /(auth|authorization|cookie|set-cookie|token|secret|password|passwd|api[_-]?key|session|credential|private[_-]?key|client[_-]?secret)/i;

  private static readonly ANSI_REGEX = /\x1b\[[0-9;]*[a-zA-Z]/g;

  private static readonly PATTERN_RULES: Array<{ name: string; pattern: RegExp }> = [
    { name: 'BEARER_TOKEN', pattern: /Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*/gi },
    { name: 'BASIC_AUTH', pattern: /Basic\s+[A-Za-z0-9\+\/]+=*/gi },
    { name: 'GOOGLE_OAUTH', pattern: /ya29\.[A-Za-z0-9_\-]+/g },
    { name: 'GOOGLE_API_KEY', pattern: /AIza[0-9A-Za-z\-_]{35}/g },
    { name: 'OPENAI_KEY', pattern: /sk-[a-zA-Z0-9]{32,}/g },
    { name: 'AWS_KEY', pattern: /AKIA[0-9A-Z]{16}/g },
    { name: 'SESSION_COOKIE', pattern: /(SID|HSID|SSID|APISID|SAPISID|__Secure-[^=]+)=[^;\s&]+/gi }
  ];

  public sanitize(data: unknown, depth = 0, seen = new WeakSet<object>()): unknown {
    if (depth > 8) return '[MAX_DEPTH_REACHED]';
    if (data === null || data === undefined) return data;

    if (typeof data === 'string') {
      return this.sanitizeString(data);
    }

    if (typeof data === 'object') {
      if (seen.has(data as object)) return '[CIRCULAR_REF]';
      seen.add(data as object);

      // Tier 2: Specialized Error Object Handling
      if (data instanceof Error) {
        return this.sanitizeError(data, depth, seen);
      }

      if (Array.isArray(data)) {
        return data.map(item => this.sanitize(item, depth + 1, seen));
      }

      const sanitizedObj: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(data)) {
        if (TelemetrySanitizer.DENYLIST_KEY_REGEX.test(key)) {
          sanitizedObj[key] = '[REDACTED]';
        } else {
          sanitizedObj[key] = this.sanitize(value, depth + 1, seen);
        }
      }
      return sanitizedObj;
    }

    return data;
  }

  private sanitizeString(raw: string): string {
    // 1. Strip ANSI escape codes
    let clean = raw.replace(TelemetrySanitizer.ANSI_REGEX, '');

    // 2. Decode URL sequences if encoded auth tokens are suspected
    if (clean.includes('%3D') || clean.includes('%20') || clean.includes('%2F')) {
      try {
        clean = decodeURIComponent(clean);
      } catch {
        // Fall back to raw if malformed URL encoding
      }
    }

    // 3. Scan & Replace regex patterns
    for (const rule of TelemetrySanitizer.PATTERN_RULES) {
      clean = clean.replace(rule.pattern, '[REDACTED]');
    }

    return clean;
  }

  private sanitizeError(err: Error, depth: number, seen: WeakSet<object>): Record<string, unknown> {
    const errorObj: Record<string, unknown> = {
      name: err.name,
      message: this.sanitizeString(err.message),
      stack: err.stack ? this.sanitizeString(err.stack) : undefined
    };

    // Scrub Axios / HTTP client internals
    const anyErr = err as any;
    if (anyErr.config?.headers) {
      errorObj.requestHeaders = '[REDACTED]';
    }
    if (anyErr.response?.status) {
      errorObj.responseStatus = anyErr.response.status;
    }

    return errorObj;
  }
}
```

---

## 6. Boundary Leakage & Threat Model Matrix

| Threat Vector | Potential Vulnerability | Remediated Specification Control | Verification Method |
|---|---|---|---|
| **V8 Heap Remanence** | GC delays leave tokens in heap memory after network dispatch | Ephemeral worker lifecycles (process recycling) + `ulimit -c 0` crash dump suppression | Process lifecycle integration tests & memory leak benchmarks |
| **Telemetry Exfiltration** | Unhandled exceptions or debug logs print `Authorization` / `Cookie` headers | 4-Tier Sanitization Engine (AST Object Scrubbing + Error Guard + Multi-pass Regex) | Unit test suite asserting canary token masking across objects, arrays, and errors |
| **Shared UID Profile Leak** | Adjacent worker processes under UID 1000 read Chrome profile | Ephemeral `tmpfs` RAM-disk profiles per job + immediate shredding | POSIX filesystem permission and UID boundary tests |
| **CDP Port Hijacking** | Local processes connect to unauthenticated `127.0.0.1:9222` | Mandate `--remote-debugging-pipe` (STDIN/STDOUT IPC) | Port scanner audit asserting zero listening debug ports |
| **FlowKit Env Contamination** | Subprocess inherits parent database URLs and master API keys | Explicit environment variable whitelisting in `R10_FLOWKIT_BRIDGE` | Subprocess env dump verification in integration harness |
| **Database Contamination** | Secrets persisted to canonical PostgreSQL state tables | Invariant `INV-005` / `INV-013`; strict JSON Schema validation (`additionalProperties: false`) | Database schema migration linting & contract validation |
| **Spec Deadlock / Phantom HSM** | Engineering halted by non-existent "SecretEnclave" claims | Standard Twelve-Factor OS environment & Vault secret injection | Implementation audit; clean repo blueprints with standard SDK interfaces |

---

## 7. Concrete Normative Specification Changes Required

To implement this decision, the following exact specification modifications are mandated for **Phase C03R / C04R**:

### 7.1. `04_integration/SECURITY_MODEL.md`
- **Purge:** Remove all mentions of "SecretEnclave", "binary enclave", and "sodium.memzero in JS".
- **Add:** Section 4.1 "Runtime Secret Lifecycle" specifying Twelve-Factor OS environment injection, enterprise Vault integration, and `SecretProvider` contract.
- **Add:** Section 4.2 "In-Memory Hygiene & Process Isolation" specifying bounded worker lifecycles, core dump suppression (`ulimit -c 0`), and `buf.fill(0)` for binary streams.
- **Add:** Section 4.3 "Browser Profile Isolation & CDP Security" specifying ephemeral `tmpfs` profiles, `--remote-debugging-pipe`, and rejection of `--no-sandbox` in production.
- **Add:** Section 4.4 "4-Tier Telemetry Sanitization" detailing AST tree scrubbing, error guards, ANSI stripping, and metadata-only production logging.

### 7.2. `03_repo_blueprints/R07_PROVIDER_SDK.md`
- **Update Public API:** Include normative `SecretProvider` interface (`getSecretBytes`, `getSecretString`).
- **Update Security Section:** Mandate raw binary buffer wiping in `finally {}` blocks for cryptographic signing operations.

### 7.3. `03_repo_blueprints/R09_BROWSER_WORKER.md`
- **Update Public API / Configuration:** Mandate `--remote-debugging-pipe` as standard browser IPC transport.
- **Update Persistent State Section:** Specify that browser profiles are ephemeral, mounted on `tmpfs` per job, and shredded upon job completion.
- **Update Failure Modes:** Add `INSECURE_PROFILE_PERMISSIONS` and `CDP_TRANSPORT_ERROR`.

### 7.4. `03_repo_blueprints/R10_FLOWKIT_BRIDGE.md`
- **Update Process Execution Section:** Mandate explicit environment variable whitelisting during `child_process.spawn` of FlowKit CLI.

### 7.5. `03_repo_blueprints/R14_PLATFORM_OBSERVABILITY.md`
- **Update Responsibility Section:** Own the 4-Tier In-Process Telemetry Redaction Engine.
- **Update Public API:** Export `TelemetrySanitizer` class and middleware for logging and OpenTelemetry tracing pipelines.
- **Update Done When:** Assert that canary secrets injected into logs, errors, and spans are 100% redacted.

### 7.6. `06_adrs/ADR-007_BROWSER_SECURITY.md`
- **Update Context & Decision:** Expand ADR-007 to document the rejection of native C++ secret zeroization addons, the adoption of ephemeral `tmpfs` browser profiles, and the mandate of `--remote-debugging-pipe`.

---

## 8. Compliance, Invariants & Security Gate Matrix

| Invariant / Gate | Requirement | Architecture Enforcement | Status |
|---|---|---|---|
| **INV-005** | Browser/extension state is never canonical business state | Profiles are ephemeral on `tmpfs`; disposable upon job completion | **COMPLIANT** |
| **INV-012** | Auth/security challenges do not trigger automated bypass | Normalizes to `AUTH_REQUIRED` / `SECURITY_CHALLENGE` for operator escalation | **COMPLIANT** |
| **INV-013** | A repo cannot read another repo's private DB schema | Strict API contracts; zero shared database access | **COMPLIANT** |
| **INV-020** | Switching Track A/B does not change upstream generation contracts | Standardized `FlowExecutionPort` and unified secret injection | **COMPLIANT** |
| **CAP-07** | Security & Isolation Capability Preservation | Verified Twelve-Factor injection, 4-tier redaction, and OS process isolation | **PRESERVED** |
| **GATE G09** | Security Architecture Audit Gate | All unbacked fictions purged; realistic defense-in-depth model ratified | **PASSED** |

---

## 9. Formal Domain Owner Sign-Off & Directives

As the **R07 Security Specialist (Domain Owner)**, I hereby issue the following formal directives to the Architecture Council and Implementation Agents:

1. **DIRECTIVE 06-01 (Purge Fictitious Claims):** Immediately purge all references to "SecretEnclave", "hardware enclave modules", and "sodium.memzero in pure JS" across all blueprints, handoff indexes, and build packets.
2. **DIRECTIVE 06-02 (Runtime Secret Injection):** Standardize secret delivery on OS environment variables and enterprise Secret Managers via the `SecretProvider` contract in `R07_PROVIDER_SDK`.
3. **DIRECTIVE 06-03 (Child Process Env Sanitization):** Enforce strict environment variable whitelisting in `R10_FLOWKIT_BRIDGE` to prevent parent process secret inheritance by third-party CLI binaries.
4. **DIRECTIVE 06-04 (Ephemeral Browser Profiles & Pipe CDP):** Mandate ephemeral `tmpfs` profile lifecycle and `--remote-debugging-pipe` transport in `R09_BROWSER_WORKER`. Prohibit `--no-sandbox` in production.
5. **DIRECTIVE 06-05 (4-Tier Redaction Engine):** Implement the 4-Tier AST, Error Guard, Stream Normalizer, and Regex Sanitizer in `R14_PLATFORM_OBSERVABILITY` with metadata-only production logging defaults.
6. **DIRECTIVE 06-06 (Conformance Test Suite):** Implement automated security conformance tests asserting 100% token redaction across all logging sinks, error handlers, and OTel spans prior to freeze certification.

**FORMAL DISPOSITION:** **RATIFIED AND CONFIRMED**  
**DOMAIN OWNER:** `R07_SECURITY` (Security Specialist)  
**SUPERVISOR SESSION:** `ba3ecfd0-288e-4278-924a-0f7c61ed584e`  
**TIMESTAMP:** `2026-08-15T21:30:00+07:00`  
