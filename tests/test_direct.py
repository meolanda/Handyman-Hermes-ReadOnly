import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from urllib.parse import unquote
from handyman_hermes.direct import DirectSheetsClient, READONLY_SCOPE
from handyman_hermes import SheetsReadError

class DirectTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads(Path('config/example.json').read_text())
        self.fixture=json.loads(Path('tests/fixtures/service-values.json').read_text())
        self.config['columns']=json.loads(Path('config/service-schema.json').read_text())['columns']

    @patch('handyman_hermes.direct.build_opener')
    def test_real_headers_mock_read_get_only(self, opener):
        response=MagicMock();response.__enter__.return_value.read.return_value=json.dumps({'values':self.fixture['values']}).encode()
        opener.return_value.open.return_value=response
        client=DirectSheetsClient(self.config)
        self.assertEqual(client.read_sales('MOCK_TOKEN'),[self.fixture['expected']])
        req=opener.return_value.open.call_args.args[0]
        self.assertEqual(req.get_method(),'GET');self.assertIsNone(req.data)
        self.assertIn("'ข้อมูลการบริการ'!A1:AD100",unquote(req.full_url))
        self.assertNotIn('MOCK_TOKEN',req.full_url)
        self.assertEqual(READONLY_SCOPE,'https://www.googleapis.com/auth/spreadsheets.readonly')

    @patch('handyman_hermes.direct.build_opener')
    def test_sanitized_failure(self, opener):
        opener.return_value.open.side_effect=RuntimeError('MOCK_SECRET')
        with self.assertRaises(SheetsReadError) as caught:
            DirectSheetsClient(self.config).read_sales('MOCK_SECRET')
        self.assertNotIn('MOCK_SECRET',str(caught.exception));self.assertIsNone(caught.exception.__context__)

    def test_unconfigured_range_rejected(self):
        for r in ['A:AD','OTHER!A1:AD100','A2:AD100']:
            with self.assertRaises(ValueError):DirectSheetsClient(dict(self.config,data_range=r))
