# OPERATOR RUNBOOK CERTIFICATE
## AI Video Factory — Publish Operator Runbook v1.0.0 Verification Certificate

**Certificate Issue Date:** 2026-08-16  
**Evaluation Model:** Gemini 3.7 Flash High  
**External Audit Model:** Claude Opus 4.6 Thinking  
**Audit Verdict:** `RUNBOOK_AUDIT_RESULT = VERIFIED_OPERATOR_RUNBOOK`  
**Final Result:** `RUNBOOK_FREEZE_RESULT = READY_FOR_HUMAN_IMPLEMENTATION`  

---

## 1. Cryptographic Baseline & Runbook Manifest Attestation

| Metric / Check | Value / Hash | Status |
|---|---|---|
| **Runbook Version** | `1.0.0` | **VERIFIED** |
| **Baseline Version** | `1.0.0` | **VERIFIED** |
| **Baseline Spec Path** | `01_FROZEN_RELEASE/v1.0.0` | **VERIFIED** |
| **Frozen Baseline Tree SHA-256** | `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846` | **VERIFIED (60/60 files)** |
| **Runbook Manifest Path** | `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RUNBOOK_MANIFEST.yaml` | **VERIFIED** |
| **Runbook Manifest SHA-256** | `41e04d7dc3a5c0ba3bdb0177ac0b6ede8811e57cf2dae534bc82b89e20add9f9` | **VERIFIED** |
| **Runbook Tree SHA-256** | `737a3f00ea8e5b35263a6f24096c1eafeaf0d2e0b3821f67ecb906aa8af2e327` | **VERIFIED (129 files)** |
| **Lockfile Path** | `OPERATOR_RUNBOOK.lock.json` | **VERIFIED** |
| **Total Prompts** | `99` (75 Repo + 6 Gates + 3 Release + 8 Recovery + 5 Checkpoints/Provisioning + 2 System) | **VERIFIED** |
| **Repositories Covered** | `15 / 15` (R01 through R15 with 5 standard prompts each) | **VERIFIED** |

---

## 2. Automated Validation Suite Results

All 7 automated validator scripts executed and passed with zero errors:

| Validator Script | Scope | Result |
|---|---|---|
| `validate_manifest.py` | Validates 99 prompt IDs, paths, and 100% gate prerequisite alignment | **PASS (1/7)** |
| `validate_prompt_headers.py` | Validates mandatory headers, `ALLOWED_WRITE_ROOT`, `FORBIDDEN_WRITE_PATHS` | **PASS (2/7)** |
| `validate_next_links.py` | Validates graph connectivity, 0 dangling next links | **PASS (3/7)** |
| `validate_repo_coverage.py` | Validates 15/15 repositories (5 prompts each = 75 repo prompts) | **PASS (4/7)** |
| `validate_model_matrix.py` | Validates model assignments, fallbacks, and 9 hostile Opus reviews | **PASS (5/7)** |
| `validate_frozen_path_guards.py` | Validates zero frozen write permissions across all 99 prompts | **PASS (6/7)** |
| `validate_remediation_invariants.py` | Validates remediation fixes (MB-01, MB-02, MA-01–07, DAG integrity) | **PASS (7/7)** |

---

## 3. External Forensic Audit Verification (27/27 Checks)

The runbook was independently audited against the normative frozen specification v1.0.0. All 27 verification items confirmed:

1. **Repo Coverage:** 15/15 repositories covered with 5-prompt suites (Plan, Implement, Test, Acceptance, Recovery).
2. **Dependency Graph Integrity:** DAG execution matches frozen architecture and build order.
3. **Prompt Self-Containment:** Every prompt specifies workspace, repo, folder, model, mode, exact `/goal`, prerequisites, allowed/forbidden writes, and standard YAML outputs.
4. **Safety Boundaries:** Complete read-only protection of frozen directories (`01_FROZEN_RELEASE/`, `02_SOURCE_KITS_READONLY/`, `03_GOVERNANCE_EVIDENCE_READONLY/`, `90_ARCHIVE_READONLY/`).
5. **Contract-First Architecture:** R01-01 strictly enforces contract definitions prior to downstream coding.
6. **Core State Isolation:** R02 is established as the sole schema & database owner.
7. **Flow Execution Port Boundary:** R08, R09, and R10 maintain independent separation behind FlowExecutionPort.
8. **Temporal Replay Durability:** Deterministic workflow execution and activity idempotency tested at GATE-01 and R06-03.
9. **Fake Provider Precedence:** FakeVideoProvider (GATE-01) strictly precedes live Google Flow (GATE-05).
10. **Anti-Abuse & Secret Protection:** Zero CAPTCHA/rate-limit bypass, mandatory automated secret redaction.
11. **Non-Destructive Git Flow:** Fast-forward merges forbidden (`--no-ff`), atomic commits, annotated release tags.
12. **Complete Traversal:** 72-step golden path verified from CHK-01 to REL-03 with zero dead-ends.
13. **Resumption Safety:** RESUME-01 deterministically computes next prompt from `RUN_STATE.yaml`.
14. **Maintenance Lifecycle:** 7 lifecycle routes documented in `19_MAINTENANCE/MAINTENANCE_LIFECYCLE.md`.

---

## 4. Operational State & Environment Configuration

| Path | Mode | Purpose |
|---|---|---|
| `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/` | **READ-ONLY** | Frozen operator runbook instructions, manifests & validators |
| `05_IMPLEMENTATION/operator-state/` | **WRITABLE** | Runtime state tracking directory |
| `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` | **WRITABLE** | Active execution state, gate statuses, repository milestones |
| `05_IMPLEMENTATION/operator-state/RUN_HISTORY/` | **WRITABLE** | Execution step logs and audit trails |
| `05_IMPLEMENTATION/operator-state/BLOCKERS/` | **WRITABLE** | Escalated blocker tickets and resolution logs |
| `05_IMPLEMENTATION/operator-state/CHANGE_REQUESTS/` | **WRITABLE** | Formal change request proposals and approvals |

---

## 5. Human Operator Implementation Entrypoint

Implementation begins at Step 1:

- **Entrypoint Document:** [IMPLEMENTATION_START_HERE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/IMPLEMENTATION_START_HERE.md)
- **First Prompt ID:** `CHK-01`
- **First Prompt Path:** [CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md)
- **Assigned Model:** **Gemini 3.7 Flash High**
- **Mode:** Local workspace
- **Workspace:** `AVF_SPEC_REVIEW/`
- **First Command:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```

---

## 6. Official Freeze Verdict

```yaml
RUNBOOK_FREEZE_RESULT: READY_FOR_HUMAN_IMPLEMENTATION
RUNBOOK_VERSION: 1.0.0
BASELINE_VERSION: 1.0.0
TOTAL_PROMPTS: 99
REPOS_COVERED: 15
RUNBOOK_TREE_SHA256: 737a3f00ea8e5b35263a6f24096c1eafeaf0d2e0b3821f67ecb906aa8af2e327
AUDIT_RESULT: VERIFIED_OPERATOR_RUNBOOK
RUNBOOK_READONLY: true
RUNTIME_STATE_WRITEABLE: true
GIT_TAG: avf-operator-runbook-v1.0.0
HUMAN_START_FILE: IMPLEMENTATION_START_HERE.md
FIRST_PROMPT: CHK-01
FIRST_MODEL: Gemini 3.7 Flash High
FIRST_WORKSPACE: AVF_SPEC_REVIEW/
FIRST_COMMAND: /goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
NEXT_REQUIRED_ACTION: RUN_FIRST_OPERATOR_PROMPT
```
