$ErrorActionPreference = "Stop"

$baseUrl = "http://localhost:8001"
$user = @{
    user_id   = "test_user_v7"
    password  = "password123"
    nickname  = "Test User"
    email     = "test_v7@example.com"
    user_lang = "en"
}

# 1. Register (ignore error if exists)
try {
    Write-Host "Registering..."
    $regBody = $user | ConvertTo-Json
    Invoke-RestMethod -Uri "$baseUrl/api/auth/register" -Method Post -Body $regBody -ContentType "application/json" | Out-Null
    Write-Host "Registered."
}
catch {
    Write-Host "Register failed (probably exists): $($_.Exception.Message)"
}

# 2. Login
try {
    Write-Host "Logging in..."
    $loginBody = @{
        user_id  = $user.user_id
        password = $user.password
    } | ConvertTo-Json
    $tokenParams = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $token = $tokenParams.access_token
    Write-Host "Got Token: $token"
}
catch {
    Write-Error "Login failed: $($_.Exception.Message)"
}

# 3. Translate
try {
    Write-Host "Testing /api/translate..."
    $transBody = @{
        text        = "Hello world"
        source_lang = "en"
        target_lang = "ko"
    } | ConvertTo-Json

    $headers = @{
        Authorization = "Bearer $token"
    }

    $response = Invoke-RestMethod -Uri "$baseUrl/api/translate" -Method Post -Body $transBody -ContentType "application/json" -Headers $headers
    
    Write-Host "Success!"
    $response | ConvertTo-Json -Depth 10
}
catch {
    Write-Host "Translate Failed:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $respBody = $reader.ReadToEnd()
        Write-Host "Response Body: $respBody"
    }
}
