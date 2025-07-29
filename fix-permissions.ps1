# PowerShell script to fix permissions and run the application

Write-Host "Fixing permissions and starting Text Ledger Application..." -ForegroundColor Green

# Navigate to the project directory
Set-Location -Path $PSScriptRoot

# Stop any running containers
Write-Host "`nStopping any existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null

# Use the simple docker-compose file that doesn't rely on shell scripts
Write-Host "`nStarting application with inline commands..." -ForegroundColor Yellow
docker-compose -f docker-compose.simple.yml up --build

# Alternative: If the above doesn't work, try running containers separately
# Write-Host "`nStarting backend..." -ForegroundColor Yellow
# docker run -d -p 8000:8000 --name ledger-backend -w /app python:3.11-slim bash -c "pip install django djangorestframework django-cors-headers && cd /app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"