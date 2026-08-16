# Security Model

## Assets requiring protection

- Google/browser accounts;
- cookies/session tokens;
- LLM/provider API keys;
- object storage credentials;
- private scripts/prompts/assets;
- generated media before publication;
- screenshots/diagnostics;
- FlowKit local execution privileges.

## Trust zones

```text
[Core/Workflow Services]
        |
  authenticated contracts
        |
[Privileged Local Execution Zone]
   | Track A browser worker
   | Track B FlowKit bridge
        |
[Chrome / Google Flow]
```

The privileged local execution zone may access browser session material. Core/creative/QC services should not.

## Browser extension rules

- minimal host permissions restricted to required Flow origins;
- no remotely hosted executable code;
- extension bundle versioned and checksummed;
- service-worker in-memory state considered disposable;
- sensitive persistent data avoided; use session/local storage only for non-canonical connection/config needs;
- logs redact cookies, bearer tokens, reCAPTCHA/security artifacts, API keys;
- diagnostics screenshot retention is configurable and access-controlled.

## Local transport

Native Messaging is preferred for packaged Track A where practical. If loopback WebSocket is used:

- bind `127.0.0.1` only;
- random installation secret/handshake;
- reject unauthenticated clients;
- message size/time limits;
- strict method allow-list;
- no arbitrary URL/fetch primitive exposed from AVF contracts.

## FlowKit bridge

FlowKit is privileged third-party/open-source code in the local execution zone.

- pin exact tested commit/release;
- review license and dependency tree;
- isolate process permissions;
- do not expose FlowKit database to core;
- do not copy undocumented credential/security challenge mechanics into shared contracts;
- normalize `AUTH_REQUIRED` / `SECURITY_CHALLENGE` and stop automation where operator/provider action is required.

## Secret handling

Development: `.env` + OS/browser profile outside Git, preferably secret manager where available. Production: secret-store integration; no credentials in release manifests.

## Threat-oriented tests

- unauthorized loopback client rejected;
- malformed oversized command rejected;
- path traversal in download/asset filename blocked;
- token/cookie redaction test;
- browser profile directory never packaged into artifacts;
- operator actions authorization/audit;
- FlowKit raw response redaction before central logs.
