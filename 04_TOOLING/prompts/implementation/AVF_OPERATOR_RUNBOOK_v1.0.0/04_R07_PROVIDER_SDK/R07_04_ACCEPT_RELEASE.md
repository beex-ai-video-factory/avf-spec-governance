# R07 PROVIDER NEUTRAL SDK & FAKEPROVIDER — ACCEPTANCE & RELEASE
## AI Video Factory — Formal Acceptance, Merge & Version Tagging

**PROMPT_ID:** `R07-04`  
**PURPOSE:** Conduct formal acceptance signoff for R07_provider_sdk (Provider Neutral SDK & FakeProvider), merge feature branch to main, apply annotated git release tag, and unlock downstream dependency gates.  
**CURRENT_PHASE:** `04_R07_PROVIDER_SDK`  
**RUN_FROM_WORKSPACE:** `AVF_SPEC_REVIEW/`  
**OPEN_REPOSITORY:** `R07_provider_sdk`  
**WORKING_DIRECTORY:** `/Applications/XAMPP/xamppfiles/htdocs/AGENTIC/AVF_SPEC_REVIEW/05_IMPLEMENTATION/repos/R07_provider_sdk`  
**MODEL:** `Gemini 3.1 Pro High`  
**MODEL_FALLBACK:** `Gemini 3.1 Pro High`  
**ANTIGRAVITY_MODE:** `Local workspace`  
**NEW_OR_EXISTING_CONVERSATION:** `NEW_OR_EXISTING`  
**EXPECTED_DURATION_CLASS:** `FAST (<3 min)`  
**PREREQUISITES:** `R07-03`  
**READ_ONLY_INPUTS:**
- `05_IMPLEMENTATION/repos/R07_provider_sdk/AUDIT_REPORT.md`
- `05_IMPLEMENTATION/repos/R07_provider_sdk/PLAN.md`
- `01_FROZEN_RELEASE/v1.0.0/FROZEN_SPEC_CANDIDATE/03_repo_blueprints/R07_PROVIDER_SDK.md`  
**ALLOWED_WRITE_ROOT:** `05_IMPLEMENTATION/repos/R07_provider_sdk/`
**WRITEABLE_PATHS:**
- `05_IMPLEMENTATION/repos/R07_provider_sdk/**`
- `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`  
**FORBIDDEN_WRITE_PATHS:**
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`
- `05_IMPLEMENTATION/repos/!( R07_provider_sdk )/**`  
**COMMAND_TO_RUN:**
```bash
/goal Read 04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/04_R07_PROVIDER_SDK/R07_04_ACCEPT_RELEASE.md and execute it completely.
```  
**EXPECTED_ARTIFACTS:**
- Released `main` branch with annotated release tag `v1.0.0`
- Updated `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`.  
**PASS_CRITERIA:**
- All tests pass on `main`.
- Clean merge commit and git tag `r07_provider_sdk-v1.0.0` applied.
- Repository status marked as `RELEASED` in `RUN_STATE.yaml`.  
**FAIL_CRITERIA:**
- Merge conflict, uncommitted changes, or failing CI checks.  
**GIT_EXPECTATION:** Tagged release commit on `main`.  
**HUMAN_ACTION_AFTER_PASS:** Copy and run the command in `RECOMMENDED_NEXT_PROMPT`.  
**HUMAN_ACTION_AFTER_FAIL:** Run `04_R07_PROVIDER_SDK/R07_RECOVERY.md`.  
**NEXT_PROMPT_IF_PASS:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md`  
**NEXT_PROMPT_IF_FAIL:** `04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/04_R07_PROVIDER_SDK/R07_RECOVERY.md`

---

### Step-by-Step Instructions:

1. **Verify Audit Signoff:**
   Inspect `05_IMPLEMENTATION/repos/R07_provider_sdk/AUDIT_REPORT.md` and confirm PASS verdict.
2. **Merge to Main Branch:**
   Checkout `main` and merge `feature/r07-impl` cleanly:
   `git checkout main && git merge --no-ff feature/r07-impl -m "feat(r07): complete R07_provider_sdk implementation"`
3. **Apply Release Tag:**
   Apply annotated git tag:
   `git tag -a "r07_provider_sdk-v1.0.0" -m "Release R07_provider_sdk v1.0.0"`
4. **Update System Runtime State:**
   In `05_IMPLEMENTATION/operator-state/RUN_STATE.yaml`, set `R07_provider_sdk.status: "RELEASED"` and record commit SHA and tag.
5. **Emit Standard Final Output:**

```yaml
PROMPT_ID: "R07-04"
RESULT: PASS
REPO: "R07_provider_sdk"
BRANCH: "main"
COMMIT_SHA: "HEAD"
FROZEN_DRIFT: 0
TESTS: {passed: 18, failed: 0}
CONTRACT_TESTS: {passed: 8, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS: []
ARTIFACTS_CREATED:
  - "05_IMPLEMENTATION/repos/R07_provider_sdk/ (tagged r07_provider_sdk-v1.0.0)"
  - "05_IMPLEMENTATION/operator-state/RUN_STATE.yaml"
RECOMMENDED_NEXT_PROMPT: "04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/17_INTEGRATION_GATES/GATE_00_FOUNDATION_GATE.md"
RECOMMENDED_NEXT_TASK: "Proceed to next scheduled prompt in master execution sequence."
HUMAN_INSTRUCTION: "Run the command in RECOMMENDED_NEXT_PROMPT."
```
