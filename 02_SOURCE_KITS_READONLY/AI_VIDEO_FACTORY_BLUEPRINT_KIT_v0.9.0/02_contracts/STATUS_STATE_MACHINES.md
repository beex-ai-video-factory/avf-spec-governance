# Canonical State Machines

## GenerationJob

```text
CREATED
  -> WAITING_FOR_ASSETS
  -> READY
  -> SUBMITTING
  -> SUBMITTED
  -> GENERATING
  -> DOWNLOADING
  -> DOWNLOADED
  -> QC_PENDING
  -> QC_RUNNING
  -> APPROVED

Recoverable/error states:
FAILED_TRANSIENT
FAILED_PROVIDER
FAILED_QC
BLOCKED_AUTH
BLOCKED_SECURITY
BLOCKED_UI_CHANGE
BLOCKED_BUDGET
HUMAN_REVIEW
CANCELLED
```

Transition rules:

- `SUBMITTING -> SUBMITTED` only after provider acknowledgement is recorded.
- On uncertain submit outcome, workflow must reconcile before issuing a new submit.
- `APPROVED` is terminal for a specific GenerationJob, but Shot can have multiple Takes/Jobs.
- `FAILED_QC` may create a new GenerationJob; it does not mutate the completed Take.

## Browser execution command

```text
QUEUED -> LEASED -> RUNNING -> SUCCEEDED
                    |-> FAILED_RETRYABLE
                    |-> FAILED_TERMINAL
                    |-> HUMAN_REQUIRED
                    |-> CANCELLED
```

## Asset

```text
INGESTING -> ACTIVE -> DEPRECATED -> TOMBSTONED
         \-> FAILED
```
