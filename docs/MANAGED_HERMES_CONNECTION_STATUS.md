# Managed Hermes connection review — 2026-10-12

Instance: aliceblue-quetzal-360983. Existing repository, spreadsheet and Apps Script are retained. No new project created.

## DONE

- Existing Apps Script source push and authenticated live header validation: PASS, 12 columns, no mismatches. Public deployment remains mock-only. See WINDOWS_PUSH_REVIEW_20261012.md.
- Local service schema and synthetic fixture reconciled with the verified S header. No spreadsheet content was edited.
- Hostinger documents browser-based Managed Hermes CLI, isolated from the underlying host. This does not establish SSH support.
- Hostinger documents dashboard Environments with masked values and staged Save & redeploy; applying changes restarts the agent. No environment values were read or changed.

## BLOCKED

WebUI and /cli opened through the available in-app browser both display Welcome to Hermes with a login form. No authenticated remote runtime inspection, adapter installation or credential setup has occurred.

User reports lshell restrictions. Current Hostinger documentation describes full command-line access inside isolated storage; actual permissions and allowed commands of this instance remain unverified. Never bypass lshell restrictions or assume root/SSH access.

Google authorization granted to the existing Apps Script does not provision a Google identity on Hostinger. The mock public URL cannot provide authenticated company data. Existing token acquisition/refresh and secure credential storage on Hostinger are not yet verified. Do not copy clasp credentials to Hostinger or logs.

## NEXT ACTION

1. User signs in directly to the retained Hermes WebUI tab; no password or token in chat.
2. Inspect supported settings/integrations and runtime through documented interfaces. Inspect only credential names/presence, never reveal secret values. Confirm installed Hermes version, read-only Google integration, persistent storage and permitted execution path.
3. Prefer the existing direct Sheets reader if an existing authorized readonly Google identity and supported runtime are available. Otherwise prepare one concrete authentication proposal within existing projects; do not create credentials, broaden scopes, change sharing or deploy without the needed approval.
4. Prepare bounded header-only live probe first and a sanitized adapter verification. Configure authenticated data access and verify Hermes end-to-end only through the supported interface. Protect Telegram recipients before exposing company records; do not send records or test messages without explicit authorization.
5. Keep source push/header verification distinct from production Hermes readiness. No time estimate for successful integration until runtime and Google authorization path are established.

## EVIDENCE

- https://www.hostinger.com/support/how-to-use-managed-hermes-cli/ — documented browser terminal and isolation boundary.
- https://www.hostinger.com/support/how-to-manage-environment-variables-in-managed-hermes/ — masked configuration storage, staged changes, restart on Save & redeploy.
- User-supplied WebUI: https://aliceblue-quetzal-360983.hostingersite.com/
- User-supplied CLI: https://aliceblue-quetzal-360983.hostingersite.com/cli

No SSH connection attempted; no Hostinger environment mutation, redeploy or company record read performed.
