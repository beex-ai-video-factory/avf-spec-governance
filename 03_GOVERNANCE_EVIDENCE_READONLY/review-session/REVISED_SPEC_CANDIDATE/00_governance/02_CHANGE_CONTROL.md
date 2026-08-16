# Change Control

Every post-freeze change request must contain:

```text
CHANGE-ID:
MOTIVATION:
AFFECTED CONTRACTS:
AFFECTED REPOS:
BACKWARD COMPATIBILITY:
DATA MIGRATION:
ROLLBACK:
TEST CHANGES:
SECURITY IMPACT:
OBSERVABILITY IMPACT:
ADR REQUIRED: yes/no
```

No implementation PR is allowed to silently redefine a contract because a coding agent found a more convenient structure.

Contract source files under `02_contracts/` take precedence over prose examples elsewhere.
