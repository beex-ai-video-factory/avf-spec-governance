# FREEZE HUMAN IMPLEMENTATION RUNBOOK
## AI Video Factory — Publish Operator Runbook v1.0.0

### RUN LOCATION
Open `AVF_SPEC_REVIEW/`.

### MODEL
**Gemini 3.7 Flash High**

### MODE
Local workspace.

### COMMAND
`/goal Read 04_TOOLING/prompts/implementation-factory/03_FREEZE_HUMAN_IMPLEMENTATION_RUNBOOK.md and execute it completely.`

Freeze/publish the runbook only after external audit returns:
`RUNBOOK_AUDIT_RESULT = VERIFIED_OPERATOR_RUNBOOK`.

Do not implement product code or alter frozen system spec.

Read generated runbook, `_AUDIT/`, frozen baseline and Git status. If audit is not VERIFIED, return `RUNBOOK_FREEZE_RESULT = BLOCKED_AUDIT` and STOP.

Actions:
1. Run all runbook validators.
2. Recompute prompt graph and verify 15/15 repo coverage.
3. Verify zero frozen-write violations.
4. Verify every execution prompt has workspace, repo, folder, model, mode, exact `/goal`, prerequisites, PASS/FAIL/BLOCKED output, next and recovery prompt.
5. Create `OPERATOR_RUNBOOK.lock.json` with version, baseline version, frozen spec hash, prompt count, manifest SHA-256, runbook tree hash, audit result/date and first operator prompt.
6. Create `OPERATOR_RUNBOOK_CERTIFICATE.md`.
7. Create root `IMPLEMENTATION_START_HERE.md` containing only current baseline, frozen-file rule, exact workspace/model/first prompt/command, resume method, PASS/FAIL behavior and rule to run only `RECOMMENDED_NEXT_PROMPT`.
8. Make runbook read-only EXCEPT runtime state.
9. Create writable `05_IMPLEMENTATION/operator-state/` with `RUN_STATE.yaml`, `RUN_HISTORY/`, `BLOCKERS/`, `CHANGE_REQUESTS/`.
10. Git commit the runbook/audit as one non-destructive checkpoint if configured.

Suggested commit:
`docs(runbook): freeze v1.0.0 human implementation operator system`

Suggested annotated tag:
`avf-operator-runbook-v1.0.0`

Never force push.

Return only:

```yaml
RUNBOOK_FREEZE_RESULT: READY_FOR_HUMAN_IMPLEMENTATION | BLOCKED
RUNBOOK_VERSION:
BASELINE_VERSION:
TOTAL_PROMPTS:
REPOS_COVERED:
RUNBOOK_TREE_SHA256:
AUDIT_RESULT:
RUNBOOK_READONLY:
RUNTIME_STATE_WRITEABLE:
GIT_COMMIT:
GIT_TAG:
HUMAN_START_FILE:
FIRST_PROMPT:
FIRST_MODEL:
FIRST_WORKSPACE:
FIRST_COMMAND:
NEXT_REQUIRED_ACTION: RUN_FIRST_OPERATOR_PROMPT | FIX_RUNBOOK_FREEZE_BLOCKER
```

STOP. Do not run first implementation prompt automatically.
