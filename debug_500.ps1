$ErrorActionPreference = "Continue"

# 1. Clean up old logs
if (Test-Path backend_err.log) { Remove-Item backend_err.log }
if (Test-Path backend_out.log) { Remove-Item backend_out.log }

Write-Host "Starting Backend Service..."

# 2. Start Backend Process with Redirection
# Using PassThru to keep reference to the process object
$proc = Start-Process python -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8002" -WorkingDirectory "backend" -PassThru -RedirectStandardError "backend_err.log" -RedirectStandardOutput "backend_out.log"

if (-not $proc) {
    Write-Error "Failed to start backend process."
    exit
}

Write-Host "Backend started with PID: $($proc.Id). Waiting for startup..."
Start-Sleep -Seconds 12

# 3. Send Request
Write-Host "Sending Register Request..."
$body = @{
    user_id   = "debug_user_500"
    password  = "password123"
    nickname  = "Debug User"
    email     = "debug500@example.com"
    user_lang = "en"
} | ConvertTo-Json

try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8002/auth/register" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Request Succeeded unexpectedly."
}
catch {
    Write-Host "Request Failed as expected: $($_.Exception.Message)"
}

# 4. Cleanup
Write-Host "Stopping Backend..."
Stop-Process -Id $proc.Id -Force

Write-Host "--- ERROR LOG CONTENT ---"
if (Test-Path backend_err.log) { Get-Content backend_err.log } else { Write-Host "No error log found." }

Write-Host "--- OUTPUT LOG CONTENT ---"
if (Test-Path backend_out.log) { Get-Content backend_out.log } else { Write-Host "No output log found." }
