# SERVICE PORT ALLOCATION MATRIX
## AI Video Factory — Local Development Ports

| Port | Protocol | Service / Component | Purpose |
|---|---|---|---|
| **3000** | HTTP | R13 Operator Console / Web UI | Developer & human operator interface |
| **5432** | TCP | PostgreSQL (R02 Core State) | Canonical database engine |
| **7233** | gRPC | Temporal Server (R06 Workflow) | Workflow engine gRPC endpoint |
| **8088** | HTTP | Temporal Web UI | Temporal workflow execution dashboard |
| **8090** | HTTP | FakeVideoProvider (R07 / R15) | Mock video generation API for offline tests |
| **8095** | HTTP | FlowKit Bridge (R10 Track B) | FlowKit bridge local endpoint |
| **9000** | HTTP | MinIO (S3 API) | Asset object storage API |
| **9001** | HTTP | MinIO Console | MinIO admin web console |
| **4317** | gRPC | OpenTelemetry Collector (OTLP gRPC) | Trace & metric ingestion |
| **4318** | HTTP | OpenTelemetry Collector (OTLP HTTP) | Trace & metric ingestion |
| **8889** | HTTP | Prometheus Metrics Exporter | Telemetry scrape endpoint |
| **9222** | WebSocket | Chrome DevTools Protocol (CDP) | Browser worker (R09 Track A) debugging |
