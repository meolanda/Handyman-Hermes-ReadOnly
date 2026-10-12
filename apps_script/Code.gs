/** API Executable entry point. Configuration comes from Script Properties. */
function readSales() {
  try {
    var config = loadConfig_();
    var range = "'" + config.sheetName.replace(/'/g, "''") + "'!" + config.dataRange;
    var response = Sheets.Spreadsheets.Values.get(config.spreadsheetId, range, {
      valueRenderOption: 'FORMATTED_VALUE', majorDimension: 'ROWS'
    });
    var values = response.values || [];
    if (!values.length || !values[0].length) throw new Error('HEADER_NOT_FOUND');
    return {ok: true, data: mapRows_(values.slice(0, config.maxRows + 1), config.columns),
      truncated: values.length - 1 > config.maxRows};
  } catch (error) {
    var known = ['CONFIG_REQUIRED', 'INVALID_CONFIG', 'UNSUPPORTED_ACTION',
      'SHEET_NOT_FOUND', 'HEADER_NOT_FOUND', 'COLUMN_NOT_FOUND', 'DUPLICATE_HEADER'];
    var code = known.indexOf(error.message) >= 0 ? error.message : 'READ_FAILED';
    return ({ok: false, error: {code: code}});
  }
}

function loadConfig_() {
  var props = PropertiesService.getScriptProperties().getProperties();
  if (!props.SPREADSHEET_ID || !props.SHEET_NAME || !props.HEADER_ROW ||
      !props.COLUMNS_JSON || !props.DATA_RANGE) throw new Error('CONFIG_REQUIRED');
  var columns;
  try { columns = JSON.parse(props.COLUMNS_JSON); }
  catch (_) { throw new Error('INVALID_CONFIG'); }
  var row = Number(props.HEADER_ROW);
  // Require a bounded, local A1 rectangle; the sheet name is configured separately.
  var match = /^([A-Z]{1,3})([1-9][0-9]*)(?::([A-Z]{1,3})([1-9][0-9]*))?$/.exec(props.DATA_RANGE);
  if (!match) throw new Error('INVALID_CONFIG');
  var firstCol = columnNumber_(match[1]);
  var lastCol = columnNumber_(match[3] || match[1]);
  var firstRow = Number(match[2]);
  var lastRow = Number(match[4] || match[2]);
  if (firstRow !== row || lastRow < firstRow || lastRow > 10000000 ||
      lastRow - firstRow > 10000 || lastCol < firstCol || lastCol > 18278 ||
      (lastRow - firstRow + 1) * (lastCol - firstCol + 1) > 100000) {
    throw new Error('INVALID_CONFIG');
  }
  var max = Number(props.MAX_ROWS || 100);
  if (!Number.isInteger(row) || row < 1 || !Number.isInteger(max) ||
      max < 1 || max > 1000 || !columns || Array.isArray(columns) ||
      typeof columns !== 'object' || !Object.keys(columns).length ||
      Object.keys(columns).some(function(key) {
        return !key || typeof columns[key] !== 'string' || !columns[key];
      })) throw new Error('INVALID_CONFIG');
  return {spreadsheetId: props.SPREADSHEET_ID, sheetName: props.SHEET_NAME,
    headerRow: row, dataRange: props.DATA_RANGE, maxRows: max, columns: columns};
}

function mapRows_(values, columns) {
  var headers = values[0];
  var keys = Object.keys(columns);
  var indexes = keys.map(function(key) {
    var index = headers.indexOf(columns[key]);
    if (index < 0) throw new Error('COLUMN_NOT_FOUND');
    if (headers.lastIndexOf(columns[key]) !== index) throw new Error('DUPLICATE_HEADER');
    return index;
  });
  return values.slice(1).filter(function(row) {
    return row.some(function(value) { return value !== ''; });
  }).map(function(row) {
    var record = Object.create(null);
    keys.forEach(function(key, i) { record[key] = row[indexes[i]] === undefined ? '' : String(row[indexes[i]]); });
    return record;
  });
}

function columnNumber_(letters) {
  return letters.split('').reduce(function(total, letter) {
    return total * 26 + letter.charCodeAt(0) - 64;
  }, 0);
}
