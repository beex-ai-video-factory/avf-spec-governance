# Council Dissent & Advisory Register (C04)

**Council Round:** C04 Voting Complete  
**Total Blocking Dissents:** 0  
**Total Advisory Cautions / Operational Notes Preserved:** 2  

---

| DISSENT_ID | CHANGE_ID | ROLE | SEVERITY | SUMMARY | MITIGATION & ADVISORY DIRECTIVE |
|---|---|---|---|---|---|
| DIS-001 | CP-006 | R02 (Reliability) | NON_BLOCKING_ADVISORY | MV3 Long-Polling Headroom | While Offscreen Document keepalive satisfies 60-min polling, production telemetry must monitor Chrome memory usage under high concurrent tab loads. |
| DIS-002 | CP-007 | R10 (DX) | NON_BLOCKING_ADVISORY | Developer Local Setup | Local development environment must provide transparent HMAC helper CLI utilities so developers do not experience friction during manual curl testing. |

---

## Detailed Dissent & Advisory Records

### DIS-001: MV3 Long-Polling Memory Headroom (R02 Reliability)
- **Context:** Chrome Extension background execution during massive concurrent video batch generation.
- **Council Resolution:** Accepted CP-006 with explicit provision that R15 Integration Harness will include memory leak detection tests under 100+ concurrent simulated tasks.

### DIS-002: Local Developer Experience with IPC HMAC (R10 DX)
- **Context:** Requiring HMAC signatures on internal HTTP endpoints could increase local development friction.
- **Council Resolution:** R10 DX tooling will supply auto-signing local proxy / CLI tokens during `NODE_ENV=development`.
