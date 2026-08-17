# AI VIDEO FACTORY v1.0.0 — HUMAN IMPLEMENTATION ENTRYPOINT

**Baseline Version:** `1.0.0` (Status: `VERIFIED_IMPLEMENTATION_BASELINE`)  
**Frozen Spec Content Tree SHA-256:** `7258ee6eac6e4887739f137939d42960417e3da3926c1f560eb91cc8aa392846`  
**Runbook Version:** `1.0.0` (Status: `READY_FOR_HUMAN_IMPLEMENTATION`)  
**Runbook Tree SHA-256:** `737a3f00ea8e5b35263a6f24096c1eafeaf0d2e0b3821f67ecb906aa8af2e327`  
**Master Workspace Root:** `AVF_SPEC_REVIEW/`

---

## 1. Frozen-File Immutability Rule

The following directories are **STRICTLY READ-ONLY** under all circumstances:
- `01_FROZEN_RELEASE/`
- `02_SOURCE_KITS_READONLY/`
- `03_GOVERNANCE_EVIDENCE_READONLY/`
- `90_ARCHIVE_READONLY/`

No tool, agent, or operator may modify, move, rename, or delete files in these directories. All production source code must be written strictly within `05_IMPLEMENTATION/repos/<repo_name>/`.

---

## 2. The Golden Execution Rule: Run Only `RECOMMENDED_NEXT_PROMPT`

> [!IMPORTANT]
> **NEVER CHOOSE OR GUESS THE NEXT STEP MANUALLY.**
> After each prompt executes, inspect the standard YAML output block:
> - **`RESULT: PASS`**: All acceptance criteria satisfied. Copy and run the exact command in `RECOMMENDED_NEXT_PROMPT`.
> - **`RESULT: FAIL`**: Implementation or test defect encountered. Execute the specific recovery prompt returned in `RECOMMENDED_NEXT_PROMPT`.
> - **`RESULT: BLOCKED`**: Unmet upstream dependency or environment condition. Execute the recovery/remediation prompt provided in `RECOMMENDED_NEXT_PROMPT`.
> - **`RESULT: HUMAN_ACTION_REQUIRED`**: Manual intervention required (e.g. security challenge, credentials, change request approval). Follow `HUMAN_INSTRUCTION`.

---

## 3. First Implementation Action

To begin building the AI Video Factory system from the frozen baseline, execute Step 1:

- **Workspace:** `AVF_SPEC_REVIEW/`
- **Model:** **Gemini 3.7 Flash High** (Mode: Local workspace)
- **First Prompt File:** [`04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md`](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md)
- **Exact Command to Run:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/00_CHECKPOINTS/CHECKPOINT_01_PREFLIGHT_AND_SECURITY.md and execute it completely.
```

---

## 4. Session Resumption Method

If your conversation ends, context resets, or you return to a paused build:

1. Open workspace `AVF_SPEC_REVIEW/`.
2. Select model **Gemini 3.7 Flash High** (Local workspace mode).
3. Run the resumption command:
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md and execute it completely.
```
4. Follow the single `RECOMMENDED_NEXT_PROMPT` returned by the resumption tool.
