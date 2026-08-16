# R12 — avf-media Blueprint

**Repository type:** Media/postproduction worker  
**Execution Type:** Deterministic  
**Specification status:** Candidate for v1.0 freeze

## PURPOSE

Ingest downloaded provider outputs, verify checksums/metadata, normalize media, assemble approved Takes, and produce final export assets.

## RESPONSIBILITY / OWNS

- media probe/normalization
- object-storage upload/download adapter
- timeline assembly
- FFmpeg wrappers
- final export manifest
- cleanup/retention operations

## DOES NOT OWN / NON-GOALS

- shot creative decisions
- provider generation
- QC semantic decisions
- canonical project state

## INPUTS

- provider output files/URIs
- approved Take refs
- timeline spec

## OUTPUTS

- AssetVersion metadata
- normalized media
- FinalOutput manifest

## PUBLIC API / CONTRACT

- IngestProviderOutput
- ProbeMedia
- NormalizeTake
- AssembleTimeline
- ExportFinal
- CleanupEphemeral

All exchanged payloads MUST use released `avf-contracts` schemas. Internal implementation types cannot escape the repository boundary.

## PERSISTENT STATE

Binary object storage; metadata/provenance returned for canonical registration.

## DEPENDENCIES

- avf-contracts
- FFmpeg/ffprobe
- object storage

Dependency rule: do not import another repository's private modules or database schema. Depend on released contracts/APIs only.

## FAILURE MODES

- corrupt download
- codec unsupported
- disk full
- FFmpeg failure
- checksum mismatch

## RETRY STRATEGY

Safe deterministic media operations retry with temp-file cleanup; never re-trigger generation.

## IDEMPOTENCY

Content hash + operation spec hash; final export key includes timeline version.

## OBSERVABILITY

- media duration/size
- processing latency
- FFmpeg exit codes
- storage errors
- checksum mismatches

Required correlation context when applicable: `trace_id`, `workflow_run_id`, `project_id`, `shot_id`, `generation_job_id`, `attempt_id`.

## TEST STRATEGY

- fixture videos
- corrupt input
- interrupted write
- re-run idempotency
- timeline golden tests

Minimum test classes: Unit, Contract, Integration, Failure. E2E is required when the repository participates in an externally observable vertical slice.

## SECURITY

- Secrets/tokens/cookies must not appear in fixtures or committed logs.
- Least privilege for external credentials.
- Validate all boundary inputs.
- Do not add security-challenge bypass behavior as an implementation convenience.

## MVP VERSION

Ingest, checksum, probe, store, concatenate approved clips.

## PRODUCTION VERSION

Audio mix, subtitles, color transforms, render profiles, retention manager.

## AGENT IMPLEMENTATION RULES

1. The coding agent receives this blueprint plus exact `avf-contracts` version.
2. The agent may choose internal classes/modules but cannot change public semantics.
3. Any discovered ambiguity is raised as a spec issue; the agent must not silently invent a cross-repo behavior.
4. Implement contract tests before real external integration where possible.
5. No unrelated feature work.

## DONE WHEN

- Every media output has checksum/provenance
- re-run does not create ambiguous duplicates
- failed temp artifacts cleaned
- no generation retry is hidden inside media worker

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
