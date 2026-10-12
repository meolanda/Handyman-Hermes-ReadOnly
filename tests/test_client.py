import contextlib
import io
import json
import logging
from pathlib import Path
import traceback
import unittest
from urllib.error import HTTPError
from unittest.mock import patch, MagicMock
from handyman_hermes import HermesSheetsClient, SheetsReadError
from handyman_hermes.client import OAUTH_SCOPES, _NoRedirect

FIXTURE = json.loads((Path(__file__).parent / 'fixtures/sales.json').read_text())
TOKEN = 'MOCK_SECRET_DO_NOT_LOG'


def operation(result=FIXTURE):
    return {'done': True, 'response': {'result': result}}


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.patch = patch('handyman_hermes.client.build_opener')
        self.opener = self.patch.start().return_value
        self.addCleanup(self.patch.stop)
        self.response = MagicMock()
        self.opener.open.return_value = self.response
        self.client = HermesSheetsClient('MOCK_SCRIPT_ID')
        self.respond(operation())

    def respond(self, payload):
        self.response.__enter__.return_value.read.return_value = json.dumps(payload).encode()

    def test_mock_read(self):
        self.assertEqual(self.client.read_sales(TOKEN), FIXTURE['data'])

    def test_post_protocol_and_secret_location(self):
        self.client.read_sales(TOKEN)
        req = self.opener.open.call_args.args[0]
        self.assertEqual(req.full_url, 'https://script.googleapis.com/v1/scripts/MOCK_SCRIPT_ID:run')
        self.assertEqual(req.get_method(), 'POST')
        self.assertEqual(req.get_header('Authorization'), 'Bearer ' + TOKEN)
        self.assertEqual(json.loads(req.data), {'function': 'readSales', 'parameters': [], 'devMode': False})
        self.assertNotIn(TOKEN, req.full_url)
        self.assertNotIn(TOKEN, req.data.decode())
        self.assertNotIn(TOKEN, repr(self.client.__dict__))

    def test_script_id_validation(self):
        for value in [None, '', 'id?token='+TOKEN, 'https://example.com', '../x']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                HermesSheetsClient(value)

    def test_token_validation(self):
        for value in [None, '', 'token\nsecret', 'has space']:
            with self.subTest(value=value), self.assertRaises(SheetsReadError):
                self.client.read_sales(value)
        self.opener.open.assert_not_called()

    def test_scopes(self):
        self.assertEqual(set(OAUTH_SCOPES), {
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/spreadsheets.readonly'})
        manifest = json.loads((Path(__file__).parents[1]/'apps_script/appsscript.json').read_text())
        self.assertEqual(set(manifest['oauthScopes']), set(OAUTH_SCOPES))

    def test_api_and_execution_errors(self):
        for error in [{'code': 403, 'message': TOKEN}, {'code': 3, 'details': [
            {'@type': 'type.googleapis.com/google.apps.script.v1.ExecutionError',
             'errorMessage': TOKEN, 'scriptStackTraceElements': [{'function': TOKEN}]}]}]:
            self.respond({'done': True, 'error': error})
            with self.assertRaisesRegex(SheetsReadError, 'API or script execution failed'):
                self.client.read_sales(TOKEN)

    def test_application_errors(self):
        for code, expected in [('CONFIG_REQUIRED', 'CONFIG_REQUIRED'), (TOKEN, 'READ_FAILED')]:
            self.respond(operation({'ok': False, 'error': {'code': code, 'message': TOKEN}}))
            with self.assertRaisesRegex(SheetsReadError, expected):
                self.client.read_sales(TOKEN)

    def test_invalid_responses(self):
        for value in [None, {}, {'done': False}, {'done': True}, operation(None),
                      operation({'ok': True, 'data': [3], 'truncated': False}),
                      operation({'ok': True, 'data': [{'x': 4}], 'truncated': False})]:
            self.respond(value)
            with self.subTest(value=value), self.assertRaises(SheetsReadError):
                self.client.read_sales(TOKEN)

    def test_truncation(self):
        self.respond(operation(dict(FIXTURE, truncated=True)))
        with self.assertRaisesRegex(SheetsReadError, 'truncated'):
            self.client.read_sales(TOKEN)

    def test_http_statuses(self):
        for status, expected in [(401, 'Authentication failed'), (403, 'Access denied'),
                                 (429, 'API rate limit'), (500, 'API HTTP error'), (302, 'API HTTP error')]:
            self.opener.open.side_effect = HTTPError('https://invalid/?token='+TOKEN, status, TOKEN, {}, None)
            with self.assertRaisesRegex(SheetsReadError, expected):
                self.client.read_sales(TOKEN)

    def test_no_secrets_in_logs_errors_or_tracebacks(self):
        output, logs = io.StringIO(), io.StringIO()
        handler = logging.StreamHandler(logs)
        logging.getLogger().addHandler(handler)
        self.addCleanup(logging.getLogger().removeHandler, handler)
        for failure in [OSError(TOKEN), HTTPError('https://invalid/'+TOKEN, 401, TOKEN, {}, None)]:
            self.opener.open.side_effect = failure
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                try:
                    self.client.read_sales(TOKEN)
                except SheetsReadError as exc:
                    rendered = ''.join(traceback.format_exception(exc))
                    self.assertNotIn(TOKEN, str(exc))
                    self.assertNotIn(TOKEN, rendered)
                    self.assertIsNone(exc.__context__)
                else:
                    self.fail('Expected sanitized error')
        self.assertNotIn(TOKEN, output.getvalue() + logs.getvalue())
        self.assertEqual(output.getvalue() + logs.getvalue(), '')

    def test_bad_json_and_size(self):
        for body in [TOKEN.encode(), b'x'*2_000_001]:
            self.response.__enter__.return_value.read.return_value = body
            with self.assertRaises(SheetsReadError) as caught:
                self.client.read_sales(TOKEN)
            self.assertNotIn(TOKEN, str(caught.exception))

    def test_redirects_blocked(self):
        self.assertIsNone(_NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://evil.invalid'))


if __name__ == '__main__':
    unittest.main()
