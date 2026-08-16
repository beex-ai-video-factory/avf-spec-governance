# PRE-IMPLEMENTATION WORKSPACE FREEZE & NORMALIZATION MASTER
## AI Video Factory — Frozen v1.0.0 → Clean Implementation Workspace

Run this as a single `/goal` with Gemini 3.7 Flash High.

You are the Pre-Implementation Workspace Custodian for AI Video Factory.

Your job is NOT to implement product features. Your job is to transform the current review/audit workspace into a clean, reproducible, read-only frozen baseline plus a writable implementation workspace while preserving the full audit chain.

## Non-negotiable outcome

At completion:
1. The verified v1.0.0 implementation baseline is uniquely identified.
2. Frozen artifacts are read-only.
3. Governance/audit evidence remains intact and traceable.
4. Loose/redundant root files are archived or safely deduplicated.
5. The workspace has one obvious entrypoint for implementation agents.
6. Antigravity workspace Rules, Skills, Hooks, and permission guidance are installed.
7. A reproducible local development bootstrap exists.
8. The 15 implementation repos are registered but NOT implemented.
9. Future agents cannot silently edit the frozen baseline.
10. Spec defects found during implementation become Errata / Change Requests.
11. Final state is mechanically verifiable.

Do not start implementation.

---

## 1. Authoritative baseline

Discover current files; do not trust filenames from memory.

Expected canonical concepts:
- `review-session/FINAL_FREEZE_V1_REMEDIATED/`
- final `AVF_FINAL_FREEZE_v1.0.0_REMEDIATED.zip`
- detached `.zip.sha256` sidecar
- latest `FINAL_REMEDIATED_FORENSIC_AUDIT/`
- final verdict `FORENSIC_RESULT = VERIFIED_IMPLEMENTATION_BASELINE`

Before reorganizing:
- verify final ZIP against detached sidecar;
- verify internal content hashes/tree hash;
- verify VERSION = 1.0.0;
- verify latest external forensic result;
- record hashes.

If any fail:
`PREIMPLEMENTATION_FREEZE_RESULT = BLOCKED_BASELINE_INTEGRITY`
STOP.

---

## 2. No blind deletion

Default obsolete-file action = ARCHIVE, not delete.

Hard-delete only:
- caches;
- `.DS_Store`;
- zero-byte accidental files with no evidentiary value;
- exact duplicates whose SHA-256 matches a preserved canonical copy;
- explicitly disposable scratch output.

Never hard-delete source kits, freeze packages, audits, raw ballots, raw subagent outputs, remediation history, Change Proposals, contract tests, manifests, hashes, or unique evidence.

Create before cleanup:
- `00_PROJECT_ADMIN/CLEANUP_PLAN.md`
- `00_PROJECT_ADMIN/PRE_CLEANUP_FILE_INVENTORY.csv`

Create after:
- `00_PROJECT_ADMIN/POST_CLEANUP_FILE_INVENTORY.csv`

For every move/delete record source, SHA-256, size, classification, action, destination, reason.

---

## 3. Target structure

Normalize toward:

```text
AVF_SPEC_REVIEW/
├── PROJECT.md
├── BASELINE.lock.json
├── .gitignore
├── .editorconfig
├── .agents/
│   ├── rules/
│   ├── skills/
│   ├── hooks.json
│   └── scripts/
├── 00_PROJECT_ADMIN/
├── 01_FROZEN_RELEASE/
│   ├── v1.0.0/
│   └── distributable/
├── 02_SOURCE_KITS_READONLY/
├── 03_GOVERNANCE_EVIDENCE_READONLY/
│   ├── review-session/
│   ├── final-forensic-audits/
│   └── external-technical-review/
├── 04_TOOLING/
│   ├── prompts/historical/
│   ├── prompts/implementation/
│   ├── validation/
│   ├── bootstrap/
│   └── docs/
├── 05_IMPLEMENTATION/
│   ├── README.md
│   ├── IMPLEMENTATION_BASELINE.md
│   ├── repo-registry.yaml
│   ├── dependency-gates.yaml
│   ├── decisions/
│   ├── change-requests/
│   ├── environment/
│   ├── integration/
│   └── repos/
│       ├── R01_contracts/
│       ├── R02_core_state/
│       ├── R03_creative/
│       ├── R04_assets_continuity/
│       ├── R05_prompt_compiler/
│       ├── R06_workflow/
│       ├── R07_provider_sdk/
│       ├── R08_google_flow_adapter/
│       ├── R09_browser_worker/
│       ├── R10_flowkit_bridge/
│       ├── R11_qc/
│       ├── R12_media/
│       ├── R13_operator_console/
│       ├── R14_platform_observability/
│       └── R15_integration_harness/
├── 90_ARCHIVE_READONLY/
└── 99_TEMP/
```

Preserve historical path compatibility. If moving `review-session/` or source kits would break forensic references, either keep their legacy paths or create compatible symlinks. Do not sacrifice audit traceability for aesthetics.

---

## 4. Root cleanup

Root should contain only entrypoint files, `.agents/`, numbered canonical directories, and compatibility symlinks if required.

Move loose historical prompts such as old autonomous masters, forensic prompts, remediation prompts, targeted patch prompts, and packaging-fix prompts to:
- `04_TOOLING/prompts/historical/` if still useful;
- otherwise `90_ARCHIVE_READONLY/pre-freeze-prompts/`.

Move superseded freeze/audit ZIPs to archive folders. Deduplicate byte-identical copies.

Keep exactly one canonical final release ZIP + detached sidecar under:
`01_FROZEN_RELEASE/distributable/`

Avoid multiple canonical-looking release copies.

---

## 5. Baseline lockfile

Create `BASELINE.lock.json` containing at least:
- project;
- baseline_version = 1.0.0;
- status = VERIFIED_IMPLEMENTATION_BASELINE;
- frozen spec path;
- release archive path;
- detached sidecar path;
- content tree SHA-256;
- final ZIP SHA-256;
- external forensic result;
- G18 status;
- mutable implementation root;
- frozen = true.

Derive hashes; never invent them.

---

## 6. Read-only protection

Protect:
- `01_FROZEN_RELEASE/`
- `02_SOURCE_KITS_READONLY/`
- `03_GOVERNANCE_EVIDENCE_READONLY/`
- `90_ARCHIVE_READONLY/`

On macOS/POSIX use normal read-only permissions such as:
`chmod -R a-w <protected-path>`

Do not use `sudo`.
Do not use `chflags uchg` unless there is a demonstrated need.

Create `00_PROJECT_ADMIN/READONLY_POLICY.md` documenting:
- protected paths;
- commands used;
- explicit human-authorized unlock procedure;
- rule that implementation agents may never unlock them.

---

## 7. Antigravity workspace Rules

Create workspace rules under `.agents/rules/`.

At minimum:

### frozen-baseline-guardian
Always On.
- read frozen v1.0.0; never edit it;
- implementation findings create Change Requests;
- no direct edits to source kits/evidence/archive;
- no modified copies written back into frozen baseline.

### contract-first
Always On or Model Decision.
- R01 contracts precede consumers;
- producer/consumer changes require contract tests;
- typed schemas are normative;
- frozen contract changes require formal CR.

### repo-boundary-enforcer
Always On for `05_IMPLEMENTATION/repos/**`.
- enforce OWNS / DOES NOT OWN;
- enforce final dependency DAG;
- only R02 owns canonical DB persistence;
- Google Flow details cannot leak upstream;
- R09 and R10 do not depend on each other.

### test-gates
Glob on implementation code.
- unit + negative tests;
- contract/conformance tests where applicable;
- integration test before DONE;
- no fake PASS/TODO acceptance.

### change-control
Always On.
Classify ambiguity:
- implementation detail → Implementation Decision Record;
- frozen architecture/contract defect → CR/ERRATA and stop affected work;
- empirical provider unknown → spike/benchmark;
- never silently rewrite spec.

Keep each Rule within Antigravity size limits.

---

## 8. Antigravity workspace Skills

Create project-local skills under `.agents/skills/<skill-name>/SKILL.md`.

Install only project-relevant skills:

1. `avf-baseline-reader`
   - locate authoritative frozen requirement/contract/invariant/repo packet;
   - distinguish normative files from audit history.

2. `avf-contract-first`
   - JSON Schema validation;
   - generated TypeScript types;
   - positive/negative fixtures;
   - producer/consumer conformance;
   - semantic compatibility.

3. `avf-repo-boundaries`
   - extract OWNS / DOES NOT OWN;
   - enforce dependency DAG and forbidden imports.

4. `avf-temporal-durability`
   - workflow determinism;
   - activities;
   - replay safety;
   - retries;
   - idempotency;
   - reconciliation before resubmit.

5. `avf-provider-adapter`
   - provider-neutral core;
   - capability profiles;
   - operation vs generation status;
   - normalized errors;
   - idempotency/cancel/download/retry.

6. `avf-flow-execution-port`
   - frozen 10-operation port;
   - Track A/B equivalence;
   - typed request/result;
   - no DOM/UI semantics upstream;
   - common conformance suite.

7. `avf-browser-worker-safety`
   - DOM → Accessibility → Visual → Agent recovery → Human;
   - persistent session recovery;
   - no CAPTCHA/rate-limit/anti-abuse bypass;
   - challenge → HUMAN_REQUIRED/BLOCKED_PROVIDER.

8. `avf-qc-media`
   - technical QC before expensive semantic QC;
   - bounded retry/DLQ/quarantine;
   - FFmpeg/FFprobe safety;
   - provenance.

9. `avf-observability-security`
   - trace/correlation IDs;
   - secret redaction;
   - no credentials in logs/events;
   - normalized errors and cost/retry metrics.

10. `avf-implementation-done`
   - validate repo handoff;
   - required tests;
   - dependency scan;
   - contract compatibility;
   - DONE WHEN;
   - no architecture invention.

Every SKILL.md needs YAML frontmatter:
`name` and `description`.

Do not install unrelated generic skills.

---

## 9. Antigravity hooks

Create `.agents/hooks.json`.

Required purposes:
1. Pre-tool safety check for attempted write/delete/move against frozen paths.
2. Post-tool lightweight validation for touched implementation repos.
3. Stop gate requiring repo DONE checklist before implementation agents terminate.

Hooks must never:
- modify frozen files;
- auto-approve destructive commands;
- call paid providers;
- bypass security challenges.

If hook matchers cannot reliably enforce path protection, OS read-only remains primary. Document the limitation.

---

## 10. Project permission plan

Create `00_PROJECT_ADMIN/PROJECT_PERMISSION_PLAN.md`.

Desired project-scoped policy:

DENY writes to:
- `01_FROZEN_RELEASE/**`
- `02_SOURCE_KITS_READONLY/**`
- `03_GOVERNANCE_EVIDENCE_READONLY/**`
- `90_ARCHIVE_READONLY/**`

ALLOW writes only to:
- `.agents/**`
- `00_PROJECT_ADMIN/**`
- `04_TOOLING/**`
- `05_IMPLEMENTATION/**`
- `99_TEMP/**`

Deny or Ask:
- sudo;
- rm -rf;
- writes outside project;
- `.ssh`;
- credential stores;
- destructive git actions;
- paid provider submissions during bootstrap.

If project permissions are programmatically available, apply them. Otherwise do not fake success: document exact manual UI/CLI steps. Subagents must inherit the same protection boundary.

---

## 11. Implementation workspace bootstrap

Create writable `05_IMPLEMENTATION/`; do NOT write production code.

Create:

### IMPLEMENTATION_BASELINE.md
- baseline 1.0.0;
- lockfile reference;
- frozen paths;
- final forensic verdict;
- G18;
- no frozen edits;
- CR process.

### repo-registry.yaml
Register R01–R15:
- repo_id;
- name;
- frozen blueprint path;
- primary contracts;
- dependencies;
- forbidden dependencies;
- status = NOT_STARTED;
- gate predecessors;
- expected artifact.

Derive from frozen baseline.

### dependency-gates.yaml
Encode final frozen dependency graph and critical implementation path.

### change-requests/README.md
Template fields:
CR_ID, discovered_by, repo, frozen requirement/contract, evidence, severity, classification, capability delta, implementation blocked?, options, approval status.

### decisions/README.md
Implementation Decision Records are permitted only where frozen architecture is silent. IDRs may not contradict frozen ADRs/contracts/invariants.

---

## 12. Development environment

Inspect frozen spec and derive required stack. Do not invent extra infrastructure.

Create `05_IMPLEMENTATION/environment/`:
- README.md
- `.env.example` with placeholders only
- TOOLCHAIN.lock.md
- bootstrap.sh
- doctor.sh
- docker-compose.dev.yml only for components justified by frozen spec
- SERVICE_PORTS.md
- LOCAL_DATA_POLICY.md

Where frozen architecture requires them, prepare local dev services for:
- PostgreSQL;
- Temporal;
- object storage/local-compatible emulator;
- observability collector;
- FakeVideoProvider/integration harness dependencies.

Do NOT add Kafka, Kubernetes, Redis, vector DB, etc. unless frozen spec requires them.

If exact tool versions are not frozen, choose stable/LTS versions only as Implementation Decisions, record them, and keep them upgradeable.

`doctor.sh` must check:
- OS/architecture;
- runtimes;
- Docker if used;
- ports;
- Postgres;
- Temporal;
- object storage;
- offline FakeProvider readiness;
- frozen baseline verification.

Do not require live Google Flow credentials for R01/R02/R07 FakeProvider bootstrap.

---

## 13. Source control prep

Do not accidentally create a monolithic product repo if the frozen strategy is polyrepo.

Prepare only:
- repo registry;
- shared bootstrap tooling;
- per-repo creation template.

Do not `git init` all 15 repos unless the frozen repo strategy says to do it now.

Create `04_TOOLING/bootstrap/create_repo_from_frozen_packet.sh` as a future skeleton generator only.

Document isolated/new-worktree operation for concurrent agents where supported.

---

## 14. R01 pre-implementation hardening register

Create `05_IMPLEMENTATION/R01_PREIMPLEMENTATION_HARDENING.md`.

Inspect the latest frozen baseline and retain only still-applicable non-blocking forensic advisories, such as:
- execution-stage docs/count alignment;
- raw JSON Schema `$id` / `$defs` / `$ref` validation;
- FlowExecutionResult result typing;
- regenerated TypeScript contract types;
- positive/negative fixtures;
- identical Track A/B port conformance.

If a hardening item requires normative semantic change, open a Change Request. Do not edit frozen v1.0.0.

---

## 15. Automated validators

Create under `04_TOOLING/validation/`:

### verify_frozen_baseline.sh
- final ZIP sidecar;
- VERSION;
- internal package verification;
- protected dirs non-writable.

### verify_workspace_layout.sh
- required structure;
- no duplicate canonical release artifacts;
- no loose historical prompts at root.

### verify_no_frozen_mutation.sh
- protected-tree hash vs baseline lock;
- fail on drift.

### verify_agent_customizations.sh
- Rules exist;
- Skills each have valid SKILL.md + description;
- hooks JSON parses.

### preimplementation_doctor.sh
Run all validators plus environment doctor.

All validators non-destructive.

---

## 16. PROJECT.md

Create root `PROJECT.md` as mandatory first-read entrypoint.

It must clearly state:

```text
AI VIDEO FACTORY

CURRENT PHASE:
IMPLEMENTATION

FROZEN BASELINE:
v1.0.0 — VERIFIED_IMPLEMENTATION_BASELINE

READ-ONLY:
01_FROZEN_RELEASE
02_SOURCE_KITS_READONLY
03_GOVERNANCE_EVIDENCE_READONLY
90_ARCHIVE_READONLY

WRITEABLE:
05_IMPLEMENTATION

RULE:
Never edit frozen baseline.
Spec defects become Change Requests.

IMPLEMENTATION START GATE:
R01 Contracts.
```

Link to:
- BASELINE.lock.json;
- implementation baseline;
- repo registry;
- dependency gates;
- environment bootstrap;
- CR process.

---

## 17. Final hygiene

At end:
- root understandable in <30 seconds;
- no ambiguous FINAL_FINAL loose files;
- no duplicate active release ZIPs;
- no old audit prompt that looks current;
- no temp outside 99_TEMP;
- no secrets;
- no writable frozen artifact.

Create `00_PROJECT_ADMIN/WORKSPACE_MAP.md` documenting before/after, moves, deletions, symlinks, protected and writable paths.

---

## 18. Preimplementation certificate

Create `00_PROJECT_ADMIN/PREIMPLEMENTATION_CERTIFICATE.md`, derived from actual checks:
- baseline;
- forensic status;
- tree hash;
- ZIP hash;
- sidecar verification;
- protected paths;
- writable paths;
- cleanup stats;
- Rules count;
- Skills count;
- Hooks status;
- environment doctor;
- frozen drift;
- secrets scan;
- repo registry 15/15;
- implementation started = NO.

---

## 19. Hard gates

PASS only if:
1. final v1.0.0 verifies;
2. final external forensic verdict is VERIFIED_IMPLEMENTATION_BASELINE;
3. canonical release is unique;
4. governance evidence preserved;
5. protected paths are read-only;
6. root normalized;
7. Rules valid;
8. Skills valid;
9. hooks valid;
10. env bootstrap exists;
11. 15/15 repos registered;
12. no implementation code created;
13. no secrets persisted;
14. no frozen semantic content modified;
15. post-cleanup canonical hashes match.

---

## 20. Final output

Return only:

```yaml
PREIMPLEMENTATION_FREEZE_RESULT: READY_FOR_IMPLEMENTATION | BLOCKED

BASELINE_VERSION:
FORENSIC_STATUS:
RELEASE_ZIP_SHA256:
CONTENT_TREE_SHA256:

ROOT_NORMALIZED: YES | NO
CANONICAL_RELEASE_COPIES: N
FILES_ARCHIVED: N
FILES_DEDUP_DELETED: N
TEMP_FILES_DELETED: N

FROZEN_PATHS_READONLY: YES | NO
FROZEN_DRIFT: 0 | N

RULES_INSTALLED: N
SKILLS_INSTALLED: N
HOOKS_VALID: YES | NO
PROJECT_PERMISSION_STATUS: APPLIED | MANUAL_STEPS_DOCUMENTED | BLOCKED

ENVIRONMENT_BOOTSTRAP: PASS | FAIL
REPOS_REGISTERED: N/15
IMPLEMENTATION_CODE_CREATED: 0

NEXT_REQUIRED_ACTION:
  START_R01_IMPLEMENTATION | FIX_PREIMPLEMENTATION_BLOCKERS
```

STOP.
Do not implement R01.
Do not create production code.
Do not submit paid provider generations.
