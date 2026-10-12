const fs=require('node:fs'), vm=require('node:vm'), assert=require('node:assert/strict');
const {test}=require('node:test');
const source=fs.readFileSync('webapp/Code.gs','utf8');
function setup(headers){
 const calls=[],logs=[];
 const context=vm.createContext({ContentService:{MimeType:{JSON:'json'},createTextOutput:s=>({setMimeType:()=>JSON.parse(s)})},
 Sheets:{Spreadsheets:{Values:{get:(...args)=>{calls.push(JSON.parse(JSON.stringify(args)));return {values:[headers]};}}}},
 console:{log:s=>logs.push(s)}});
 vm.runInContext(source,context);return {context,calls,logs};
}
function headers(){
 const result=Array(30).fill('');
 const pairs={0:'วันที่',1:'ลูกค้า',5:'รายการบริการ',6:'ประเภทบริการ',17:'สถานะงาน',18:'สรุปงานอาการเสีย และ หมายเหตุ',19:'งานที่ต้องทำต่อ',20:'สถานะใบเก็บเงิน',21:'Quotation NO.',26:'รายได้จากการบริการ',27:'ปี-เดือน',29:'job_id'};
 for(const [i,v] of Object.entries(pairs))result[i]=v;return result;
}
test('public doGet remains identical to PR mock and never reads Sheets',()=>{
 const {context,calls,logs}=setup(headers());
 assert.deepEqual(context.doGet(),{ok:true,service:'Handyman-Hermes-Test',mode:'mock',message:'Connection test only'});
 assert.deepEqual(calls,[]);assert.deepEqual(logs,[]);
});
test('header test checks 12 positions via read-only formatted GET',()=>{
 const {context,calls}=setup(headers());const result=context.testReadHeaders();
 assert.equal(result.status,'PASS');assert.equal(result.columnsChecked,12);
 assert.deepEqual(calls,[['1tqIJGOAkQnvCmu88MdBFu3vYxvOJ4gh2URxeCUsF9_Q',"'ข้อมูลการบริการ'!A1:AD1",{valueRenderOption:'FORMATTED_VALUE',majorDimension:'ROWS'}]]);
});
test('mismatch reports only column identifiers',()=>{
 const h=headers();h[18]='MOCK_PRIVATE_HEADER';const {context,logs}=setup(h);
 assert.equal(context.testReadHeaders().status,'NEEDS_REVIEW');assert.ok(!logs.join('').includes('MOCK_PRIVATE_HEADER'));
});
test('service errors sanitized and not logged',()=>{
 const {context,logs}=setup(headers());context.Sheets.Spreadsheets.Values.get=()=>{throw new Error('MOCK_SECRET');};
 assert.throws(()=>context.testReadHeaders(),/HEADER_READ_FAILED/);assert.deepEqual(logs,[]);
});
test('manifest uses only readonly scope and advanced sheets v4',()=>{
 const m=JSON.parse(fs.readFileSync('webapp/appsscript.json','utf8'));
 assert.deepEqual(m.oauthScopes,['https://www.googleapis.com/auth/spreadsheets.readonly']);
 assert.equal(m.dependencies.enabledAdvancedServices[0].serviceId,'sheets');
 assert.equal(m.dependencies.enabledAdvancedServices[0].version,'v4');
 assert.doesNotMatch(source,/SpreadsheetApp|\.Values\.(update|append|clear)|UrlFetchApp/);
});
