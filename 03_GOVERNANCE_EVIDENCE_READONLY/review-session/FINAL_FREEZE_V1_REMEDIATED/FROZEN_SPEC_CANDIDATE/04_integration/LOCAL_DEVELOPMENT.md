# Local Development Composition

## Goal

A developer/agent should run most of the system without Google Flow or generation credits.

Minimum composition:

```text
PostgreSQL
Temporal dev server
Object storage (MinIO or local S3-compatible)
Core State
Workflow Worker
FakeVideoProvider
QC fake
Media worker
```

Google Flow Track A or Track B is an optional profile.

Suggested profiles:

```bash
docker compose --profile core up
# deterministic pipeline

docker compose --profile track-a up
# core + controlled browser bridge services; Chrome may run on host

docker compose --profile track-b up
# core + FlowKit compatibility bridge; FlowKit/Chrome may run on host
```

Browser profiles and credentials are host-local and excluded from Compose images and Git.
