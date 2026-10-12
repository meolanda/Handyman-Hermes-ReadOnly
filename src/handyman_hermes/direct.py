"""Direct Sheets API reader; no deployment or token persistence."""
import json
import re
from urllib.parse import quote, urlencode
from urllib.error import HTTPError
from urllib.request import Request, build_opener
from .client import SheetsReadError, _NoRedirect

READONLY_SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'


class DirectSheetsClient:
    def __init__(self, config, *, timeout=20):
        spreadsheet_id = config.get('spreadsheet_id')
        tab = config.get('sheet_name')
        local_range = config.get('data_range')
        columns = config.get('columns')
        match = re.fullmatch(r'([A-Z]{1,3})([1-9][0-9]*):([A-Z]{1,3})([1-9][0-9]*)', local_range or '')
        if (not isinstance(spreadsheet_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', spreadsheet_id)
                or not isinstance(tab, str) or not tab or not match
                or int(match[2]) != config.get('header_row') or int(match[4]) < int(match[2])
                or not isinstance(columns, dict) or not columns
                or any(not isinstance(k, str) or not isinstance(v, str) or not k or not v
                       for k, v in columns.items())):
            raise ValueError('Invalid read configuration')
        self.columns = dict(columns)
        self.max_rows = config.get('max_rows', 100)
        if not isinstance(self.max_rows, int) or not 1 <= self.max_rows <= 1000:
            raise ValueError('Invalid row limit')
        self.timeout = timeout
        a1 = "'" + tab.replace("'", "''") + "'!" + local_range
        self.endpoint_url = ('https://sheets.googleapis.com/v4/spreadsheets/' +
                             quote(spreadsheet_id, safe='') + '/values/' + quote(a1, safe='') +
                             '?' + urlencode({'valueRenderOption':'FORMATTED_VALUE', 'majorDimension':'ROWS'}))

    def read_sales(self, access_token):
        if (not isinstance(access_token, str) or not access_token or
                any(ord(c) <= 32 or ord(c) >= 127 for c in access_token)):
            raise SheetsReadError('Invalid access token')
        failure = None
        result = None
        try:
            req = Request(self.endpoint_url, headers={'Authorization':'Bearer '+access_token,
                          'Accept':'application/json'}, method='GET')
            with build_opener(_NoRedirect()).open(req, timeout=self.timeout) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                failure = 'Response too large'
            else:
                result = json.loads(body)
        except HTTPError as exc:
            failure = {401:'Authentication failed',403:'Access denied',429:'API rate limit'}.get(exc.code,'API HTTP error')
        except Exception:
            failure = 'Unable to read API response'
        if failure:
            raise SheetsReadError(failure)
        if not isinstance(result, dict) or 'error' in result:
            raise SheetsReadError('Invalid API response')
        rows = result.get('values', [])
        if (not isinstance(rows, list) or not rows or
                any(not isinstance(row, list) or any(not isinstance(cell, str) for cell in row) for row in rows)):
            raise SheetsReadError('Invalid or missing header')
        if len(rows)-1 > self.max_rows:
            raise SheetsReadError('Result truncated')
        indexes = {}
        for key, header in self.columns.items():
            if rows[0].count(header) != 1:
                raise SheetsReadError('Missing or duplicate header')
            indexes[key] = rows[0].index(header)
        return [{key:row[index] if index < len(row) else '' for key,index in indexes.items()}
                for row in rows[1:] if any(cell != '' for cell in row)]
