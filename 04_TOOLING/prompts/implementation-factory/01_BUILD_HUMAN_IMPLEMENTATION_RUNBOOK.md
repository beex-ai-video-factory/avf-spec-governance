# BUILD HUMAN IMPLEMENTATION RUNBOOK MASTER
## AI Video Factory — Operator Prompt System Factory v1.0.0

### RUN LOCATION
Open workspace root: `AVF_SPEC_REVIEW/`

### MODEL
Parent model: **Gemini 3.7 Flash High**

### MODE
Local workspace mode.

### COMMAND
`/goal Read 04_TOOLING/prompts/implementation-factory/01_BUILD_HUMAN_IMPLEMENTATION_RUNBOOK.md and execute it completely.`

---

You are the AI Video Factory Human-Operator Runbook Architect.

Your task is NOT to implement application code. Generate the complete human-operable implementation runbook that lets a human build AI Video Factory from frozen v1.0.0 by following one numbered instruction at a time.

The human must never infer which workspace/repo/folder to open, which model or mode to select, which prompt to run, prerequisites, expected artifacts, PASS/FAIL criteria, or next action.

Do not implement R01–R15. Do not modify frozen spec or governance evidence. Do not run paid provider generations.

## 1. Authoritative inputs

Read CURRENT workspace, not memory:
- `PROJECT.md`
- `BASELINE.lock.json`
- `00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md`
- `05_IMPLEMENTATION/IMPLEMENTATION_BASELINE.md`
- `05_IMPLEMENTATION/repo-registry.yaml`
- `05_IMPLEMENTATION/dependency-gates.yaml`
- `05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md`
- `05_IMPLEMENTATION/environment/`
- `.agents/rules/`
- `.agents/skills/`
- `.agents/hooks.json`
- `01_FROZEN_RELEASE/v1.0.0/` including contracts, ADRs, dependency graph, build order, integration/test strategy, repo blueprints, and agent packets.

Ignore superseded historical prompts as normative inputs.

Require:
`PREIMPLEMENTATION_FREEZE_RESULT = READY_FOR_IMPLEMENTATION`
`FORENSIC_STATUS = VERIFIED_IMPLEMENTATION_BASELINE`
Otherwise return `RUNBOOK_FACTORY_RESULT = BLOCKED_BASELINE` and STOP.

## 2. Target runbook

Create:
`04_TOOLING/prompts/implementation/AVF_OPERATOR_RUNBOOK_v1.0.0/`

Target structure:

```text
AVF_OPERATOR_RUNBOOK_v1.0.0/
├── START_HERE.md
├── RUNBOOK_MANIFEST.yaml
├── RUN_STATE_TEMPLATE.yaml
├── MODEL_MATRIX.md
├── OPERATOR_RULES.md
├── WORKSPACE_AND_REPO_MAP.md
├── MASTER_SEQUENCE.md
├── FAILURE_DECISION_TREE.md
├── RESUME_PROJECT.md
├── 00_CHECKPOINTS/
├── 01_REPO_PROVISIONING/
├── 02_R01_CONTRACTS/
├── 03_R02_CORE_STATE/
├── 04_R07_PROVIDER_SDK/
├── 05_R06_WORKFLOW/
├── 06_R15_INTEGRATION_HARNESS/
├── 07_R08_GOOGLE_FLOW_ADAPTER/
├── 08_R10_FLOWKIT_BRIDGE/
├── 09_R09_BROWSER_WORKER/
├── 10_R03_CREATIVE/
├── 11_R04_ASSETS_CONTINUITY/
├── 12_R05_PROMPT_COMPILER/
├── 13_R11_QC/
├── 14_R12_MEDIA/
├── 15_R14_OBSERVABILITY/
├── 16_R13_OPERATOR_CONSOLE/
├── 17_INTEGRATION_GATES/
├── 18_RELEASE/
└── 99_RECOVERY/
```

Use actual frozen dependency gates as authoritative. Numbering may be refined but must provide one unambiguous linear path plus explicitly marked parallel-safe branches.

## 3. Mandatory header for every execution prompt

Every prompt must declare:

```text
PROMPT_ID
PURPOSE
CURRENT_PHASE
RUN_FROM_WORKSPACE
OPEN_REPOSITORY
WORKING_DIRECTORY
MODEL
MODEL_FALLBACK
ANTIGRAVITY_MODE
NEW_OR_EXISTING_CONVERSATION
EXPECTED_DURATION_CLASS
PREREQUISITES
READ_ONLY_INPUTS
WRITEABLE_PATHS
FORBIDDEN_PATHS
COMMAND_TO_RUN
EXPECTED_ARTIFACTS
PASS_CRITERIA
FAIL_CRITERIA
GIT_EXPECTATION
HUMAN_ACTION_AFTER_PASS
HUMAN_ACTION_AFTER_FAIL
NEXT_PROMPT_IF_PASS
NEXT_PROMPT_IF_FAIL
```

Favor `/goal` for bounded implementation/testing/audit/integration/release tasks. The human must be able to copy one exact `/goal ...` command.

## 4. Standard final output contract

Every execution prompt MUST end with:

```yaml
PROMPT_ID:
RESULT: PASS | FAIL | BLOCKED | HUMAN_ACTION_REQUIRED
REPO:
BRANCH:
COMMIT_SHA:
FROZEN_DRIFT: 0 | N
TESTS: {passed: 0, failed: 0}
CONTRACT_TESTS: {passed: 0, failed: 0}
INTEGRATION_TESTS: {passed: 0, failed: 0}
BLOCKERS:
ARTIFACTS_CREATED:
RECOMMENDED_NEXT_PROMPT:
RECOMMENDED_NEXT_TASK:
HUMAN_INSTRUCTION:
```

Repo acceptance prompts also return gate/version/tag/remote/dependency unlock status. Cross-repo gates return gate ID/result, repos/versions, contract matrix, E2E result and next gate. Never finish with vague prose.

## 5. Model routing

Generate `MODEL_MATRIX.md`.

Primary builder: **Gemini 3.7 Flash High** for implementation planning, coding, unit tests, iterative debugging, docs, mechanical Git.

Critical technical reviewer: **Gemini 3.1 Pro High** for at least R01, R02, R06, R07, R08, R09, R10, R15 and any contract/security/reliability dispute.

Cross-family hostile acceptance: **Claude Opus 4.6 Thinking**, NEW conversation, at least for R01 acceptance, foundation gate, R06 durability acceptance, R08/R09/R10 Flow boundary acceptance, and final full-system release audit.

If exact model unavailable, record fallback. Never claim cross-family review occurred when it did not.

## 6. Polyrepo isolation

Assume polyrepo. One coding task owns one repo. Every repo prompt must state exact repo name/local path, OWNS/DOES NOT OWN, frozen blueprint, contracts, dependencies, forbidden dependencies, required upstream versions and downstream gates unlocked.

Cross-repo changes require owner repo change first, released upstream artifact, then separate consumer upgrade. Never allow downstream agent to quick-fix upstream source.

## 7. GitHub/source control section

Generate a provisioning sequence that first inspects then, only under explicit human-authorized prompt, creates or configures GitHub repos. Use repo-registry-derived names; recommended names if compatible:
`avf-spec-governance`, `avf-contracts`, `avf-core-state`, `avf-creative`, `avf-assets-continuity`, `avf-prompt-compiler`, `avf-workflow`, `avf-provider-sdk`, `avf-google-flow-adapter`, `avf-browser-worker`, `avf-flowkit-bridge`, `avf-qc`, `avf-media`, `avf-operator-console`, `avf-observability`, `avf-integration-harness`.

Git policy: releasable `main`, short-lived branches, PR, required CI, no force push, tags/releases, checkpoint before migrations.

## 8. Implementation order

Derive actual order from frozen `dependency-gates.yaml` and build order, not numeric repo IDs. Conceptual critical path:
preflight → Git/GitHub → env doctor → R01 → R02 + R07/FakeProvider → foundation gate → R06 → R15 → FakeProvider E2E → R08 → R10/R09 → FlowExecutionPort conformance → creative/assets/prompt → QC/media → observability/operator → full E2E → controlled live Flow → release.

Mark each step `SEQUENTIAL_REQUIRED` or `PARALLEL_SAFE_AFTER_GATE_X`.

## 9. Five-prompt pattern per repo

For each R01–R15 generate:
- `<repo>_01_PLAN.md`: plan/test plan only, no production code; cover all 16 blueprint sections and DONE WHEN.
- `<repo>_02_IMPLEMENT.md`: implement approved scope with tests; commit; no frozen/upstream edits.
- `<repo>_03_TEST_AND_REVIEW.md`: independent negative/contract/dependency/security/observability review; use Pro High for critical repos.
- `<repo>_04_ACCEPT_RELEASE.md`: CI/PR/release/tag/publish when authorized; unlock downstream gate.
- `<repo>_RECOVERY.md`: classify IMPLEMENTATION_BUG / CONTRACT_DEFECT / FROZEN_SPEC_DEFECT / ENVIRONMENT / DEPENDENCY / EXTERNAL_PROVIDER and route to exact recovery prompt.

## 10. R01 hardening

R01 prompts must read `05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md` and validate remaining applicable advisories. If normative semantics need change, open Change Request and stop affected implementation; do not edit frozen v1.0.0.

## 11. Test orchestration

Across runbook include lint/type, unit, positive/negative schemas, contract/conformance, component, FakeVideoProvider integration, Temporal replay/recovery, retry/idempotency, dependency DAG, security, observability/redaction, R15 E2E, controlled live provider, release smoke tests. TODO/skipped critical tests/mock-only assertions cannot count as PASS.

## 12. Runtime state

Create `RUN_STATE_TEMPLATE.yaml` tracking baseline version/hash, phase/current/last passed prompt, repo R01–R15 state/version/commit/gate, system gates, CRs and blockers. Runtime state later lives outside the frozen prompt pack.

## 13. Recovery tree

Create recovery prompts for:
- blocked dependency
- contract break
- frozen spec defect/change request
- failed test gate
- failed integration gate
- stalled agent
- Git recovery
- environment failure
- external provider blocker

Provider security challenge/CAPTCHA must route to HUMAN_REQUIRED/BLOCKED_PROVIDER; no bypass.

## 14. START_HERE quality

First screen must tell human current state, app/workspace, model, exact first prompt path, exact `/goal`, expected PASS, failure action, resume procedure, repo safety and frozen-file rule.

Golden rule:
> Do not choose the next step yourself. Run only `RECOMMENDED_NEXT_PROMPT` after PASS or the specified recovery prompt after FAIL/BLOCKED.

## 15. Resume prompt

Create a read-only `RESUME_PROJECT.md` that reads runtime state, validates Git/repos/frozen drift and returns exact next workspace/repo/model/command without code changes.

## 16. Self-contained prompts

Every execution prompt must work in a NEW conversation and resolve context from repo/frozen baseline/runtime state. Never depend on previous chat memory.

## 17. Manifest

Create `RUNBOOK_MANIFEST.yaml` for every prompt with id/path/phase/repo/purpose/model/mode/prerequisites/pass_next/fail_next/parallel_group/writes_to/forbidden_writes.

Validate unique IDs, all next links exist, no accidental cycles, R01–R15 covered, all gates covered and final path terminates in release/maintenance.

## 18. Validators

Create and run non-destructive:
- `validate_manifest.py`
- `validate_prompt_headers.py`
- `validate_next_links.py`
- `validate_repo_coverage.py`
- `validate_model_matrix.py`
- `validate_frozen_path_guards.py`

Require 15/15 repos, 5 prompts each, zero dangling next links, zero frozen writes, model/path/mode in every implementation prompt, output contract everywhere, reviewer at critical gates and new-conversation safety.

## 19. Internal isolated review

Use real isolated subagents to review actual generated files: Build/Dependency, QA/Test, DX/Human Operator, Security/Boundary. Fix runbook defects only. Frozen architecture wins conflicts.

## 20. Final output

Return only:

```yaml
RUNBOOK_FACTORY_RESULT: READY_FOR_EXTERNAL_RUNBOOK_AUDIT | BLOCKED
RUNBOOK_PATH:
TOTAL_PROMPTS:
TOTAL_REPOS_COVERED:
TOTAL_GATES:
RECOVERY_PROMPTS:
MANIFEST_VALID:
NEXT_LINKS_VALID:
MODEL_ROUTING_VALID:
FROZEN_GUARDS_VALID:
NEW_CONVERSATION_SELF_CONTAINMENT_VALID:
IMPLEMENTATION_CODE_CREATED: 0
FROZEN_DRIFT: 0
FIRST_OPERATOR_PROMPT:
FIRST_MODEL:
FIRST_WORKSPACE:
FIRST_COMMAND:
NEXT_REQUIRED_ACTION: EXTERNAL_RUNBOOK_AUDIT | FIX_RUNBOOK_FACTORY_BLOCKERS
```

STOP. Do not begin R01 implementation.
