"""Credential-free readiness check by default; --live requires operator approval.

Never prints credentials, tokens, header contents, upstream errors or records.
No credential creation, IAM changes, sheet writes or token persistence.
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENT_KEY = 'HANDYMAN_GOOGLE_SERVICE_ACCOUNT_JSON'
ACCOUNT = 'handyman-hermes-reader@handyman-hermes-reader.iam.gserviceaccount.com'
SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SHEET = '1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q'
RANGE = "'ข้อมูลการบริการ'!A1:AD1"


def credential_status():
    # Presence only; do not retrieve or parse the secret during default preflight.
    return ('CREDENTIAL_PRESENT_REQUIRES_APPROVED_LIVE_CHECK'
            if ENVIRONMENT_KEY in os.environ else 'CREDENTIAL_NOT_PROVISIONED')


def approved_credential_info():
    raw = os.environ.get(ENVIRONMENT_KEY, '')
    if not raw or len(raw) > 32768:
        raise ValueError('INVALID_CREDENTIAL_CONFIGURATION')
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('INVALID_CREDENTIAL_CONFIGURATION')
            result[key] = value
        return result
    info = json.loads(raw, object_pairs_hook=unique_object)
    if (not isinstance(info, dict) or info.get('type') != 'service_account'
            or info.get('client_email') != ACCOUNT
            or info.get('project_id') != 'handyman-hermes-reader'
            or info.get('token_uri') != 'https://oauth2.googleapis.com/token'
            or info.get('universe_domain', 'googleapis.com') != 'googleapis.com'
            or not isinstance(info.get('private_key'), str)
            or not info['private_key'].startswith('-----BEGIN PRIVATE KEY-----')):
        raise ValueError('INVALID_CREDENTIAL_CONFIGURATION')
    # Only forward the approved fields. No credential-source URL or executable.
    return {key: info[key] for key in ('type', 'client_email', 'project_id',
                                     'token_uri', 'private_key')}


def verify_headers(rows, schema):
    headers = rows[0] if rows else []
    normalize = lambda value: ' '.join(str(value).split())
    mismatches = []
    for key, position in schema['positions'].items():
        index = 0
        for char in position:
            index = index * 26 + ord(char) - 64
        actual = headers[index - 1] if len(headers) >= index else ''
        expected = normalize(schema['columns'][key])
        if (normalize(actual) != expected
                or sum(normalize(value) == expected for value in headers) != 1):
            mismatches.append(position)
    return {'status': 'NEEDS_REVIEW' if mismatches else 'PASS',
            'columnsChecked': len(schema['columns']), 'mismatches': mismatches,
            'readRange': 'A1:AD1', 'readonly': True}


def live_probe():
    # Deliberately opt-in: no default ADC discovery or token creation in preflight.
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    from urllib.parse import quote
    credentials = service_account.Credentials.from_service_account_info(
        approved_credential_info(), scopes=[SCOPE])
    if (credentials.service_account_email != ACCOUNT
            or getattr(credentials, '_subject', None) is not None
            or getattr(credentials, '_token_uri', None) != 'https://oauth2.googleapis.com/token'):
        return {'status': 'BLOCKED', 'reason': 'UNEXPECTED_CREDENTIAL_IDENTITY'}
    endpoint = ('https://sheets.googleapis.com/v4/spreadsheets/' + SHEET
                + '/values/' + quote(RANGE, safe=''))
    with AuthorizedSession(credentials) as session:
        response = session.get(endpoint, params={'valueRenderOption': 'FORMATTED_VALUE',
                              'majorDimension': 'ROWS'}, timeout=20, allow_redirects=False,
                               stream=True)
        if response.status_code != 200:
            response.close()
            return {'status': 'BLOCKED', 'reason': 'AUTHORIZED_HEADER_READ_FAILED'}
        raw = response.raw.read(65537, decode_content=True)
        response.close()
        if len(raw) > 65536:
            return {'status': 'BLOCKED', 'reason': 'HEADER_RESPONSE_TOO_LARGE'}
        payload = json.loads(raw)
    rows = payload.get('values', [])
    if (not isinstance(rows, list) or len(rows) > 1
            or any(not isinstance(row, list) or len(row) > 30
                   or any(not isinstance(value, str) for value in row) for row in rows)):
        return {'status': 'BLOCKED', 'reason': 'INVALID_HEADER_RESPONSE'}
    schema = json.loads((ROOT / 'config/service-schema.json').read_text(encoding='utf-8'))
    return verify_headers(rows, schema)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true',
                        help='Only after approval to use credentials and mint an access token')
    args = parser.parse_args(argv)
    status = credential_status()
    if not args.live or status != 'CREDENTIAL_PRESENT_REQUIRES_APPROVED_LIVE_CHECK':
        print(json.dumps({'status': 'BLOCKED', 'reason': status,
                          'tokenIssued': False, 'liveReadAttempted': False}))
        return 2
    try:
        result = live_probe()
    except Exception:
        result = {'status': 'BLOCKED', 'reason': 'LIVE_PROBE_FAILED'}
    print(json.dumps(result))
    return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
