# I07 — Systematic Debugging

For any failing test/integration:
1. reproduce;
2. gather evidence;
3. trace root cause;
4. distinguish product bug vs test bug vs spec mismatch vs dependency mismatch;
5. fix root cause;
6. add regression test;
7. rerun impacted suites;
8. record evidence.

Do not patch symptoms with sleep/retry unless the contract explicitly requires it.
