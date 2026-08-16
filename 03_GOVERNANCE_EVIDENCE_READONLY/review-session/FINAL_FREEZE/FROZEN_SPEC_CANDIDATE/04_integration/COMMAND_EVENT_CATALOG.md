# Command and Event Catalog

## Rule

Commands are requests to do something. Events are facts that already happened. State is the current canonical projection.

## Core commands

| Command | Owner | Idempotent key |
|---|---|---|
| CreateProject | Core | command_id |
| CreateShotVersion | Core | command_id |
| RegisterPromptVersion | Core | input_hash or command_id |
| StartShotGeneration | Workflow | workflow business key |
| SubmitGeneration | Provider | generation idempotency key |
| RegisterTake | Core | generation_job_id + output checksum |
| EvaluateTake | QC | take checksum + evaluator profile |
| ApproveTake | Core | command_id |
| RegenerateShot | Workflow | command_id / new attempt |
| PauseProject | Workflow/Core | command_id |
| ResumeProject | Workflow/Core | command_id |

## Domain events

- ProjectCreated
- ShotVersionCreated
- PromptCompiled
- GenerationJobCreated
- GenerationSubmissionAcknowledged
- GenerationStarted
- GenerationCompleted
- TakeRegistered
- QCCompleted
- TakeApproved
- TakeRejected
- GenerationBlocked
- HumanReviewRequested
- WorkflowResumed
- AssetIngested
- AssetUsageRecorded

## Event delivery semantics

MVP/V1 does not require Kafka. Recommended delivery:

- Core transaction writes canonical state + outbox row atomically.
- Dispatcher publishes/forwards events to interested local/service consumers.
- Consumers are idempotent by message_id.
- Event log is useful for integration/audit but does not replace canonical relational state.

## External observation events

Browser/session events are operational, not domain facts unless translated:

```text
ExtensionDisconnected -> operational telemetry
AuthExpired -> normalized GenerationBlocked(AUTH_REQUIRED)
FlowUIUnknown -> normalized GenerationBlocked(UI_CHANGED)
```
