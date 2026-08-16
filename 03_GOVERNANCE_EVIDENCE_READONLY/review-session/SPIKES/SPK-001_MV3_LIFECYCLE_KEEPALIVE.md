# Technical Spike Specification: SPK-001 — Chrome MV3 Extension Lifecycle & Offscreen IPC Resilience

**SPIKE_ID:** SPK-001  
**SOURCE_FINDING:** F-R02-006, F-R06-004  
**ASSIGNED_OWNERS:** R06 (Flow/Browser) & R02 (Reliability)  
**STATUS:** DESIGNED & SPECIFIED (Incorporated into CP-006)  

---

## Objective & Test Harness Specification
Validate Chrome Manifest V3 service worker lifecycle keepalive mechanics during 60-minute long-running Google Flow video generation polling under simulated background tab throttling and network stalls.

## Architecture Design
1. **Offscreen Document Keepalive Channel:** Chrome Offscreen API maintains an active message port and low-frequency heartbeat.
2. **Native Messaging Host Supervisor:** Standalone Node.js/Go daemon connects via standard Chrome Native Messaging pipe, providing an external watchdog timer and direct CDP connection.
3. **Automatic Session Re-hydration:** If the Chrome renderer is restarted, the worker reads persistent state from IndexedDB/Chrome Storage and re-attaches to existing Flow job polling.

## Kill Criteria & Contingency
If MV3 service worker keepalive fails under empirical tests, Track A architecture mandates running browser automation via headless containerized Playwright instances directly connecting to CDP without extension wrapping.
