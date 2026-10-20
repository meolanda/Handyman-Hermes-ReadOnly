# Hostinger live header verification — 2026-10-20

## Verified result

The existing Managed Hermes instance `aliceblue-quetzal-360983` successfully read the real Google Sheets header using the existing service account. Browser CLI output was observed directly:

```json
{"status": "PASS", "columnsChecked": 12, "mismatches": [], "readRange": "A1:AD1", "readonly": true}
```

Command executed from the authenticated Hostinger CLI:

```text
python3 /data/workspace/handyman/readonly-adapter/scripts/hostinger_readiness.py --live > /data/workspace/handyman/header-probe-result.json
cat /data/workspace/handyman/header-probe-result.json
```

The result file contains only the sanitized JSON above, not credentials, tokens, header values or customer records. An earlier invocation lost the CLI connection and its outcome was not observable; the recorded invocation above completed and was verified.

## Authorization and boundaries

The user explicitly approved one key for the existing account, private entry into Environments, restart to apply, and a header-only test. The user created/downloaded the JSON and entered it privately. Apply changes was submitted; subsequent credential-free preflight confirmed the environment variable was present, with tokenIssued=false and liveReadAttempted=false. Live mode then authenticated successfully.

- Existing project: `handyman-hermes-reader`.
- Existing account: `handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com`.
- Environment name: `HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON`; value was never revealed or copied into chat, CLI commands or Git.
- Fixed spreadsheet: `1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q`.
- Fixed tab/range: `ข้อมูลการบริการ!A1:AD1`.
- Requested OAuth scope: `https://www.googleapis.com/auth/spreadsheets.readonly`.
- No spreadsheet writes, IAM/sharing changes, new service account/project or Apps Script deployment were performed in this verification.

This confirms credential propagation, successful Google authentication and the 12 selected header mappings. It does not independently audit every IAM/ACL grant. The service-account key remains accessible to programs in the instance and subject to Hostinger managed backups, as previously disclosed.

## Remaining integration work

Header PASS is not production readiness. Hermes has not yet been connected to business-record queries or authorized Telegram delivery. Next define the permitted questions, row/column boundaries, recipients and revenue/status rules; review the Python pagination, phone masking and Decimal aggregation before authorizing record reads. Do not enable schedules or expose company data through a public Web App. The existing public mock deployment was not changed by this test; its endpoint was not rechecked during this verification.

For revocation and cleanup, follow `ENVIRONMENT_CREDENTIAL_APPROVAL.md`; no key revocation or downloaded-key deletion was performed.
