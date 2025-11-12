@echo off
echo Starting Axiom-Flame System...
cd /d "%~dp0"

REM Start Flask API
echo Starting Flask API...
python axiom-flame\packages\api\start_api.py start --daemon 8089

REM Wait for API to start
timeout /t 3 /nobreak > nul

REM Test API health
echo Testing API health...
curl -s http://localhost:8089/health

echo.
echo Axiom-Flame System started successfully!
echo API Access: http://localhost:8089
echo Health Check: http://localhost:8089/health
echo.
echo Available Commands:
echo   python system_health_check.py     - System diagnostics
echo   python system_validation.py       - Full validation  
echo   python axiom-flame\axiom_flame.py health - CLI health
echo.
pause