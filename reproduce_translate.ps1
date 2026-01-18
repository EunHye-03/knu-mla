$ErrorActionPreference = "Stop"

try {
    $body = @{
        text        = "Hello world"
        source_lang = "en"
        target_lang = "ko"
    } | ConvertTo-Json

    Write-Host "Sending Request to http://localhost:8001/api/translate"
    $response = Invoke-RestMethod -Uri "http://localhost:8001/api/translate" -Method Post -Body $body -ContentType "application/json"
    Write-Host "Success:"
    $response | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "Error:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $respBody = $reader.ReadToEnd()
        Write-Host "Response Body: $respBody"
    }
}
