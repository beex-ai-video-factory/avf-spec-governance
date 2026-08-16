# Global Definition of Done

A repository is not done because it compiles. It is done when:

- scope and non-goals match its blueprint;
- public contract is versioned;
- unit tests pass;
- contract tests pass;
- integration tests against fakes pass;
- failure tests required by the blueprint pass;
- structured logs contain required correlation IDs;
- all external side effects are idempotent or explicitly documented as non-idempotent;
- secrets are not committed;
- no private database of another repo is accessed;
- API errors map to shared error taxonomy;
- `README` includes local run and health-check instructions;
- compatibility matrix is updated;
- agent-generated implementation contains no new architecture decisions without ADR approval.
