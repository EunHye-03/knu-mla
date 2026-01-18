$ErrorActionPreference = "Continue"

Write-Host "Stopping existing processes..."
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
Stop-Process -Name node -Force -ErrorAction SilentlyContinue

Write-Host "Starting Backend on 8001..."
$backend = Start-Process python -ArgumentList "-m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001" -WorkingDirectory "backend" -PassThru

Write-Host "Starting Frontend on 3000..."
$frontend = Start-Process npm.cmd -ArgumentList "run dev" -WorkingDirectory "frontend" -PassThru

Write-Host "Services started!"
Write-Host "Backend PID: $($backend.Id)"
Write-Host "Frontend PID: $($frontend.Id)"
Write-Host "Access Frontend at: http://localhost:3000"
