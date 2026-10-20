# Read-only duplicate audit — 2026-10-20

User authorized investigation of duplicate job identifiers after the activation blocker. The count-only audit ran on the existing Hostinger instance against the real approved spreadsheet, using the existing service account and spreadsheets.readonly. Only columns A, R, AA and AD were read; no customer names, phones or notes were fetched. Two scans of the selected data matched. This is a sampled consistency check, not a transactional snapshot.

Observed sanitized result:

```json
{"status":"AUDIT_COMPLETE","rowsChecked":5199,"blankJobIdRows":4035,"duplicateGroups":137,"rowsInDuplicateGroups":690,"excessRowsBeyondOnePerId":553,"groupsIdenticalInSelectedFields":66,"groupsDifferentInSelectedFields":71,"groupsWithDifferentDate":0,"groupsWithDifferentStatus":0,"groupsWithDifferentRevenue":71,"comparedColumns":["A","R","AA","AD"],"fullRowEqualityVerified":false,"deduplicationPerformed":false,"readonly":true,"matchingReads":2}
```

Interpretation: 66 groups share the same date/status/revenue strings within each group; this does NOT prove the full rows are duplicates. 71 groups have different revenue strings; even these differences are not proof of distinct billable line items (blank-versus-value and formatting differences are included). No job identifiers, cell values or monetary totals are published. The 4,035 blank-ID rows were counted separately and not treated as one duplicate group. The 5,199 rows are nonempty in at least one selected field, not independently verified distinct service jobs.

Do not apply automatic deduplication, choose a first/last row, infer missing IDs or sum as distinct jobs. Source-owner guidance is required to determine the row's business unit and treatment of missing IDs. Both equal-looking and differing groups may represent multiple service items under one job. Pending job count and revenue require separate policies.

Activation remains off; no recipient pin or Hermes skill was installed and no Telegram report was sent. Sheets and existing manuals remain unchanged. Local offline suite: 41 tests passed. Remote installed audit code: e544aef. The count-only audit output is stored outside the repository on Hostinger at /data/workspace/handyman/duplicate-audit.json.
