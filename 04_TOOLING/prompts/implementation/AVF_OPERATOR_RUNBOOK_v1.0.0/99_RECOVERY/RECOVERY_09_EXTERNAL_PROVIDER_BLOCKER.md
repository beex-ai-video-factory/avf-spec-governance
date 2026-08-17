# RECOVERY 09: EXTERNAL PROVIDER BLOCKER & CAPTCHA ESCALATION
## AI Video Factory — Anti-Abuse Safety & Human Operator Escalation

**PROMPT_ID:** `REC-09`  
**PURPOSE:** Handle Google Flow security challenges, bot detections, CAPTCHAs, or rate limit blocks strictly through human operator escalation without unauthorized automation bypass.  
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
- `05_IMPLEMENTATION/repos/R08_google_flow_adapter/**`
- `05_IMPLEMENTATION/repos/R09_browser_worker/**`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R08_google_flow_adapter/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/99_RECOVERY/RECOVERY_09_EXTERNAL_PROVIDER_BLOCKER.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Escalation record in `RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- Anti-abuse zero-bypass rule strictly enforced.
- Operator escalation notification generated.
- State mapped to `BLOCKED_PROVIDER` until human completes manual session challenge.  
**FAIL_CRITERIA:**
- Attempting automated CAPTCHA solver or credential brute-forcing.  
**GIT_EXPECTATION:** State preserved cleanly.  
**HUMAN_ACTION_AFTER_PASS:** Human operator opens browser, resolves challenge manually, then runs `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Stop all automated provider requests.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/RESUME_PROJECT.md`

---

### Step-by-Step Instructions:

1. **Verify Security Challenge:**
   Record challenge type (`CAPTCHA`, `AUTH_EXPIRED`, `RATE_LIMIT_EXCEEDED`).
2. **Enforce Zero-Bypass Invariant:**
   Do not attempt automated solver scripts.
3. **Escalate to Human Operator:**
   Provide manual resolution instructions.
4. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "REC-09"
RESULT: HUMAN_ACTION_REQUIRED
REPO: "SYSTEM_RECOVERY"
BRANCH: "main"
COMMIT_SHA: "N/A"
FROZEN_DRIFT: 0
TESTS: {passed: 1, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: ["Provider security challenge requiring manual operator resolution"]
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_05_CONTROLLED_LIVE_FLOW_GATE.md"
RECOMMENDED_NEXT_TASK: "Resume live Flow gate after human completes security verification."
HUMAN_INSTRUCTION: "Open browser session, solve challenge manually, and re-run GATE_05."
```
