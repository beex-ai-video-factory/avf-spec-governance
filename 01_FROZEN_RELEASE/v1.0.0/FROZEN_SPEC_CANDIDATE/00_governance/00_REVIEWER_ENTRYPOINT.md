# Reviewer Entry Point

## Review question

The council is asked to decide whether this specification is sufficiently complete and internally consistent to be frozen before implementation.

Reviewers should not ask whether every proposed technology is fashionable. Review in this order:

1. **Correctness:** Are domain rules and ownership unambiguous?
2. **Recoverability:** Can failures resume without corrupting state or duplicating paid generation?
3. **Maintainability:** Can one subsystem be replaced without changing unrelated domains?
4. **Modularity:** Can repositories be built and tested independently?
5. **Testability:** Are contracts and deterministic fakes sufficient to build without live Google Flow?
6. **Observability:** Can every output be traced to inputs, provider, attempt, and QC result?
7. **Replaceability:** Can FlowKit/Google Flow be removed later?
8. **Developer velocity:** Can coding agents receive bounded work packets?
9. **Automation level:** Is automation increased only after correctness is established?
10. **Scale:** Is scale deferred until the pipeline is stable?

## Decisions that MUST be frozen before implementation

- Canonical source of truth and database ownership.
- Core entity identities and version semantics.
- `VideoGenerationProvider` contract.
- `FlowExecutionPort` / browser command contract.
- GenerationJob state machine.
- Idempotency rules.
- Event envelope and correlation identifiers.
- Repository ownership boundaries.
- Track A vs Track B compatibility boundary.
- Security boundary for browser profiles, cookies, tokens, and secrets.

## Decisions that MAY remain implementation-specific

- FastAPI vs equivalent HTTP framework inside a repo.
- SQL ORM choice.
- UI framework for operator console.
- Exact semantic QC model.
- Exact selector strategy inside a Google Flow execution implementation.
- Exact object-storage provider.

## Reviewer output

Use one of:

- `APPROVE_FOR_FREEZE`
- `APPROVE_WITH_BLOCKING_CHANGES`
- `REJECT_ARCHITECTURE`

Every blocking change must identify:

- affected contract/repo;
- why current specification is unsafe or ambiguous;
- proposed replacement;
- migration/compatibility effect;
- whether it changes the critical path.
