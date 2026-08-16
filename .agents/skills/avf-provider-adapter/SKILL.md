---
name: avf-provider-adapter
description: Implement provider-neutral interfaces, capability profile negotiation, operation vs generation status tracking, error normalization, and cancel/download/retry semantics.
---

# Skill: AVF Provider Adapter & Abstraction

## Purpose
Enforces provider neutrality (ADR-003) across all video and media generation integrations in R07 Provider SDK and R08 Google Flow Adapter.

## Core Directives
1. **Neutral Core Abstraction:**
   - The core pipeline communicates exclusively via `VideoProvider` interface:
     - `submitGeneration(request: ProviderRequest): Promise<SubmitResult>`
     - `getGenerationStatus(generationId: string): Promise<ProviderResult>`
     - `cancelGeneration(generationId: string): Promise<CancelResult>`
     - `downloadAsset(assetUrl: string, destinationPath: string): Promise<DownloadResult>`
2. **Capability Profiles:**
   - Providers declare supported aspects (e.g., resolutions: 720p/1080p, aspect ratios: 16:9/9:16/1:1, max duration: 5s/10s, camera motion controls).
   - Incompatible requests are rejected before dispatch.
3. **Normalized Error Hierarchy:**
   - All provider-specific HTTP/gRPC errors must be mapped into canonical error categories:
     - `RATE_LIMITED`
     - `INVALID_PROMPT`
     - `CONTENT_FILTERED`
     - `QUOTA_EXCEEDED`
     - `SERVICE_UNAVAILABLE`
     - `AUTH_EXPIRED`
     - `TIMEOUT`
