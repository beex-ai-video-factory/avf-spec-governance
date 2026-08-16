# End-to-End Integration Protocol

## Release manifest

The integration repo pins component versions:

```yaml
release: avf-1.0.0-rc1
components:
  avf-contracts: 1.0.0
  avf-core-state: 1.0.0-rc2
  avf-workflow: 1.0.0-rc3
  avf-provider-sdk: 1.0.0
  avf-google-flow-adapter: 1.0.0-rc1
  flow_execution_track: track-a
  avf-browser-worker: 1.0.0-rc1
```

Track B swaps only the execution component:

```yaml
flow_execution_track: track-b
avf-flowkit-bridge: 1.0.0-rc1
```

## Required integration suites

### Suite A — FakeProvider deterministic

- single-shot success;
- provider failure;
- timeout then retry;
- crash after submit acknowledgement;
- crash with uncertain acknowledgement;
- duplicate command delivery;
- budget block;
- QC fail then creative retry.

### Suite B — FlowExecutionPort contract

Run against Track A and Track B separately.

- ensure session;
- attach assets;
- submit prompt;
- observe generating/completed state;
- download result;
- disconnect/reconnect;
- expired auth => normalized `AUTH_REQUIRED`;
- UI/integration incompatibility => normalized `UI_CHANGED`/`UNSUPPORTED_CAPABILITY`.

### Suite C — Live Google Flow smoke

Executed manually/on controlled schedule, not every CI run.

No test may attempt to bypass security challenges. A challenge is a valid test result and must map to an operator-blocked state.

## Promotion rule

A release candidate is promotable only when:

- all contract tests green;
- deterministic E2E green;
- selected Flow execution track passes its contract suite;
- migration compatibility checked;
- risk exceptions documented;
- observability fields verified.
