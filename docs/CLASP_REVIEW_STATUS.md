# Clasp push preparation — BLOCKED, not pushed to Google

Reviewed PR #2 head: 6235e363b9732236505ac97bdb588ff73172f9f7.

Runtime is Linux cloud, not the user's Windows machine. `command -v clasp` returned no executable; local ~/.clasprc.json absent. Windows backup path is not mounted under /mnt/c/Users/Wichaya/Handyman-Hermes-Backup. No Windows remote-execution tool is available. Therefore Google login/account, remote Script ID ownership, target editor source, backup contents and public deployment response have NOT been verified. No credentials were inspected or copied.

Prepared source is in webapp/Code.gs and webapp/appsscript.json; local isolated staging is /workspace/Handyman-Hermes-Clasp-Staging. Its .clasp.json names exactly 1KXQ0h_tNY9HcwFhQvC22ZS5xqXMoJ88OilIMx2xCUqnk26m3EJHHbuZe, rootDir webapp. This records the intended destination, not proof of access or ownership. Proposed push source files are Code.gs and appsscript.json only. clasp push replaces the entire target project source, so extra remote files could be removed; remote file list and backup must be verified before approval.

PR #2 used SpreadsheetApp under spreadsheets.readonly. Prepared version uses Sheets.Spreadsheets.Values.get with FORMATTED_VALUE instead, declares advanced Sheets v4, and retains only spreadsheets.readonly scope. No sheet-write operation exists. doGet mock response is preserved. testReadHeaders outputs only PASS/NEEDS_REVIEW, counts and mismatch column letters. Internal API error messages are sanitized.

PR #2 expects S = สรุปงานอาการเสีย และ หมายเหตุ, whereas the earlier supplied schema says สรุปงานและหมายเหตุ. This preparation retains PR expectation without claiming either matches live data. Verify during authorized live header read; never silently accept mismatches.

Mock verification: Python 16, Node 21, total 37 passed; no skips or failures. These do not establish a live read. No clasp push, Google consent, permission change, deployment or production activation occurred. The PR GitHub Actions workflow was not copied, enabled or triggered.

Next prerequisite: attach an authorized local Windows execution session with access to the existing clasp login and backup. Then verify account/target/backup, pull remote source into a separate inspection directory, enumerate replaced/removed files, and request one concrete approval before push. If enabling Sheets API is also needed, include that permission/configuration action in the same review. After approval push only to the exact Script ID, run testReadHeaders with the authorized account, record sanitized live evidence, and check existing public doGet still returns mock. Executing via scripts.run may require API Executable configuration; do not assume clasp can execute arbitrary editor functions without it.

Hermes real-data integration remains pending authentication/access-control design. Source push alone does not update an existing versioned deployment or establish production readiness. Never deploy sheet-reading responses as Anyone.
