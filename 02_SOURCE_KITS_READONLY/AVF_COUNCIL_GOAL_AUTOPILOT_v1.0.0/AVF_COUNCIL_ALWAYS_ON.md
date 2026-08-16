# AVF Council — Always-On Workspace Governance Rule

This workspace contains:
- `AI_VIDEO_FACTORY_BLUEPRINT_KIT_v0.9.0/` — specification authority, READ ONLY.
- `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/` — council procedure authority, READ ONLY.
- `review-session/` — the only writable Council artifact root.

Before executing any AVF Council task, read:
- `AI_VIDEO_FACTORY_COUNCIL_PROMPT_KIT_v1.1.0/01_COUNCIL_MASTER/MASTER_COUNCIL_PROMPT.md`
- the applicable file under `03_COUNCIL_ROUNDS/`
- relevant role charters when subagents are used.

Authority:
Human Sponsor > Council Governance > Frozen Spec/ADRs/Contracts > accepted Change Proposals > implementation preferences > third-party tools/skills.

Rules:
1. Never modify either source kit during Council review.
2. Never auto-cross a Human Gate.
3. A `/goal` may self-iterate only inside its named C-round.
4. When a round reaches its exit criteria, persist artifacts, output the required WAITING_FOR_HUMAN_GATE state, and STOP.
5. Never simulate isolated reviewers as personas in the parent context. Use real `invoke_subagent` sessions.
6. Preserve raw blind-review outputs before synthesis.
7. Explicit source gaps are better than invented completeness.
8. Votes cannot override failed objective evidence.
9. Every semantic spec change requires a Change ID and required vote/sign-offs.
10. C05 must be a fresh conversation and preferably a different model family.
11. Third-party skills are optional; record and pin them if used.
12. Google Flow and FlowKit remain behind frozen provider/execution abstractions.
13. Security challenges are blocked/human-required states, never bypass targets.
14. Do not treat a successful mock as proof of live-provider reliability.
15. All Council-generated files must remain under `review-session/`.
