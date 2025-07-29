@echo off
echo Starting Text Ledger Application...
echo.

REM Use the simple docker-compose that doesn't require shell scripts
echo Using simplified Docker configuration...
docker-compose -f docker-compose.simple.yml up --build

pause