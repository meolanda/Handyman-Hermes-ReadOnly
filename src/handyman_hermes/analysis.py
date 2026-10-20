"""Offline business-query preparation. No credentials, network or model calls."""
import re
from datetime import date
from decimal import Decimal, InvalidOperation


class AnalysisError(ValueError):
    pass


def normalize_header(value):
    return ' '.join(str(value).split())


def map_headers(headers, columns):
    normalized = [normalize_header(value) for value in headers]
    expected = [normalize_header(value) for value in columns.values()]
    if len(set(expected)) != len(expected):
        raise AnalysisError('Duplicate configured header')
    if any(normalized.count(value) != 1 for value in expected):
        raise AnalysisError('Missing or duplicate header')
    return {key: normalized.index(normalize_header(value))
            for key, value in columns.items()}


def read_complete_pages(fetch_page, headers, columns, total_rows, *, page_size=500,
                        max_rows=100000):
    """Callback(start_row, end_row) returns lists; total_rows includes header.

    Caller must obtain the grid bound and ensure a stable source separately.
    Short pages may contain omitted trailing blank rows; later pages still run.
    No network implementation or credential access is included here.
    """
    if (type(total_rows) is not int or total_rows < 1 or total_rows > max_rows
            or type(page_size) is not int or not 1 <= page_size <= 1000):
        raise AnalysisError('Invalid or excessive row bound')
    indexes = map_headers(headers, columns)
    records = []
    try:
        for start in range(2, total_rows + 1, page_size):
            end = min(start + page_size - 1, total_rows)
            page = fetch_page(start, end)
            if (not isinstance(page, list) or len(page) > end - start + 1
                    or any(not isinstance(row, list)
                           or any(not isinstance(cell, str) for cell in row)
                           for row in page)):
                raise AnalysisError('Invalid page')
            for row in page:
                if any(cell.strip() for cell in row):
                    records.append({key: row[index] if index < len(row) else ''
                                    for key, index in indexes.items()})
    except Exception:
        # Never return partial records or retain upstream secret-bearing errors.
        failed = True
    else:
        failed = False
    if failed:
        raise AnalysisError('Incomplete read')
    return records


# Conservative Thai phone mask, including +66, spaces, parentheses and dashes.
# This is not a general PII scrubber; addresses/names require separate policy.
_PHONE = re.compile(r'(?<![0-9A-Za-z])(?:\+?66[\s().-]*[1-9](?:[\s().-]*\d){7,8}'
                    r'|0[1-9](?:[\s().-]*\d){7,8})(?![0-9A-Za-z])')


def mask_phones(value):
    return _PHONE.sub('[PHONE]', value)


def model_safe_records(records):
    return [{key: mask_phones(value) for key, value in row.items()}
            for row in records]


def parse_date(value):
    """Explicit ISO or day/month/year; Thai Buddhist years are converted."""
    value = value.strip()
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            return date.fromisoformat(value)
        if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{4}', value):
            day, month, year = map(int, value.split('/'))
            return date(year - 543 if year >= 2400 else year, month, day)
    except ValueError:
        pass
    return None


def latest_jobs(records, *, statuses, limit=10):
    if not statuses or type(limit) is not int or not 1 <= limit <= 100:
        raise AnalysisError('Explicit statuses and limit required')
    selected = [row for row in records if row.get('job_status', '').strip() in statuses]
    dated = [(parse_date(row.get('date', '')), row) for row in selected]
    valid = [(day, row) for day, row in dated if day is not None]
    valid.sort(key=lambda item: (item[0], item[1].get('job_id', '')), reverse=True)
    return {'records': model_safe_records([row for _, row in valid[:limit]]),
            'matchedRows': len(selected), 'invalidDateRows': len(dated) - len(valid),
            'returnedRows': min(limit, len(valid)),
            'limited': len(valid) > limit, 'statuses': sorted(statuses),
            'dateRule': 'ISO or D/M/YYYY; Buddhist year minus 543'}


def parse_money(value):
    value = value.strip()
    if not re.fullmatch(r'-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d{1,2})?', value):
        raise AnalysisError('Invalid monetary value')
    try:
        return Decimal(value.replace(',', ''))
    except InvalidOperation:
        raise AnalysisError('Invalid monetary value') from None


def monthly_revenue(records, month, *, statuses):
    """Explicit status policy; invalid amounts in selected month fail closed."""
    if not re.fullmatch(r'\d{4}-(?:0[1-9]|1[0-2])', month) or not statuses:
        raise AnalysisError('Explicit month and statuses required')
    total = Decimal('0.00')
    counted = invalid_date = outside = excluded = 0
    for row in records:
        if row.get('job_status', '').strip() not in statuses:
            excluded += 1
            continue
        day = parse_date(row.get('date', ''))
        if day is None:
            invalid_date += 1
            continue
        if day.strftime('%Y-%m') != month:
            outside += 1
            continue
        total += parse_money(row.get('service_revenue', ''))
        counted += 1
    return {'total': format(total, '.2f'), 'month': month,
            'statuses': sorted(statuses), 'countedRows': counted,
            'invalidDateRows': invalid_date, 'outsideMonthRows': outside,
            'excludedStatusRows': excluded, 'inputRows': len(records),
            'amountColumn': 'service_revenue', 'dateColumn': 'date',
            'completeForSelectedStatuses': invalid_date == 0,
            'dateRule': 'ISO or D/M/YYYY; Buddhist year minus 543'}
