"""Connection metadata only: no credential values, tokens or network calls."""
import json
import os
import shutil
from pathlib import Path


def main():
    import yaml
    from dotenv import dotenv_values
    home = Path('/data')
    config_path = home / 'config.yaml'
    config = yaml.safe_load(config_path.read_text()) if config_path.is_file() else {}
    config = config if isinstance(config, dict) else {}
    servers = config.get('mcp_servers', {})
    keys = set(os.environ)
    dotenv_path = home / '.env'
    if dotenv_path.is_file():
        keys.update(dotenv_values(dotenv_path).keys())
    skill = home / 'skills/productivity/google-workspace/SKILL.md'
    output = {
        'status': 'METADATA_INSPECTED',
        'configPresent': config_path.is_file(),
        'mcpServerEntries': len(servers) if isinstance(servers, (dict, list)) else None,
        'mcpConfigSectionPresent': 'mcp' in config,
        'gwsOnPath': shutil.which('gws') is not None,
        'gcloudOnPath': shutil.which('gcloud') is not None,
        'googleWorkspaceSkillAtBundledPath': skill.is_file(),
        'flowNamedEnvironmentEntries': sum('FLOW' in key.upper() for key in keys),
        'sheetsCredentialPresentInProcess': 'HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON' in os.environ,
        'googleCalendarLiveAccessTested': False,
        'googleDriveLiveAccessTested': False,
        'flowAccountLiveAccessTested': False,
        'credentialValuesPrinted': False,
        'networkCalls': 0,
    }
    print(json.dumps(output))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('{"status":"BLOCKED","reason":"INVENTORY_FAILED"}')
        raise SystemExit(2)
