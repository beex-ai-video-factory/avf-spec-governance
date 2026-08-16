# AI Video Factory Frozen Spec v1.0.0 — Independent Technical Review

## Scope
Reviewed:
- uploaded `AVF_FINAL_FREEZE_v1.0.0.zip`
- its `FINAL_FREEZE/` certification artifacts
- the complete `FROZEN_SPEC_CANDIDATE/`
- the original `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0.zip` for byte/hash comparison

This is an implementation-readiness review, not a re-run of Council voting.

## Verdict

**FINAL VERDICT: NOT READY TO IMPLEMENT AS A FROZEN v1.0.0 BASELINE**

The architecture is a strong review candidate, but the frozen release package contains internal integrity errors, contract/model contradictions, and certification claims that are not present in the normative frozen spec.

Suggested status:

`v1.0.0-freeze-candidate-invalid -> remediation required -> re-audit -> re-freeze`

### Quality profile

| Area | Assessment |
|---|---|
| High-level modular architecture | Strong |
| Canonical-state/provider/browser separation | Strong |
| Failure/recovery philosophy | Strong |
| Contract implementation readiness | Weak/Incomplete |
| Frozen-package integrity | Failed |
| Cross-document consistency | Failed |
| Coding-agent handoff readiness | Partial |
| Final certification trustworthiness | Failed pending remediation |

---

# BLOCKERS

## B01 — Frozen candidate is still internally identified as v0.9.0 review candidate

Inside `FROZEN_SPEC_CANDIDATE/`:

- `VERSION` still contains `0.9.0-review-candidate`.
- `README.md` still says `Specification candidate: v0.9.0-review-candidate`.
- `KIT_MANIFEST.yaml` still says `version: 0.9.0-review-candidate` with intended freeze version 1.0.0.

This directly contradicts the outer Freeze Certificate claiming the candidate itself is frozen v1.0.0.

**Impact:** release identity is ambiguous; coding agents and automation cannot reliably determine whether they are consuming the frozen contract set.

---

## B02 — Internal KIT_MANIFEST hashes are stale

`KIT_MANIFEST.yaml` has 58 file entries.

Recomputed hashes show exactly 4 mismatches:

1. `02_contracts/domain-entities.schema.json`
2. `02_contracts/event-envelope.schema.json`
3. `02_contracts/provider-request.schema.json`
4. `02_contracts/provider-result.schema.json`

These are exactly the contract files changed by the freeze synthesis.

**Impact:** the frozen kit's own integrity manifest does not describe the frozen kit.

---

## B03 — Claimed 15 Change Proposals are not integrated into the normative spec

A byte-level comparison against the original Blueprint v0.9.0 shows:

- original normative files compared: 60
- byte-identical in frozen candidate: 56
- changed: 4

Only these changed:

- `domain-entities.schema.json`
- `event-envelope.schema.json`
- `provider-request.schema.json`
- `provider-result.schema.json`

All repo blueprints, master architecture docs, ADRs, security model, state-machine docs, test strategy, build packets, Flow Track A/B specs, etc. are byte-identical to v0.9.0.

Yet the certificate claims CP-001 through CP-015 introduced/certified broad behavior such as:

- RFC 8785 JCS
- lease fencing
- 3-layer prompt AST
- SecretEnclave
- MV3 keepalive supervisor
- hexagonal FlowExecutionPort
- two-phase credit settlement
- DLQ replay
- and more

Many of these terms/controls do not exist in the frozen normative candidate.

**Impact:** the frozen spec is not the semantic result that the certification artifacts claim was voted and accepted.

---

## B04 — Canonical data schema contradicts the Master Data Model

Examples:

### ShotVersion / PromptVersion provenance direction

Master Data Model says:

`ShotVersion -> PromptVersion -> GenerationJob`

and requires PromptVersion provenance to include `shot_version_id`.

Frozen schema instead:

- `ShotVersion` requires `prompt_version_id`
- `PromptVersion` references `shot_id`, not `shot_version_id`

This reverses/muddles the immutable provenance direction.

### GenerationJob missing required provenance

Master Data Model requires GenerationJob fields including:

- `shot_id`
- `shot_version_id`
- `prompt_version_id`
- provider capability/profile version
- attempt number
- provider job id
- Flow execution track
- browser session id
- requested/submitted/completed timestamps
- normalized error

Frozen `GenerationJob` schema contains only:

- job_id
- shot_version_id
- provider_id
- idempotency_key
- status
- cost fields
- lease fields
- entity version
- attempt index

Critically, it does **not** contain `prompt_version_id`.

**Impact:** exact generation provenance cannot be guaranteed by the frozen canonical schema.

---

## B05 — GenerationJob state machine and frozen schema are incompatible

`STATUS_STATE_MACHINES.md` defines GenerationJob states including:

CREATED, WAITING_FOR_ASSETS, READY, SUBMITTING, SUBMITTED,
GENERATING, DOWNLOADING, DOWNLOADED, QC_PENDING, QC_RUNNING,
APPROVED, plus multiple blocked/failure states.

Frozen `domain-entities.schema.json` allows only:

QUEUED, RESERVED, RUNNING, COMPLETED, FAILED, RECONCILED.

These two normative sources cannot both be implemented.

**Impact:** R02 Core State, R06 Workflow, operator UI, event handling and migrations would need to invent which model is authoritative.

---

## B06 — FlowExecutionPort is not frozen enough for independent Track A / Track B implementation

`browser-command.schema.json` freezes the 10 operation names, but:

- `params` is an unrestricted object (`additionalProperties: true`);
- there is no corresponding normative `FlowExecutionResult` JSON schema;
- command-specific parameter/result semantics are not frozen;
- error/result payload semantics are not frozen per operation.

Yet R09 and R10 are required to independently conform to the same FlowExecutionPort.

**Impact:** two coding agents can build two mutually incompatible implementations while each believes it follows the spec.

This defeats one of the architecture's most important protected capabilities: Track A / Track B replaceability.

---

## B07 — Event envelope documentation and JSON Schema conflict

`CONTRACTS_OVERVIEW.md` documents a common envelope with fields such as:

- `message_id`
- `occurred_at`
- `trace_id`
- `workflow_run_id`
- `project_id`
- `type`

`event-envelope.schema.json` instead requires:

- `event_id`
- `event_type`
- `aggregate_id`
- `aggregate_version`
- `timestamp_utc`
- `correlation_id`
- `schema_version`
- `payload`

Additionally, the schema requires `event_type` to match a lowercase three-part dotted pattern, while `COMMAND_EVENT_CATALOG.md` names events such as:

- `ProjectCreated`
- `GenerationJobCreated`
- `TakeRegistered`
- `QCCompleted`

Those names do not satisfy the frozen regex.

**Impact:** producer/consumer contract tests cannot be written consistently.

---

## B08 — Provider result contract cannot represent the required provider lifecycle/error model

`provider-result.schema.json` status only allows:

- SUCCESS
- FAILED
- RETRYABLE_ERROR

This is insufficient for `get_status` semantics and for the lifecycle implied by the workflow/provider design.

Its error category enum is only:

- TRANSIENT
- PERMANENT
- POLICY
- RESOURCE

while `CONTRACTS_OVERVIEW.md` defines normalized classes including:

- PROVIDER_RATE_LIMIT
- AUTH_REQUIRED
- SECURITY_CHALLENGE
- UI_CHANGED
- BUDGET_EXHAUSTED
- UNSUPPORTED_CAPABILITY
- etc.

The overview also says retry logic keys off the normalized error class.

**Impact:** retry/reconciliation policy cannot consume a single unambiguous frozen error contract.

---

## B09 — Final implementation handoff contains unsupported specifications

Examples:

`FINAL_IMPLEMENTATION_HANDOFF_INDEX.md` claims:

- R07: SecretEnclave tests
- R09: MV3 keepalive & CDP worker tests
- R10: FlowKit gRPC Port
- R13: WebSocket event protocol

The corresponding frozen repo blueprints do not define several of those items.

In particular:

- no `SecretEnclave` appears in the frozen spec;
- R10 does not freeze a gRPC port;
- no MV3 offscreen/keepalive supervisor is specified;
- R13 does not freeze a WebSocket event protocol.

**Impact:** the handoff index introduces architecture that is not part of the normative repo specification.

---

## B10 — Final repository dependency graph is incomplete/inconsistent

Examples:

- R15 blueprint says it depends on **all component artifacts**, but the final DAG shows only limited edges.
- Master architecture sends Track A and Track B telemetry to Observability, but the final dependency graph only shows R02/R06 -> R14.
- Workflow blueprint references creative/assets/prompt/qc/media activity interfaces, while the final DAG does not fully represent those dependencies.

**Impact:** the final file called a “Dependency Graph” cannot safely be used as the dependency authority by implementation agents.

---

## B11 — Freeze package hash generation is not self-consistent

`build_final_freeze.py` computes `freeze_pkg_hash` **before** writing the final:

- `FILE_HASHES.json`
- `FINAL_SPEC_MANIFEST.md`

Therefore the recorded package hash cannot be a canonical hash of the eventual final directory.

A recomputation of the uploaded final package does not match the recorded `final_freeze_package_tree_sha256`.

**Impact:** final package-level integrity certification is invalid even though individual artifact hashes are present.

---

## B12 — Certification “signatures” are generated assertions, not independent attestations

`build_final_freeze.py` writes the entire Freeze Certificate as a hard-coded string, including statements such as:

- `R01 ... SIGNED`
- `R02 ... SIGNED`
- ...
- `AUDITOR-C ... SIGNED`

The builder does not verify or import a cryptographic/immutable signature record from those roles when generating the certificate.

This does not prove the upstream votes did not occur; it means the **final certificate itself is not evidence of those signatures**.

**Impact:** certification cannot be independently trusted from the Frozen package alone.

---

# MAJOR TECHNICAL ISSUES

## M01 — ShotVersion lost important creative intent fields

The original contract and Master Data Model call for immutable ShotVersion semantics such as:

- duration
- action
- camera
- environment
- character/style refs
- asset refs
- hard/soft constraints
- continuity refs

The frozen expanded ShotVersion schema lacks much of this and instead introduces `prompt_version_id`.

That is a regression in the primary creative-intent boundary.

## M02 — AssetVersion provenance is incomplete

Master Data Model requires source, rights/license/provenance and object metadata.

Frozen AssetVersion contains storage URI, checksum, size, pHash and MIME type, but does not freeze the required rights/source/provenance model.

## M03 — Implementation-specific technology choices leaked into canonical entities

Examples:

- `CharacterVersion.face_embedding_hash` required
- `StyleVersion.lora_weights_uri`

These are narrower implementation choices than the Master Blueprint requires.

Requiring them in canonical contracts may over-couple the domain to specific continuity/model techniques.

## M04 — UUID schema is weak

The shared UUID def uses:

`^[0-9a-fA-F-]{36}$`

which accepts many non-UUID 36-character strings.

Use JSON Schema `format: uuid` and/or a stricter canonical UUID pattern if format validation is required.

## M05 — Domain schema is only a `$defs` container

The root schema validates an arbitrary object and does not define a root entity union/discriminator.

This can be acceptable as a schema package, but the contract docs need to state clearly that consumers reference fragments such as:

`domain-entities.schema.json#/$defs/GenerationJob`

Otherwise generated-model tooling and contract-test entrypoints are ambiguous.

---

# WHAT IS GOOD

The underlying architecture remains strong in several areas:

1. Canonical PostgreSQL state is separated from browser/FlowKit/workflow memory.
2. Provider-neutral architecture is preserved conceptually.
3. Google Flow remains an adapter rather than the core.
4. Track A / Track B strategy is structurally sound.
5. Durable workflow and reconciliation-before-resubmit are good design choices.
6. Human/security challenge behavior is correctly non-bypass.
7. Repo blueprints consistently state OWNS / DOES NOT OWN / retry / idempotency / observability / tests.
8. FakeProvider-first and integration-harness-first implementation order is excellent.
9. The original 15-repo decomposition is practical and agent-friendly.

This means the project does **not** need an architectural restart.

It needs a **freeze synthesis repair**.

---

# RECOMMENDED STATUS

Do not discard the Council work.

Do not start 15-repo implementation against this package yet.

Recommended state:

`ARCHITECTURE_APPROVED_IN_PRINCIPLE`

but:

`FROZEN_SPEC_v1.0.0 = INVALID / REMEDIATION_REQUIRED`

The remediation should:

1. reopen C04/C05/C06/C07 as required;
2. integrate every accepted Change Proposal into actual normative files;
3. eliminate contract/data-model/state-machine contradictions;
4. fully freeze FlowExecutionPort request + result semantics;
5. reconcile provider status/error contracts;
6. update README/VERSION/KIT_MANIFEST to 1.0.0;
7. regenerate all internal hashes after final content exists;
8. ensure final certificate is derived from real immutable vote/audit records;
9. run cross-family forensic audit;
10. re-freeze only after the rebuilt package is internally self-consistent.

---

# FINAL SCORE

As a high-level architecture candidate: **8/10**

As a frozen implementation baseline for independent coding agents: **4/10**

Overall recommendation:

**DO NOT START IMPLEMENTATION YET. REPAIR THE FREEZE PACKAGE, THEN RE-AUDIT.**
