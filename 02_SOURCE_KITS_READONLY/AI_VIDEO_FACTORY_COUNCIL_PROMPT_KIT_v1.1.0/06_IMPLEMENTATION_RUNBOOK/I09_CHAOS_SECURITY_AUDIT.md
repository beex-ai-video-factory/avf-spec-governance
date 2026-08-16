# I09 — Failure / Chaos / Security Audit

Inject relevant failures:
- process crash;
- dependency timeout;
- duplicate command/event;
- invalid input;
- stale version;
- dependency unavailable;
- partial side effect;
- restart;
- corrupted/unauthorized data where applicable.

Security reviewer checks:
- secrets;
- permissions;
- transport;
- logging/redaction;
- dependency supply chain;
- least privilege.

Fix findings through normal TDD/review loop.
