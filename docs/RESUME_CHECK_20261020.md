# Resume inspection — 2026-10-20 (Asia/Bangkok)

Read RESUME_HANDOFF.md and SERVICE_ACCOUNT_AUTH_PROPOSAL.md. Local checkout is clean and matched origin at ee10ddb before this report. Historical 2026-10-12 installation/header PASS evidence is retained, not represented as fresh testing.

## Current observations

- Existing Hermes WebUI opens in the in-app browser; navigation and System page work.
- System page displays WebUI v0.52.113 and Agent 0.21.5. An update notice is visible; no update performed.
- Gateway status, MCP servers and MCP tools remain Loading. This does not establish whether the gateway is running, stopped or inaccessible.
- Existing /cli loads its terminal frame but shows no prompt/output. Input preparation failed with explicit no-input-sent outcome. One intentional reload still showed the empty terminal. No remote command executed in this resumed session.
- Prior remote workspace, adapter and identity state could not be revalidated today. Do not infer deleted files, lost credentials or instance failure from an empty CLI.
- No key/token created, downloaded, transmitted or configured; no sharing/IAM, sheet, Apps Script or Hostinger configuration change, restart or redeploy performed.

## Authentication research update

Hostinger's skills guide describes required_credential_files and credential passthrough for service-account JSON. Its security guide recommends limited credential passthrough and file permissions. These general instructions do not independently verify a private import UI, serving boundaries, per-instance access isolation or credential-file persistence for this Managed Hermes instance.

Hostinger's current backup documentation states daily backups retained for seven days and downloadable backups. It does not establish credential-file exclusions or access separation. Such backup copies must be covered by credential lifecycle/revocation planning.

No official Hostinger documentation establishing an outbound per-instance OIDC/SAML workload assertion for Google federation was found. Support remains unconfirmed, not ruled out. Prior inbound WebUI OAuth plugins are not outbound workload federation evidence.

## Next action

User should open the existing instance's Manage page in Hostinger dashboard, inspect status, and launch Command line (CLI) through the dashboard. Reauthenticate if requested. Do not restart, restore, update or redeploy merely because this browser's CLI is empty. Once a prompt is available, resume read-only verification of the existing runtime and storage.

Before credential approval, obtain Hostinger's documented answer about workload identity and secure credential-file handling. The following support draft is prepared but NOT sent; sending requires explicit user authorization.

### Prepared support message

Hello. I use Hostinger Managed AI Automation Apps / Managed Hermes, instance aliceblue-quetzal-360983 (not a self-managed VPS).

1. The WebUI opens, but Gateway/MCP status stays Loading and /cli shows an empty terminal with no prompt after one reload. What supported diagnostic or dashboard action should I take without resetting the app or losing stored files?
2. Does this product expose a per-instance outbound OIDC or SAML workload identity usable with Google Workload Identity Federation? If yes, please provide issuer/JWKS documentation, subject/audience binding, and the supported assertion acquisition/refresh mechanism. Please do not send actual assertions or tokens.
3. If not, what supported method imports a Google service-account JSON credential privately outside the WebUI workspace, repository and downloadable artifacts? Please document runtime ownership/access boundaries, persistence across redeploys, public-serving exclusions, backup/restore handling and whether credential files can be excluded from backups.
4. Does required_credential_files / terminal.credential_files work in Managed Hermes as documented in your general skills/security guides, and what isolation remains if agent tools execute as the same Unix user?

I intend to reuse an existing Google service account with Viewer access to one spreadsheet, request only spreadsheets.readonly, and avoid creating or transmitting credentials until the storage/authentication approach is approved. I am not requesting SSH/root access, a new service account/project, or a public data endpoint.

## Sources checked

- https://www.hostinger.com/ca/tutorials/?p=145307
- https://www.hostinger.com/ca/tutorials/hermes-agent-security/
- https://www.hostinger.com/support/how-to-manage-backups-in-managed-hermes/

No support message sent. Production Hermes-to-Sheets integration remains incomplete.
