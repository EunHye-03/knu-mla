$ErrorActionPreference = "Continue"

# Cleanup
if (Test-Path backend_err.log) { Remove-Item backend_err.log }

Write-Host "Starting Backend Service on Port 8003..."
$proc = Start-Process python -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8003" -WorkingDirectory "backend" -PassThru -RedirectStandardError "backend_err.log" -RedirectStandardOutput "backend_out.log"

Write-Host "Waiting for startup..."
Start-Sleep -Seconds 12

$rnd = Get-Random
$uid = "user_$rnd"
$email = "user_$rnd@example.com"

Write-Host "SENDING REGISTER REQUEST for $uid..."
try {
    $body = @{user_id = $uid; password = "password123"; nickname = "Final"; email = $email; user_lang = "en" } | ConvertTo-Json
    $res = Invoke-RestMethod -Uri "http://127.0.0.1:8003/auth/register" -Method Post -Body $body -ContentType "application/json"
    Write-Host "REGISTER SUCCESS!"
    Write-Host "User ID: $($res.user_id)"
    
    Start-Sleep -Seconds 1
    
    Write-Host "SENDING LOGIN REQUEST..."
    $login = @{user_id = $uid; password = "password123" } | ConvertTo-Json
    $token = Invoke-RestMethod -Uri "http://127.0.0.1:8003/auth/login" -Method Post -Body $login -ContentType "application/json"
    Write-Host "LOGIN SUCCESS! Token Obtained."
    
    Write-Host "SENDING TRANSLATE REQUEST..."
    $trans = @{text = "Backend Fixed"; target_lang = "ko" } | ConvertTo-Json
    $headers = @{Authorization = "Bearer $($token.access_token)" }
    $tRes = Invoke-RestMethod -Uri "http://127.0.0.1:8003/translate" -Method Post -Body $trans -Headers $headers -ContentType "application/json"
    Write-Host "TRANSLATE SUCCESS! Result: $($tRes.data.translated_text)"

}
catch {
    Write-Host "REQUEST FAILED: $($_.Exception.Message)"
    $stream = $_.Exception.Response.GetResponseStream()
    if ($stream) { $reader = New-Object System.IO.StreamReader($stream); Start-Sleep -Seconds 1; Write-Host "DETAIL: $($reader.ReadToEnd())" }
}

Write-Host "Stopping Backend..."
Stop-Process -Id $proc.Id -Force
Start-Sleep -Seconds 1

Write-Host "--- SERVER LOG ---"
if (Test-Path backend_err.log) { Get-Content backend_err.log }
