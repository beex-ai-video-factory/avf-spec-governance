# I02 — Contract Tests First

Before implementation:
1. import/generate models from frozen `avf-contracts`;
2. implement contract/conformance test fixtures;
3. write failing tests for every public interface and relevant invariant;
4. create fake/mocked dependencies at contract boundaries;
5. prove tests fail for missing implementation.

No implementation code may be used to make RED tests pass yet.

Output:
- test inventory;
- traceability from contract clause -> test;
- RED evidence.
