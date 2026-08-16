# Source Ledger and Evidence Boundary

This kit is based on the uploaded research report and technical blueprint prompt, plus targeted current-source verification for browser/FlowKit architecture.

## User-provided research

- `Nghiên cứu Giải pháp Chrome Extension Tự động hóa Google Flow.md`
  - Report proposes three approaches and recommends an Agent-Bridge architecture using a Chrome extension and local WebSocket.
  - It also makes strong claims about anti-bot immunity and fixed-cost economics; those claims are treated as hypotheses/risk items rather than frozen facts.

- `Pasted markdown(20260813-142328).md`
  - Defines required technical due diligence: bounded services, deterministic vs AI responsibilities, source of truth, provider abstraction, browser isolation, versioning, retry taxonomy, QC boundaries, phase strategy, test-first contracts, agent build packets, risk/kill criteria, and final review format.

## Current primary/official technical references checked for this kit

### FlowKit

- Repository: https://github.com/crisng95/flowkit
- Plan: https://github.com/crisng95/flowkit/blob/main/PLAN.md
- License observed: MIT.
- Current architecture describes Python/FastAPI/SQLite + localhost WebSocket + Chrome MV3 extension.
- Its current plan also contains undocumented Google endpoint and browser/security-challenge handling details. This kit intentionally treats those details as FlowKit-private and does not make them part of the AVF contract.

### Chrome Extensions

- Native Messaging: https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging
- MV3 service worker lifecycle: https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle
- Storage API: https://developer.chrome.com/docs/extensions/reference/api/storage
- Content scripts: https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts

Evidence relevant to design:
- MV3 service workers are lifecycle-managed/short-lived, so canonical state must not depend on in-memory globals.
- Chrome provides Native Messaging for extension ↔ native application communication.
- `chrome.storage` exists for extension-local persistence, but it remains non-canonical for factory business state.

### Playwright

- Persistent context: https://playwright.dev/docs/api/class-browsertype#browser-type-launch-persistent-context
- Persistent context can use a dedicated user-data directory, but current Playwright documentation warns against automating the default Chrome profile; use a dedicated automation profile.

### VeoFlow reference implementation

- https://github.com/MuazAshraf/flow_automation_tool
- Demonstrates a simpler MV3 content-script/background worker approach for queueing, UI interaction, and auto-download.

## Evidence classification

**Strong design evidence:** Chrome extension lifecycle/API behavior; repository architecture visible in source; contract-first software engineering principles from the user-provided specification.

**Implementation hypotheses requiring Phase 0 measurement:** Google Flow UI reliability, auth persistence, selector stability, rate limits, download reliability, comparative success of Track A vs Track B.

**Never treated as guaranteed:** “Chrome extension is immune to anti-bot”, “marginal cost is zero”, “character consistency is guaranteed”, or “FlowKit internals will remain stable”.
