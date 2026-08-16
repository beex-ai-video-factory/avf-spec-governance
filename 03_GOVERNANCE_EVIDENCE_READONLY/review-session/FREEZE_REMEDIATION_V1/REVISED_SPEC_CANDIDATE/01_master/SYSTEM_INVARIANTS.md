# System Invariants

These rules are normative. An implementation that violates them is non-conformant even if end-to-end output appears correct.

1. A `Take` belongs to exactly one `Shot` and references exactly one `GenerationJob`.
2. A `GenerationJob` references immutable `ShotVersion` and `PromptVersion` identifiers.
3. Every external side effect has an idempotency key or an explicit documented reason it cannot.
4. LLMs and agents may propose state changes but cannot directly mutate canonical project state.
5. Browser/extension/FlowKit state is never canonical business state.
6. Every generated artifact preserves provenance and content checksum.
7. Google Flow-specific fields do not appear in core Shot/Project contracts unless represented as namespaced provider metadata.
8. Provider adapters cannot directly modify Project/Shot records.
9. QC models recommend; deterministic policy decides retry/approval escalation.
10. Technical retries do not create new PromptVersions.
11. Creative retries create a new attempt and create a new PromptVersion when prompt semantics changed.
12. Authentication/security challenges do not trigger automated bypass behavior.
13. A repo cannot read another repo's private database schema directly.
14. Contract consumers must validate schema versions at boundaries.
15. Correlation IDs must propagate across workflow, provider, browser execution, QC, and media processing.
16. A completed `Take` cannot be overwritten; replacement produces another Take/AssetVersion.
17. Deleting source assets cannot silently invalidate historical provenance; deletion is logical/tombstoned according to retention policy.
18. Budget limits are enforced by deterministic policy before external generation requests.
19. A browser worker can crash without losing canonical queue truth.
20. Switching between Track A and Track B does not change upstream generation contracts.
