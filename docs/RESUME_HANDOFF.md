# Resume Handyman–Hermes integration

Read CURRENT_STATUS.md first. It is the single current status record. Do not infer live connection state from the initial README scaffold or archived reports.

## Verified as of 2026-10-20 (Asia/Bangkok)

- Existing Google service-account authentication works from Hostinger.
- Apps Script live header test passed 12 columns; public Web App stays mock-only.
- Hermes skill handyman-readonly-queries is installed/enabled. Direct private Telegram delivery was verified, including execution by Hermes itself.
- Generic python3 selected /usr/local/bin/python3 without Google libraries. Code c491a83 now re-executes the same script under the existing /opt/venv/bin/python3, preserving identity/environment and arguments. Exact legacy command returned SENT through Hermes. 44 tests passed on Windows and Hostinger.
- Only Handyman2026 / ข้อมูลการบริการ is connected. The reader fetches A/R/AA/AD; a successful count is not a job-quality audit or proof of other sources.
- Calendar, Drive and FlowAccount access from this Hermes instance is NOT verified. Connectors in Codex/ChatGPT do not automatically exist inside Hostinger Hermes.
- Pending output is still a limited row/ID summary. It does not include customer/service/next-action details. Date parsing rejected many rows; do not present dated top-ten output as a complete work queue.

## Owner scope already authorized

Use the existing project/account/credential only. Sheets reads and reports to the existing pinned private Telegram destination are approved. Pending = ไม่จบ; revenue = จบ. Include all service-row amounts, including repeated/blank IDs. Distinguish service-row counts from distinct jobs. No source writes, new scopes/sharing/IAM, public company-data endpoint, group delivery or cron is approved by this read-only integration.

## Locations

- Windows checkout: C:/Users/Wichaya/Handyman-Hermes-Work-20261012
- Original backup remains untouched: C:/Users/Wichaya/Handyman-Hermes-Backup
- Hostinger checkout: /data/workspace/handyman/readonly-adapter
- Instance: aliceblue-quetzal-360983
- Existing Script ID: 1KXQ0h_tNY9HcwFhQvC22ZS5xqXMoJ88OilIMx2xCUqnk26m3EJHHbuZe
- Spreadsheet ID: 1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q
- Existing service account: handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com
- Credential environment name: HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON. Never reveal/copy its value.

## Next work

1. Status cleanup is propagated to Hostinger and the installed skill; reference check true, SAFE/ALLOWED, enabled. See STATUS_CLEANUP_VERIFIED_20261020.md. Do not repeat this setup without evidence of regression.
2. Inspect existing integration metadata without secret values. Review CONNECTION_EXTENSION_REVIEW_20261020.md for researched paths and unresolved access/permission questions.
3. Prepare one daily-job review using actual approved sources; separate verified source facts, missing evidence and drafts. Existing read-only code is not full daily-job-review capability.
4. Get one concrete approval bundle before new Calendar/Drive/FlowAccount permissions or credential provisioning. Do not create projects/accounts, copy Codex tokens, assume SSH, or bypass a login/filter.

## Evidence and history

- HERMES_RUNTIME_FIX_20261020.md: reproduced interpreter failure and exact legacy-command SENT verification.
- TELEGRAM_ACTIVATION_20261020.md: installed skill, private delivery and boundaries.
- HOSTINGER_LIVE_HEADER_PASS_20261020.md: authenticated live headers.
- WINDOWS_PUSH_REVIEW_20261012.md: Apps Script push and mock endpoint evidence.
- Previous mixed handoff preserved at archive/RESUME_HANDOFF_before_cleanup_20261020.md; it is historical, not current instructions/status.

Do not ask the owner to repeatedly test an unchanged failure. Diagnose first, change the implementation, verify with the actual Hermes tool, then describe exactly what remains unverified.
