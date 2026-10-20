# Hermes runtime failure repaired — 2026-10-20

## Reported failure

Owner's incoming Telegram invocation selected the skill but returned BLOCKED at the old combined credentials stage with QUERY_OR_DELIVERY_FAILED. That error alone did not establish a bad key, and no automatic send retry was attempted.

## Reproduced cause

Using the real Hermes WebUI terminal tool, a presence-only diagnostic returned:

```json
{"command1":{"python":"/usr/local/bin/python3","credentialPresent":true,"googleAuthAvailable":false,"requestsAvailable":false,"dotenvAvailable":false,"tokenIssued":false,"liveReadAttempted":false},"command2":{"status":"READ_VERIFIED","query":"pending","rowsChecked":5217,"matchingReads":2,"readonly":true}}
```

Command1 used generic python3 with query_runtime_check.py. Command2 used /opt/venv/bin/python3 with hermes_queries.py --query pending, without --send. The corrected interpreter's diagnostic also confirmed Google auth, requests, dotenv and credential presence. No secret values were parsed by the diagnostic or displayed. The problem was interpreter selection/missing dependencies, not missing credentials.

## Repair and verification

Code commit 4b8ae27 pins the skill's query commands to /opt/venv/bin/python3. It separates runtime dependency, credential presence, parse/load and schema stages into sanitized diagnostics. No library install, credential creation/copy, environment filtering bypass, permission change or restart was required. Offline suite still passes 42 tests.

The existing skill was reinstalled from the pinned reviewed GitHub source through the installed Hermes CLI. Existing-name replacement required its --force reinstall flag; security scan still ran and returned SAFE / ALLOWED, with no blocked verdict overridden. Installed skill content now uses the absolute interpreter path.

Then Hermes itself, through its WebUI terminal tool, executed exactly once:

```text
/opt/venv/bin/python3 /data/workspace/handyman/readonly-adapter/scripts/hermes_queries.py --query pending --send
```

The visible tool output (not merely the model's narrative) was:

```json
{"status":"SENT","query":"pending","rowsChecked":5217,"matchingReads":2,"readonly":true}
```

This verifies Hermes tool execution → Google Sheets → pinned private Telegram delivery. It does not prove the human read the message. Re-test the owner's incoming Telegram slash request against the updated skill to confirm that surface uses the new instructions rather than old session content. The previous incoming failure is preserved as historical evidence, not treated as success.

No customer data, monetary values, tokens or credential contents were logged in this evidence. Read-only scope, fixed source and recipient guards remain unchanged. The WebUI diagnostic conversation is retained for inspection; no source Sheets or manuals were modified.
