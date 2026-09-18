$assessUrl = "https://endpoint-532eb3d4-0d9d-4b19-93c1-2ebc3060bca4.agentbase-runtime.aiplatform.vngcloud.vn/assess"
$memoUrl = "https://endpoint-05361e8d-12de-4860-8c26-d6e637d5aa42.agentbase-runtime.aiplatform.vngcloud.vn/build-memo-docx"

$payload = [System.IO.File]::ReadAllText("eb_credit_payload_real.json", [System.Text.Encoding]::UTF8)
$bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)

Write-Output "=== Step 1: POST /assess (eb-credit-agent) ==="
Write-Output "Payload: eb_credit_payload_real.json (real BCTC data)"
Write-Output ""

$t1 = Measure-Command { $assessResult = Invoke-RestMethod -Uri $assessUrl -Method Post -Body $bytes -ContentType "application/json; charset=utf-8" }
$assessJson = $assessResult | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText("assess_result_real.json", $assessJson, [System.Text.Encoding]::UTF8)

Write-Output ("HTTP 200 OK | Time: {0}s | Size: {1} bytes" -f [math]::Round($t1.TotalMilliseconds/1000, 3), $assessJson.Length)
Write-Output ""
Write-Output "Key results from /assess:"
Write-Output ("  Assessment ID: {0}" -f $assessResult.assessment_id)
Write-Output ("  Status: {0}" -f $assessResult.status)
Write-Output ("  Company: {0}" -f $assessResult.company.name)
Write-Output ("  Reporting Period: {0}" -f $assessResult.reporting_period)
Write-Output ("  Preliminary Decision: {0}" -f $assessResult.preliminary_decision.outcome)
Write-Output ("  Product 039: {0}" -f $assessResult.product_039_evaluation.decision)
Write-Output ""

Write-Output "  Ratios:"
Write-Output ("    NWC:     {0:N0} VND" -f $assessResult.ratios.nwc)
Write-Output ("    DSCR:    {0:F4}x" -f $assessResult.ratios.dscr)
Write-Output ("    ICR:     {0:F4}x" -f $assessResult.ratios.icr)
Write-Output ("    Net CF:  {0:N0} VND" -f $assessResult.ratios.net_cash_flow)
Write-Output ""

Write-Output "  Red Flags:"
foreach ($rf in $assessResult.red_flags) {
    $tag = if ($rf.triggered) { "[TRIGGERED]" } else { "[PASS]" }
    Write-Output ("    {0} {1} ({2})" -f $tag, $rf.title, $rf.severity)
}
Write-Output ""

Write-Output "  Supply Chain:"
Write-Output ("    Supplier concentration: {0}" -f $assessResult.supply_chain_analysis.supplier_concentration)
Write-Output ("    Buyer concentration:   {0}" -f $assessResult.supply_chain_analysis.buyer_concentration)
Write-Output ("    Top5 supplier ratio:   {0:P0}" -f $assessResult.supply_chain_analysis.top5_supplier_ratio)
Write-Output ("    Top5 buyer ratio:      {0:P0}" -f $assessResult.supply_chain_analysis.top5_buyer_ratio)
Write-Output ""

Write-Output "  Statement Anomalies:"
Write-Output ("    Triggered: {0} | Max severity: {1}" -f $assessResult.statement_anomaly_summary.triggered_count, $assessResult.statement_anomaly_summary.max_severity)
foreach ($an in $assessResult.statement_anomaly_summary.anomalies) {
    $tag = if ($an.triggered) { "[ALERT]" } else { "[OK]" }
    Write-Output ("    {0} {1} ({2}) - count: {3}" -f $tag, $an.title, $an.severity, $an.count)
}
Write-Output ""

Write-Output "  SWOT:"
Write-Output "    Strengths:"
foreach ($s in $assessResult.swot_analysis.strengths) { Write-Output "      + $s" }
Write-Output "    Weaknesses:"
foreach ($w in $assessResult.swot_analysis.weaknesses) { Write-Output "      - $w" }
Write-Output "    Opportunities:"
foreach ($o in $assessResult.swot_analysis.opportunities) { Write-Output "      > $o" }
Write-Output "    Threats:"
foreach ($t in $assessResult.swot_analysis.threats) { Write-Output "      ! $t" }
Write-Output ""

Write-Output "  Credit Covenants:"
Write-Output "    Conditions Precedent:"
foreach ($cp in $assessResult.credit_covenants.conditions_precedent) { Write-Output "      * $cp" }
Write-Output "    Conditions Subsequent:"
foreach ($cs in $assessResult.credit_covenants.conditions_subsequent) { Write-Output "      * $cs" }
Write-Output ""

Write-Output "=== Step 2: POST /build-memo-docx (credit-memo-builder) ==="
$t2 = Measure-Command { $memoResult = Invoke-RestMethod -Uri $memoUrl -Method Post -Body $bytes -ContentType "application/json; charset=utf-8" }
$memoJson = $memoResult | ConvertTo-Json -Depth 5
Write-Output ("HTTP 200 OK | Time: {0}s" -f [math]::Round($t2.TotalMilliseconds/1000, 3))
Write-Output ("  Status: {0}" -f $memoResult.status)
Write-Output ("  File: {0}" -f $memoResult.file_path)
Write-Output ("  Assessment ID: {0}" -f $memoResult.assessment_id)
Write-Output ("  Decision: {0}" -f $memoResult.preliminary_decision)
Write-Output ("  Product 039: {0}" -f $memoResult.product_039_decision)
Write-Output ""

Write-Output "=== Done! ==="
Write-Output ("Total time: {0}s" -f [math]::Round(($t1.TotalMilliseconds + $t2.TotalMilliseconds)/1000, 3))
Write-Output "Results saved to: assess_result_real.json"
