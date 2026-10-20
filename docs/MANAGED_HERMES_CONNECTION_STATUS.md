# Managed Hermes connection review — 2026-10-12

> HISTORICAL INITIAL INSPECTION ONLY. Its missing-credential/not-connected blockers were resolved on 2026-10-20. Read CURRENT_STATUS.md for current facts: live Sheets and private Telegram delivery verified; Calendar/Drive/FlowAccount remain unverified. Do not use the historical BLOCKED section below as today's status.

Instance: aliceblue-quetzal-360983. Existing repository, spreadsheet and Apps Script are retained. No new project created.

## DONE

Authenticated inspection after user login:

- WebUI v0.52.113; Agent 0.21.5. System page reports no configured MCP servers or active MCP tools. Plugins page had no native Sheets reader identified; this does not prove absence of all possible skills.
- Hostinger /cli accepted documented shell help, hermes --help, python3 and git. No SSH, root access or lshell escape attempted.
- Runtime Python 3.13.16; google.auth installed. Home /data; working directory /data. gws and gcloud were not installed in PATH.
- Only matching Google/GWS/Handyman environment variable name observed: HANDYMAN_TEST_ENV. Values were not read. No ADC/GWS credential file in the standard locations checked. google.auth.default requested only spreadsheets.readonly and returned sanitized ADC UNAVAILABLE (DefaultCredentialsError handled without printing its text). This does not rule out credentials in an undisclosed secure location.
- Existing company workspace /data/workspace/handyman contained AGENTS.md and Handyman-Agent-Manual.md. Both were read before adding code; neither modified. No cron, company records or external messages created.
- Existing repository branch cloned into /data/workspace/handyman/readonly-adapter at b9b1634. No new Google/Hostinger project created. Adapter is staged source, not registered as an active Hermes skill or production reader.
- Python mock tests ran inside Hostinger: MOCK_TESTS_PASS, tests=16. No package installation or dependency download was needed.

- Existing Apps Script source push and authenticated live header validation: PASS, 12 columns, no mismatches. Public deployment remains mock-only. See WINDOWS_PUSH_REVIEW_20261012.md.
- Local service schema and synthetic fixture reconciled with the verified S header. No spreadsheet content was edited.
- Validation: Node 21/21 and Python 16/16 mock tests passed. Python on this Windows locale requires UTF-8 mode (`python -X utf8 -m unittest discover -s tests -v`); the initial default-encoding attempt failed decoding Thai fixture files, then passed in UTF-8 mode. No remote live read is implied by these tests.
- Hostinger documents browser-based Managed Hermes CLI, isolated from the underlying host. This does not establish SSH support.
- Hostinger documents dashboard Environments with masked values and staged Save & redeploy; applying changes restarts the agent. No environment values were read or changed.

## BLOCKED

Initial login blocker is resolved by user login. Current blocker is missing usable Google authorization on Hostinger: ADC unavailable and no configured Google MCP connection identified. Staged adapter has not made a live Sheets request.

User reports lshell restrictions. Actual help allowlist and selected permitted commands were checked in this instance; this does not authorize other commands, root access or SSH. Never bypass shell restrictions.

Google authorization granted to the existing Apps Script does not provision a Google identity on Hostinger. The mock public URL cannot provide authenticated company data. Existing token acquisition/refresh and secure credential storage on Hostinger are not yet verified. Do not copy clasp credentials to Hostinger or logs.

## NEXT ACTION

1. Identify the existing authorized Google Viewer/service-account or OAuth identity and the secure storage location of its existing credentials. Ask only for type/location, never credential contents in chat. Do not create keys or copy Windows clasp credentials to Hostinger.
2. Validate the approved existing identity's allowed scope and sheet access, then prepare secure storage and bounded header-only probe. Runtime, versions and permitted Python execution are now verified; persistence across Hostinger redeployment remains untested.
3. Prefer the existing direct Sheets reader if an existing authorized readonly Google identity and supported runtime are available. Otherwise prepare one concrete authentication proposal within existing projects; do not create credentials, broaden scopes, change sharing or deploy without the needed approval.
4. Prepare bounded header-only live probe first and a sanitized adapter verification. Configure authenticated data access and verify Hermes end-to-end only through the supported interface. Protect Telegram recipients before exposing company records; do not send records or test messages without explicit authorization.
5. Keep source push/header verification distinct from production Hermes readiness. No time estimate for successful integration until runtime and Google authorization path are established.

## EVIDENCE

- https://www.hostinger.com/support/how-to-use-managed-hermes-cli/ — documented browser terminal and isolation boundary.
- https://www.hostinger.com/support/how-to-manage-environment-variables-in-managed-hermes/ — masked configuration storage, staged changes, restart on Save & redeploy.
- User-supplied WebUI: https://aliceblue-quetzal-360983.hostingersite.com/
- User-supplied CLI: https://aliceblue-quetzal-360983.hostingersite.com/cli

No SSH connection attempted; no Hostinger environment mutation, redeploy or company record read performed. Only reversible adapter source preparation within the existing company workspace was performed.
