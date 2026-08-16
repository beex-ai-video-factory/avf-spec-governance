# PROJECT PERMISSION PLAN & SECURITY BOUNDARIES
## AI Video Factory — Agent Sandbox & File System Access Control

**Status:** APPLIED (via POSIX Permissions) + MANUAL IDE STEPS DOCUMENTED  
**Scope:** Primary Agent, Subagents, Tool Execution  

---

## 1. Access Control Matrix

| Path / Scope | Permission | Enforcement Mechanism | Purpose |
|---|---|---|---|
| `01_FROZEN_RELEASE/**` | **DENY WRITES (READ-ONLY)** | POSIX `chmod a-w` + Hook Guard | Authoritative frozen v1.0.0 baseline |
| `02_SOURCE_KITS_READONLY/**` | **DENY WRITES (READ-ONLY)** | POSIX `chmod a-w` + Hook Guard | Immutable input source kits |
| `03_GOVERNANCE_EVIDENCE_READONLY/**` | **DENY WRITES (READ-ONLY)** | POSIX `chmod a-w` + Hook Guard | Complete historical audit evidence |
| `90_ARCHIVE_READONLY/**` | **DENY WRITES (READ-ONLY)** | POSIX `chmod a-w` + Hook Guard | Superseded archives and snapshots |
| `05_IMPLEMENTATION/**` | **ALLOW READ/WRITE** | POSIX `chmod u+w` | Implementation code, tests, and configuration |
| `04_TOOLING/**` | **ALLOW READ/WRITE** | POSIX `chmod u+w` | Developer scripts, validators, bootstraps |
| `00_PROJECT_ADMIN/**` | **ALLOW READ/WRITE** | POSIX `chmod u+w` | Administrative registers, plans, certs |
| `99_TEMP/**` | **ALLOW READ/WRITE** | POSIX `chmod u+w` | Temporary scratch files |
| `.agents/**` | **ALLOW READ/WRITE** | POSIX `chmod u+w` | Agent rules, skills, hooks |
| Outside Workspace (`~/.ssh`, etc.) | **DENY ALL** | Agent Sandbox | Prevent data exfiltration or credential leaks |

---

## 2. Command Execution Restrictions

The following commands are strictly prohibited for autonomous agents or require explicit human intervention:

- `sudo` / privileged root escalations (FORBIDDEN).
- `rm -rf /` or recursive unconstrained deletes (FORBIDDEN).
- Direct modification of user SSH keys (`~/.ssh`) or global git credentials (FORBIDDEN).
- Hard resetting remote git branches or destructive git force-pushes (FORBIDDEN).
- Dispatching billable / paid provider generation calls during bootstrap/testing (FORBIDDEN — use `FakeVideoProvider`).

---

## 3. Antigravity IDE / Subagent Configuration

Subagents spawned by the parent agent inherit the exact working directory, sandbox limitations, and filesystem permissions:
- If running in IDE sandbox, ensure read/write access is restricted to the `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/` directory tree.
- The pre-tool hook in `.agents/hooks.json` intercepts tool invocations targeting frozen directories and immediately blocks execution.
