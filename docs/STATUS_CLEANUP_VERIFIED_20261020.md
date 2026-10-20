# Status cleanup verified — 20 October 2026 (Asia/Bangkok)

## Completed changes

- Replaced the misleading initial README opening with current connection facts.
- Rewrote RESUME_HANDOFF.md as one coherent current handoff; preserved previous mixed history under docs/archive with an explicit historical label.
- Added docs/CURRENT_STATUS.md as the canonical current record, distinguishing live Sheets/private Telegram evidence from incomplete business reports and unverified Calendar/Drive/FlowAccount access.
- Marked the old Managed Hermes connection review as historical.
- Updated the existing Hermes skill to read the canonical status before claiming connection state.
- Researched official integration options and documented permission/storage limits in CONNECTION_EXTENSION_REVIEW_20261020.md.

## Verified on the actual existing Hermes instance

CLI requested login. Instead of requiring the owner to repeat login, used the already authenticated WebUI session and Hermes terminal tool. The clean existing checkout was fast-forwarded to afcf504. Hermes read CURRENT_STATUS.md and correctly distinguished connected Sheets from missing cross-source daily-review functionality.

Actual metadata inventory returned:

```json
{"status":"METADATA_INSPECTED","configPresent":true,"mcpServerEntries":0,"mcpConfigSectionPresent":false,"gwsOnPath":false,"gcloudOnPath":false,"googleWorkspaceSkillAtBundledPath":true,"flowNamedEnvironmentEntries":0,"sheetsCredentialPresentInProcess":true,"googleCalendarLiveAccessTested":false,"googleDriveLiveAccessTested":false,"flowAccountLiveAccessTested":false,"credentialValuesPrinted":false,"networkCalls":0}
```

The generic hermes executable was not on the agent terminal's PATH (exit 127, no install). Used the previously verified /opt/venv/bin/hermes absolute path, without installing software or changing PATH/security. Existing skill was replaced using its normal reinstall option; scanner returned SAFE / ALLOWED. Observed verification:

```json
{"install":{"status":"INSTALLED","verdict":"SAFE","decision":"ALLOWED","name":"handyman-readonly-queries"},"currentStatusReferencePresent":true,"hubSkills":[{"name":"handyman-readonly-queries","source":"url","trust":"community","status":"enabled"}]}
```

No credential values, new scopes, ACL changes, new integration credentials, Telegram sends, company-record reads or manual changes were performed in this cleanup. Local offline suite remains 44/44 passing. Metadata absence is not proof of all possible credential absence. Existing conversations may contain old messages; this change updates the documents and installed skill, not the past chat history.

## What remains

Calendar, Drive and FlowAccount are not claimed connected by this work. Their concrete resource/identity/storage/permission bundle must be resolved before authorization/provisioning. The useful daily-job-review output is still unimplemented; status cleanup is not delivery of that business workflow. Do not ask the owner to keep repeating unsupported daily-review questions.
