# API and Contract Compatibility Policy

## Version format

`MAJOR.MINOR` at message/schema level; repository releases use Semantic Versioning.

## Breaking examples

- changing `shot_version_id` from immutable reference to mutable alias;
- changing retry semantics for the same error code;
- making optional field required;
- changing state transition meaning;
- allowing an adapter to own canonical state.

## Non-breaking examples

- optional metadata fields;
- new query endpoint;
- additional diagnostics inside a namespaced object;
- new provider capability code when callers must tolerate unknown capabilities.

## Consumer-driven contract tests

Every consumer publishes fixtures representing what it accepts. The integration harness executes provider + consumer contract suites before a release manifest can be promoted.
