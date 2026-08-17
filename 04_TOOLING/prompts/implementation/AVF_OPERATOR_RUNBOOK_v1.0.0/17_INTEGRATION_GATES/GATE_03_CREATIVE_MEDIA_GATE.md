# GATE 03: CREATIVE & MEDIA PIPELINE GATE
## AI Video Factory — Scripting, Continuity, Prompting, QC & Assembly Integration

**PROMPT_ID:** `GATE-03`  
**PURPOSE:** Verify the integration of the creative automation pipeline: R03 Creative -> R04 Assets Continuity -> R05 Prompt Compiler -> R11 QC -> R12 Media Processing.  
**CURRENT_PHASE:** `17_INTEGRATION_GATES`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `AVF_SPEC_REVIEW`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.7 Flash High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `MEDIUM (5-8 min)`  
**PREREQUISITES:** `R12-04`, `R11-04`, `R05-04`, `R04-04`, `R03-04`, `GATE-02`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R03_creative/**`
- `05_IMPLEMENTATION/repos/R04_assets_continuity/**`
- `05_IMPLEMENTATION/repos/R05_prompt_compiler/**`
- `05_IMPLEMENTATION/repos/R11_qc/**`
- `05_IMPLEMENTATION/repos/R12_media/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R03_creative/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_03_CREATIVE_MEDIA_GATE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml` with GATE_03: PASSED.  
**PASS_CRITERIA:**
- Multi-shot script decompiles into structured scene/shot descriptors.
- Continuity tokens are injected consistently.
- Provider dialect compilation generates valid prompt payloads.
- Technical QC (FFprobe) and Semantic QC evaluate test video clips.
- FFmpeg media worker stitches shots and attaches audio track without errors.  
**FAIL_CRITERIA:**
- Schema validation error, broken continuity tokens, FFprobe failure, or FFmpeg crash.  
**GIT_EXPECTATION:** Clean working tree.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_01_PLAN.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_05_INTEGRATION_GATE_FAILURE.md`

---

### Step-by-Step Verification Instructions:

1. **Execute End-to-End Creative Compilation:**
   Transform raw narrative into compiled provider prompt sequences.
2. **Execute Video QC Inspection:**
   Run sample video assets through R11 technical container analyzer and semantic evaluator.
3. **Execute FFmpeg Assembly Pipeline:**
   Stitch multiple shots into final master video asset using R12 Media Service.
4. **Update State and Output Result:**

```yaml
PROMPT_ID: "GATE-03"
RESULT: PASS
REPO: "SYSTEM_GATE"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 15, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 8, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/16_R13_OPERATOR_CONSOLE/R13_01_PLAN.md"
RECOMMENDED_NEXT_TASK: "Begin R13 Operator Console implementation planning."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
