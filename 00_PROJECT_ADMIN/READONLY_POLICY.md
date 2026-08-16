# READ-ONLY PROTECTION POLICY
## AI Video Factory — Frozen Baseline & Governance Immutability

**Version:** 1.0.0  
**Effective Date:** 2026-08-16  
**Scope:** Workspace-wide  

---

## 1. Objective & Immutability Standard

The AI Video Factory v1.0.0 specification has been formally frozen, certified by the Council, and independently verified by external forensic audit. To prevent drift, unintentional corruption, or silent modifications during downstream implementation, all baseline, source, governance, and archive directories are strictly protected as **Read-Only**.

---

## 2. Protected Directories

The following directory trees are designated as permanently read-only:

1. **`01_FROZEN_RELEASE/`**
   - Contains `v1.0.0/` normative specification, JSON schemas, repo blueprints, and `distributable/` final release zip + detached SHA-256 sidecar.
2. **`02_SOURCE_KITS_READONLY/`**
   - Contains immutable input kits (`AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0`, `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0`, `AVF_COUNCIL_GOAL_AUTOPILOT_v1.0.0`).
3. **`03_GOVERNANCE_EVIDENCE_READONLY/`**
   - Contains complete historical review session logs, ballots, deliberations, dissent registers, and forensic audit reports.
4. **`90_ARCHIVE_READONLY/`**
   - Contains superseded release archives and legacy audit packages.

---

## 3. Enforcement Mechanisms

### A. Operating System Permissions
POSIX permissions are applied to strip write privileges from all users, groups, and others:
```bash
chmod -R a-w 01_FROZEN_RELEASE 02_SOURCE_KITS_READONLY 03_GOVERNANCE_EVIDENCE_READONLY 90_ARCHIVE_READONLY
```

### B. Antigravity Agent Rules & Hooks
- `frozen-baseline-guardian` rule enforces read-only access at the agent planning and tool execution layer.
- Pre-tool safety hooks intercept write, edit, delete, or move commands targeting any path under protected directories.

---

## 4. Strict Agent Constraints

- **Autonomous Implementation Agents are FORBIDDEN from modifying protected paths.**
- Implementation agents may **NEVER** execute `chmod +w`, `rm`, `mv`, or file edit tools against protected paths.
- If an agent discovers a defect, inconsistency, or gap in the frozen specification, it must **NOT** attempt to edit the spec. It must open a formal **Change Request (CR)** in `05_IMPLEMENTATION/change-requests/` and await human triage.

---

## 5. Human-Authorized Unlock Procedure (Emergency / Governance Only)

Under normal development, protected directories remain permanently locked. In the rare event that a formal version upgrade (e.g., v1.1.0 release) is approved by the human project sponsor:

1. **Human Authorization:** The human sponsor must provide explicit written instruction.
2. **CR Reference:** An approved Change Request or Version Transition Plan must be linked.
3. **Manual Unlock Command:**
   ```bash
   chmod -R u+w <target-protected-directory>
   ```
4. **Relock Immediately:** Following authorized modification, recalculate manifests and re-execute:
   ```bash
   chmod -R a-w <target-protected-directory>
   ```
