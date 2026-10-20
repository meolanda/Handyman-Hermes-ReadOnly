import contextlib
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('readiness', Path(__file__).resolve().parents[1] / 'scripts/hostinger_readiness.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReadinessTests(unittest.TestCase):
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
