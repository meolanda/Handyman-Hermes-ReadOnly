"""No credential parsing, authentication, network or business-data access."""
import importlib.util
import json
import os
import sys


def available(module):
    try:
        return importlib.util.find_spec(module) is not None
    except (ModuleNotFoundError, ImportError, ValueError):
        return False


if __name__ == '__main__':
    print(json.dumps({'python': sys.executable,
                      'credentialPresent': 'HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON' in os.environ,
                      'googleAuthAvailable': available('google.oauth2.service_account'),
                      'requestsAvailable': available('requests'),
                      'dotenvAvailable': available('dotenv'),
                      'tokenIssued': False, 'liveReadAttempted': False}))
