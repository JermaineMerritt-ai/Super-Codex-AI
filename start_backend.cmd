@echo off
REM Super-Codex-AI Backend Startup Script
echo Starting Super-Codex-AI Integrated Backend...

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

REM Set environment variables
set PYTHONPATH=%CD%
set HOST=127.0.0.1
set PORT=8012

REM Start the backend
echo.
echo ===============================================
echo   Super-Codex-AI Backend Starting
echo   Host: %HOST%:%PORT%
echo   Frontend: http://localhost:3000
echo ===============================================
echo.

python -m uvicorn integrated_backend:app --host %HOST% --port %PORT% --reload

pause