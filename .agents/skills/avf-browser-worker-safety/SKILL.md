---
name: avf-browser-worker-safety
description: Implement multi-layer selector resolution (DOM, Accessibility, Visual, Agent recovery), persistent browser sessions, anti-abuse safety, and human escalation gates for R09.
---

# Skill: AVF Browser Worker Safety & Recovery

## Purpose
Governs browser automation safety and multi-tiered fallback strategies within R09 Browser Worker (ADR-007).

## Multi-Layer Selector Strategy
When interacting with dynamic provider UIs, resolve interactive elements using the 4-tier hierarchy:
1. **Tier 1: Semantic DOM Selectors** (e.g., `data-testid`, semantic tag + ARIA role).
2. **Tier 2: Accessibility Tree Locators** (e.g., `getByRole('button', { name: 'Generate' })`).
3. **Tier 3: Visual / Coordinate Anchor** (bounding box offset from stable visual landmarks).
4. **Tier 4: Multimodal Agent Recovery** (screenshot + vision prompt to locate bounding box).

## Human Escalation & Anti-Abuse Rules
- **No CAPTCHA / Bot Mitigation Bypasses:** The worker must NEVER attempt to solve CAPTCHAs, inject anti-bot evasion scripts, or bypass rate limits.
- **Immediate Escalation:** Upon encountering an authentication challenge, CAPTCHA, or verification modal:
  1. Capture screenshot and failure context.
  2. Transition task to `HUMAN_INTERVENTION_REQUIRED`.
  3. Emit alert to R13 Operator Console.
  4. Wait for human operator resolution before resuming.
