# Resume Handyman–Hermes integration

## Current verified state — 2026-10-20

LATEST FIX: Owner's Telegram request failed in old credentials stage. Reproduced inside Hermes: generic python3 resolves /usr/local/bin/python3 without Google auth/requests/dotenv, despite credential presence. Correct /opt/venv/bin/python3 returned READ_VERIFIED. Skill pinned/reinstalled at 4b8ae27, SAFE/ALLOWED scan. Hermes WebUI terminal tool then ran corrected pending --send once and visibly returned SENT (5217 rows, two matching reads, readonly). See HERMES_RUNTIME_FIX_20261020.md. Next owner can retry incoming Telegram slash request; do not recreate keys or broaden scopes. No blind retry of uncertain delivery.

LATEST: Owner confirmed summing every service row including repeated and blank IDs. Applied in 0af1c30, installed on Hostinger. Hermes skill handyman-readonly-queries installed via supported CLI, SAFE scan, listed enabled. Private recipient pinned outside repo (0600). Pending and current-month revenue each returned SENT, rowsChecked=5217, matchingReads=2, readonly=true. 42 tests pass on Windows and Hostinger. See TELEGRAM_ACTIVATION_20261020.md. Duplicate/blank-ID blocker below is historical. Still verify OWNER-INITIATED incoming Telegram skill request; direct script delivery is proven but natural-language/skill dispatch from Telegram is not yet observed. Do not recreate credentials/restart or repeat existing approvals. Source remains one tab; other tabs/Calendar/Drive are not connected.

LATEST DUPLICATE AUDIT: User authorized read-only follow-up. Two selected-field scans matched: 5,199 nonempty selected-field rows, 4,035 blank job IDs, 137 duplicate-ID groups (690 rows). 66 groups have equal date/status/revenue strings; 71 differ in revenue strings. Neither finding establishes full-row duplication or legitimate line-item semantics. No automatic deduplication or delivery. See DUPLICATE_AUDIT_20261020.md. Source-owner rules for row versus job counting and blank IDs are required before activation.

LATEST ACTIVATION RESULT: User approved exact statuses (pending ไม่จบ, revenue จบ) and delivery to their existing private Telegram chat. Query reader installed on Hostinger at bc9c216; 39 offline tests passed there. Live record read STOPPED with allowlisted reason Duplicate job IDs at read stage. No two-scan complete-data PASS, Telegram delivery or skill activation. Do not repeat approval for the existing authorized scope; next obtain the duplicate-job business rule or source-owner correction. Do not silently deduplicate or edit Sheets. See ACTIVATION_CHECK_20261020.md. No private recipient pin was created.

Offline follow-up: analysis.py now prepares callback pagination, normalized header mapping, date-sorted masked job results and Decimal monthly totals with explicit statuses and skip counts. All 34 Python tests pass in UTF-8 mode. See PYTHON_QUERY_PREPARATION.md for activation gates and privacy limitations. This code has not been installed or activated on Hostinger; no record reads or Telegram sends occurred. Do not infer real-data authorization from offline preparation approval.

This update supersedes the historical blockers and unapproved-credential statements below. The user explicitly approved the existing service-account key, private Hostinger Environments entry, apply/restart and header-only live probe. The user completed credential entry. Hostinger CLI now returned PASS, columnsChecked=12, mismatches=[], readRange=A1:AD1, readonly=true against the real spreadsheet. See HOSTINGER_LIVE_HEADER_PASS_20261020.md for exact sanitized evidence. No business-record read, Hermes query registration, Telegram delivery or schedule is active. Next agree the business-query/data-delivery scope and validate the Python privacy/aggregation layer before activation. Do not repeat credential creation or restart on resume.


Latest support result (2026-10-20, message 11:19 reviewed by Marijus): Managed Hermes has no outbound Google WIF and no supported credential-file import/custom path with backup exclusions. Supported secrets surface is Environments; runtime/CLI access and daily backup exposure must be accepted explicitly before any credential provisioning. No key, restart or migration approved. See HOSTINGER_SUPPORT_20261020.md for the received answer. Prior private-file setup proposal is NOT supported by this managed product per Support.

Support follow-up 2026-10-20: user authorized sending the prepared question. Submitted in hPanel, requested human review and submitted technical context. UI shows Marijus is reviewing your request; no case ID or final technical answer yet. Retained hPanel browser tab. See HOSTINGER_SUPPORT_20261020.md. No credential or configuration actions authorized/performed by this inquiry.

Latest setup: 2026-10-20 — CLI is working again. Existing remote adapter updated to 1c45036. Default credential-free preflight installed and returned CREDENTIAL_NOT_PROVISIONED, tokenIssued=false, liveReadAttempted=false. Hostinger Python tests passed 22/22. See HOSTINGER_PREFLIGHT_SETUP_20261020.md. Credential provisioning and activation still require the previously specified method/storage review and approval.

Latest resumed inspection: 2026-10-20 — see RESUME_CHECK_20261020.md. WebUI opens, but Gateway/MCP status remains Loading and browser CLI shows no prompt after one reload; no remote command executed. No credentials or configuration changed. Next restore supported dashboard/CLI access and obtain Hostinger authentication/storage capability confirmation.

Saved at user's request on 2026-10-12 (Asia/Bangkok). Work stops here until the user returns. No automation or background monitoring requested.

## Locations and identities

- Repository: https://github.com/meolanda/Handyman-Hermes-ReadOnly
- Original reviewed PR: https://github.com/meolanda/Handyman-Hermes-ReadOnly/pull/2
- Working branch: fix/windows-readonly-push-review-20261012
- Windows checkout: C:/Users/Wichaya/Handyman-Hermes-Work-20261012
- Untouched original backup: C:/Users/Wichaya/Handyman-Hermes-Backup
- Local ignored snapshots: remote-before/ and remote-after/. .clasp.json is ignored; never copy OAuth credentials to Git/chat/Hostinger.
- Sole approved Apps Script ID: 1KXQ0h_tNY9HcwFhQvC22ZS5xqXMoJ88OilIMx2xCUqnk26m3EJHHbuZe
- Google user observed in clasp/editor: wichaya.s@dif2020.com
- Spreadsheet: 1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q; tab ข้อมูลการบริการ.
- Managed Hostinger instance: aliceblue-quetzal-360983.
- WebUI: https://aliceblue-quetzal-360983.hostingersite.com/
- Supported browser CLI: https://aliceblue-quetzal-360983.hostingersite.com/cli
- Remote staged source: /data/workspace/handyman/readonly-adapter, cloned at b9b1634. Later documentation commits are on GitHub and have not been pulled remotely.
- Existing Google project display name supplied by user: Handyman-Hermes-Reader. Service account: handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com. Verify project ID rather than using display name for mutations.

## Completed and verified

User explicitly approved the two-file Apps Script source replacement and OAuth limited to spreadsheets.readonly. Push succeeded; independent pullback matched source and parsed manifest. Public version 1 deployment was not changed and repeatedly returned exactly mock JSON. No sheet edited.

User completed Google authorization personally. Actual editor log on 2026-10-12 at 22:45:26–22:45:27 showed:

```json
{"status":"PASS","columnsChecked":12,"mismatches":[],"readRange":"A1:AD1","readonly":true}
```

The S header is สรุปงานอาการเสีย และ หมายเหตุ. Local service schema and synthetic fixture were updated to that verified value. Local tests: Node 21/21 and Python 16/16. Windows Python requires UTF-8 mode for Thai fixtures. CLI scripts.run returned NOT_FOUND; it is not the successful execution route. No API Executable deployment was created.

After user logged into Hermes WebUI, authenticated inspection confirmed WebUI v0.52.113, Agent 0.21.5, Python 3.13.16, google-auth present; no MCP servers configured. gws/gcloud absent in PATH. Hostinger restricted shell help listed python3 and git, which were used without bypassing shell restrictions. Remote adapter mock tests passed 16/16. Source is staged, not registered or activated as a Hermes reader.

Remote Google ADC check returned UNAVAILABLE. Standard credential paths checked were absent; only matching Google/GWS/Handyman environment variable name observed was HANDYMAN_TEST_ENV (value never read). No live Sheets request from Hostinger occurred.

Existing remote /data/workspace/handyman/AGENTS.md and Handyman-Agent-Manual.md were read and not modified. Read/analyze authorized data is permitted; production writes and external business actions require approval. Do not create cron, edit manuals or invent business facts. Re-read applicable instructions before remote changes on resume.

## Latest user-provided account facts

User states the existing service account has Viewer access to Handyman2026, its Cloud Console Keys page shows no service-account key, and there is no confirmed Google credential in Hostinger Environments. These facts are user-reported; do not present them as an independently audited ACL/IAM/key inventory.

Use this existing service account; do not create a replacement. Do not create/download/send a key or token without approval. Before credential actions, present storage, least-privilege and revocation details.

## Current blocker and concrete next steps

No usable Google identity exists on Hostinger in the paths inspected. Apps Script user consent does not provision Hostinger identity. Public mock endpoint is not a company-data integration.

1. Verify whether Hostinger supports per-instance outbound workload OIDC/SAML identity suitable for Google Workload Identity Federation. No evidence establishing support has been found; absence of documentation is not proof of impossibility. Do not confuse inbound WebUI OAuth with outbound workload identity.
2. If supported, prepare tightly scoped federation/impersonation of the existing service account within the existing Google project; permission changes require explicit approval. Keep tokens short-lived and in memory.
3. If unsupported, verify Hostinger's supported secure private credential-file import, isolation, persistence, public-serving boundaries and backup handling BEFORE asking for approval for a service-account JSON key. Proposed /data/credentials path is not validated. Environments should store only the file path, not private-key JSON/token. Owner-only file permissions do not isolate secrets from an agent sharing the Unix identity; disclose that limitation.
4. Once the chosen method and exact changes are reviewable, obtain credential/permission approval. No blanket approval currently exists for this stage.
5. Run a header-only live probe on Hostinger, then validate the actual Hermes invocation. Company-record range and Telegram recipients/record delivery require explicit authorized scope. Do not treat staged tests or header PASS as production readiness.

Prepared Hostinger support question is in SERVICE_ACCOUNT_AUTH_PROPOSAL.md; it has NOT been sent. No authority to send support messages was given.

## Hard constraints

No new Google project or service account. No changes to Handyman2026 or other Apps Script projects. No real-data Anyone/public Web App deployment. No sharing/IAM changes without approval. No credential/token values in chat, logs, GitHub, screenshots, CLI command text or artifacts. No SSH assumption, security bypass, restricted-shell escape, Hostinger restart/redeploy or cron without the appropriate authorized scope. No token copying from Windows clasp.

## Evidence index

- WINDOWS_PUSH_REVIEW_20261012.md: push, live 12-column PASS and mock endpoint evidence.
- MANAGED_HERMES_CONNECTION_STATUS.md: authenticated remote inspection and mock tests.
- SERVICE_ACCOUNT_AUTH_PROPOSAL.md: authentication options, storage requirements, risks, revocation and primary sources.
- Key commits: e1df469 preparation; 996d755 push evidence; ba1de1b live PASS; acac02f schema; b9b1634 UTF-8 validation; 0db19fc Hostinger evidence; c4d8497 authentication proposal.

On resume, start from this file and those three evidence documents. Check git status and current remote state before changing anything. Browser login may expire; ask the user to sign in directly if needed, never request passwords/tokens in chat.
