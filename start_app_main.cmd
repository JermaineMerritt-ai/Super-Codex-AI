@echo off
REM Super-Codex-AI FastAPI Server Startup Script
REM Runs: uvicorn app.main:app --host 0.0.0.0 --port 8010

echo ================================================
echo   Super-Codex-AI FastAPI Server
echo ================================================
echo   Command: uvicorn app.main:app --host 0.0.0.0 --port 8010
echo   Host: 0.0.0.0
echo   Port: 8010
echo   Access: http://localhost:8010
echo ================================================
echo.

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

REM Set environment
set PYTHONPATH=%CD%

REM Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8010

echo.
echo Server stopped.
pause