# PowerShell script to check if services are running

Write-Host "Checking Text Ledger Application services..." -ForegroundColor Green

# Check if backend is running
Write-Host "`nChecking backend (port 8000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health/" -Method GET -ErrorAction Stop
    Write-Host "✓ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend is NOT running" -ForegroundColor Red
    Write-Host "  Start it with: cd backend && python manage.py runserver" -ForegroundColor Gray
}

# Check if frontend is running
Write-Host "`nChecking frontend (port 8080)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -Method GET -ErrorAction Stop
    Write-Host "✓ Frontend is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Frontend is NOT running" -ForegroundColor Red
    Write-Host "  Start it with: cd frontend && npm run serve" -ForegroundColor Gray
}

# Check Docker status
Write-Host "`nChecking Docker containers..." -ForegroundColor Yellow
$dockerRunning = docker ps 2>$null
if ($LASTEXITCODE -eq 0) {
    $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null
    if ($containers -match "text-ledger") {
        Write-Host "Docker containers found:" -ForegroundColor Green
        Write-Host $containers
    } else {
        Write-Host "No Text Ledger Docker containers running" -ForegroundColor Gray
    }
} else {
    Write-Host "Docker is not available or not running" -ForegroundColor Gray
}

Write-Host "`n" -NoNewline
Read-Host "Press Enter to exit"