# Specification Freeze Checklist

## Architecture

- [ ] Canonical state owner approved.
- [ ] Repository boundaries approved.
- [ ] Forbidden dependencies approved.
- [ ] Google Flow dual-track boundary approved.
- [ ] Durable workflow ownership approved.

## Contracts

- [ ] Domain IDs/version semantics frozen.
- [ ] Provider request/result schemas frozen.
- [ ] FlowExecutionPort methods frozen.
- [ ] Error taxonomy frozen.
- [ ] Event envelope frozen.
- [ ] Correlation IDs frozen.
- [ ] Idempotency rules frozen.

## Reliability

- [ ] GenerationJob state machine frozen.
- [ ] Technical/provider/creative retry taxonomy frozen.
- [ ] Uncertain-submit reconciliation behavior frozen.
- [ ] Human escalation states frozen.

## Security

- [ ] Secret/browser profile boundary approved.
- [ ] No security-challenge bypass requirement exists.
- [ ] FlowKit trust boundary approved.
- [ ] Log/screenshot redaction policy approved.

## Implementation readiness

- [ ] Every repo has purpose/non-goals/interfaces/dependencies/tests/DONE WHEN.
- [ ] FakeProvider is specified before live provider implementation.
- [ ] Integration release manifest format approved.
- [ ] Phase 0 measurement protocol approved.
- [ ] Reviewer blocking comments resolved.

When all boxes are complete, create `v1.0.0-rc1`; after contract defect fixes only, tag `v1.0.0`.
