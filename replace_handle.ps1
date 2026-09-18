$content = Get-Content 'templates/index.html' -Raw -Encoding UTF8
$start = $content.IndexOf('function handleFileSelect(e)')
$end = $content.IndexOf('function populateExtraction(data)', $start)
if ($start -ge 0 -and $end -gt $start) {
    $newContent = $content.Substring(0, $start) + $code + "
    " + $content.Substring($end)
    $newContent | Set-Content 'templates/index.html' -Encoding UTF8
}
