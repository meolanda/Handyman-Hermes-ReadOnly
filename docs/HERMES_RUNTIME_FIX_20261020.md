# Hermes runtime failure repaired — 2026-10-20

## Follow-up: legacy command compatibility verified

Owner's next Telegram invocation still failed at runtime_dependencies, consistent with continued use of the legacy generic-python command. Updating skill text alone was insufficient. Commit c491a83 adds an entry-point runtime selection: when running outside /opt/venv on POSIX and the fixed installed interpreter exists, os.execv restarts this same script with the same arguments and environment under /opt/venv/bin/python3 before Google-library imports. No shell, secret retrieval/copy, dependency installation or security-filter bypass is used. sys.prefix prevents restart loops despite shared interpreter symlinks. Windows and Hostinger suites each pass 44 tests.

Installed on the existing Hostinger checkout, then explicitly tested by Hermes WebUI terminal tool with the EXACT legacy command (not substituting an absolute Python path):

```text
python3 /data/workspace/handyman/readonly-adapter/scripts/hermes_queries.py --query pending --send
```

Visible real terminal-tool output:

```json
{"status":"SENT","query":"pending","rowsChecked":5217,"matchingReads":2,"readonly":true}
```

This repairs the generic-python command used by older sessions and verifies one new private report accepted by Telegram. The owner's subsequent incoming Telegram request remains a separate user-facing check; do not claim that was observed. No credentials, recipient, scopes or source data changed.

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
