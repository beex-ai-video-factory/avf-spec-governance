# ECC Role Mapping Template

Do not hard-code ECC skill names until the selected ECC commit has been inspected.

For each Council/Implementation role, fill:

| AVF Role | Required capability | ECC agent/skill | ECC commit | Allowed tools/hooks | Notes |
|---|---|---|---|---|---|
| Reliability Architect | distributed failure analysis | TBD | PIN | read-only during review | |
| Security Reviewer | threat modeling/supply-chain | TBD | PIN | no destructive hooks | |
| QA Architect | contract/chaos testing | TBD | PIN | test execution | |
| Data Architect | DB schema/migrations | TBD | PIN | read-only during council | |
| Implementation Builder | language/framework skill | TBD | PIN | repo-scoped edit | |

Rule: map only after reading the exact skill/agent file at the pinned version.

ECC is an accelerator, not a normative source.
