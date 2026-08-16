# ADR-007 — BROWSER — SECURITY

## Context
Security challenges are blocked states.

## Decision
Automation does not bypass CAPTCHA/anti-abuse/security challenges; surfaces operator/provider fallback.

## Alternatives
Automated challenge evasion.

## Why
Policy/security risk containment.

## Tradeoffs
Adds explicit contracts and integration work; reduces hidden coupling.

## Revisit Trigger
Revisit only when measured operational evidence invalidates the assumptions or a supported provider capability materially changes the boundary.
