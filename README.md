# Handyman-Hermes-ReadOnly

โครงการอ่านชีตที่มีอยู่แล้ว **สรุปยอดขาย Handyman2026** ด้วย Apps Script API Executable (`scripts.run`) และ Python Client สำหรับเรียกจาก Hermes ภายหลัง ไม่มี Web App `doGet`/`doPost` หรือ public endpoint

งานนี้เปลี่ยนเฉพาะไฟล์ใน checkout นี้ ไม่มีการสร้าง OAuth Credentials/Refresh Token, Deploy, เชื่อมชีตจริง, แก้ Handyman Web App เดิม, แก้ Config ของ Hermes หรือติดตั้ง/เปิดใช้ Google Workspace Skill เดิม

## ไฟล์และ protocol

- `apps_script/Code.gs`: entry point `readSales()` คืน JSON-compatible object อ่านเฉพาะชีต/แท็บ/คอลัมน์จาก Script Properties
- `apps_script/appsscript.json`: V8 และ scopes สองรายการด้านล่าง
- `src/handyman_hermes/client.py`: HTTPS POST ไปยัง `https://script.googleapis.com/v1/scripts/{scriptId}:run`
- `config/example.json`: Config สำหรับช่วงทดสอบแรก มี Spreadsheet ID/ชื่อแท็บแล้ว; script ID ยังรอตั้งค่า
- `tests/fixtures/sales.json`: ข้อมูลสมมติ ไม่ได้มาจากชีตจริง
- `tests/test_client.py`, `tests/test_apps_script.cjs`: ทดสอบทั้งหมดด้วย Mock

Request body: `{"function":"readSales","parameters":[],"devMode":false}` และ header `Authorization: Bearer <access_token>` ไม่มี token/API key ใน URL หรือ body ไม่มีการ log request/header/token และบล็อก HTTP redirect เพื่อไม่ส่ง Authorization ไปปลายทางอื่น

Apps Script ไม่รับ Spreadsheet ID/ชื่อแท็บจาก request ไม่มีคำสั่งเขียนชีต อ่านผ่าน `Sheets.Spreadsheets.Values.get()` เท่านั้น โดยใช้ `valueRenderOption: "FORMATTED_VALUE"` และ `majorDimension: "ROWS"` ไม่ตีความยอดเงินหรือวันที่เอง และไม่คำนวณยอดรวม

## OAuth 2.0 scopes

กำหนดตรงกันใน manifest, Config template และ `OAUTH_SCOPES` ของ Python:

- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/spreadsheets.readonly`

ไม่ขอ Drive scope หรือ scope เขียน Sheets รายการ scopes เป็นเพียงการประกาศ ไม่ได้เชื่อมบัญชีหรือสร้าง Credentials

Python Client **ไม่รับผิดชอบการสร้าง/ต่ออายุ/เก็บ token** ผู้เรียกต้องส่ง short-lived access token ในแต่ละครั้ง Client ไม่เก็บ token เป็น attribute และไม่เปลี่ยน Hermes Config ห้ามส่ง token ผ่าน command-line arguments หรือบันทึก token ลง config/example.json

## ทดสอบ offline

ใช้ checkout ปัจจุบัน ไม่ต้องสร้าง Git worktree ต้องมี Python >=3.10 และ Node.js >=18 ไม่มี runtime dependency ภายนอก

```bash
cd /workspace/Handyman-Hermes-ReadOnly
PYTHONPATH=src python -m unittest discover -s tests -v
node --test tests/test_apps_script.cjs
```

Python tests mock HTTP opener ทั้งหมด Apps Script tests ใช้ Node VM และ Sheets.Spreadsheets.Values.get/PropertiesService จำลอง ไม่มีการเรียกบริการจริง

ครอบคลุม protocol POST, header authentication, scope consistency, API/ExecutionError, HTTP 401/403/429, network failure, malformed response, truncation, redirect blocking และ token ไม่ปรากฏใน URL/body/client state/log/error/exception chain/traceback ที่จัดรูปแบบตามปกติ

ขอบเขตการป้องกันความลับ: debugger, memory dump หรือ traceback tool ที่ dump local variables ยังอาจเห็น token/request ในหน่วยความจำได้ ผู้เรียกต้องปิดการ log HTTP headers และไม่ dump locals; Client ไม่สามารถควบคุม logger ของโปรแกรมภายนอกได้

## ติดตั้งและตั้งค่าภายหลัง

ขั้นตอนนี้เป็นเอกสารเท่านั้น ต้องได้รับอนุญาตก่อนทำงานกับ Google Cloud หรือข้อมูลจริง

```bash
python -m venv .venv
.venv/bin/python -m pip install -e .
```

การติดตั้ง package อาจดาวน์โหลด setuptools จาก PyPI การทดสอบด้านบนไม่ต้องติดตั้ง package

คัดลอก `config/example.json` เป็น `config/local.json` ที่ถูก ignore หากต้องการจดค่าที่ไม่ใช่ความลับ ไฟล์นี้ไม่ได้โหลดเข้า Apps Script/Python อัตโนมัติ:

| ค่า | ความหมาย |
| --- | --- |
| spreadsheet_id | ID ของชีตเดิม |
| sheet_name | ชื่อแท็บจริง ต้องตรงทุกตัวอักษร |
| header_row | เลขแถวหัวตาราง เริ่มที่ 1 ต้องตรงกับแถวแรกของ data_range |
| data_range | ช่วง A1 แบบมีขอบเขต เช่นรูปแบบ `A1:D101` (ตัวอย่างสมมติ ไม่ใช่ช่วงจริง) ไม่รวมชื่อแท็บ |
| columns | mapping ชื่อ field ที่ตกลงกับ Hermes → ข้อความหัวคอลัมน์จริง |
| script_id | Script ID สำหรับ scripts.run ไม่ใช่ Web App URL หรือ Spreadsheet ID |
| max_rows | 1–1000 ค่าเริ่มต้น 100 |
| oauth_scopes | scopes สองรายการข้างต้น ไม่ใช่ access token |

ตั้ง Apps Script Properties ภายหลัง: `SPREADSHEET_ID`, `SHEET_NAME`, `HEADER_ROW`, `COLUMNS_JSON`, `MAX_ROWS`, `DATA_RANGE` หัวคอลัมน์ที่เลือกต้องไม่ซ้ำ Config ไม่ครบคืน `CONFIG_REQUIRED`

### สิ่งที่ต้องยืนยันก่อนใช้งานจริง

1. API Executable deployment และสิทธิ์ผู้ใช้ที่ได้รับอนุญาต ไม่ Deploy เป็น Web App สาธารณะ
2. Apps Script และ OAuth client ใช้ standard Google Cloud project ที่เหมาะสมร่วมกัน และเปิด Apps Script API ตามข้อกำหนดของ scripts.run ตรวจ OAuth consent/ผู้ใช้ทดสอบ/นโยบายองค์กรภายหลัง
3. OAuth user ต้องมีสิทธิ์อ่านชีต และ token ต้องครอบคลุม scopes ทั้งหมดของ script ไม่ใช้ service account แทน OAuth user สำหรับ scripts.run
4. Manifest ประกาศ Advanced Sheets Service (`userSymbol: Sheets`, `serviceId: sheets`, `version: v4`) แล้ว แต่ยังไม่ได้เปิด Sheets API ใน Google Cloud จริง ต้องเปิดและยืนยันสิทธิ์ภายหลัง โดยคง scope อ่านอย่างเดียว
5. ยืนยัน script ID, Spreadsheet ID, ชื่อแท็บ/คอลัมน์จริง และ MAX_ROWS สำหรับข้อมูลจริง
6. การได้มา/ต่ออายุ/เก็บ access token และการเชื่อม adapter กับ Hermes ยังไม่ได้อนุมัติหรือ implement ต้องกำหนดแยกต่างหาก

### ตัวอย่างเรียก Python ภายหลัง

```python
from handyman_hermes import HermesSheetsClient

client = HermesSheetsClient(script_id=YOUR_APPROVED_SCRIPT_ID)
records = client.read_sales(access_token=ACCESS_TOKEN_FROM_APPROVED_PROVIDER)
```

ตัวแปรในตัวอย่างเป็น placeholder ไม่ใช่ credentials จริง ไม่มีการสร้างหรือเก็บ Refresh Token

Client ตรวจ `done`, `error` และ `response.result` ของ scripts.run โดยไม่แสดง remote error messages/stack traces ซึ่งอาจมีข้อมูลลับ API errors และ script execution errors คืน `SheetsReadError` แบบข้อความคงที่ Application error codes ผ่าน allowlist เท่านั้น ข้อมูลผิด schema หรือ `truncated: true` ถือเป็น error เพื่อไม่ให้ Hermes ใช้ข้อมูลยอดขายไม่ครบ ไม่มี automatic retry/refresh token

## ผลตรวจและข้อจำกัด

Mock tests พิสูจน์ logic/protocol เท่านั้น ไม่ยืนยัน Google permissions, Apps Script runtime/scopes, deployment, OAuth consent หรือข้อมูล Production โครงการนี้เป็น adapter ที่แยกจาก Hermes ยังไม่ได้ติดตั้งเป็น Hermes plugin

## ขอบเขตช่วงอ่าน

`DATA_RANGE` เป็นค่าที่ผู้ดูแลกำหนดใน Script Properties เท่านั้น ต้องเป็นสี่เหลี่ยม A1 มีต้น/ปลายชัดเจน เช่น `B3:F1003` และ `HEADER_ROW` ต้องเป็น 3 ในตัวอย่างนี้ ชื่อแท็บถูก quote/escape แยกต่างหาก ไม่รับ range/ID/แท็บจาก arguments ของ `readSales()`

เพื่อจำกัดทรัพยากร ช่วงอ่านต้องไม่เกิน 10,001 แถวและ 100,000 เซลล์ Client ได้ไม่เกิน MAX_ROWS แถวข้อมูล ส่วน `truncated` หมายถึงมีแถวเกิน MAX_ROWS **ภายใน DATA_RANGE เท่านั้น** ไม่ตรวจหรืออ้างว่าครอบคลุมข้อมูลนอกช่วง ผู้ดูแลต้องกำหนดช่วงให้ครอบคลุมข้อมูลที่ต้องการเอง แถวหัวตารางคือแถวแรกของช่วงที่กำหนด ค่าท้ายแถวที่ Sheets API ไม่ส่งมาจะถูกเติมเป็น string ว่าง

โค้ดไม่มีคำสั่ง update/append/create หรือ token จริง ค่า `MOCK_SECRET_DO_NOT_LOG` ในชุดทดสอบเป็น sentinel สมมติ ใช้พิสูจน์ว่า error/log ไม่เปิดเผยข้อมูล ไม่ใช่ credential

## Config ตามข้อมูลที่ผู้ใช้แจ้ง (ขั้นตอนปัจจุบัน)

`config/example.json` ตั้ง Spreadsheet ID และแท็บ `ข้อมูลการบริการ` แล้ว ช่วงทดสอบจำกัดอยู่ที่ **`'ข้อมูลการบริการ'!A1:AD100`** หัวตารางแถว 1 โดยเลือก mapping เฉพาะ `date → วันที่` สำหรับ probe นี้ `config/script-properties.json` เป็นค่าพร้อมคัดลอกลง Script Properties ภายหลัง ไม่มี token/credential และยังไม่ได้ส่งค่าเหล่านี้ไป Google

`readSales()` อ่านแถวหัวตารางและแถวข้อมูลภายใน A1:AD100 โดย Config ปัจจุบันส่งออกเฉพาะ field `date` ตาม mapping ที่ตั้งไว้ หากไม่มีแถวข้อมูลจะคืน `data: []` ผล Mock ไม่ยืนยันข้อมูลจริงหรือยอดขายครบทั้งชีต

`config/service-schema.json` บันทึก mapping ทั้ง 12 คอลัมน์และตำแหน่งตามผู้ใช้แจ้ง (A, B, F, G, R, S, T, U, V, AA, AB, AD) โดย `data_range` ยังเป็น null สำหรับการอ่านแถวบริการจริง Field ภาษาอังกฤษเป็นชื่อภายใน adapter ไม่ใช่การเปลี่ยนหัวตารางหรือ Config ของ Hermes

`tests/fixtures/service-values.json` เป็นหัวคอลัมน์ตามที่แจ้งพร้อมแถวข้อมูลสมมติ ช่องอื่นที่ไม่ได้แจ้งใช้ค่าว่าง ไม่เดาชื่อหัวคอลัมน์ โครงสร้าง response อ่านเต็ม schema ผ่าน Mock เท่านั้น โดยใช้ช่วง `A1:AD2` ใน test และไม่ได้นำช่วงดังกล่าวไปตั้ง Config สำหรับอ่านจริง

ขั้นตอนติดตั้ง Apps Script ภายหลังเมื่ออนุญาต:

1. นำ Code.gs และ appsscript.json ไปยังโครงการ Apps Script ที่เลือกอย่างชัดเจน ไม่แก้ Handyman Web App เดิม และไม่สร้างชีตใหม่
2. ตรวจ manifest มี Advanced Sheets Service v4 และ scopes userinfo.email/spreadsheets.readonly; เปิด Sheets API ใน standard Google Cloud project ที่ถูกต้องเมื่อได้รับอนุญาต
3. คัดลอกค่าจาก config/script-properties.json เป็น Script Properties; JSON นี้ไม่โหลดอัตโนมัติ
4. ก่อนใช้งานผ่าน scripts.run ต้องอนุมัติ API Executable deployment, OAuth และ token acquisition แยกต่างหาก ขั้นตอนเหล่านี้ยังไม่ได้ทำ
5. การอ่านรายการบริการทั้ง 12 fields ต้องกำหนดช่วงจริงที่ครอบคลุมถึง AD และแถวข้อมูล พร้อมใช้ columns จาก service-schema.json แทน probe mapping ช่วงปัจจุบัน A1:AD100 ครอบคลุมถึง AD แล้ว แต่ mapping ปัจจุบันยังมีเฉพาะ date; การเพิ่ม mapping ต้องได้รับอนุญาต

การตรวจครั้งนี้ใช้ข้อมูลที่ผู้ใช้แจ้งและ Mock เท่านั้น ยังไม่ได้ยืนยันชื่อหัวคอลัมน์ ข้อมูล สิทธิ์ หรือ runtime ของชีตจริงใน Workspace

## ผลทดสอบก่อนนำขึ้น GitHub

Python 13 tests และ Apps Script Mock 16 tests รวม 29/29 ผ่าน ไม่มีการข้าม tests ไม่มีการเชื่อมข้อมูลจริง Config มี Spreadsheet ID ที่ผู้ใช้ให้มา (ไม่ใช่ credential) แต่ไม่มีข้อมูลแถวลูกค้าจริง Fixtures ทั้งหมดเป็นข้อมูลจำลอง
