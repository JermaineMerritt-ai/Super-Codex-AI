@echo off
REM AXIOM CLI Batch Wrapper
REM Activates virtual environment and runs the Python CLI

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run the CLI with all arguments
python cli\axiom_cli.py %*

REM Pause if there was an error (for debugging)
if %errorlevel% neq 0 pause