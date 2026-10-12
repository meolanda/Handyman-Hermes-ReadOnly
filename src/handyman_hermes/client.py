"""Read-only scripts.run adapter. Token acquisition/storage belongs to the caller."""
import json
import re
from urllib.error import HTTPError
from urllib.request import Request, build_opener, HTTPRedirectHandler

OAUTH_SCOPES = (
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
)
_SAFE_CODES = frozenset({"CONFIG_REQUIRED", "INVALID_CONFIG", "SHEET_NOT_FOUND",
                         "HEADER_NOT_FOUND", "COLUMN_NOT_FOUND", "DUPLICATE_HEADER",
                         "READ_FAILED"})


class SheetsReadError(RuntimeError):
    """Sanitized error: never includes remote messages or credentials."""


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward the Authorization header to a redirect destination.
        return None


class HermesSheetsClient:
    def __init__(self, script_id, *, timeout=20):
        if not isinstance(script_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", script_id):
            raise ValueError("Invalid script ID")
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValueError("timeout must be positive")
        self.endpoint_url = f"https://script.googleapis.com/v1/scripts/{script_id}:run"
        self.timeout = timeout

    def read_sales(self, access_token):
        """Receive a short-lived token per call; do not retain or refresh it."""
        if (not isinstance(access_token, str) or not access_token or
                any(ord(c) <= 32 or ord(c) >= 127 for c in access_token)):
            raise SheetsReadError("Invalid access token")
        payload = None
        failure = None
        try:
            request = Request(self.endpoint_url,
                              data=json.dumps({"function": "readSales", "parameters": [],
                                               "devMode": False}).encode(),
                              headers={"Accept": "application/json",
                                       "Content-Type": "application/json",
                                       "Authorization": "Bearer " + access_token},
                              method="POST")
            with build_opener(_NoRedirect()).open(request, timeout=self.timeout) as response:
                body = response.read(2_000_001)
            if len(body) > 2_000_000:
                failure = "Response too large"
            else:
                payload = json.loads(body)
        except HTTPError as exc:
            failure = {401: "Authentication failed", 403: "Access denied",
                       429: "API rate limit"}.get(exc.code, "API HTTP error")
        except Exception:
            failure = "Unable to read API response"
        # Raise outside exception handlers: no credential-bearing exception chain.
        if failure:
            raise SheetsReadError(failure)
        return self._parse(payload)

    @staticmethod
    def _parse(payload):
        if not isinstance(payload, dict):
            raise SheetsReadError("Invalid API response")
        if "error" in payload:
            # Covers API errors and ExecutionError details; omit remote text/stack.
            raise SheetsReadError("API or script execution failed")
        if payload.get("done") is not True:
            raise SheetsReadError("Script execution incomplete")
        response = payload.get("response")
        result = response.get("result") if isinstance(response, dict) else None
        if not isinstance(result, dict):
            raise SheetsReadError("Invalid script result")
        if result.get("ok") is not True:
            error = result.get("error")
            code = error.get("code") if isinstance(error, dict) else None
            safe = code if isinstance(code, str) and code in _SAFE_CODES else "READ_FAILED"
            raise SheetsReadError(safe)
        records = result.get("data")
        if (not isinstance(records, list) or
                any(not isinstance(row, dict) or
                    any(not isinstance(k, str) or not isinstance(v, str)
                        for k, v in row.items()) for row in records) or
                not isinstance(result.get("truncated"), bool)):
            raise SheetsReadError("Invalid response schema")
        if result["truncated"]:
            raise SheetsReadError("Result truncated")
        return records
