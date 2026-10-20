import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from inspect_duplicate_jobs import summarize


class DuplicateAuditTests(unittest.TestCase):
    def test_conflicts_counts_without_values(self):
        def row(job, day='2026-09-01', status='จบ', amount='10'):
            return dict(job_id=job, date=day, job_status=status, service_revenue=amount)
        rows = [row('PRIVATE_A'), row('PRIVATE_A'), row('PRIVATE_B'),
                row('PRIVATE_B', status='ไม่จบ', amount='20'), row('')]
        result = summarize(rows)
        self.assertEqual(result['duplicateGroups'], 2)
        self.assertEqual(result['groupsIdenticalInSelectedFields'], 1)
        self.assertEqual(result['groupsDifferentInSelectedFields'], 1)
        self.assertEqual(result['groupsWithDifferentRevenue'], 1)
        self.assertEqual(result['blankJobIdRows'], 1)
        self.assertNotIn('PRIVATE', str(result))
        self.assertFalse(result['fullRowEqualityVerified'])

    def test_empty_is_not_duplicate(self):
        self.assertEqual(summarize([])['duplicateGroups'], 0)
