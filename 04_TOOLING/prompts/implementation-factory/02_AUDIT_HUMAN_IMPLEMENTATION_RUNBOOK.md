# EXTERNAL HUMAN RUNBOOK AUDIT
## AI Video Factory — Operator Runbook Forensic Validation

### RUN LOCATION
Open `AVF_SPEC_REVIEW/` in a NEW conversation.

### MODEL
**Claude Opus 4.6 Thinking**, or strongest available non-Gemini reasoning model.

### MODE
Local workspace, read-mostly.

### COMMAND
`/goal Read 04_TOOLING/prompts/implementation-factory/02_AUDIT_HUMAN_IMPLEMENTATION_RUNBOOK.md and execute it completely.`

Audit `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/` against CURRENT frozen v1.0.0 and implementation workspace.

Do not implement product code. Do not modify frozen baseline. Do not trust runbook claims. Write only under runbook `_AUDIT/`.

Required checks:
1. 15/15 repo coverage.
2. Dependency order matches frozen DAG.
3. Every execution prompt specifies workspace/repo/folder/model/mode/exact `/goal`.
4. Every prompt is new-conversation-safe.
5. Prerequisites and allowed/forbidden writes are explicit.
6. Every repo has Plan/Implement/Test/Accept/Recovery.
7. Every PASS and FAIL/BLOCKED next link exists.
8. No unintended cycles/dead ends.
9. Parallel steps are dependency-safe.
10. Contract-first architecture preserved.
11. No coding agent may opportunistically edit upstream repo.
12. No frozen edits.
13. R01 hardening represented.
14. R02-only DB ownership preserved.
15. R08/R09/R10 FlowExecutionPort boundary preserved.
16. R09 and R10 remain independent.
17. Provider-neutral core preserved.
18. FakeVideoProvider precedes live Flow.
19. Temporal retry/reconciliation/idempotency tests included.
20. R15 integration gates are correctly placed.
21. Live Flow only after fake/conformance gates.
22. No CAPTCHA/rate-limit/anti-abuse bypass.
23. Git/GitHub flow is non-destructive.
24. Every result has PASS/FAIL/BLOCKED semantics and mechanically valid next prompt.
25. Resume workflow works after closing conversations.
26. Release workflow includes version/tag/CI/integration/security acceptance.
27. Maintenance/change-request path exists.

Simulate complete PASS traversal from first prompt to final release. Sample every failure edge. Perform adversarial human simulation assuming minimal operator knowledge; identify undocumented judgment points.

Create under `_AUDIT/`:
- `RUNBOOK_FORENSIC_AUDIT.md`
- `PROMPT_GRAPH_AUDIT.md`
- `DEPENDENCY_ORDER_AUDIT.md`
- `HUMAN_DX_AUDIT.md`
- `MODEL_ROUTING_AUDIT.md`
- `SAFETY_BOUNDARY_AUDIT.md`
- `FINAL_BLOCKERS.md`

Allowed result:
`VERIFIED_OPERATOR_RUNBOOK`, `REMEDIATION_REQUIRED`, or `INSUFFICIENT_EVIDENCE`.

VERIFIED requires zero critical missing prompts, zero dangling links, zero frozen-write permission, correct dependency order, exact operator instructions, recovery path for every failure class, 15/15 repos and reachable final release.

Return only:

```yaml
RUNBOOK_AUDIT_RESULT:
CRITICAL_BLOCKERS:
MAJOR_BLOCKERS:
MINOR_ADVISORIES:
PROMPTS_AUDITED:
REPOS_COVERED:
DANGLING_NEXT_LINKS:
INVALID_DEPENDENCY_EDGES:
FROZEN_WRITE_VIOLATIONS:
HUMAN_AMBIGUITY_POINTS:
RECOMMENDED_ACTION: FREEZE_OPERATOR_RUNBOOK | TARGETED_RUNBOOK_REMEDIATION
```

STOP. Do not implement application code.
