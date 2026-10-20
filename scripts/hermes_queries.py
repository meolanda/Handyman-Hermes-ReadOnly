"""Approved read-only queries; direct delivery only to the existing private chat.

Never print records, amounts, credentials or upstream errors. No public endpoint.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from handyman_hermes.analysis import AnalysisError, latest_jobs, monthly_revenue
from hostinger_readiness import ACCOUNT, SCOPE, SHEET, approved_credential_info, verify_headers

TAB = 'ข้อมูลการบริการ'
RECIPIENT_FILE = Path('/data/workspace/handyman/readonly-recipient.json')
FIELDS = {'date': 'A', 'job_status': 'R', 'service_revenue': 'AA', 'job_id': 'AD'}
BASE = 'https://sheets.googleapis.com/v4/spreadsheets/' + SHEET


def get_json(session, url, params):
    with session.get(url, params=params, timeout=30, allow_redirects=False,
                     stream=True) as response:
        if response.status_code != 200:
            raise AnalysisError('Read failed')
        body = response.raw.read(2_000_001, decode_content=True)
        if len(body) > 2_000_000:
            raise AnalysisError('Response too large')
        return json.loads(body)


def grid_bound(get):
    metadata = get(BASE, {'fields': 'sheets(properties(title,gridProperties(rowCount)))'})
    matches = [s['properties']['gridProperties']['rowCount']
               for s in metadata['sheets'] if s['properties']['title'] == TAB]
    if len(matches) != 1 or type(matches[0]) is not int or not 1 <= matches[0] <= 100000:
        raise AnalysisError('Unsupported grid')
    return matches[0]


def scan(get, schema):
    from urllib.parse import quote
    bound = grid_bound(get)
    header = get(BASE + '/values/' + quote("'" + TAB + "'!A1:AD1", safe=''),
                 {'valueRenderOption': 'FORMATTED_VALUE'}).get('values', [])
    if verify_headers(header, schema)['status'] != 'PASS':
        raise AnalysisError('Header changed')
    records = []
    for start in range(2, bound + 1, 1000):
        end = min(start + 999, bound)
        ranges = ["'" + TAB + "'!" + col + str(start) + ':' + col + str(end)
                  for col in FIELDS.values()]
        payload = get(BASE + '/values:batchGet',
                      {'ranges': ranges, 'majorDimension': 'ROWS',
                       'valueRenderOption': 'FORMATTED_VALUE'})
        pages = payload.get('valueRanges', [])
        if len(pages) != len(FIELDS):
            raise AnalysisError('Incomplete columns')
        values = []
        for page, expected in zip(pages, ranges):
            # Response may quote/normalize the tab name; validate the cell range.
            if page.get('range', '').split('!')[-1] != expected.split('!')[-1]:
                raise AnalysisError('Unexpected range')
            rows = page.get('values', [])
            if (not isinstance(rows, list) or len(rows) > end - start + 1
                    or any(not isinstance(row, list) or len(row) > 1
                           or any(not isinstance(cell, str) for cell in row) for row in rows)):
                raise AnalysisError('Invalid page')
            values.append([row[0] if row else '' for row in rows])
        for offset in range(max(map(len, values), default=0)):
            row = {key: cells[offset] if offset < len(cells) else ''
                   for key, cells in zip(FIELDS, values)}
            if any(value.strip() for value in row.values()):
                records.append(row)
    if grid_bound(get) != bound:
        raise AnalysisError('Source changed')
    ids = [row['job_id'].strip() for row in records if row['job_id'].strip()]
    if len(set(ids)) != len(ids):
        raise AnalysisError('Duplicate job IDs')
    return records


def read_verified(get, schema):
    first = scan(get, schema)
    second = scan(get, schema)
    digest = lambda rows: hashlib.sha256(json.dumps(rows, ensure_ascii=False,
                                sort_keys=True).encode()).digest()
    if digest(first) != digest(second):
        raise AnalysisError('Source changed between reads')
    return second


def report_text(records, query, month):
    lines = ['Handyman — อ่านอย่างเดียว',
             'ตรวจข้อมูลที่เลือก 2 รอบตรงกัน (ไม่ใช่ snapshot แบบธุรกรรม)',
             'แถวข้อมูลที่อ่าน: ' + str(len(records))]
    if query == 'pending':
        # Drop all free text and amounts before constructing any model-facing data.
        safe = [{key: row[key] for key in ('date', 'job_status', 'job_id')} for row in records]
        result = latest_jobs(safe, statuses={'ไม่จบ'}, limit=10)
        lines += ['งานค้าง = สถานะ ไม่จบ: ' + str(result['matchedRows']),
                  'วันที่อ่านไม่ได้/ว่าง: ' + str(result['invalidDateRows']),
                  'แสดงล่าสุดตามวันที่สูงสุด 10 งาน:']
        from handyman_hermes.analysis import parse_date
        for row in result['records']:
            job = row['job_id'].strip()
            if not re.fullmatch(r'JB[0-9]{8,20}-[0-9]{1,8}', job):
                job = '[รหัสต้องตรวจสอบ]'
            lines.append(str(parse_date(row['date'])) + ' | ' + job)
    else:
        try:
            result = monthly_revenue(records, month, statuses={'จบ'})
        except AnalysisError:
            lines += ['รายได้เดือน ' + month + ': ต้องตรวจสอบยอดว่าง/รูปแบบเงิน',
                      'ไม่แสดงยอดรวมที่อาจไม่ครบ']
        else:
            lines += ['รายได้ = สถานะ จบ; วันที่จากคอลัมน์ A; เงินจาก AA',
                      'เดือน: ' + month,
                      ('ยอดรวมที่นับได้ (ยังไม่สมบูรณ์): ' if not result['completeForSelectedStatuses']
                       else 'ยอดรวม: ') + result['total'] + ' บาท',
                      'แถวที่นับ: ' + str(result['countedRows']),
                      'แถวสถานะจบที่วันที่อ่านไม่ได้: ' + str(result['invalidDateRows']),
                      'ข้ามสถานะอื่น: ' + str(result['excludedStatusRows']),
                      'นอกเดือน: ' + str(result['outsideMonthRows'])]
    lines += ['ไม่ส่งชื่อ เบอร์โทร หรือหมายเหตุลูกค้า; ไม่แก้ไขชีต']
    return '\n'.join(lines)


def deliver(text):
    import requests
    from dotenv import dotenv_values
    config = dotenv_values('/data/.env')
    recipient = json.loads(RECIPIENT_FILE.read_text())['chat_id']
    if not isinstance(recipient, str) or not re.fullmatch(r'[1-9][0-9]{4,15}', recipient):
        raise AnalysisError('Pinned private recipient required')
    allowed = (config.get('TELEGRAM_ALLOWED_USERS') or '').strip()
    home = (config.get('TELEGRAM_HOME_CHANNEL') or '').strip()
    token = config.get('TELEGRAM_BOT_TOKEN')
    if allowed != recipient or home != recipient or not token:
        raise AnalysisError('Recipient configuration changed')
    # Telegram getChat verifies the destination is private before sending data.
    base = 'https://api.telegram.org/bot' + token
    with requests.Session() as session:
        info = session.post(base + '/getChat', json={'chat_id': recipient},
                            timeout=20, allow_redirects=False)
        if info.status_code != 200:
            raise AnalysisError('Recipient verification failed')
        chat = info.json()
        if (chat.get('ok') is not True or chat['result'].get('type') != 'private'
                or str(chat['result'].get('id')) != recipient):
            raise AnalysisError('Private recipient required')
        sent = session.post(base + '/sendMessage', json={'chat_id': recipient,
                            'text': text, 'protect_content': True},
                            timeout=20, allow_redirects=False)
        if sent.status_code != 200 or sent.json().get('ok') is not True:
            raise AnalysisError('Delivery failed; do not retry blindly')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--query', choices=['pending', 'revenue'], required=True)
    parser.add_argument('--month')
    parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    if args.month and not re.fullmatch(r'\d{4}-(?:0[1-9]|1[0-2])', args.month):
        parser.error('Invalid month')
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
        credentials = service_account.Credentials.from_service_account_info(
            approved_credential_info(), scopes=[SCOPE])
        if credentials.service_account_email != ACCOUNT:
            raise AnalysisError('Identity mismatch')
        schema = json.loads((ROOT / 'config/service-schema.json').read_text(encoding='utf-8'))
        with AuthorizedSession(credentials) as session:
            records = read_verified(lambda url, params: get_json(session, url, params), schema)
        month = args.month or datetime.now(ZoneInfo('Asia/Bangkok')).strftime('%Y-%m')
        text = report_text(records, args.query, month)
        if args.send:
            deliver(text)
        print(json.dumps({'status': 'SENT' if args.send else 'READ_VERIFIED',
                          'query': args.query, 'rowsChecked': len(records),
                          'matchingReads': 2, 'readonly': True}))
        return 0
    except Exception:
        print('{"status":"BLOCKED","reason":"QUERY_OR_DELIVERY_FAILED"}')
        return 2


if __name__ == '__main__':
    sys.exit(main())
