"""Read-only duplicate audit. Outputs counts only; never IDs or cell values."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import hermes_queries as q


def summarize(records):
    groups = defaultdict(list)
    blank = 0
    for row in records:
        job = row['job_id'].strip()
        if not job:
            blank += 1
        else:
            groups[job].append(row)
    duplicates = [rows for rows in groups.values() if len(rows) > 1]
    fields = ('date', 'job_status', 'service_revenue')
    identical = sum(len({tuple(row[key] for key in fields) for row in rows}) == 1
                    for rows in duplicates)
    return {'status': 'AUDIT_COMPLETE', 'rowsChecked': len(records),
            'blankJobIdRows': blank, 'duplicateGroups': len(duplicates),
            'rowsInDuplicateGroups': sum(map(len, duplicates)),
            'excessRowsBeyondOnePerId': sum(len(rows) - 1 for rows in duplicates),
            'groupsIdenticalInSelectedFields': identical,
            'groupsDifferentInSelectedFields': len(duplicates) - identical,
            'groupsWithDifferentDate': sum(len({row['date'] for row in rows}) > 1 for rows in duplicates),
            'groupsWithDifferentStatus': sum(len({row['job_status'] for row in rows}) > 1 for rows in duplicates),
            'groupsWithDifferentRevenue': sum(len({row['service_revenue'] for row in rows}) > 1 for rows in duplicates),
            'comparedColumns': ['A', 'R', 'AA', 'AD'],
            'fullRowEqualityVerified': False, 'deduplicationPerformed': False,
            'readonly': True, 'matchingReads': 2}


def main():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
        credentials = service_account.Credentials.from_service_account_info(
            q.approved_credential_info(), scopes=[q.SCOPE])
        schema = json.loads((q.ROOT / 'config/service-schema.json').read_text(encoding='utf-8'))
        with AuthorizedSession(credentials) as session:
            get = lambda url, params: q.get_json(session, url, params)
            first = q.scan(get, schema, inspect_duplicates=True)
            second = q.scan(get, schema, inspect_duplicates=True)
        fingerprint = lambda rows: hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).digest()
        if fingerprint(first) != fingerprint(second):
            raise q.AnalysisError('Source changed')
        print(json.dumps(summarize(second)))
        return 0
    except Exception:
        print('{"status":"BLOCKED","reason":"DUPLICATE_AUDIT_FAILED"}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
