# Installation status

Status: BLOCKED — real Google Sheets read and Hermes execution on Hostinger have not been verified.

Baseline: faa1e0f6d8d9172ac3ee6ec73b510e5bd36e28e4. Existing Apps Script and scripts.run client retained unchanged.

## Decision

Prefer direct Google Sheets API: no Apps Script deployment, no shared Apps Script/OAuth project requirement, one spreadsheets.readonly scope. Existing scripts.run requires API Executable deployment, script ID and OAuth scopes of the script; none is configured yet. Direct API still requires an authorized identity with access to this sheet. No anonymous or public sheet access is assumed. No credentials were created.

New DirectSheetsClient performs only GET values requests, blocks redirects, uses FORMATTED_VALUE, maps configured headers and sanitizes errors. Token acquisition/persistence remains outside this client. Existing Config files are unchanged. Live probe uses all 12 supplied fields in memory and A1:AD100; source headers are not independently confirmed until a live request succeeds.

## Evidence

- GitHub main baseline verified by fetch and ls-remote.
- Mock tests: Python 16, Apps Script 16 passed (32 total). These are not live evidence.
- Managed environment reports no configured secret or outbound identity bindings; identity manifest connections list is empty.
- GOOGLE_APPLICATION_CREDENTIALS name and file presence checked without reading credential contents. Standard google-auth ADC loader attempted with spreadsheets.readonly: DefaultCredentialsError. SDK installed only in /tmp for diagnosis.
- Live probe exits 2 with BLOCKED: Google read-only access token unavailable. No fallback to mock.
- No Hostinger endpoint/user/identity exposed by configured tools or relevant variable names. Common agent/workspace SSH config paths absent. Hostinger SSH has not been attempted because destination and authorized identity are unknown.
- Google API destinations are absent from the current network allowlist; prior Google documentation request was denied with proxy 403. Current Google API reachability is untested; network permission must be configured before a live test.
- No remote production installation/deployment or Hermes configuration changes performed.

## Pending access and validation

User must provide a secure authorized access path for this Workspace to Google (read-only identity usable for Sheets API) and Hostinger (host, user, approved SSH identity, known-host verification and permitted network route). Do not paste tokens, keys or passwords in chat. Existing connected Drive chat credentials are not available to this runtime.

After access is provisioned: run live probe; verify actual headers and rows; inspect Hermes version/interface on Hostinger read-only; prepare isolated adapter installation and exact change for approval; activate on Hostinger only after production approval; invoke through Hermes and retain sanitized evidence. A live probe alone does not establish Hermes integration.
