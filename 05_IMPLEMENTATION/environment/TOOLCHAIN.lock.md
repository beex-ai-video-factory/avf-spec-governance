# TOOLCHAIN & RUNTIME LOCK
## AI Video Factory — Approved Developer & CI Toolchains

**Status:** APPROVED (Implementation Decisions)  
**Date:** 2026-08-16  

---

## 1. Runtime Specifications

| Runtime / Tool | Minimum Version | Recommended Version | Purpose |
|---|---|---|---|
| **Node.js** | `>= 20.10.0 LTS` | `22.x LTS` | TypeScript microservices (R01, R02, R05, R06, R08, R09, R10, R13, R14, R15) |
| **npm** | `>= 10.0.0` | `10.8.x` | Package manager |
| **TypeScript** | `>= 5.3.0` | `5.6.x` | Strongly typed contract and service implementation |
| **Python** | `>= 3.10.0` | `3.11.x` | Quality Control analysis, FFmpeg binding helpers, and validator scripts |
| **Docker / Compose** | `>= 24.0.0` / `>= 2.20.0` | Latest Desktop / Engine | Local containerized dependencies (Postgres, Temporal, MinIO) |
| **Temporal CLI (`temporal`)** | `>= 0.13.0` | Latest | Local Temporal development and workflow debugging |
| **FFmpeg / FFprobe** | `>= 6.0` | `7.x` | Video stream inspection (R11 QC) and assembly stitching (R12 Media) |

---

## 2. Infrastructure Version Baseline

- **PostgreSQL:** `16-alpine`
- **Temporal Server:** `1.24.x` (or `temporalio/admin-tools:latest`)
- **MinIO:** `RELEASE.2024-01-01T00-00-00Z` or later
- **OpenTelemetry Collector Contrib:** `0.95.x` or later
