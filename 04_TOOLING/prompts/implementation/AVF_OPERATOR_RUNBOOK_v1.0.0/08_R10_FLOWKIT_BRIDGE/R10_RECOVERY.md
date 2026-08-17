# R10 TRACK B DIRECT FLOWKIT BRIDGE — RECOVERY & TRIAGE
## AI Video Factory — Local Repository Defect Triage & Routing

**PROMPT_ID:** `R10-REC`  
**PURPOSE:** Triage failures occurring within R10_flowkit_bridge (Track B Direct FlowKit Bridge), categorize the defect class, and route to local remediation or master system recovery.  
**CURRENT_PHASE:** `08_R10_FLOWKIT_BRIDGE`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R10_flowkit_bridge`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R10_flowkit_bridge`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** None  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R10_flowkit_bridge/**`
- `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/FAILURE_DECISION_TREE.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R10_flowkit_bridge/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R10_flowkit_bridge/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/08_R10_FLOWKIT_BRIDGE/R10_RECOVERY.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Diagnostic defect analysis and targeted recovery action.  
**PASS_CRITERIA:**
- Defect correctly categorized (IMPLEMENTATION_BUG, CONTRACT_DEFECT, FROZEN_SPEC_DEFECT, ENVIRONMENT, DEPENDENCY, EXTERNAL_PROVIDER).
- Exact remediation command or recovery prompt returned.  
**FAIL_CRITERIA:**
- Unclassified defect.  
**GIT_EXPECTATION:** Worktree preserved for debugging.  
**HUMAN_ACTION_AFTER_PASS:** Execute the returned `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Escalate to human architect.  
**NEXT_PROMPT_IF_PASS:** Deterministic routing based on defect classification (see Defect Classification & Dispatch Matrix below: IMPLEMENTATION_BUG -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/08_R10_FLOWKIT_BRIDGE/R10_02_IMPLEMENT.md, CONTRACT_BREAK -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md, FROZEN_SPEC_DEFECT -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md, DEPENDENCY_BLOCK -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md, GIT -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md, ENVIRONMENT -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md, EXTERNAL_PROVIDER -> 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md)  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_06_STALLED_AGENT.md`

---


> [!IMPORTANT]
> **AUTONOMOUS DEFECT CLASSIFICATION MANDATE:**
> The recovery agent MUST analyze the failure logs, classify the defect into exactly ONE category in the Dispatch Matrix below, and output the EXACT single prompt path in `RECOMMENDED_NEXT_PROMPT`.
> Under NO circumstances should the agent output "Dynamic routing based on defect class" or leave branch selection to the human operator.

### Defect Classification & Dispatch Matrix:

1. **Category A: Local Implementation Bug (Syntax, Logic, Local Unit Test)**
   - **Action:** Fix code within `05_IMPLEMENTATION/repos/R10_flowkit_bridge/src/` and re-run `08_R10_FLOWKIT_BRIDGE/R10_02_IMPLEMENT.md`.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/08_R10_FLOWKIT_BRIDGE/R10_02_IMPLEMENT.md`
2. **Category B: Schema Incompatibility / Contract Break**
   - **Action:** Open contract change triage.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_02_CONTRACT_BREAK.md`
3. **Category C: Frozen Spec Contradiction**
   - **Action:** Open formal Change Request.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_03_FROZEN_SPEC_DEFECT_CR.md`
4. **Category D: Upstream Dependency Missing or Broken**
   - **Action:** Verify upstream repository release.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_01_BLOCKED_DEPENDENCY.md`
5. **Category E: Git Conflict / Branch State Issue**
   - **Action:** Run git state reconciliation.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_07_GIT_RECOVERY.md`
6. **Category F: Environment / Toolchain Failure**
   - **Action:** Re-run environment doctor.
   - **Next:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_08_ENVIRONMENT_FAILURE.md`
