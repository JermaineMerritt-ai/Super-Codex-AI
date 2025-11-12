@echo off
REM FastAPI Server Launcher - Command Line Interface
REM Usage: 
REM   launch_dev.cmd     - Development server (uvicorn)
REM   launch_prod.cmd    - Production server (gunicorn)

echo 🚀 FastAPI Development Server Launcher
echo ======================================

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo ✅ Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️ Virtual environment not found, using system Python
)

REM Set environment variables
set PYTHONPATH=%CD%
set PYTHONUNBUFFERED=1

echo 🎯 Starting development server...
echo 🌐 Server will be available at: http://0.0.0.0:8010
echo 📚 API docs available at: http://0.0.0.0:8010/docs
echo.

REM Stable development launch
python -m uvicorn app.main:app --host 0.0.0.0 --port 8010 --log-level info

echo.
echo 🏁 Server stopped.
pause