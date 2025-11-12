# AXIOM CLI PowerShell Wrapper
# Activates virtual environment and runs the Python CLI

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Run the CLI with all arguments
& python cli\axiom_cli.py @Arguments

# Check for errors
if ($LASTEXITCODE -ne 0) {
    Write-Host "Command exited with code $LASTEXITCODE" -ForegroundColor Red
}