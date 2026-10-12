const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {test} = require('node:test');
const source = fs.readFileSync('apps_script/Code.gs', 'utf8');
const valid = {SPREADSHEET_ID:'MOCK_ID', SHEET_NAME:'MOCK_TAB', HEADER_ROW:'1',
 DATA_RANGE:'A1:B1001', COLUMNS_JSON:'{"mock_item":"MOCK_ITEM","mock_total":"MOCK_TOTAL"}'};
function setup(props={}, values=[['MOCK_ITEM','MOCK_TOTAL'],['A','1,000.00'],[]]) {
 const calls=[], logs=[];
 const context=vm.createContext({PropertiesService:{getScriptProperties:()=>({getProperties:()=>props})},
 Sheets:{Spreadsheets:{Values:{get:(...args)=>{calls.push(JSON.parse(JSON.stringify(args)));return {values};}}}},
 console:{log:(...args)=>logs.push(args),error:(...args)=>logs.push(args)},Logger:{log:(...args)=>logs.push(args)}});
 vm.runInContext(source,context);
 return {context,calls,logs};
}
test('uses Values.get only with configured range and formatted strings',()=>{
 const {context,calls}=setup(valid);const result=context.readSales();
 assert.equal(result.ok,true);assert.equal(result.data.length,1);
 assert.equal(result.data[0].mock_total,'1,000.00');
 assert.deepEqual(calls,[['MOCK_ID',"'MOCK_TAB'!A1:B1001",{valueRenderOption:'FORMATTED_VALUE',majorDimension:'ROWS'}]]);
});
test('caller cannot override configured spreadsheet, tab or range',()=>{
 const {context,calls}=setup(valid);
 context.readSales({spreadsheetId:'OTHER',sheetName:'OTHER',dataRange:'Z1:Z9'});
 assert.equal(calls[0][0],'MOCK_ID');assert.equal(calls[0][1],"'MOCK_TAB'!A1:B1001");
});
test('quotes tab names and escapes apostrophes',()=>{
 const {context,calls}=setup({...valid,SHEET_NAME:"ฝ่ายขาย '2026!"});context.readSales();
 assert.equal(calls[0][1],"'ฝ่ายขาย ''2026!'!A1:B1001");
});
test('missing configuration fails without API call',()=>{
 for(const key of ['SPREADSHEET_ID','SHEET_NAME','HEADER_ROW','COLUMNS_JSON','DATA_RANGE']){
  const props={...valid};delete props[key];const {context,calls}=setup(props);
  assert.equal(context.readSales().error.code,'CONFIG_REQUIRED');assert.equal(calls.length,0);
 }
});
test('invalid and unbounded ranges fail without API call',()=>{
 for(const overrides of [{HEADER_ROW:'0'},{MAX_ROWS:'1001'},{COLUMNS_JSON:'bad'},{COLUMNS_JSON:'{}'},
 {DATA_RANGE:'A:B'},{DATA_RANGE:'OTHER!A1:B2'},{DATA_RANGE:'B1:A2'},{DATA_RANGE:'A2:B3'},
 {DATA_RANGE:'A1:B10002'},{DATA_RANGE:'A1:ZZZ1001'},{DATA_RANGE:'A1:B0'}]){
 const {context,calls}=setup({...valid,...overrides});
 assert.equal(context.readSales().error.code,'INVALID_CONFIG');assert.equal(calls.length,0);
 }
});
test('missing and duplicate headers fail',()=>{
 assert.equal(setup(valid,[['OTHER']]).context.readSales().error.code,'COLUMN_NOT_FOUND');
 assert.equal(setup(valid,[['MOCK_ITEM','MOCK_ITEM','MOCK_TOTAL']]).context.readSales().error.code,'DUPLICATE_HEADER');
});
test('empty API result reports missing header',()=>{
 assert.equal(setup(valid,undefined).context.readSales().ok,true);
 assert.equal(setup(valid,[]).context.readSales().error.code,'HEADER_NOT_FOUND');
 const {context}=setup(valid);context.Sheets.Spreadsheets.Values.get=()=>({});
 assert.equal(context.readSales().error.code,'HEADER_NOT_FOUND');
});
test('pads omitted trailing cells and preserves formatted values',()=>{
 const {context}=setup(valid,[['MOCK_ITEM','MOCK_TOTAL'],['A'],['B','0.00']]);
 assert.equal(context.readSales().data[0].mock_total,'');
 assert.equal(context.readSales().data[1].mock_total,'0.00');
});
test('reports truncation within configured range',()=>{
 const {context}=setup({...valid,MAX_ROWS:'1'},[['MOCK_ITEM','MOCK_TOTAL'],['A','1'],['B','2']]);
 const result=context.readSales();assert.equal(result.truncated,true);assert.equal(result.data.length,1);
});
test('JSON-compatible API Executable result with no web entry points',()=>{
 const {context}=setup(valid);assert.equal(typeof context.doGet,'undefined');assert.equal(typeof context.doPost,'undefined');
 assert.equal(JSON.parse(JSON.stringify(context.readSales())).data[0].mock_item,'A');
});
test('API secrets do not appear in response or logs',()=>{
 const {context,logs}=setup(valid);
 context.Sheets.Spreadsheets.Values.get=()=>{throw new Error('MOCK_SECRET_DO_NOT_LOG');};
 assert.deepEqual(JSON.parse(JSON.stringify(context.readSales())),{ok:false,error:{code:'READ_FAILED'}});
 assert.deepEqual(logs,[]);
});
test('manifest registers Sheets v4 and contains only approved scopes',()=>{
 const manifest=JSON.parse(fs.readFileSync('apps_script/appsscript.json','utf8'));
 assert.deepEqual(manifest.dependencies.enabledAdvancedServices,[{userSymbol:'Sheets',serviceId:'sheets',version:'v4'}]);
 assert.deepEqual(manifest.oauthScopes,['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/spreadsheets.readonly']);
 assert.doesNotMatch(source,/SpreadsheetApp|ContentService|UrlFetchApp|Logger\.|console\./);
 assert.deepEqual([...source.matchAll(/Sheets\.Spreadsheets\.([A-Za-z.]+)/g)].map(m=>m[1]),['Values.get']);
});
test('configured A1 probe validates date header and returns no service records',()=>{
 const props=JSON.parse(fs.readFileSync('config/script-properties.json','utf8'));
 const {context,calls}=setup(props,[['วันที่']]);
 assert.deepEqual(JSON.parse(JSON.stringify(context.readSales())),{ok:true,data:[],truncated:false});
 assert.equal(calls[0][1],"'ข้อมูลการบริการ'!A1:AD100");
 assert.equal(calls[0][0],props.SPREADSHEET_ID);
});
test('A1 probe rejects mismatched header',()=>{
 const props=JSON.parse(fs.readFileSync('config/script-properties.json','utf8'));
 assert.equal(setup(props,[['ผิดหัวตาราง']]).context.readSales().error.code,'COLUMN_NOT_FOUND');
});
test('user supplied headers map all twelve fields using synthetic service row',()=>{
 const fixture=JSON.parse(fs.readFileSync('tests/fixtures/service-values.json','utf8'));
 const schema=JSON.parse(fs.readFileSync('config/service-schema.json','utf8'));
 const props={...valid,DATA_RANGE:'A1:AD2',COLUMNS_JSON:JSON.stringify(schema.columns)};
 const result=setup(props,fixture.values).context.readSales();
 assert.deepEqual(JSON.parse(JSON.stringify(result)),{ok:true,data:[fixture.expected],truncated:false});
});
test('full schema cannot be mistaken for an A1-only successful read',()=>{
 const schema=JSON.parse(fs.readFileSync('config/service-schema.json','utf8'));
 assert.equal(setup({...valid,DATA_RANGE:'A1',COLUMNS_JSON:JSON.stringify(schema.columns)},[['วันที่']]).context.readSales().error.code,'COLUMN_NOT_FOUND');
});
