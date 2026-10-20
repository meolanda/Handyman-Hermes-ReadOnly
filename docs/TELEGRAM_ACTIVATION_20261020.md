# Installed Hermes skill and verified private delivery — 2026-10-20

## Owner rules now applied

One job can contain multiple service rows. Include every row's amount, including repeated IDs and blank IDs. Revenue includes status จบ only. Pending service rows are status ไม่จบ; report row counts separately from distinct nonblank job IDs and missing-ID counts. Never silently deduplicate. These owner confirmations supersede the earlier duplicate-ID activation blocker.

## Observed installation and checks

- Existing Hostinger checkout clean before update, fast-forwarded to code commit 0af1c30.
- Official installed Hermes CLI used to install the reviewed SKILL.md from the pinned public repository commit. Scanner verdict SAFE, decision ALLOWED; no --force or scanner bypass used.
- `hermes skills list --source hub` lists handyman-readonly-queries as enabled (1 enabled, 0 disabled).
- The recipient pin was created outside Git at /data/workspace/handyman/readonly-recipient.json, restricted to mode 0600. It matches the single existing allowed Telegram user and existing home channel. No recipient ID, token or credential value is published.
- Delivery code revalidates both recipient settings and Telegram getChat type=private/id match before sendMessage, with redirects disabled and protected content.
- Windows and Hostinger offline Python suites each passed 42 tests.

## Real private-delivery evidence

Executed the fixed reader with --query pending --send, then --query revenue --send (default month in Asia/Bangkok). Each completed and the sanitized status files were read from CLI:

```json
{"status":"SENT","query":"pending","rowsChecked":5217,"matchingReads":2,"readonly":true}
{"status":"SENT","query":"revenue","rowsChecked":5217,"matchingReads":2,"readonly":true}
```

SENT means Telegram API accepted the message for the verified existing private destination; it does not prove the human read it. Full report text, job identifiers and monetary values were not printed to CLI or committed. Revenue report can contain an explicit incomplete/invalid-amount warning rather than a definitive total; delivery success is not independent validation of the financial result. The selected data count has changed since the earlier 5,199-row audit; do not treat that earlier count as a permanent fixture.

No spreadsheet edits, new credentials, permission changes, public Web App deployment or schedule were performed. Customer names/phones/notes are not fetched by this reader. Source remains ONLY the approved Handyman2026 tab ข้อมูลการบริการ, columns A/R/AA/AD, with 12-header validation and two matching selected-data scans (not a transactional snapshot).

## Remaining user-initiated check

The skill is installed/enabled and direct Sheets-to-private-Telegram delivery is verified. An incoming Telegram request selecting the skill has NOT yet been observed. Ask the owner to send `/handyman-readonly-queries มีรายการงานค้างอะไรบ้าง` in the existing private conversation; confirm Hermes invokes the reader and sends a fresh report. If the old session fails to discover the command, investigate skill discovery/session configuration instead of claiming production readiness. Do not blindly retry a send whose outcome is uncertain.

No general arbitrary-sheet Q&A, other tabs, Calendar or Drive capability is claimed. Skill dispatch reference: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
