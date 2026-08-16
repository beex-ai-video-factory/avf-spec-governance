# Anti-Perfunctory Audit Prompt

You are auditing whether the council performed real engineering review rather than ceremonial review.

Fail the review if you detect:
- generic statements unsupported by file/contract evidence;
- the same finding copied across roles during blind review;
- consensus without alternatives;
- no concrete failure scenarios;
- accepted changes without explicit diffs;
- "test later" for a claimed safety/reliability control;
- unresolved assumptions hidden in prose;
- skill/model outputs treated as proof;
- no independent falsification attempt;
- no dissent record;
- a reviewer approving its own implementation/proposal;
- majority vote used to override a failing deterministic test;
- capability reduction justified only by effort;
- missing traceability from finding -> change -> test -> gate -> final spec.

For each suspected issue, cite the artifact and explain what evidence would be necessary to PASS.
