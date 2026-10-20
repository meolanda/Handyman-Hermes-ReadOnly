# Activation check — 2026-10-20

## Authorization received

User confirmed activation scope: pending jobs are exactly status ไม่จบ; revenue is exactly status จบ; destination is the existing owner's private Telegram chat, with phone protection. This supersedes earlier statements that record reads and private delivery lacked approval. No schedule, group delivery, spreadsheet writes, IAM change or public deployment is authorized.

## Implemented and installed

Added scripts/hermes_queries.py and a proposed Hermes SKILL.md. Existing Hostinger checkout was clean and fast-forwarded to bc9c216. Windows and Hostinger offline suites passed 39 tests before live inspection; final diagnostic changes were rechecked locally. No new package, credential, project or service account was created.

The reader gets the live grid row bound, checks all 12 headers, and reads only A (date), R (status), AA (service revenue), AD (existing job ID) in bounded pages. It does not fetch customer names, phones or notes. Two matching scans are required, with no claim of transactional snapshot consistency. Duplicate nonblank job IDs block output rather than silently deduplicating or counting twice. No raw records are logged or persisted.

Delivery code verifies the pinned destination matches both existing allowed-user and home-channel settings, verifies Telegram getChat returns that same private chat, and sends directly without exposing business values to the model. Recipient ID/token values are not included in this report or Git. The pin file has NOT been created and delivery has NOT been invoked.

## Observed live blocker

The authorized live read returned the sanitized diagnostic:

```json
{"status":"BLOCKED","reason":"Duplicate job IDs","stage":"read"}
```

This is a real-sheet observation, not an Excel inference. No duplicate identifiers, record values or amounts are included in evidence. The duplicate condition occurred before completion of the two-scan verification, so no full-data PASS or accurate job/revenue count is claimed.

No Telegram report was sent. The proposed skill was NOT installed in /data/skills and activation remains off. Existing Google header PASS remains valid evidence for authentication only. No changes were made to the source spreadsheet, public mock deployment or existing manuals.

## Next action

Agree how duplicate job IDs should be treated, or have the data owner correct them through their normal process. Do not choose one duplicate by row order/date, delete rows, or merge amounts without an approved business rule. Keeping the reader blocked is the default. Once resolved, rerun complete reads, create the private recipient pin, verify delivery once, install the skill through the supported Hermes mechanism and validate an owner-initiated Telegram query. Do not report activation successful until that flow is observed.

Hermes skill format/discovery reference: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
