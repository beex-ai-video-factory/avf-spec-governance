# I06 — Independent Code Review

Use a fresh reviewer subagent/context.

Review in two stages:

Stage A — Spec compliance
- Does code satisfy frozen interfaces/invariants?
- Any scope creep?
- Any hidden cross-repo assumption?
- Any contract divergence?

Stage B — Code quality
- correctness;
- failure handling;
- maintainability;
- security;
- observability;
- tests;
- performance where material.

Critical/spec violations block progress.

Reviewer must not be the implementation agent.
