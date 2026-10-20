import unittest
from handyman_hermes.analysis import (AnalysisError, map_headers,
    read_complete_pages, mask_phones, latest_jobs, monthly_revenue, parse_money)


class AnalysisTests(unittest.TestCase):
    def test_header_normalization_and_duplicate_rejection(self):
        self.assertEqual(map_headers(['วันที่', '\tjob_id'], {'id': 'job_id'}), {'id': 1})
        for headers in [['job_id', '\tjob_id'], ['other']]:
            with self.assertRaises(AnalysisError):
                map_headers(headers, {'id': 'job_id'})

    def test_all_4960_rows_and_tail_read(self):
        calls = []
        def fetch(start, end):
            calls.append((start, end))
            return [[str(row)] for row in range(start, end + 1)]
        rows = read_complete_pages(fetch, ['id'], {'id': 'id'}, 4961)
        self.assertEqual(len(rows), 4960)
        self.assertEqual(rows[-1], {'id': '4961'})
        self.assertEqual(calls[-1], (4502, 4961))

    def test_short_blank_page_does_not_stop_later_pages(self):
        rows = read_complete_pages(lambda start, end: [] if start == 2 else [['tail']],
                                   ['id'], {'id': 'id'}, 5, page_size=2)
        self.assertEqual(rows, [{'id': 'tail'}])

    def test_partial_read_failure_is_sanitized(self):
        def fetch(start, end):
            if start > 2:
                raise RuntimeError('SECRET')
            return [['first']]
        with self.assertRaises(AnalysisError) as caught:
            read_complete_pages(fetch, ['id'], {'id': 'id'}, 5, page_size=2)
        self.assertIsNone(caught.exception.__context__)
        self.assertNotIn('SECRET', str(caught.exception))

    def test_phones_and_false_positives(self):
        for text in ['0812345678', 'โทร081-234-5678ครับ', '+66 81 234 5678',
                     '(02) 123 4567']:
            self.assertIn('[PHONE]', mask_phones(text))
        for text in ['2026-09-30', '1,442,105.30', 'JB20260930072756-646', '012345678901']:
            self.assertEqual(mask_phones(text), text)

    def test_latest_is_by_date_and_masks_every_field(self):
        rows = [{'date': '1/9/2569', 'job_status': 'ไม่จบ', 'customer': 'โทร0812345678'},
                {'date': '2026-09-30', 'job_status': 'ไม่จบ', 'next_actions': 'โทร0812345678'},
                {'date': 'จัดคิว', 'job_status': 'ไม่จบ'}]
        result = latest_jobs(rows, statuses={'ไม่จบ'}, limit=1)
        self.assertEqual(result['records'][0]['date'], '2026-09-30')
        self.assertEqual(result['records'][0]['next_actions'], 'โทร[PHONE]')
        self.assertEqual(result['invalidDateRows'], 1)
        self.assertTrue(result['limited'])

    def test_decimal_status_policy_and_skips(self):
        rows = [{'date': '2026-09-01', 'job_status': 'จบ', 'service_revenue': '0.10'},
                {'date': '2/9/2569', 'job_status': 'จบ', 'service_revenue': '0.20'},
                {'date': '2026-09-03', 'job_status': 'ไม่จบ', 'service_revenue': '99'},
                {'date': 'จัดคิว', 'job_status': 'จบ', 'service_revenue': '10'},
                {'date': '2026-08-01', 'job_status': 'จบ', 'service_revenue': '10'}]
        result = monthly_revenue(rows, '2026-09', statuses={'จบ'})
        self.assertEqual(result['total'], '0.30')
        self.assertEqual(result['countedRows'], 2)
        self.assertEqual(result['invalidDateRows'], 1)
        self.assertFalse(result['completeForSelectedStatuses'])
        self.assertEqual(result['excludedStatusRows'], 1)
        self.assertEqual(monthly_revenue(rows, '2026-09', statuses={'จบ', 'ไม่จบ'})['total'], '99.30')

    def test_invalid_amounts_fail_instead_of_silent_zero(self):
        for amount in ['', 'NaN', '1,23', '1.234', '1e3']:
            with self.assertRaises(AnalysisError):
                parse_money(amount)


if __name__ == '__main__':
    unittest.main()
