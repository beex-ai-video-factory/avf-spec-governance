# AVF Council Goal Autopilot v1.0.0

Purpose: minimize Human Sponsor copy/paste while preserving mandatory human gates.

Do NOT run one `/goal` across C00-C07.

Use one `/goal` per round. Each goal may self-iterate within its own round until its exit criteria pass, then MUST stop at the human gate.

Recommended model routing:
- C00: Gemini 3.7 Flash High
- C01: Gemini 3.7 Flash High + isolated inherit/flash subagents
- C02: Gemini 3.7 Flash High; fresh Pro-tier advisory subagent for disputed BLOCKER/CRITICAL issues
- C03: Gemini 3.7 Flash High; escalate hard cross-domain solution comparisons to Pro-tier advisory subagent
- C04: Gemini 3.7 Flash High; Pro-tier verification for critical changes
- C05: NEW CONVERSATION, Claude Opus 4.6 Thinking, `/goal`
- C06: Gemini 3.7 Flash High
- C07: Gemini 3.7 Flash High; Human performs final freeze authorization

Install `AVF_COUNCIL_ALWAYS_ON.md` as an Always-On Workspace Rule if desired.
Then the Human only needs the one-line commands in `QUICK_COMMANDS.md`.
