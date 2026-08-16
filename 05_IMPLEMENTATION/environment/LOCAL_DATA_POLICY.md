# LOCAL DATA & STORAGE POLICY
## AI Video Factory — Ephemeral Storage, Mock Isolation & Privacy

**Status:** ACTIVE  
**Scope:** Local Development, Automated Testing, CI Pipelines  

---

## 1. Local Storage Invariants

1. **Ephemeral Test Artifacts:** All video files, audio tracks, and temporary images generated during automated integration tests must be written to `05_IMPLEMENTATION/environment/tmp_data/` or MinIO bucket `avf-video-assets` with automated lifecycle expiration.
2. **No Persistent Credentials in Storage:** Never store unencrypted session tokens, cookies, or account passwords in local files, docker volumes, or sqlite databases.
3. **Database Reset Safety:** Local test databases (`avf_canonical_state_test`) may be dropped and recreated dynamically during test suite execution. Production databases must never be targeted by test runners.
4. **Offline Isolation:** All unit tests and default CI jobs must run completely disconnected from paid third-party provider APIs, utilizing `FakeVideoProvider` for generation emulation.
