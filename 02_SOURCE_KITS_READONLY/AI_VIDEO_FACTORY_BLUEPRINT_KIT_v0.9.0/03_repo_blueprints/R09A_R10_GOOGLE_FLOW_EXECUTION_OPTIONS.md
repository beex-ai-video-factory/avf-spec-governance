# Google Flow Execution Options — Decision Package

This document expands the shared boundary between `avf-google-flow-adapter` and the execution implementation.

## Frozen upstream boundary

Upstream depends only on:

```text
FlowExecutionPort
  ENSURE_SESSION
  OPEN_FLOW
  CREATE_OR_SELECT_PROJECT
  ATTACH_ASSETS
  SET_GENERATION_OPTIONS
  SUBMIT_PROMPT
  READ_GENERATION_STATE
  DOWNLOAD_OUTPUT
  CAPTURE_DIAGNOSTIC
  CANCEL
```

The implementation below that interface is replaceable.

---

## Option A1 — Chrome MV3 + Native Messaging (most Chrome-native local bridge)

### Architecture

```text
Google Flow page
   ↕ DOM
Content Script
   ↕ chrome.runtime messaging
MV3 Service Worker
   ↕ Chrome Native Messaging
Native Host / Browser Worker
   ↕ FlowExecutionPort
GoogleFlowAdapter
```

### Why

Chrome officially supports content scripts for page interaction and Native Messaging for extension-to-native-process communication. MV3 service workers are lifecycle-managed, so business state remains in the native worker/core.

### Advantages

- documented Chrome extension mechanisms;
- narrow host allow-list;
- no localhost TCP port required for extension/native communication;
- strong separation between page code and local process;
- long-term maintainability under our control.

### Costs

- OS-specific native-host registration/packaging;
- more installer engineering;
- still dependent on Google Flow DOM/UI stability.

### Recommended use

V1 production if Phase 0 proves UI automation reliability and desktop packaging is acceptable.

---

## Option A2 — Chrome MV3 + authenticated loopback WebSocket

### Architecture

```text
Content Script <-> MV3 Service Worker <-> wss/ws 127.0.0.1 <-> Browser Worker
```

### Advantages

- fastest clean implementation;
- cross-platform development simplicity;
- similar bridge shape to FlowKit without importing FlowKit domain.

### Requirements

- bind loopback only;
- random per-install shared secret or mutual handshake;
- origin/extension ID validation where possible;
- reconnection because MV3 service worker can stop/restart;
- no canonical in-memory queue inside extension.

### Recommended use

Phase 0/MVP controlled implementation.

---

## Option A3 — Playwright dedicated persistent profile, with optional helper extension

### Architecture

```text
Browser Worker -> Playwright persistent context -> dedicated Chrome/Chromium profile -> Google Flow
```

Optional MV3 helper extension can expose page semantics/download hooks while Playwright manages browser lifecycle.

### Advantages

- excellent deterministic test/trace tooling;
- browser lifecycle controlled by worker;
- no separate operator extension UI required for basic automation.

### Constraints

Current Playwright documentation recommends a dedicated automation user-data directory and warns against automating the user's normal default Chrome profile. This option must therefore use a dedicated profile and must be benchmarked for authentication/reliability.

### Recommended use

Strong Phase 0 comparison candidate and browser regression harness. Production adoption depends on measured reliability, not assumption.

---

## Option B — FlowKit Compatibility Bridge

### Architecture

```text
GoogleFlowAdapter
      ↓ FlowExecutionPort
avf-flowkit-bridge
      ↓ translation
FlowKit local agent / extension
      ↓
Google Flow
```

### Advantages

- fastest path to reuse substantial existing Google Flow work;
- FlowKit currently has a local Python agent + WebSocket + MV3 extension architecture and an MIT license;
- useful for validating reference assets, generation, status polling, downloading, and end-to-end workflows quickly.

### Hard boundary

FlowKit internals are **not** our contract. In particular:

- FlowKit SQLite is not AVF state;
- FlowKit queue/request IDs are not AVF business IDs;
- undocumented Google endpoint details are not exported upstream;
- provider-security challenge handling is not promoted into AVF requirements;
- FlowKit upgrade is treated like upgrading a third-party driver.

### Fork policy

1. Prefer pin + adapter first.
2. Fork only if required interfaces cannot be obtained cleanly.
3. If forked, keep changes minimal and upstream-rebaseable.
4. Maintain `FLOWKIT_COMPATIBILITY.md` with tested commit/release.
5. Never merge AVF core domain into the fork.

---

## Option comparison

| Criterion | A1 Native Messaging | A2 Loopback WS | A3 Playwright profile | B FlowKit bridge |
|---|---:|---:|---:|---:|
| Initial dev speed | Medium | High | High | Very High |
| Chrome-supported bridge mechanism | Very High | Medium | N/A/Playwright-supported | Medium |
| Our control of implementation | Very High | Very High | Very High | Medium |
| UI dependency | High | High | High | Mixed / implementation-dependent |
| Packaging complexity | High | Low | Medium | Medium |
| Existing Flow-specific functionality | Low initially | Low initially | Low initially | Very High |
| Long-term replaceability | Very High | Very High | High | High **only through bridge** |
| Phase 0 value | High | Very High | Very High | Very High |

## Recommended decision sequence

1. Freeze `FlowExecutionPort` first.
2. Build the conformance test runner.
3. Implement Track B minimal bridge quickly to obtain a working baseline.
4. In parallel spike A2/A3; A1 follows when behavior is proven and packaging matters.
5. Run identical benchmark scenarios across candidates.
6. Choose the primary MVP track by measured success/recovery/maintenance risk.
7. Keep the other conformant track as fallback where economical.

The architecture deliberately permits **FlowKit-first implementation without FlowKit-first architecture**.
