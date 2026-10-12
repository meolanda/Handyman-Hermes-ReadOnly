const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {test} = require('node:test');
const source = fs.readFileSync('webapp/Code.gs', 'utf8');
const fixture = JSON.parse(fs.readFileSync('tests/fixtures/service-values.json', 'utf8'));
const expectedHeaders = [...fixture.values[0]];
expectedHeaders[18] = 'สรุปงานอาการเสีย และ หมายเหตุ'; // PR #2 expectation; live verification remains pending.
function setup(values) {
  const calls = [], logs = [];
  const context = vm.createContext({
    Sheets: {Spreadsheets: {Values: {get: (...args) => {calls.push(args); return {values};}}}},
    console: {log: value => logs.push(value)},
    ContentService: {MimeType: {JSON: 'application/json'}, createTextOutput: text => ({text, setMimeType(type) {this.type = type; return this;}})}
  });
  vm.runInContext(source, context);
  return {context, calls, logs};
}
test('public doGet preserves backup mock exactly and never reads Sheets', () => {
  const {context, calls} = setup();
  const output = context.doGet({parameter: {action: 'testReadHeaders'}});
  assert.deepEqual(JSON.parse(output.text), {ok:true,service:'Handyman-Hermes-Test',mode:'mock',message:'Connection test only'});
  assert.equal(output.type, 'application/json');
  assert.equal(calls.length, 0);
  assert.equal(typeof context.doPost, 'undefined');
});
test('checks twelve headers with one bounded read and logs metadata only', () => {
  const {context, calls, logs} = setup([expectedHeaders]);
  assert.equal(context.testReadHeaders().status, 'PASS');
  assert.equal(calls.length, 1);
  assert.equal(calls[0][1], "'ข้อมูลการบริการ'!A1:AD1");
  assert.deepEqual(JSON.parse(logs[0]), {status:'PASS',columnsChecked:12,mismatches:[],readRange:'A1:AD1',readonly:true});
});
test('empty or mismatched headers fail verification', () => {
  assert.deepEqual(JSON.parse(JSON.stringify(setup([fixture.values[0]]).context.testReadHeaders().mismatches)), ['S']);
  assert.equal(setup([]).context.testReadHeaders().status, 'NEEDS_REVIEW');
  const headers = [...fixture.values[0]]; headers[0] = 'PRIVATE_VALUE';
  const {context, logs} = setup([headers]);
  assert.equal(context.testReadHeaders().status, 'NEEDS_REVIEW');
  assert.doesNotMatch(logs.join(''), /PRIVATE_VALUE/);
});
test('upstream error details are sanitized', () => {
  const {context, logs} = setup();
  context.Sheets.Spreadsheets.Values.get = () => {throw new Error('PRIVATE_SECRET');};
  assert.throws(() => context.testReadHeaders(), /HEADER_READ_FAILED/);
  assert.deepEqual(logs, []);
});
test('manifest allows only readonly Sheets scope and code has only Values.get', () => {
  const manifest = JSON.parse(fs.readFileSync('webapp/appsscript.json', 'utf8'));
  assert.deepEqual(manifest.oauthScopes, ['https://www.googleapis.com/auth/spreadsheets.readonly']);
  assert.deepEqual(manifest.dependencies.enabledAdvancedServices, [{userSymbol:'Sheets',serviceId:'sheets',version:'v4'}]);
  assert.equal(manifest.webapp, undefined);
  assert.doesNotMatch(source, /SpreadsheetApp|UrlFetchApp|setValues|appendRow/);
  assert.deepEqual([...source.matchAll(/Sheets\.Spreadsheets\.([A-Za-z.]+)/g)].map(m => m[1]), ['Values.get']);
});
