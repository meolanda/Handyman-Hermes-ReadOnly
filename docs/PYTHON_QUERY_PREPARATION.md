# Offline query layer preparation

Implemented in `src/handyman_hermes/analysis.py`. No network, credential loading, Hostinger installation, record reads or Telegram sends are performed by this layer.

- Header whitespace is normalized (including leading tab in job_id); missing/duplicate normalized mappings fail.
- A callback-based reader visits every page through an explicit grid row bound, including pages after an empty page. A page failure rejects all partial results. A synthetic 4,960-record test verifies the final page is included.
- Latest jobs are sorted by parsed dates, with an explicit status filter and result limit. Invalid dates and omitted results are counted. ISO and D/M/YYYY are accepted; Buddhist years are converted.
- Thai-format phone strings using ordinary digits are masked in every returned text field before model-facing records are returned. Tests include formatted numbers, Thai text adjacency and false-positive cases (dates, money and job IDs).
- Monthly totals use Decimal and require explicit statuses. Malformed/blank amounts in the selected month fail rather than becoming zero. Output includes month, status/date/amount rules, counted and skipped rows. Invalid dates mark the total incomplete.

## Still required before activation

This is an offline preparation layer, not an active Hermes integration. The callback must be wired to a bounded, authenticated Google reader after record-access scope is approved. Grid metadata, consistent source handling during pagination (Google values requests are not a snapshot), and header revalidation must be implemented before claiming a complete live dataset. The older fixed-range DirectSheetsClient is unchanged and must not be used as a full-data reader.

Phone masking is heuristic, not a guarantee that records are anonymous. Thai numeral phones, unusual encodings, international numbers beyond the configured pattern, names, addresses and other identifiers need privacy review. No model or Telegram recipient has been configured. Do not send raw pages to a model; direct callers must use the safe projection and an approved field allowlist.

Confirm business definitions before activation: which statuses count as pending; whether revenue means completed jobs only or all statuses; how undated jobs, blank prices, cancellations, duplicate job IDs and negative adjustments should be treated. Do not present an incomplete total as a definitive revenue figure. No Excel reference totals have been verified against the live spreadsheet by this layer.

Validation: Windows Python offline unittest suite run with UTF-8 mode; synthetic fixtures only. Initial run using the Windows legacy default encoding failed when existing tests loaded Thai fixture files; rerun with `python -X utf8 -m unittest discover -s tests -q` is the supported verification command here.
