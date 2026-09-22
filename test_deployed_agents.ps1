$PAYLOAD = Get-Content "data_test\1. CTY DAU TU GROUP (MOCK AN DANH)\eb_credit_payload.json" -Raw -Encoding UTF8

$ASSESS_URL = "https://endpoint-532eb3d4-0d9d-4b19-93c1-2ebc3060bca4.agentbase-runtime.aiplatform.vngcloud.vn"
$MEMO_URL   = "https://endpoint-05361e8d-12de-4860-8c26-d6e637d5aa42.agentbase-runtime.aiplatform.vngcloud.vn"

Write-Host "=== 1. Health Check ===" -ForegroundColor Cyan
$health1 = curl.exe -s "$ASSESS_URL/health"
$health2 = curl.exe -s "$MEMO_URL/health"
Write-Host "eb-credit-agent:       $health1"
Write-Host "credit-memo-builder:   $health2"

Write-Host "`n=== 2. Test /assess (eb-credit-agent) ===" -ForegroundColor Cyan
$payloadFile = "$env:TEMP\test_payload.json"
[System.IO.File]::WriteAllText($payloadFile, $PAYLOAD, [System.Text.UTF8Encoding]::new($false))
$resp1 = curl.exe -s -X POST "$ASSESS_URL/assess" -H "Content-Type: application/json" -d "@$payloadFile" -w "`nHTTP:%{http_code} TIME:%{time_total}s SIZE:%{size_download}"
Write-Host $resp1

Write-Host "`n=== 3. Test /build-memo-docx (credit-memo-builder) ===" -ForegroundColor Cyan
$memoBody = '{"eb_payload":' + $PAYLOAD + '}'
$memoFile = "$env:TEMP\test_memo.json"
[System.IO.File]::WriteAllText($memoFile, $memoBody, [System.Text.UTF8Encoding]::new($false))
$resp2 = curl.exe -s -X POST "$MEMO_URL/build-memo-docx" -H "Content-Type: application/json" -d "@$memoFile" -w "`nHTTP:%{http_code} TIME:%{time_total}s SIZE:%{size_download}"
Write-Host $resp2

Write-Host "`n=== 4. Stress Test (5 requests x each agent) ===" -ForegroundColor Cyan
for ($i = 1; $i -le 5; $i++) {
    $t1 = (curl.exe -s -o NUL -w "%{time_total}" -X POST "$ASSESS_URL/assess" -H "Content-Type: application/json" -d "@$payloadFile")
    $t2 = (curl.exe -s -o NUL -w "%{time_total}" -X POST "$MEMO_URL/build-memo-docx" -H "Content-Type: application/json" -d "@$memoFile")
    Write-Host "  Request ${i}: assess=${t1}s  memo=${t2}s"
}
Write-Host "`nDone!" -ForegroundColor Green
