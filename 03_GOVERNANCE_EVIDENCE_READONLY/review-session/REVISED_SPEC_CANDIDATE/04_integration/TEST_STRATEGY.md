# System Test Strategy

## Test pyramid adapted for distributed AI/video workflow

### 1. Unit

Pure domain/state transitions, retry policy, hashing, compilers, parsers, media utilities.

### 2. Contract

Mandatory between every independent repository. Highest priority for agent-built components.

Contract suites include:

- avf-contracts schema fixtures;
- Provider conformance;
- FlowExecutionPort conformance;
- Core command/query contract;
- QC evaluator contract;
- Media result contract.

### 3. Integration

Real Postgres/Temporal/object storage with fakes for expensive/external providers.

### 4. Deterministic E2E

FakeVideoProvider drives complete Shot -> Take -> QC -> approval pipeline.

### 5. Failure/chaos

Required scenarios:

1. kill workflow worker before submit;
2. kill after submit returned but before canonical ack persisted;
3. uncertain submit outcome;
4. duplicate command delivery;
5. provider timeout;
6. browser disconnect mid-wait;
7. MV3 extension restart;
8. browser crash during upload;
9. download interrupted;
10. Core DB temporarily unavailable;
11. QC unavailable;
12. invalid LLM structured output;
13. missing asset/reference;
14. budget exhausted;
15. auth expired/security challenge;
16. Flow UI changed/unknown state.

### 6. Live Google Flow smoke

Small controlled suite, manually/scheduled. Never used as the sole CI proof. Results are classified by exact version of browser/extension/FlowKit adapter and observed Flow UI state.

## FakeProvider requirement

At least 80% of workflow/system behavior must be developable/testable without live video-generation credits.

Fake scenarios:

```text
success(delay=0)
success(delay=30s)
fail_transient(times=2)
fail_provider
rate_limit(retry_after)
timeout
accepted_then_status_unknown
complete_with_corrupt_output
```

## Golden fixtures

Maintain versioned golden fixtures for:

- ShotVersion -> PromptVersion;
- browser observation -> normalized provider state;
- Take + QC profile -> technical QC result;
- FlowKit raw result -> FlowExecutionResult.
