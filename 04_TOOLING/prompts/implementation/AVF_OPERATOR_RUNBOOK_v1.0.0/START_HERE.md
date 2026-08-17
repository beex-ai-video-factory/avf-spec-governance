# AI VIDEO FACTORY v1.0.0 — OPERATOR IMPLEMENTATION RUNBOOK
## Start Here — Human Operator Master Entrypoint

**Document Version:** 1.0.0  
**Baseline Lock:** `BASELINE.lock.json` (SHA-256: `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846`)  
**Forensic Status:** `FORENSIC_STATUS = VERIFIED_IMPLEMENTATION_BASELINE`  
**Current System State:** `READY_FOR_IMPLEMENTATION`  
**Workspace Root:** `AVF_SPEC_REVIEW/`

---

## 1. The Golden Operator Rule

> [!IMPORTANT]
> **DO NOT CHOOSE THE NEXT STEP YOURSELF.**
> After each prompt completes, read the standard YAML output block:
> - If `RESULT: PASS`: all acceptance criteria satisfied; copy and execute `RECOMMENDED_NEXT_PROMPT`.
> - If `RESULT: FAIL`: local implementation/test defect exists; execute the returned recovery prompt.
> - If `RESULT: BLOCKED`: task cannot proceed due to unmet upstream dependency, external condition, contract issue, or environment outage; execute the specific recovery/remediation prompt provided in `RECOMMENDED_NEXT_PROMPT`.
> - If `RESULT: HUMAN_ACTION_REQUIRED`: operator intervention is required (e.g. credentials, CR approval, security challenge); follow `HUMAN_INSTRUCTION`.
> - Never guess, skip steps, or alter the canonical sequence manually.

---

## 2. Absolute Immutability & Positive Write Allowlist

The frozen baseline directories are **STRICTLY READ-ONLY** (`FORBIDDEN_WRITE_PATHS`):
- `01_FROZEN_RELEASE/`
- `02_SOURCE_KITS_READONLY/`
- `03_GOVERNANCE_EVIDENCE_READONLY/`
- `90_ARCHIVE_READONLY/`

> [!NOTE]
> **Path Security Semantics:**
> - `FORBIDDEN_WRITE_PATHS`: Read access is permitted when needed for specification context; write/delete/move/rename is strictly forbidden.
> - `ALLOWED_WRITE_ROOT`: Positive allowlist specifying the exact repository or workspace path for the current task. Everything outside `ALLOWED_WRITE_ROOT` is write-forbidden unless explicitly listed as a state/tooling output. All production code must be written strictly within `05_IMPLEMENTATION/repos/<repo_name>/`.

---

## 3. Quick Reference Map

| Document | Purpose |
|---|---|
| [MASTER_SEQUENCE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/MASTER_SEQUENCE.md) | End-to-end linear & parallel execution graph |
| [MODEL_MATRIX.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/MODEL_MATRIX.md) | Mandatory model assignments per prompt class |
| [OPERATOR_RULES.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/OPERATOR_RULES.md) | 10 Non-negotiable implementation invariants |
| [WORKSPACE_AND_REPO_MAP.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/WORKSPACE_AND_REPO_MAP.md) | Polyrepo boundaries, paths, OWNS / DOES NOT OWN |
| [FAILURE_DECISION_TREE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/FAILURE_DECISION_TREE.md) | Error taxonomy and recovery dispatch matrix |
| [RESUME_PROJECT.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md) | Read-only resumption tool when restarting sessions |
| [19_MAINTENANCE/MAINTENANCE_LIFECYCLE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/19_MAINTENANCE/MAINTENANCE_LIFECYCLE.md) | Post-v1.0.0 maintenance lifecycle & patch routing |

---

## 4. First Operator Action

To begin implementation of AI Video Factory v1.0.0, execute Step 1:

### Step 1: Preflight & Security Checkpoint
- **Workspace:** Open `AVF_SPEC_REVIEW/`
- **Model:** **Gemini 3.7 Flash High** (Mode: Local workspace)
- **Prompt File:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md`
- **Command to Run:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```

---

## 5. Session Resumption Procedure

If your session is interrupted, restarted, or you open a fresh terminal/conversation:
1. Open workspace `AVF_SPEC_REVIEW/`.
2. Select model **Gemini 3.7 Flash High**.
3. Run the resumption command:
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md and execute it completely.
```
4. Follow the single `RECOMMENDED_NEXT_PROMPT` returned by the resumption tool.
