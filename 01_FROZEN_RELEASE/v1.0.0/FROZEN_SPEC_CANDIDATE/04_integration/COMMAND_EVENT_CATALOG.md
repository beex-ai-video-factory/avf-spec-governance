# COMMAND & EVENT CATALOG
## AI Video Factory — Event Architecture & Topic Naming
**VERSION:** 1.0.0

---

## 1. Domain Event Catalog

| Domain Entity | TypeScript Event Class | Canonical Event Type (`event_type`) | Description |
|---|---|---|---|
| **Project** | `ProjectCreatedEvent` | `avf.project.created` | New creative project initialized. |
| **Project** | `ProjectUpdatedEvent` | `avf.project.updated` | Project metadata updated. |
| **Shot** | `ShotVersionCreatedEvent` | `avf.shot.version_created` | New creative shot version saved. |
| **Prompt** | `PromptVersionCreatedEvent` | `avf.prompt.version_created` | New compiled prompt version generated. |
| **GenerationJob** | `GenerationJobQueuedEvent` | `avf.generation.job_queued` | Job enqueued for budget reservation. |
| **GenerationJob** | `GenerationJobReservedEvent` | `avf.generation.job_reserved` | Budget reserved; ready for submission. |
| **GenerationJob** | `GenerationJobSubmittedEvent` | `avf.generation.job_submitted` | Prompt submitted to remote video engine. |
| **GenerationJob** | `GenerationJobProgressEvent` | `avf.generation.job_progress` | Generation progress update received. |
| **GenerationJob** | `GenerationJobCompletedEvent` | `avf.generation.job_completed` | Render completed and Take registered. |
| **GenerationJob** | `GenerationJobFailedEvent` | `avf.generation.job_failed` | Job failed with normalized error. |
| **GenerationJob** | `GenerationJobCancelledEvent` | `avf.generation.job_cancelled` | Job cancelled by operator or user. |
| **GenerationJob** | `GenerationJobReconciledEvent` | `avf.generation.job_reconciled` | Job reconciled after lease crash. |
| **Take** | `TakeRegisteredEvent` | `avf.take.registered` | New take media file registered. |
| **QC** | `QCCompletedEvent` | `avf.qc.completed` | Automated QC evaluation completed. |
| **Media** | `MediaRenderQuarantinedEvent` | `avf.media.quarantined` | Media file quarantined in DLQ. |
