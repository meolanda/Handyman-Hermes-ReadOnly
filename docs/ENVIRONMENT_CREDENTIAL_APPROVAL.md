# Concrete credential setup for approval

Prepared 2026-10-20. User selected retaining Managed Hermes and asked to prepare setup. This document does NOT record approval to create, download, import or use a key yet.

Preparation evidence: code commit 4f2bdd9 installed by clean fast-forward in the existing Hostinger checkout. Python mock tests passed 26/26 on Windows and Hostinger. No credentials entered, token issued, live probe run or managed redeploy performed during this preparation. These tests do not validate a real key or Environments propagation.

## Exact proposed change

Use only existing service account handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com in existing project handyman-hermes-reader (verify Cloud Console ID before creation). Independently review its IAM roles and existing spreadsheet sharing before provisioning; stop if broader access than intended is found. No new service account/project, domain delegation, sheet copy, sheet edits or public endpoint.

After explicit approval, create ONE JSON key for that existing account, have the user handle its direct download and entry into Hostinger's native Environments form for instance aliceblue-quetzal-360983. Environment name: HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON. Value: complete JSON, entered privately by the user, not through chat, CLI, screenshots, workspace upload or Git. Do not use base64 as security. No agent reading/unmasking or echoing the value. A key is a persistent secret; it is NOT itself limited to the adapter's OAuth scope.

Hostinger's human-reviewed support answer confirms Environments is supported, not that service-account JSON size/encoding has been live-tested. The user should confirm native entry preserves the JSON (including escaped private-key newlines); do not ask to share it for troubleshooting. If rejected by the form/runtime, stop and report sanitized failure rather than move the key into a workspace or command line. Do not automate new credential entry on behalf of the user.

Applying Environments requires one Save & redeploy and temporarily interrupts Hermes/Telegram. Approval must cover that interruption. Do not change other variables or reveal existing secret values. This credential is available to the whole instance's runtime, not isolated to one script. Hostinger cannot provide the requested backup exclusion; storage/backup copies remain within its managed boundary. User already selected this direction; final approval must expressly cover creation/import/use and restart.

## Code and initial test

scripts/hostinger_readiness.py now uses ONLY the named environment variable; the obsolete proposed private-file path is removed. Default invocation checks variable-name presence without retrieving/parsing its value, contacting Google or minting tokens. --live is opt-in after credential-use approval.

Live mode validates expected service-account email/project, service_account type and fixed Google token endpoint before library use. Only approved fields are passed to google-auth; only spreadsheets.readonly is requested. Tokens remain in process memory and refresh automatically through google-auth; no user refresh token is needed and no access token is persisted. Reads are fixed to the existing spreadsheet's ข้อมูลการบริการ!A1:AD1. Output includes PASS/count/mismatch column letters only. No company records, phone numbers or header values printed. Google library/HTTP debugging must remain off. Native Env access, same-UID processes or malicious code can still obtain the key; application guards do not solve that exposure.

Tests use invalid synthetic key text only and never authenticate to Google. Default no-token behavior, rejected identity/endpoint, malformed/oversized/duplicate JSON, field filtering, header normalization/duplicates and sanitized failures are covered. Real credential parsing, token issuance and live Hostinger environment propagation are not yet tested.

## Permission limits

Viewer on the intended spreadsheet only; inspect and do not silently alter ACL/IAM. No Editor/Owner or domain-wide delegation. A compromised key could access all resources the service account can access, not just this range. Scope and fixed range are application controls; Viewer prevents spreadsheet editing but does not prevent copying the spreadsheet. No company-record read, outgoing Telegram report or scheduled job is included in the initial header-test approval.

## Revocation and cleanup

Stop the reader, disable the specific key in Google Cloud, verify new token minting fails, then delete that key when safe. Remove the Hostinger environment variable through dashboard and redeploy; CLI removal is not permanent for dashboard-managed variables. User removes the local downloaded copy via the approved deletion process; do not put it in repo/OneDrive/shared folders. Revoked key copies in backups cannot mint fresh tokens, but backup controls and access must still be considered. Existing short-lived tokens are not revoked merely by disabling/deleting the key; urgent incident response may require disabling the service account or removing its sheet sharing, with explicit authorization and awareness of other consumers. No cleanup/revocation action is performed automatically by this proposal.

## One approval requested once prepared

Approve one key for the existing service account, private user-managed transfer to the exact Hostinger environment above, one Save & redeploy interruption, and in-memory token issuance limited by the code to spreadsheets.readonly for the A1:AD1 header probe only. Explicitly accept same-instance runtime and managed backup exposure. No approval inferred for public deployment, other IAM/ACL changes, record reads, Telegram sends or cron.
