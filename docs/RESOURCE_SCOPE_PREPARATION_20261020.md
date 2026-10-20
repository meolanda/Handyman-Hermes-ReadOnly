# Resource scope prepared — 20 October 2026

## Verified discovery (existing Codex connectors only)

Read calendar-list, shared-drive/folder metadata and FlowAccount company metadata. No events, quotation contents, job photos or handover documents were downloaded during discovery. No permissions, resource contents or credentials were modified. This does not authenticate Hostinger Hermes to these sources.

- Selected 17 work calendars: 14 technician calendars plus follow-up scheduling, postponed/cancelled work and quotation scheduling. Personal, holiday and marketing calendars excluded. The returned list did not contain technician 6; do not invent a calendar ID or claim all numbered calendars exist.
- Located the existing October work folder and its exact 15 October subfolder in the current-year job-photo shared drive. Initial read scope proposed only for that day's folder/descendants, not the full shared drive or other dates.
- Located the existing field-upload system folder, but its inspected child-folder page showed older month names; it is not automatically included in the first approved scope or treated as the 15 October source.
- FlowAccount connector identifies the existing company and Owner role. No claim of provider-level read-only access is made for that identity.

Exact calendar names/IDs, folder IDs and company identity are saved locally in ignored config/connection-scope.local.json and docs/CONNECTION_APPROVAL_PRIVATE.local.md. They are intentionally not published in this repository. Metadata ACL response did not establish the service account's folder access; that remains unverified.

## Proposed Google change (NOT approved/applied)

Use the existing service account and existing key, no new project/account/key. Resource sharing would be reader on the selected calendars and Viewer on the one day folder, subject to Google company/shared-drive policy. Request only calendar.events.readonly and drive.readonly in addition to existing spreadsheets.readonly, after approval. Google APIs may need enablement in the existing project; verify first.

Drive readonly scope is not folder-limited: it can read resources accessible to that service account. Google ACL restrictions plus an application root allowlist are both required. If sharing the specific folder/calendar is blocked, stop rather than add entire-drive membership, domain delegation or a broader user credential. Shared-runtime/managed-backup exposure persists. Removal of these specific shares/scopes is preferable to revoking the account/key that already supports Sheets, unless a separate incident response is authorized.

Test window proposed: work on 15 October 2026, follow-up calendar checks until before 15 November, Asia/Bangkok. The expected output is one job entry with service work, outstanding action, follow-up appointment, quotation match and document evidence. No source writes, scheduling, customer messages or public links are part of the read-only test.

## FlowAccount path identified (NOT authorized/authenticated)

Official FlowAccount documentation publishes https://mcp.flowaccount.com/mcp with OAuth company selection. This offers a route to evaluate before creating any OpenAPI client secret. It does not prove compatibility with Managed Hermes or that OAuth can be restricted to reads. The connector can create documents when its authenticated user has permissions. Use an exact read-tool include list after verified tools/list and disable unnecessary resource/prompt wrappers; those client filters do not reduce the underlying token's provider permissions.

Hermes docs describe native OAuth with loopback callback and cached tokens at its home mcp-tokens directory (mode 0600). A managed remote callback and acceptable secret storage must be verified before OAuth is started. No localhost tunnel, SSH, public callback service, copied Codex token or manual token transfer is authorized here. Until callback/storage and read access are reviewable, do not request broad FlowAccount authorization.

Sources checked: [FlowAccount official connector](https://flowaccount.com/help-center/category/ai-connector-mcp/flowaccount-connector-in-claude), [Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp), [Calendar scopes](https://developers.google.com/workspace/calendar/api/auth), [Drive scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).

## Authentication compatibility checks actually performed

Installed Hermes help was read through the actual WebUI terminal tool, with --help only. mcp login advertises browser/PKCE and device/RFC8628 flows; mcp add help did not expose callback/storage options. No login/add operation was started.

Unauthenticated public discovery requests from Windows (not a live Hermes authentication test) returned HTTP 401 at the official FlowAccount MCP endpoint and pointed to https://mcp.flowaccount.com/.well-known/oauth-protected-resource/mcp. That public resource metadata named https://mcp.flowaccount.com as authorization server. Its public authorization-server metadata advertised authorization_code and refresh_token, PKCE S256 and scopes openid/profile/flowaccount-api/offline_access. No device_authorization_endpoint was advertised. This does not prove device flow can never be supported, but no supported device path was established, and flowaccount-api is not a demonstrated read-only scope. No registration/token/authorization endpoint was called and no client or token was created.

The Google resource-sharing proposal is concrete and can be approved independently. FlowAccount authentication/enablement is excluded from that approval until its managed callback, storage and residual provider permissions are reviewed; do not infer authority to provision a broad token from approval to read Google work resources.
