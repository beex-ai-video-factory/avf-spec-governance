# Assumption Register

| ASSUMPTION_ID | DESCRIPTION | CLASSIFICATION | STATUS | VALIDATION_STRATEGY | RESPONSIBLE_COUNCIL_ROUND |
|---|---|---|---|---|---|
| A-01 | Google Flow web UI stability, selector volatility, and challenge rates remain within acceptable operational limits. | RESEARCH_REQUIRED | OPEN | 100-run Phase 0 benchmark measuring automation success rate and UI drift frequency | C01 (R06 Flow/Browser review) & Phase 0 Spike |
| A-02 | FlowKit open-source codebase can be cleanly bridged via FlowExecutionPort without leaking internal dependencies into core. | SPIKE_REQUIRED | OPEN | Prototype avf-flowkit-bridge against pinned FlowKit release in Phase 0 | C01 (R06 Flow/Browser & R13 OSS) & Phase 0 Spike |
| A-03 | Chrome MV3 background service worker lifecycle and Native Messaging transport provide sufficient uptime and throughput. | SPIKE_REQUIRED | OPEN | Isolated browser worker lifecycle and crash recovery test suite | C01 (R06 Flow/Browser & R02 Reliability) |
| A-04 | Google Flow generation latency, queuing delays, and daily quota limits support multi-shot production pipeline needs. | BENCHMARK_REQUIRED | OPEN | Execute Phase 0 100-run benchmark across different times of day | C01 (R14 Perf/Cost) & Phase 0 Benchmark |
| A-05 | Browser profile persistence and session tokens can be safely maintained on local worker nodes without credential leakage. | RESEARCH_REQUIRED | OPEN | Threat modeling and local execution zone security review in C01/C02 | C01 (R07 Security) |
| A-06 | Zero marginal software cost claim for Google Flow remains economically viable after factoring in local hardware, proxies, and maintenance. | BENCHMARK_REQUIRED | OPEN | Total Cost of Ownership (TCO) model comparing Track A/B against direct commercial API providers | C01 (R14 Perf/Cost) |
