# Hostinger support inquiry — 2026-10-20

## Human-reviewed answer received

Read in authenticated hPanel conversation on 2026-10-20; displayed message time 11:19, Response reviewed by Marijus. The UI states:

- Managed Hermes does not currently support per-instance outbound identity through Google Workload Identity Federation.
- No supported custom credential-file path/import mechanism that excludes the service-account JSON from backups.
- Supported secret storage is the dashboard Environments section, masked in UI; applying changes requires Save & redeploy.
- Application is backed up daily; CLI can access instance environment. Anything stored in the instance should be treated as readable by anything running there.
- Hostinger suggested a Hermes VPS for server-level credential/backup control. This is an alternative offered by support, not an approved migration, purchase or evidence that a VPS alone solves same-user access.

This is product-specific human-reviewed support guidance, not an independently tested guarantee. No credentials created, no settings changed, no deployment/restart performed in response.

The earlier plan to provision a private credential file with backup exclusions is not supported on this Managed offering according to this answer. Do not provision that proposed path or treat local chmod as an isolation boundary.

Next decision: either retain the existing Managed instance and explicitly accept its shared-runtime/backup exposure before designing an Environments-based credential flow, or pause real-data integration while evaluating an alternative approved authentication/execution boundary. No approval to migrate, create new projects or service accounts, or provision any key is inferred. An Environments JSON-key flow would be a change from the prior file-only proposal and needs explicit approval after the concrete flow and revocation controls are prepared. Never place raw keys in this chat, CLI command text, Git or support messages.

User explicitly approved contacting Hostinger Support. Inquiry sent through authenticated hPanel Hostinger Agent. No secrets, sheet records, passwords, key material or tokens transmitted. Instance identifier and technical requirements only.

Questions: whether Managed Hermes supports outbound per-instance OIDC/SAML for Google Workload Identity Federation; official issuer/JWKS and subject/audience/assertion documentation; otherwise supported private credential-file import outside workspace/Git/artifacts with access isolation, persistence, serving restrictions and backup exclusions; managed support for required_credential_files and terminal.credential_files, including same-UID limitations.

Message explicitly prohibited credential creation, configuration changes, purchases, restarts and redeploys. Existing service account's Viewer access and absence of a key were described as supplied by the user; no account secrets or Google account access delegated.

Hostinger Agent replied that available product documentation does not confirm these features and did not provide a supported authentication/storage method. Agent said it could not create a support case from that chat path; no case ID issued. This is not a definitive denial of product support.

Requested a human specialist and selected the visible Wait for a human review option. UI then showed: Marijus is reviewing your request; Your request is being reviewed. Added and submitted a concise technical note to human support. Message appeared in the conversation, confirming submission. No final technical answer yet.

Support browser tab retained in this chat for follow-up at https://hpanel.hostinger.com/. No background polling automation created. Next inspect that conversation for the human-reviewed answer; do not create credentials based only on generic documentation or the initial AI response.

Integration remains BLOCKED on confirmed authentication/provisioning method and subsequent explicit credential approval. Hostinger source/preflight remains at 1c45036; no remote mutations made during this support inquiry.
