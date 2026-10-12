# Windows installation review — 2026-10-12

State: SOURCE PUSH DONE; live header verification BLOCKED at Google authorization dialog.

## Approved push outcome

- User explicitly approved source push and OAuth limited to spreadsheets.readonly in this chat.
- Immediately before push, remote baseline was pulled again and the backup hash still matched. Manifest remained unchanged from the inspected baseline.
- clasp push --force returned Pushed 2 files: appsscript.json and Code.gs, for the sole approved Script ID. No deployment command was run.
- Independent pull into ignored remote-after/ returned exactly appsscript.json and Code.js (clasp's local extension normalization). Source comparison ignoring line endings passed; parsed manifest comparison passed.
- Deployment listing after push remained HEAD and version 1, with the same deployment IDs. Public version 1 endpoint was probed again and returned mode=mock, service=Handyman-Hermes-Test.
- clasp run testReadHeaders returned a storage NOT_FOUND exception, despite shell exit code 0. This is NOT evidence of successful execution or live header validation. No API Executable deployment was created to work around this.
- The actual Windows Chrome editor was opened to the exact approved Script ID. Title: Handyman-Hermes-ReadOnly. Signed-in UI account matched wichaya.s@dif2020.com; Sheets service and uploaded Code.gs were visible.
- testReadHeaders was selected and Run clicked. Google displayed its authorization-required dialog. No live PASS, count result or mismatches have been produced. No permission was granted by the agent.
- Windows computer-use instructions prohibit automation of user authentication dialogs and security/privacy permission requests; the dialog was left for the user to complete. No credentials or token material was read, output or committed.

Next user action: in the existing Chrome editor dialog, review authorization using the intended account and allow only Sheets read-only if that is the sole requested data scope. Stop if broader access, administrator intervention or security bypass is requested. Then rerun testReadHeaders and retain only sanitized result metadata. Hermes real-data integration remains pending and production readiness is not claimed.

## Verified target and baseline

- Repository: meolanda/Handyman-Hermes-ReadOnly; PR #2 head 6235e363b9732236505ac97bdb588ff73172f9f7.
- Local clasp 3.4.1 authenticates as wichaya.s@dif2020.com. Successful source pull proves access to the specified project, not independent proof of project ownership or sheet access.
- Sole approved target: 1KXQ0h_tNY9HcwFhQvC22ZS5xqXMoJ88OilIMx2xCUqnk26m3EJHHbuZe.
- Backup untouched: C:/Users/Wichaya/Handyman-Hermes-Backup. Separate checkout: C:/Users/Wichaya/Handyman-Hermes-Work-20261012.
- Latest remote source saved locally in ignored remote-before/. Remote รหัส.js and backup รหัส.js SHA256: 58A2F1CB5C0A1FC8FC6C8FA10AF42DDB3359A2E38A55B69B99D3469623CD8E4E.
- Existing version 1 deployment HTTP probe returned exactly the four expected mock fields, with mode=mock. No business values were returned.

## Exact source replacement proposed

clasp status selects ONLY webapp/Code.gs and webapp/appsscript.json. Local .clasp.json is excluded from upload and Git.

Remote รหัส.js will be removed/replaced by Code.gs. Remote appsscript.json will be replaced. This is a complete two-file editor source replacement; no other source files exist in the pulled baseline.

- doGet preserves the backup mock response and cannot dispatch a live read, including via query parameters.
- testReadHeaders uses only Sheets.Spreadsheets.Values.get with FORMATTED_VALUE and the fixed range 'ข้อมูลการบริการ'!A1:AD1. It logs only PASS/NEEDS_REVIEW, 12-count, mismatch column letters, range and readonly flag. Upstream exception details are suppressed.
- Manifest enables Advanced Sheets v4 and explicitly declares only https://www.googleapis.com/auth/spreadsheets.readonly. It does not request a public webapp deployment. Existing immutable version 1 is not redeployed.
- No deploy, redeploy, API enablement, sharing, sheet changes, credential creation or permission changes performed.

## Validation and unresolved items

21 Node tests pass, including bounded read, mock isolation, sanitized failures and manifest restrictions. These tests use synthetic values, NOT the live sheet.

PR expects S = สรุปงานอาการเสีย และ หมายเหตุ; existing schema/fixture expects สรุปงานและหมายเหตุ. The test explicitly flags the old fixture as mismatch S. Actual sheet headers must be checked after approval; do not weaken validation or alter the sheet to force PASS.

After approval, re-pull and compare the remote baseline, verify the target ID and two-file upload list again, push only this project, then pull back to verify source. Execute testReadHeaders in the authenticated editor if possible. Any Google consent must remain within the separately approved readonly scope; stop on broader consent or unsupported API setup. Record only sanitized result metadata on GitHub.

Hermes currently has only mock connectivity evidence supplied by the user. Real-data integration still requires an authenticated private read path, authorized identity, bounded data mapping, and end-to-end Hostinger verification. A source push or header PASS alone does not establish production readiness.

Scope references: https://developers.google.com/workspace/sheets/api/scopes and https://developers.google.com/apps-script/advanced/sheets.
