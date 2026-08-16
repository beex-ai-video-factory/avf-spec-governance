# Skill Orchestration Policy

## Principle

Define review/implementation roles by **capability**, not by third-party skill name.

Third-party skill repositories evolve. Therefore:

`role -> capability requirements -> local skill adapter -> pinned external skill`

Never:

`architecture role == ECC skill X forever`

## Recommended layers

### Layer 1 — Council rules
Normative. This Prompt Kit.

### Layer 2 — Process discipline
Optional Superpowers capabilities:
- brainstorming/design refinement;
- writing plans;
- TDD;
- systematic debugging;
- requesting/receiving code review;
- verification before completion;
- parallel/subagent execution.

### Layer 3 — Specialist capability
Optional curated ECC skills/agents:
- architecture;
- security;
- test engineering;
- database;
- performance;
- DevOps/platform;
- language/framework-specific implementation.

### Layer 4 — Project-local skills
AVF-specific skills derived after the specification is frozen.

## Rules

1. Pin exact commit/release.
2. Record hash.
3. Review skill instructions before use.
4. Audit hooks/scripts and permissions.
5. No auto-update mid-session.
6. Per-role allowlist only.
7. Do not load hundreds of unrelated skills into context.
8. External skill cannot override council governance or frozen contracts.
9. Run a small A/B evaluation before making a skill mandatory.
10. If a skill conflicts with current project evidence/version, project evidence wins.
