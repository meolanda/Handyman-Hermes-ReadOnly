# Handyman Hermes — controlled GitHub → Apps Script source push

## Scope
This preparation is **not yet connected** to Google. It is deliberately manual-only, not automatic on every commit. Only `webapp/Code.gs` and `webapp/appsscript.json` are pushed to the *existing isolated* Apps Script project when the workflow is deliberately run.

The public `doGet()` remains the same **mock-only JSON response**. The separate `testReadHeaders()` function can be executed **only from the Apps Script editor** for read-only header checks `ข้อมูลการบริการ!A1:AD1`. It neither publishes data nor writes Sheets. No customer rows are output. Existing `apps_script/` and Direct API code are untouched.

**Important:** `clasp push` replaces the **entire editor source** of the target Apps Script project. It does not create a new version or update a deployed /exec URL automatically. Use this only for the isolated new project, never the original Handyman Web App. Before first use, save a copy of any manual changes in the target editor and confirm the target Script ID. Do not use a public-production deployment for customer data.

## One-time prerequisites (human action required)
1. In Google Apps Script user settings, enable **Google Apps Script API** if it is disabled.
2. Sign in locally to official `@google/clasp` with the Google account that owns the **isolated Apps Script project**. Use the official `clasp login` interactive browser flow, not pasted credentials in ChatGPT.
3. On GitHub, configure a protected GitHub Environment called `apps-script-staging` with required reviewer approval.
4. In **that environment** set variable `HANDYMAN_SCRIPT_ID` to the isolated project's Script ID from Project Settings (not the /exec deployment ID).
5. In **that environment**, set secret `HANDYMAN_CLASP_AUTH_JSON` with the clasp OAuth auth JSON **using GitHub's secret-entry form only**; never paste it into chat, commit, issue, or screenshots. The OAuth credentials represent your Google login and should be treated as highly sensitive. A keyless / federation approach is preferable if supported in a future design.
6. Review this branch/PR and merge only after reviewing the source and expected script target.

## Explicitly start a push
Actions → **Push isolated Apps Script source (manual only)** → Run workflow → type `PUSH_STAGING_ONLY`. The protected environment may require a reviewer. The action checks the target variable and auth secret; without them it fails safely. No `clasp create-deployment` is executed.

## Validation gate
- First verify the existing public /exec deployment still returns mock JSON.
- In the Apps Script editor run **testReadHeaders**, review requested Google consent: Sheets read-only, no write scope. Check execution log for `PASS` and 12 columns; stop on `NEEDS_REVIEW`.
- Do **not** redeploy a public Apps Script endpoint with Sheets data. A separate authentication and access-control design is mandatory before any public response includes business information.
- The owner account remains a higher-privilege identity even when the OAuth scope of this particular script is read-only.

## Alternatives and limitations
This GitHub Actions method requires an OAuth auth JSON secret (not the existing Viewer service account's JSON key). Google Apps Script API deployment with clasp is a **different permission path** than Google Sheets access. No GitHub Action can create Google login permissions on its own. If storing OAuth refresh credentials in GitHub Secrets is unacceptable, do **not** configure the workflow; use clasp locally with the authorized Google login and push manually instead.

Original project GitHub: https://github.com/meolanda/Handyman-Hermes-ReadOnly
