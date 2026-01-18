$ErrorActionPreference = "Continue"

Write-Host "Killing old processes..."
# Stop existing node/python to free ports
taskkill /F /IM node.exe 2>$null
taskkill /F /IM python.exe 2>$null
taskkill /F /IM uvicorn.exe 2>$null

Start-Sleep -Seconds 2

Write-Host "Starting Backend on Port 8001..."
# Run python uvicorn in a new window/process
$backend = Start-Process python -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8001" -WorkingDirectory "backend" -PassThru -WindowStyle Minimized

Write-Host "Starting Frontend on Port 3000..."
# Run npm via cmd /c to ensure batch file execution matches Windows environment
$frontend = Start-Process cmd -ArgumentList "/c npm run dev" -WorkingDirectory "frontend" -PassThru -WindowStyle Minimized

Write-Host "Waiting for services to initialize..."
Start-Sleep -Seconds 5

Write-Host "Services launched!"
Write-Host "Backend PID: $($backend.Id)"
Write-Host "Frontend PID: $($frontend.Id)"
Write-Host "--------------------------------"
Write-Host "Open Browser: http://localhost:3000"
