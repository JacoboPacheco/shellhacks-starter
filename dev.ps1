# Starts backend (auto-reloads on save) and frontend in two new windows.
# Usage, from the repo root in PowerShell:  .\dev.ps1
# If Windows blocks it: powershell -ExecutionPolicy Bypass -File .\dev.ps1

$root = $PSScriptRoot

if ($env:SSH_CONNECTION -or $env:SSH_CLIENT) {
    Write-Host "You're connected over SSH. The windows this script opens would appear on the remote machine's screen, not yours." -ForegroundColor Yellow
    Write-Host "Instead, open two terminals and run:"
    Write-Host "  cd backend;  .\venv\Scripts\python -m uvicorn main:app --reload --port 8000"
    Write-Host "  cd frontend; npm run dev"
    exit 1
}

if (-not (Test-Path "$root\backend\venv\Scripts\python.exe")) {
    Write-Host "backend\venv is missing. Run the backend setup steps in README.md first." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$root\backend\.env")) {
    Write-Host "backend\.env is missing. Copy backend\.env.example to backend\.env and set JWT_SECRET (see README.md)." -ForegroundColor Red
    exit 1
}
if (-not (Test-Path "$root\frontend\node_modules")) {
    Write-Host "frontend\node_modules is missing. Run 'npm install' in frontend first." -ForegroundColor Red
    exit 1
}

Start-Process powershell -ArgumentList '-NoExit', '-Command', "Set-Location '$root\backend'; .\venv\Scripts\python -m uvicorn main:app --reload --port 8000"
Start-Process powershell -ArgumentList '-NoExit', '-Command', "Set-Location '$root\frontend'; npm run dev"

Write-Host "Backend:  http://localhost:8000/api/health"
Write-Host "Frontend: http://localhost:5173"
