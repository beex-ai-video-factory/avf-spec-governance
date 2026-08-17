# RECOVERY 03: FROZEN SPEC DEFECT & CHANGE REQUEST
## AI Video Factory — Formal Specification Change Control

**PROMPT_ID:** `REC-03`  
**PURPOSE:** Open and document a formal Change Request (CR) when an irreconcilable defect, impossibility, or contradiction is discovered in the frozen v1.0.0 specification.  
**CURRENT_PHASE:** `99_RECOVERY`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `01_FROZEN_RELEASE/v1.0.0/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/change-requests/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- `05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-XX.md`  
**PASS_CRITERIA:**
- Formal CR created with impact analysis, alternative solutions, and affected repository lists.
- Zero modification to frozen baseline files.
- Affected repository marked as `PAUSED_FOR_CR` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Direct edits to `01_FROZEN_RELEASE/`.  
**GIT_EXPECTATION:** CR document committed.  
**HUMAN_ACTION_AFTER_PASS:** Human sponsor must review and approve/reject CR.  
**HUMAN_ACTION_AFTER_FAIL:** Revert any unauthorized edits to frozen files.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Draft Change Request Document:**
   Create `05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-01.md`.
2. **Detail Specification Conflict:**
   Document exact file, line, and contradiction in frozen spec.
3. **Record Blocker in State:**
   Add CR to `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-03"
RESULT: HUMAN_ACTION_REQUIRED
REPO: "SYSTEM_GOVERNANCE"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: ["CR pending human sponsor approval"]
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/change-requests/CR-YYYYMMDD-01.md"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md"
RECOMMENDED_NEXT_TASK: "Human sponsor review of Change Request."
HUMAN_INSTRUCTION: "Review the Change Request and approve before resuming implementation."
```
