# R04 — avf-assets-continuity Blueprint

**Repository type:** Bounded service/worker  
**Execution Type:** Deterministic-first hybrid ranking  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Manage asset metadata, checksums, rights/provenance, character/style versions, reference sets, and asset resolution for a shot.

## RESPONSIBILITY / OWNS

- Asset metadata
- content checksum/dedup policy
- CharacterVersion
- StyleVersion
- ReferenceSet
- asset resolution policy
- usage history

## DOES NOT OWN / NON-GOALS

- object storage infrastructure credentials outside its adapter
- provider upload execution
- prompt final syntax
- generation workflow

## INPUTS

- uploaded/imported asset metadata
- ShotVersion requirements
- character/style versions

## OUTPUTS

- Asset refs
- ResolvedAssetSet
- continuity constraints
- rights validation result

## PUBLIC API / CONTRACT

- IngestAssetMetadata
- CreateCharacterVersion
- CreateStyleVersion
- CreateReferenceSet
- ResolveAssetsForShot
- RecordAssetUsage

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Canonical asset/continuity state committed through core ownership boundary or service-owned tables if freeze chooses separate ownership; no shared-table access. Recommended: service API + core stores immutable refs.

## DEPENDENCIES

- avf-contracts
- object storage adapter
- avf-core-state command API

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- checksum mismatch
- missing rights metadata
- missing reference
- unsupported media
- ambiguous resolution

## RETRY STRATEGY

Technical storage retry only; unresolved asset becomes explicit BLOCKED_ASSET/HUMAN_REQUIRED.

## IDEMPOTENCY

Content hash + source scope; request id for ingest.

## OBSERVABILITY

- ingest failures
- dedup ratio
- resolve hit/miss
- rights-block count

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- hash/dedup tests
- rights rules
- resolver deterministic filters
- fake embedding/ranker contract
- missing asset failure tests

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Metadata + checksum + CharacterVersion/StyleVersion + manual ReferenceSet.

## PRODUCTION VERSION

Embeddings/vision ranking and richer continuity scoring after evidence.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Historical generated Take can trace exact asset versions
- duplicate ingest is safe
- resolver returns typed result or explicit unresolved reason
- no browser/provider-specific upload logic exists here

## HANDOFF ARTIFACTS

Implementation repo must contain:

```text
README.md
ARCHITECTURE.md
COMPATIBILITY.yaml
CHANGELOG.md
src/ or app/
tests/unit/
tests/contract/
tests/integration/
tests/failure/
docs/runbook.md
```

Where applicable it must also contain migrations, container definition, health/readiness endpoint, and generated API docs.
