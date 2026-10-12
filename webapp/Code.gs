/**
 * Handyman Hermes isolated test Web App.
 * Public doGet NEVER reads Sheets or returns private data.
 * Read-only live header verification is a separate editor-only function.
 */
function doGet() {
  return ContentService.createTextOutput(JSON.stringify({
    ok: true,
    service: "Handyman-Hermes-Test",
    mode: "mock",
    message: "Connection test only"
  })).setMimeType(ContentService.MimeType.JSON);
}

function testReadHeaders() {
  // Uses the existing Handyman2026 document; no writes.
  const spreadsheetId = "1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q";
  let response;
  try {
    response = Sheets.Spreadsheets.Values.get(spreadsheetId, "'ข้อมูลการบริการ'!A1:AD1", {
      valueRenderOption: "FORMATTED_VALUE", majorDimension: "ROWS"
    });
  } catch (_) {
    // Do not expose upstream errors, identifiers, or cell contents in logs.
    throw new Error("HEADER_READ_FAILED");
  }
  const headers = (response.values || [])[0] || [];
  const normalize = value => String(value == null ? "" : value).replace(/\s+/g, " ").trim();
  const expected = {
    A: "วันที่", B: "ลูกค้า", F: "รายการบริการ", G: "ประเภทบริการ",
    R: "สถานะงาน", S: "สรุปงานอาการเสีย และ หมายเหตุ",
    T: "งานที่ต้องทำต่อ", U: "สถานะใบเก็บเงิน",
    V: "Quotation NO.", AA: "รายได้จากการบริการ",
    AB: "ปี-เดือน", AD: "job_id"
  };
  const toIndex = col => [...col].reduce((n,c) => n*26+c.charCodeAt(0)-64,0)-1;
  const mismatches = Object.entries(expected).filter(([col,name]) =>
    normalize(headers[toIndex(col)]) !== normalize(name)).map(([col])=>col);
  const result = {
    status: mismatches.length ? "NEEDS_REVIEW" : "PASS",
    columnsChecked: Object.keys(expected).length,
    mismatches: mismatches,
    readRange: "A1:AD1",
    readonly: true
  };
  console.log(JSON.stringify(result));
  return result;
}
