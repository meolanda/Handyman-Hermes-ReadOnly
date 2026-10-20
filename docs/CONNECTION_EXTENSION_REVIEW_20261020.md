# Calendar / Drive / FlowAccount — connection review, 2026-10-20

## What was actually inspected

Reviewed the existing repository, current runtime/delivery evidence, Hostinger's previously received human support answer, and official Hermes/Google/FlowAccount documentation. No new credential was created, token minted for another scope, permission changed, connector installed or source data read in this review.

The direct CLI reached a login screen, but the existing authenticated WebUI session remained usable. Hermes then updated its clean checkout to afcf504 and ran connection_inventory.py through its terminal tool. Current metadata was observed: mcpServerEntries=0, mcpConfigSectionPresent=false, gwsOnPath=false, gcloudOnPath=false, googleWorkspaceSkillAtBundledPath=true, flowNamedEnvironmentEntries=0, sheetsCredentialPresentInProcess=true. No credential values were printed and this inventory made zero network calls. These observations do not rule out undocumented connections or prove live access to Calendar/Drive/FlowAccount. Codex has separate Google/FlowAccount connector capabilities; their presence is not evidence of Hostinger Hermes authentication, and their tokens must not be copied to Hermes.

## Google Calendar and Drive

Official Hermes documents a Google Workspace skill using OAuth with automatic refresh, preferring gws when installed and otherwise Python clients. It also supports MCP tool servers. Neither mechanism automatically authorizes Google data. The built-in Workspace setup examples include write-capable commands and new-project setup; do NOT apply those defaults to this existing read-only project.

Sources: [Hermes Google Workspace](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/google-workspace.md), [Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp).

Two possible paths, to be evaluated against exact approved resources:

1. Existing service account + selected-resource sharing, if company Google policies allow it. Calendar events reads would request calendar.events.readonly for explicit calendar IDs. Drive content reads would require drive.readonly and explicit authorized files/folders/shared-drive policy. These new scopes/ACL grants are NOT covered by existing spreadsheets.readonly approval. Do not request tokens for them until approved. Folder/ID allowlists in application code supplement Google resource permissions; they do not narrow an otherwise broad OAuth scope on their own. No domain-wide delegation proposed.
2. Existing Google project + user OAuth for the selected read services, if service-account sharing is unsuitable. Prepare the OAuth client/consent and managed storage/refresh review first; do not reuse clasp or Codex tokens. User OAuth drive.readonly can read all files that user can access, so it is broader than a single approved folder. Do not describe it as file-limited access. drive.file is narrower but cannot be assumed to provide arbitrary historical company-folder search without file selection/authorization design.

Official scopes: [Calendar](https://developers.google.com/workspace/calendar/api/auth), [Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).

Storage constraint: received Hostinger support answer says Environments is supported, shared with instance runtime, with managed backup exposure; no confirmed WIF or backup-excluded custom credential import. The existing JSON key is already stored by the owner there; that does not establish safe support for the Workspace skill's credential-file OAuth setup. Do not create a token file as a workaround without reviewing and approving storage.

Before one approval bundle can be concrete: inspect installed runtime integration metadata without values; resolve exact company calendar IDs and Drive folder/shared-drive IDs; verify existing sharing/API enablement read-only; choose identity path; list proposed scopes/sharing changes, secrets storage, revocation and one bounded test. No production setup completion is claimed.

## FlowAccount

Official OpenAPI supports Client Credentials and OpenID flows. Client Credentials requires the application's client ID/secret and issues access tokens; use the production versus test endpoint deliberately. The official material reviewed does NOT establish that the resulting credential can be restricted by the provider to quotation-read-only. Do not claim a GET-only adapter makes a broad account token read-only at the provider.

Sources: [FlowAccount connection overview](https://developers.flowaccount.com/tutorial/connect-open-api), [Client Credentials](https://developers.flowaccount.com/tutorial/connect/client-credentials-flow/), [OpenID](https://developers.flowaccount.com/tutorial/connect/open-id-flow), [API reference](https://developers.flowaccount.com/api-reference/).

First inspect whether this Hermes already has an approved FlowAccount MCP/API connection (names/tool lists only). If none, establish the existing company's OpenAPI eligibility, supported credential/storage arrangement and provider permissions. The Codex FlowAccount app is NOT automatically reusable as a remote MCP URL and no transferable endpoint/credentials have been verified. Do not scrape browser tokens, publish share links, email support, buy a plan or create a new integration credential during this review.

For the first daily-job audit expose only document search/get to the adapter, no create/update/payment/email/share-link tools. Record the residual risk if the underlying credential is broader. Any drafts/writes require a separately authorized operation even if another Codex chat allowed similar tasks there.

## Acceptance test that serves the owner

Review jobs on 15 October using each authorized actual source: service entries, technician calendars, matching quotations, job photos and handover forms. Deliver one entry per job with source links, work performed, remaining work, next appointment, quotation match and missing documents; explicitly separate unavailable evidence from absent documents. No fabricated prices, schedules or completion status. Do not declare full daily-review capability until this cross-source test is observed.
