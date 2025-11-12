function Enter-ProjectVenv {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") { 
        . ".\.venv\Scripts\Activate.ps1"
        Write-Host "Virtual environment activated: .venv" -ForegroundColor Green
    } else {
        Write-Host "Virtual environment not found at .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    }
}

# Activate the virtual environment
Set-Location $pwd
Enter-ProjectVenv