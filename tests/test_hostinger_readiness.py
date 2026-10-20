import contextlib
import importlib.util
import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('readiness', Path(__file__).resolve().parents[1] / 'scripts/hostinger_readiness.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReadinessTests(unittest.TestCase):
    def info(self):
        # Deliberately invalid synthetic key, never a usable credential.
        return {'type':'service_account','client_email':module.ACCOUNT,
                'project_id':'handyman-hermes-reader',
                'token_uri':'https://oauth2.googleapis.com/token',
                'private_key':'-----BEGIN PRIVATE KEY-----SYNTHETIC_NOT_A_KEY'}

    def test_default_presence_does_not_parse_or_print_secret(self):
        output = io.StringIO()
        with patch.dict(os.environ, {module.ENVIRONMENT_KEY:'PRIVATE_SENTINEL'}), patch.object(module, 'approved_credential_info') as loader, contextlib.redirect_stdout(output):
            self.assertEqual(module.main([]), 2)
        loader.assert_not_called()
        self.assertNotIn('PRIVATE_SENTINEL', output.getvalue())

    def test_rejects_wrong_identity_scope_source_and_endpoint(self):
        for key, value in [('type','external_account'), ('client_email','other@example.com'),
                           ('project_id','other'), ('token_uri','https://example.com/token'),
                           ('universe_domain','example.com')]:
            info = self.info(); info[key] = value
            with patch.dict(os.environ, {module.ENVIRONMENT_KEY:json.dumps(info)}):
                with self.assertRaises(ValueError):
                    module.approved_credential_info()

    def test_allowlists_forwarded_fields(self):
        info = self.info(); info['credential_source'] = {'executable': 'DO_NOT_RUN'}
        with patch.dict(os.environ, {module.ENVIRONMENT_KEY:json.dumps(info)}):
            self.assertNotIn('credential_source', module.approved_credential_info())

    def test_rejects_empty_large_malformed_and_duplicate_json(self):
        for value in ['', 'x'*32769, 'bad', '[]', '{"type":"service_account","type":"external_account"}']:
            with patch.object(module.os, 'environ', {module.ENVIRONMENT_KEY:value}):
                with self.assertRaises((ValueError, json.JSONDecodeError)):
                    module.approved_credential_info()

    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.schema = json.loads((root / 'config/service-schema.json').read_text(encoding='utf-8'))
        self.rows = json.loads((root / 'tests/fixtures/service-values.json').read_text(encoding='utf-8'))['values'][:1]

    def test_default_never_issues_token_or_calls_live(self):
        output = io.StringIO()
        with patch.object(module, 'credential_status', return_value='CREDENTIAL_PRESENT_REQUIRES_APPROVED_LIVE_CHECK'), patch.object(module, 'live_probe') as live, contextlib.redirect_stdout(output):
            self.assertEqual(module.main([]), 2)
        live.assert_not_called()
        self.assertFalse(json.loads(output.getvalue())['tokenIssued'])

    def test_missing_credentials_prevent_live(self):
        with patch.object(module, 'credential_status', return_value='CREDENTIAL_NOT_PROVISIONED'), patch.object(module, 'live_probe') as live, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(module.main(['--live']), 2)
        live.assert_not_called()

    def test_normalizes_tab_and_checks_twelve_columns(self):
        self.rows[0][29] = '\tjob_id'
        result = module.verify_headers(self.rows, self.schema)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['columnsChecked'], 12)

    def test_duplicate_normalized_header_fails(self):
        self.rows[0][2] = '\tjob_id'
        self.assertEqual(module.verify_headers(self.rows, self.schema)['mismatches'], ['AD'])

    def test_mismatch_returns_letters_not_values(self):
        self.rows[0][0] = 'PRIVATE_SENTINEL'
        result = module.verify_headers(self.rows, self.schema)
        self.assertEqual(result['mismatches'], ['A'])
        self.assertNotIn('PRIVATE_SENTINEL', json.dumps(result))

    def test_exception_is_sanitized(self):
        output = io.StringIO()
        with patch.object(module, 'credential_status', return_value='CREDENTIAL_PRESENT_REQUIRES_APPROVED_LIVE_CHECK'), patch.object(module, 'live_probe', side_effect=RuntimeError('PRIVATE_SENTINEL')), contextlib.redirect_stdout(output):
            self.assertEqual(module.main(['--live']), 2)
        self.assertEqual(json.loads(output.getvalue())['reason'], 'LIVE_PROBE_FAILED')
        self.assertNotIn('PRIVATE_SENTINEL', output.getvalue())
