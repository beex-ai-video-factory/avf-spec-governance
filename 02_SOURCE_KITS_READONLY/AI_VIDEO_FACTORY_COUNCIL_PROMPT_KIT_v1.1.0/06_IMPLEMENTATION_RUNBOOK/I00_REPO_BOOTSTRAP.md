# I00 — Repository Bootstrap

You are starting implementation of ONE AVF repository.

Inputs:
- frozen Master Blueprint version;
- frozen contract package version;
- matching repo context profile;
- applicable ADRs;
- dependency release manifest.

Tasks:
1. verify versions/hashes;
2. list owned responsibilities and explicit non-goals;
3. list public interfaces consumed/provided;
4. list forbidden dependencies;
5. create `IMPLEMENTATION_TRACEABILITY.md`;
6. create project-local assumptions register;
7. refuse to implement any requirement that requires guessing a frozen contract—raise `SPEC_CLARIFICATION_REQUEST` instead.

No production code yet.

Gate: repo scope can be described without referring to internal implementation of unrelated repos.
