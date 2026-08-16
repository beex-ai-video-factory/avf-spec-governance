# AI Video Factory — Local Development Environment

**Status:** INITIALIZED  
**Baseline Reference:** `01_FROZEN_RELEASE/v1.0.0/04_integration/LOCAL_DEVELOPMENT.md`  

---

## 1. Quick Start

1. **Verify Environment:**
   ```bash
   ./doctor.sh
   ```
2. **Bootstrap Toolchains & Packages:**
   ```bash
   ./bootstrap.sh
   ```
3. **Start Local Core Services (PostgreSQL, Temporal, MinIO, FakeProvider):**
   ```bash
   docker compose -f docker-compose.dev.yml --profile core up -d
   ```

---

## 2. Environment Structure

- **`docker-compose.dev.yml`**: Justified local dependencies (PostgreSQL, Temporal, MinIO, OpenTelemetry Collector, FakeVideoProvider mock).
- **`.env.example`**: Standardized environment variables with safe development defaults and no production secrets.
- **`TOOLCHAIN.lock.md`**: Approved toolchain runtime versions and minimum requirements.
- **`SERVICE_PORTS.md`**: Port allocation table preventing port conflicts across services.
- **`LOCAL_DATA_POLICY.md`**: Rules governing ephemeral dev storage, session isolation, and test teardown.
- **`bootstrap.sh`**: Non-destructive setup script initializing local dev dependencies.
- **`doctor.sh`**: Automated environment diagnostics validating runtimes, port availability, container health, and frozen baseline integrity.
