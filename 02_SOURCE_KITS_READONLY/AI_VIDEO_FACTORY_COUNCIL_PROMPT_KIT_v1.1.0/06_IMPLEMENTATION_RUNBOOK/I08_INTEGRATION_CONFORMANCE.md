# I08 — Integration Conformance

Against dependency fakes and/or real compatible versions:

- validate request/result schemas;
- validate error behavior;
- validate version negotiation;
- validate correlation IDs;
- validate idempotency;
- validate observability;
- validate no forbidden dependency leakage.

Use `avf-integration-harness` where applicable.

A repository cannot self-certify integration PASS.
