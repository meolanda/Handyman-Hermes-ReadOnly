# Hostinger preflight setup — 2026-10-20

User reported CLI ready and requested configuration. Earlier explicit credential/permission approval boundaries remain in force.

## Changes completed

- Browser CLI prompt is available again. Remote metadata check confirmed existing company workspace and readonly-adapter checkout, HERMES_HOME=/data, no environment variable names matching OIDC/WORKLOAD/FEDERATION/GOOGLE_APPLICATION_CREDENTIALS, and no /data/credentials directory. This does not prove federation is impossible or rule out undisclosed credentials.
- Existing AGENTS.md and company manual were inspected; neither modified. A read command was interrupted by CLI disconnect/reconnect; no mutation was involved. Later terminal status confirmed reconnection.
- Remote git status was clean. Existing branch fast-forwarded from b9b1634 to 1c45036 using git pull --ff-only. No unrelated files overwritten.
- Added scripts/hostinger_readiness.py and six unit tests to the same repository. Local Python tests and Hostinger Python tests both passed 22/22.
- Ran default preflight on Hostinger. Exact result:

```json
{"status":"BLOCKED","reason":"CREDENTIAL_NOT_PROVISIONED","tokenIssued":false,"liveReadAttempted":false}
```

## What this setup does

Default command only inspects metadata at the proposed fixed credential-file location; it does not open credential contents, contact Google, discover ADC or mint tokens. Live mode is explicitly opt-in and has NOT been run. Live code restricts the service-account email, OAuth token endpoint, scope, spreadsheet and header-only range; rejects unsafe file/directory mode, symlinks at those checked entries, unexpected identity, redirected Sheets responses, oversized responses and duplicate normalized headers. Only sanitized metadata is printed. It is not a credential vault, full record reader, Telegram integration or guarantee against a process with the same UID.

Proposed credential path remains unprovisioned and its persistence/backup/public-serving boundaries remain unvalidated. No credential directory created or key requested. No actual Google credential fixture was used in tests; service-account live authentication remains untested.

## Remaining gate

Hostinger-supported workload identity or a validated private credential-file provisioning mechanism is still required. No key created/downloaded/transmitted; no Google IAM/sharing changes, Apps Script push/deploy, Hostinger restart/redeploy, agent skill registration, cron or external message performed. Production Hermes-to-Sheets integration is NOT complete.

Next request to approve, if user wishes: send the already prepared Hostinger support question about outbound workload identity and secure credential-file import/persistence/backup boundaries. Sending that support message is not yet authorized. Only after storage/method are validated should a concrete credential/permission approval be requested.
