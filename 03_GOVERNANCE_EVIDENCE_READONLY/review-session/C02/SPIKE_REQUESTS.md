# C02 — Technical Spike & Benchmark Requests

The following technical spikes were commissioned during C02 cross-examination to establish empirical evidence and validate high-risk runtime mechanics.

| SPIKE_ID | SOURCE_FINDING | TOPIC | ASSIGNED_OWNERS | DELIVERABLE |
|---|---|---|---|---|
| SPK-001 | F-R02-006 | MV3 Service Worker Lifecycle & Offscreen IPC Resilience Spike | R06 (Browser/Flow) & R02 (Reliability) | Working prototype test harness verifying 60-minute long-running video generation polling without silent SW termination |

---

## Technical Spike Specifications

### SPK-001: MV3 Service Worker Lifecycle & Offscreen IPC Resilience Spike
- **Source Finding:** `F-R02-006`
- **Assigned Owners:** `R06 (Browser/Flow) & R02 (Reliability)`
- **Objective:** Implement a prototype Chrome Extension Manifest V3 background service worker with offscreen document IPC keepalive and native messaging heartbeat. Subject it to simulated 60-minute Google Flow generation jobs with induced network stalls and tab backgrounding.
- **Expected Deliverable:** Working prototype test harness verifying 60-minute long-running video generation polling without silent SW termination
- **Kill Criteria:** If MV3 service worker cannot be reliably kept alive or re-hydrated without losing in-flight WebSocket state, Track A architecture must mandate a native host process for CDP connection management.

