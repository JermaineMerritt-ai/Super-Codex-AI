@echo off
REM FastAPI Production Server Launcher
REM Uses gunicorn with uvicorn workers for production deployment

echo 🏭 FastAPI Production Server Launcher
echo ====================================

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

REM Check if gunicorn is installed
python -m pip show gunicorn >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Gunicorn not installed. Installing...
    python -m pip install gunicorn
)

echo 🎯 Starting production server with gunicorn...
echo 👥 Workers: 4 (gunicorn processes)
echo 🌐 Server will be available at: http://0.0.0.0:8010
echo 📚 API docs available at: http://0.0.0.0:8010/docs
echo.

REM Production-grade launch
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010 --workers 4 --log-level info

echo.
echo 🏁 Production server stopped.
pause