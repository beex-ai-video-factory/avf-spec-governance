# Phase 0 — Google Flow Execution Benchmark

## Purpose

Select the MVP execution track using measured evidence rather than architectural preference.

Candidates:

- A2: MV3 + authenticated loopback WS;
- A3: Playwright dedicated persistent profile, optional helper extension;
- B: FlowKit compatibility bridge;
- A1 Native Messaging may be evaluated once core UI behavior is proven because packaging effort is higher.

## Standard scenario

A test run must record:

```text
run_id
candidate/version/commit
Chrome version
OS
Flow UI observed version/fingerprint if possible
account/profile ID alias (not credential)
capability/mode
asset count/type
prompt fixture ID
start time
submission outcome
provider job correlation
completion detection
output download outcome
elapsed time
manual intervention category
normalized error
screenshots/diagnostic ref
```

## Proposed benchmark

At least 100 controlled single-shot runs per serious candidate across more than one session/day if feasible.

Measure:

- successful submit rate;
- correct completion detection rate;
- correct download rate;
- duplicate/ambiguous submit count;
- auth/security challenge incidence;
- selector/protocol break incidence;
- reconnect recovery rate;
- manual interventions per 100 runs;
- median/p95 control-plane overhead excluding generation time;
- engineering defects found during test.

## Fault injection subset

- extension/service worker restart;
- worker reconnect;
- browser/tab reload;
- network interruption during status wait;
- output download interruption;
- stale/unknown page state.

## Provisional gates

These are proposed review gates, not claimed current capability:

- >=95% end-to-end single-shot control success for production dependence consideration;
- zero unintended duplicate paid submits in benchmark;
- every auth/security challenge becomes an explicit blocked/operator state;
- recovery behavior documented for every observed failure class.

If gates fail, do not hide failures by adding an unconstrained AI clicker. Either repair deterministic integration, use the alternate track, or choose a supported API provider.
