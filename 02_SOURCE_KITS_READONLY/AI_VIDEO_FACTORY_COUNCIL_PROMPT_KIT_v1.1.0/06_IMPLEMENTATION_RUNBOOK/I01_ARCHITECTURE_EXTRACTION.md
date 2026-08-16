# I01 — Repo Architecture Extraction

From the frozen repo blueprint, produce:
- component/module diagram;
- internal dependency rules;
- public interfaces;
- persistence ownership;
- side effects;
- error taxonomy;
- idempotency/retry responsibilities;
- observability points;
- security boundary;
- configuration surface.

Every design element must trace to the frozen spec or be explicitly implementation-local.

Create `REPO_DESIGN.md`.

Independent reviewer checks for scope creep before PASS.
