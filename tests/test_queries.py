import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import hermes_queries as q


class QueryTests(unittest.TestCase):
    def test_reports_never_include_customer_notes_or_phone(self):
        rows = [{'date': '2026-09-01', 'job_status': 'ไม่จบ',
                 'job_id': 'JB20260930072756-646', 'service_revenue': '10',
                 'customer': 'SECRET 0812345678', 'summary_notes': 'SECRET'}]
        report = q.report_text(rows, 'pending', '2026-09')
        self.assertNotIn('SECRET', report)
        self.assertNotIn('0812345678', report)
        self.assertIn('JB20260930072756-646', report)

    def test_bad_id_cannot_inject_text_or_phone(self):
        rows = [{'date': '2026-09-01', 'job_status': 'ไม่จบ',
                 'job_id': 'call 0812345678', 'service_revenue': ''}]
        self.assertNotIn('0812345678', q.report_text(rows, 'pending', '2026-09'))

    def test_bad_amount_does_not_become_zero(self):
        rows = [{'date': '2026-09-01', 'job_status': 'จบ',
                 'job_id': '', 'service_revenue': ''}]
        report = q.report_text(rows, 'revenue', '2026-09')
        self.assertIn('ต้องตรวจสอบ', report)
        self.assertNotIn('0.00', report)

    def test_owner_rule_sums_repeated_and_blank_ids(self):
        rows = [dict(date='2026-09-01', job_status='จบ', job_id=job, service_revenue=amount)
                for job, amount in [('JB20260930072756-646','10.10'),
                                    ('JB20260930072756-646','20.20'), ('','30.30')]]
        report = q.report_text(rows, 'revenue', '2026-09')
        self.assertIn('60.60', report)
        for row in rows:
            row['job_status'] = 'ไม่จบ'
        pending = q.report_text(rows, 'pending', '2026-09')
        self.assertIn('3 แถว', pending)
        self.assertIn('เฉพาะที่มีรหัส): 1', pending)
        self.assertIn('รายการค้างที่ไม่มีรหัส: 1', pending)

    def test_two_reads_must_match(self):
        with patch.object(q, 'scan', side_effect=[[{'x':'1'}], [{'x':'2'}]]):
            with self.assertRaises(q.AnalysisError):
                q.read_verified(None, None)

    def test_pagination_bounds_and_duplicate_ids(self):
        schema = json.loads((SCRIPTS.parent/'config/service-schema.json').read_text(encoding='utf-8'))
        headers = [''] * 30
        for key, pos in schema['positions'].items():
            index = 0
            for char in pos:
                index = index * 26 + ord(char) - 64
            headers[index - 1] = schema['columns'][key]
        starts = []
        def get(url, params):
            if url == q.BASE:
                return {'sheets':[{'properties':{'title':q.TAB,'gridProperties':{'rowCount':1502}}}]}
            if url.endswith('batchGet'):
                ranges = params['ranges']
                starts.append(ranges[0])
                return {'valueRanges':[{'range':r, 'values':[[value]]}
                    for r,value in zip(ranges, ['2026-09-01','จบ','0.10',ranges[0]])]}
            return {'values':[headers]}
        rows = q.scan(get, schema)
        self.assertEqual(len(rows), 2)
        self.assertIn('A1002:A1502', starts[-1])


if __name__ == '__main__':
    unittest.main()
