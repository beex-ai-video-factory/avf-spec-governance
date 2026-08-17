# AI VIDEO FACTORY v1.0.0 — OPERATOR RULES
## 10 Non-Negotiable System Invariants & Operational Rules

**Version:** 1.0.0  
**Authority:** Technical Architecture Board & Security Custodian

---

### Rule 1: The Golden Routing Rule
Never guess or manually pick the next execution step. After every prompt execution, strictly follow the `RECOMMENDED_NEXT_PROMPT` provided in the standardized YAML output block.

### Rule 2: Immutability of the Frozen Baseline & FORBIDDEN_WRITE_PATHS
The directories `01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, and `90_ARCHIVE_READONLY/` are permanently frozen. Any modification, deletion, move, or write inside these paths is strictly forbidden (`FORBIDDEN_WRITE_PATHS`). Read operations are permitted when necessary for specification context.

### Rule 3: Strict Polyrepo Isolation & Positive Write Allowlist (ALLOWED_WRITE_ROOT)
One coding task owns exactly one repository. When working in `05_IMPLEMENTATION/repos/RXX/`, the agent is restricted to `ALLOWED_WRITE_ROOT: 05_IMPLEMENTATION/repos/RXX/`. Everything outside `ALLOWED_WRITE_ROOT` is write-forbidden unless explicitly listed as a state/tooling output. The agent must never edit files belonging to another repository. Upstream changes require completing and releasing the upstream repo first.

### Rule 4: Single-Ownership Database Principle
Only `R02_core_state` owns database access and credentials. No other service, worker, workflow, or UI may connect directly to PostgreSQL. All persistence occurs through R02's strongly typed REST/gRPC interfaces.

### Rule 5: FlowExecutionPort Isolation Principle
`R08_google_flow_adapter` must interact with Track A (`R09_browser_worker`) and Track B (`R10_flowkit_bridge`) strictly through the 10-operation `FlowExecutionPort` contract. Track A and Track B must remain mutually independent with zero cross-imports.

### Rule 6: FakeProvider-First Verification
At least 80% of all workflow, failure, and edge-case behavior must be proven deterministically against `FakeVideoProvider` in `R07_provider_sdk` before incurring paid external generation credits.

### Rule 7: Anti-Abuse & Zero-Bypass Policy
No automated agent, test, or worker may attempt to bypass CAPTCHAs, bot detections, or rate limits. When a security challenge occurs, the system must immediately escalate to a `HUMAN_REQUIRED` / `BLOCKED_PROVIDER` state.

### Rule 8: Temporal Determinism & Replay Safety
All workflow definitions in `R06_workflow` must be strictly deterministic. No direct I/O, random number generation, system clocks, or unversioned state mutations inside workflow functions.

### Rule 9: Observability & Automated Secret Redaction
All logs, metrics, and trace spans emitted via `R14_platform_observability` must pass through automated secret redaction filters. Zero plain-text tokens, passwords, or cookies in telemetry.

### Rule 10: Strict Standardized Output Contract & Result Taxonomy
Every execution prompt must conclude with the exact YAML output contract block containing `PROMPT_ID`, `RESULT`, `REPO`, `BRANCH`, `COMMIT_SHA`, `FROZEN_DRIFT`, `TESTS`, `BLOCKERS`, and `RECOMMENDED_NEXT_PROMPT`. Prose-only conclusions are invalid.

Valid values for `RESULT`:
- `PASS`: All required acceptance criteria satisfied; execution proceeds to `RECOMMENDED_NEXT_PROMPT`.
- `FAIL`: Implementation or test defect exists locally in current repository; remediation is possible locally via recovery prompt.
- `BLOCKED`: The current prompt cannot safely proceed because of an unmet dependency, external service/provider condition, contract incompatibility, environment requirement, or required upstream action.
- `HUMAN_ACTION_REQUIRED`: Operator authentication, credentials, specification CR approval, or security challenge intervention is required before proceeding.
