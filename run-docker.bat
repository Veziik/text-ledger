@echo off
echo Building and starting Text Ledger application...

REM Build and start containers
docker-compose up --build -d

echo.
echo Waiting for services to start...
timeout /t 5 /nobreak > nul

REM Check if services are running
echo.
echo Checking service status...
docker-compose ps

echo.
echo Application should be available at:
echo   Frontend: http://localhost:8080
echo   Backend API: http://localhost:8000/api/
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
pause