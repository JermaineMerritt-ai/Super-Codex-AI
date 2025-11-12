<#
.SYNOPSIS
    Interactive launcher menu for FastAPI server

.DESCRIPTION
    Provides a simple menu to choose between development and production launch modes
#>

Write-Host @"
╔════════════════════════════════════════════════════════╗
║                FastAPI Server Launcher                 ║
║                    Select Launch Mode                  ║
╚════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host ""
Write-Host "Available launch options:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [1] 🛠️  Development Server (Uvicorn)" -ForegroundColor Green
Write-Host "      • Single process" -ForegroundColor Gray
Write-Host "      • Easy debugging" -ForegroundColor Gray
Write-Host "      • Hot reload ready" -ForegroundColor Gray
Write-Host ""
Write-Host "  [2] 🏭 Production Server (Gunicorn)" -ForegroundColor Blue
Write-Host "      • Multiple workers (4)" -ForegroundColor Gray
Write-Host "      • High availability" -ForegroundColor Gray
Write-Host "      • Load balancing" -ForegroundColor Gray
Write-Host ""
Write-Host "  [3] ⚙️  Custom Configuration" -ForegroundColor Magenta
Write-Host "      • Interactive setup" -ForegroundColor Gray
Write-Host ""
Write-Host "  [Q] 🚪 Exit" -ForegroundColor Red
Write-Host ""

do {
    $choice = Read-Host "Enter your choice [1-3, Q]"
    
    switch ($choice.ToUpper()) {
        "1" {
            Write-Host "🚀 Launching development server..." -ForegroundColor Green
            & ".\launch_server.ps1"
            return
        }
        "2" {
            Write-Host "🏭 Launching production server..." -ForegroundColor Blue
            & ".\launch_server.ps1" -Production
            return
        }
        "3" {
            Write-Host ""
            Write-Host "⚙️ Custom Configuration" -ForegroundColor Magenta
            Write-Host "========================" -ForegroundColor Magenta
            
            $mode = Read-Host "Production mode? [y/N]"
            $isProduction = $mode -match '^[Yy]'
            
            $host = Read-Host "Host address [0.0.0.0]"
            if ([string]::IsNullOrWhiteSpace($host)) { $host = "0.0.0.0" }
            
            $port = Read-Host "Port [8010]"
            if ([string]::IsNullOrWhiteSpace($port)) { $port = 8010 } else { $port = [int]$port }
            
            $logLevel = Read-Host "Log level [info]"
            if ([string]::IsNullOrWhiteSpace($logLevel)) { $logLevel = "info" }
            
            if ($isProduction) {
                $workers = Read-Host "Number of workers [4]"
                if ([string]::IsNullOrWhiteSpace($workers)) { $workers = 4 } else { $workers = [int]$workers }
                
                Write-Host "🏭 Launching custom production server..." -ForegroundColor Blue
                & ".\launch_server.ps1" -Production -Host $host -Port $port -Workers $workers -LogLevel $logLevel
            } else {
                Write-Host "🚀 Launching custom development server..." -ForegroundColor Green
                & ".\launch_server.ps1" -Host $host -Port $port -LogLevel $logLevel
            }
            return
        }
        "Q" {
            Write-Host "👋 Goodbye!" -ForegroundColor Yellow
            return
        }
        default {
            Write-Host "❌ Invalid choice. Please select 1, 2, 3, or Q." -ForegroundColor Red
        }
    }
} while ($true)