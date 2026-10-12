"""Live-only probe. Never falls back to fixtures or prints customer records."""
import hashlib
import json
import os
import sys
from pathlib import Path
from handyman_hermes.direct import DirectSheetsClient
from handyman_hermes import SheetsReadError


def main():
    token = os.environ.get('HANDYMAN_SHEETS_ACCESS_TOKEN')
    if not token:
        print(json.dumps({'status':'BLOCKED','reason':'Google read-only access token unavailable'}))
        return 2
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root/'config/example.json').read_text())
    config['columns'] = json.loads((root/'config/service-schema.json').read_text())['columns']
    try:
        records = DirectSheetsClient(config).read_sales(token)
    except SheetsReadError as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)}))
        return 2
    if not records:
        print(json.dumps({'status':'BLOCKED','reason':'No service rows found in test range'}))
        return 2
    print(json.dumps({'status':'LIVE_READ_PASSED','range':config['data_range'],
                      'record_count':len(records),'field_count':len(config['columns']),
                      'method':'GET','scope':'spreadsheets.readonly',
                      'sha256':hashlib.sha256(json.dumps(records,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
