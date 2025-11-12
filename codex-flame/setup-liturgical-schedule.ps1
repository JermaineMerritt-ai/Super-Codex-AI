# setup-liturgical-schedule.ps1
# PowerShell script to set up Codex-Flame liturgical scheduling on Windows

param(
    [string]$CodexPath = "C:\Users\JMerr\OneDrive\Documents\.vscode\codex_project\backend\services\dominion\Super-Codex-AI\codex-flame",
    [string]$PythonPath = "python"
)

Write-Host "Setting up Codex-Flame Liturgical Scheduling..." -ForegroundColor Green

# Daily liturgy at 6:00 AM
$DailyAction = New-ScheduledTaskAction -Execute $PythonPath -Argument "eternal_flame_liturgy.py" -WorkingDirectory $CodexPath
$DailyTrigger = New-ScheduledTaskTrigger -Daily -At 6:00AM
$DailySettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName "Codex-Flame-Daily-Liturgy" -Action $DailyAction -Trigger $DailyTrigger -Settings $DailySettings -Force
    Write-Host "✅ Daily liturgy scheduled for 6:00 AM" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to schedule daily liturgy: $_" -ForegroundColor Red
}

# Weekly liturgy on Sunday at 8:00 AM
$WeeklyAction = New-ScheduledTaskAction -Execute $PythonPath -Argument "eternal_flame_liturgy.py" -WorkingDirectory $CodexPath
$WeeklyTrigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 8:00AM
$WeeklySettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName "Codex-Flame-Weekly-Liturgy" -Action $WeeklyAction -Trigger $WeeklyTrigger -Settings $WeeklySettings -Force
    Write-Host "✅ Weekly liturgy scheduled for Sundays at 8:00 AM" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to schedule weekly liturgy: $_" -ForegroundColor Red
}

# Test run
Write-Host "`nTesting liturgical cycle..." -ForegroundColor Yellow
Push-Location $CodexPath
try {
    & $PythonPath eternal_flame_liturgy.py
    Write-Host "✅ Liturgical cycle test successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Liturgical cycle test failed: $_" -ForegroundColor Red
} finally {
    Pop-Location
}

Write-Host "`nLiturgical scheduling setup complete!" -ForegroundColor Green
Write-Host "Tasks created:" -ForegroundColor Cyan
Write-Host "  - Codex-Flame-Daily-Liturgy (daily at 6:00 AM)" -ForegroundColor White
Write-Host "  - Codex-Flame-Weekly-Liturgy (Sundays at 8:00 AM)" -ForegroundColor White
Write-Host "`nTo view tasks: Get-ScheduledTask -TaskName 'Codex-Flame-*'" -ForegroundColor Gray