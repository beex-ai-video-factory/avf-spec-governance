# AI VIDEO FACTORY v1.0.0 — FAILURE DECISION TREE
## Systematic Error Triage & Recovery Routing Matrix

**Version:** 1.0.0 (Remediated)  
**Authority:** Technical Architecture Board  

---

## 1. Result Taxonomy & Triage Classification

| Result State | Definition | Operator Action |
|---|---|---|
| `RESULT: PASS` | All required acceptance criteria satisfied. | Copy and run `RECOMMENDED_NEXT_PROMPT`. |
| `RESULT: FAIL` | Local implementation or test defect exists; remediable in current repository. | Run `<REPO>_RECOVERY.md` or `REC-04`. |
| `RESULT: BLOCKED` | Execution cannot proceed due to unmet dependency, external service/provider condition, contract incompatibility, environment outage, or upstream block. | Run exact recovery prompt returned in `RECOMMENDED_NEXT_PROMPT`. |
| `RESULT: HUMAN_ACTION_REQUIRED` | Human intervention required (operator credentials, security challenge resolution, CR sponsor approval). | Follow `HUMAN_INSTRUCTION`. |

---

## 2. Systematic Triage Decision Tree

```
Issue Detected during Prompt Execution
│
├── 1. Is the error a localized implementation bug (syntax error, failed unit test in current repo)?
│   └── YES [RESULT: FAIL] ──> Run Local Repo Recovery: <REPO>_RECOVERY.md (or REC-04)
│
├── 2. Is the error caused by a broken schema, missing field, or incompatible type definition?
│   └── YES [RESULT: BLOCKED] ──> Run Contract Break Recovery: 99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md
│
├── 3. Does the error reveal a contradiction or flaw in the frozen specification (01_FROZEN_RELEASE/)?
│   └── YES [RESULT: HUMAN_ACTION_REQUIRED] ──> Open Formal Change Request: 99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md
│
├── 4. Is the failure due to an unbuilt or unreleased upstream dependency?
│   └── YES [RESULT: BLOCKED] ──> Run Blocked Dependency Recovery: 99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md
│
├── 5. Did a system integration gate or scenario harness fail?
│   └── YES [RESULT: FAIL / BLOCKED] ──> Run Integration Gate Recovery: 99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md
│
├── 6. Did the coding agent stall, loop endlessly, or produce truncated code?
│   └── YES [RESULT: FAIL] ──> Run Stalled Agent Recovery: 99_RECOVERY/RECOVERY_06_STALLED_AGENT.md
│
├── 7. Is the failure a Git conflict, dirty worktree, or branch drift?
│   └── YES [RESULT: FAIL / BLOCKED] ──> Run Git Recovery: 99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md
│
├── 8. Is Docker, PostgreSQL, Temporal, MinIO, or the dev environment unhealthy?
│   └── YES [RESULT: BLOCKED] ──> Run Environment Recovery: 99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md
│
└── 9. Did Google Flow present a CAPTCHA, bot detection challenge, or rate limit?
    └── YES [RESULT: HUMAN_ACTION_REQUIRED] ──> Run External Provider Recovery: 99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md
```

---

## 3. Recovery Prompt Dispatch Catalog

| Category Code | Recovery Scenario | Typical Result | Dispatch Recovery Prompt |
|---|---|---|---|
| `REC-01` | Blocked Upstream Dependency | `BLOCKED` | [RECOVERY_01_BLOCKED_DEPENDENCY.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md) |
| `REC-02` | Contract Incompatibility / Schema Break | `BLOCKED` | [RECOVERY_02_CONTRACT_BREAK.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md) |
| `REC-03` | Frozen Spec Defect / Formal CR Required | `HUMAN_ACTION_REQUIRED` | [RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md) |
| `REC-04` | Unit / Conformance Test Gate Failure | `FAIL` | [RECOVERY_04_TEST_GATE_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_04_TEST_GATE_FAILURE.md) |
| `REC-05` | System Integration Gate Failure | `FAIL` / `BLOCKED` | [RECOVERY_05_INTEGRATION_GATE_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md) |
| `REC-06` | Stalled or Hallucinating Agent | `FAIL` | [RECOVERY_06_STALLED_AGENT.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md) |
| `REC-07` | Git Conflicts & Branch State Inconsistencies| `FAIL` / `BLOCKED` | [RECOVERY_07_GIT_RECOVERY.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md) |
| `REC-08` | Docker / Local Dev Environment Outage | `BLOCKED` | [RECOVERY_08_ENVIRONMENT_FAILURE.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md) |
| `REC-09` | External Provider Security Challenge / CAPTCHA| `HUMAN_ACTION_REQUIRED` | [RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md](file:///Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md) |
