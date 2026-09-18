C:\Users\finan = 'C:\Users\finan'
Write-Host 'Temp:' C:\Users\finan\AppData\Local\Temp
Write-Host 'LocalAppData:' C:\Users\finan\AppData\Local
Write-Host 'Home:' 
# Check if there's a get_token.sh anywhere
 = Get-ChildItem -Path (Join-Path C:\Users\finan\AppData\Local\Temp 'opencode') -Filter '*.sh' -ErrorAction SilentlyContinue
if () { 
    foreach ( in ) { 
        Write-Host 'Found:' .FullName 
    }
} else {
    Write-Host 'No .sh files found in Temp/opencode'
}
