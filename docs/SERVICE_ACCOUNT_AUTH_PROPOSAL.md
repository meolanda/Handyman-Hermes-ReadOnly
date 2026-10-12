# Existing service account authentication proposal

Date: 2026-10-12. State: proposal only; no credentials created, downloaded, transmitted or configured.

User identified existing project display name Handyman-Hermes-Reader and service account handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com. The email implies project ID handyman-hermes-reader; verify in Cloud Console before any mutation. User reports this account is Viewer on Handyman2026 and its Keys page contains no user-managed key. These account/key/ACL facts are user-reported, not independently inspected by this agent.

## Preferred: workload identity federation, conditional on Hostinger support

Google supports exchanging an external workload assertion for short-lived credentials and impersonating an existing service account. We have not found a documented Hostinger Managed Hermes workload OIDC/SAML issuer, per-instance assertion mechanism or Google federation integration. WebUI login/OAuth capability is NOT evidence of an outbound workload identity provider. An arbitrary self-signed JWT would not establish a trusted identity.

Required evidence from Hostinger: issuer/discovery/JWKS, per-instance subject and audience, supported secure assertion acquisition and refresh within the managed environment. Do not obtain or print an actual assertion during this capability review.

If supported, prepare configuration in the EXISTING Google project: trust only the exact instance identity, audience and issuer; bind roles/iam.workloadIdentityUser narrowly on the EXISTING service account. No blanket pool impersonation, new service account or domain-wide delegation. All Google configuration/permission changes require the user's separate explicit approval. Use service account impersonation to preserve the existing Sheets Viewer identity; request only spreadsheets.readonly. Never claim direct federated IAM roles alone grant access to a Google Sheets file.

Storage: external-account configuration is not a private key but must have integrity protection. Keep assertion and Google access token in process memory where the supported credential source permits. Protect the credential source from arbitrary command/URL substitution. No token in CLI arguments, chat, logs or Git.

Revocation: stop adapter; remove the precise impersonation binding or disable the federation provider. Already-issued access tokens may persist until expiration. For urgent loss of access, remove the service account's Viewer sharing on the sheet or disable the service account after assessing other consumers; either is a separately approved permission change.

## Fallback: one user-managed JSON key on the EXISTING service account

Technically supported by installed google-auth and outbound HTTPS, but NOT approved or storage-validated yet. No key exists ready for use. Do not create/download a key merely to complete setup faster. Do not bypass an organization policy that disables key creation.

Before asking for key approval, verify a supported secure import path and private persistent storage outside /data/workspace, repository, skills, session files and downloadable WebUI artifacts. Candidate path /data/credentials/handyman-hermes-reader.json is only a proposal, not an existing verified secure mount. Require owner-only directory 0700 and file 0600, appropriate runtime ownership, no public serving, no broad runtime/tool access where separation is supported, and documented backup/restore handling. These controls do not isolate a key from an agent with arbitrary command execution under the same Unix identity; that residual risk must be explicitly accepted or a separate credential broker selected. Do not create a new broker/project within this task.

Hostinger Environments should hold only GOOGLE_APPLICATION_CREDENTIALS pointing to the protected file and non-secret reader settings. Do not place service-account JSON, private key, refresh token or access token in an environment variable or encode them as base64 to simulate protection. Hostinger's own skills guide distinguishes credential files from simple API-key environment settings. The dashboard masks values, but masking does not establish a secret vault, encryption guarantees or separation from the agent.

Creation/import, if later approved: human handles Cloud Console credential download and direct secure import on approved surfaces; never paste credential JSON into a chat or terminal command. Agent prepares code and paths without accessing credential contents, verifies only presence/permissions, and lets google-auth load the file internally. No screenshots of credentials, debug locals, HTTP headers or environment dumps. Remove temporary download copies using the approved procedure; account for managed backups and revoke old keys so restored copies cannot authenticate.

Least privilege: independently confirm Viewer only on the named existing spreadsheet; no Editor/Owner grants, unrelated file sharing, project data roles, domain-wide delegation or impersonation grants. Project IAM roles and Sheets file ACL are different controls. Adapter requests only https://www.googleapis.com/auth/spreadsheets.readonly and only the fixed spreadsheet/tab/bounded range. A private key itself is not scope-restricted: a holder can mint other scopes up to the service account's effective privileges. Viewer also permits reading the whole spreadsheet, not just 12 columns; bounded code reads are application controls, not an ACL boundary.

Reader tokens: created/refreshed by google-auth only after credential-use approval; held in memory, no manual token copying or persistent access-token environment variable. Header-only A1:AD1 probe first; return PASS/count/mismatch letters only. Approval for real records/Telegram delivery is separate. Production verification must include failure paths, actual adapter invocation by Hermes and permitted recipients before company data leaves the read process.

Revocation: stop adapter, disable the specific key, verify loss of new token minting, then delete the key when safe. Remove protected local copies and configuration; handle backups under Hostinger policy. Deleting/disable of a key does not revoke already-issued access tokens; urgent response may additionally remove sheet sharing or disable the service account with explicit user authorization. Key replacement/rotation is separately approved; retain no stale working key. Track key ID and lifecycle timestamps only, never key content.

## Current decision and next action

Do not request blanket approval for credentials yet. First confirm whether Hostinger provides workload identity federation, and if not confirm its supported secure credential-file import, persistence, backup access and serving restrictions. A concrete final approval must enumerate the chosen method, exact service account/project, permission changes, secret destination, managed restart, testing scope and revocation procedure. No changes to Apps Script public deployment or sheet sharing are proposed now.

Prepared question for Hostinger support (NOT sent): Does Managed Hermes instance aliceblue-quetzal-360983 support outbound OIDC/SAML workload identity suitable for Google Workload Identity Federation? If yes, provide issuer/JWKS documentation and the per-instance subject/audience/assertion acquisition method. If no, what supported mechanism securely imports a service-account JSON credential outside the WebUI workspace, limits runtime access, persists it across redeploys, and controls backup/restore and public serving? Do not include any credentials in the reply.

## Primary sources

- https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-other-providers
- https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys
- https://docs.cloud.google.com/iam/docs/keys-create-delete
- https://developers.google.com/identity/protocols/oauth2/service-account
- https://www.hostinger.com/support/how-to-manage-environment-variables-in-managed-hermes/
- https://www.hostinger.com/ca/tutorials/?p=145307
