# Repository Strategy

## Decision

Use a **polyrepo implementation model with one integration/composition repository**, while keeping the number of deployable services smaller than the number of repositories when useful.

Why:

- coding agents can own bounded repos;
- contract versions make coordination explicit;
- high-risk browser/FlowKit code is physically separated from core;
- teams can replace providers without touching creative/domain repos;
- implementation can still co-deploy multiple workers on one machine to avoid operational microservice overhead.

## Repository classes

### Contract/library repos

- `avf-contracts`
- `avf-provider-sdk`

### Stateful service

- `avf-core-state`

### Stateless/bounded workers or services

- `avf-creative`
- `avf-assets-continuity`
- `avf-prompt-compiler`
- `avf-qc`
- `avf-media`

### Orchestration

- `avf-workflow`

### Provider/execution adapters

- `avf-google-flow-adapter`
- `avf-browser-worker`
- `avf-flowkit-bridge`

### Application/platform

- `avf-operator-console`
- `avf-platform-observability`
- `avf-integration-harness`

## Version dependency rule

Each repo declares exact supported contract major/minor range. Example:

```yaml
contracts:
  avf-contracts: ">=1.0,<2.0"
  provider-sdk: ">=1.0,<2.0"
```

No repository consumes `main` branch of another repo in production.

## Integration repository

`avf-integration-harness` contains:

- Docker Compose;
- pinned component versions;
- contract compatibility checks;
- test fixtures;
- FakeProvider scenarios;
- live-provider test profiles;
- E2E acceptance tests;
- release manifest.

This repository is the place where a collection of independently built components becomes a releasable system.
