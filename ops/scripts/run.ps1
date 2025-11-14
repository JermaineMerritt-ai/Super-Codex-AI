# ops/scripts/run.ps1
# Super Codex AI - Six Engines Constellation Server Runner
# Sets environment variables and starts the FastAPI server

param(
    [string]$ServerHost = "0.0.0.0",
    [int]$Port = 8080,
    [int]$Workers = 2,
    [string]$Module = "server:app",
    [switch]$Help
)

if ($Help) {
    Write-Host "🔥 Six Engines Constellation Server Runner" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Usage: .\ops\scripts\run.ps1 [OPTIONS]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -ServerHost <string> Host to bind to (default: 0.0.0.0)" -ForegroundColor Gray
    Write-Host "  -Port <int>         Port to bind to (default: 8080)" -ForegroundColor Gray
    Write-Host "  -Workers <int>      Number of worker processes (default: 2)" -ForegroundColor Gray
    Write-Host "  -Module <string>    Python module to run (default: server:app)" -ForegroundColor Gray
    Write-Host "  -Help               Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Environment Variables Set:" -ForegroundColor White
    Write-Host "  VECTOR_DIR          ./data/vectors" -ForegroundColor Gray
    Write-Host "  VECTOR_NAME         index.faiss" -ForegroundColor Gray
    Write-Host "  CORPUS_DIR          ./data/corpus" -ForegroundColor Gray
    Write-Host "  AUDIT_LOG_PATH      ./data/audit.log" -ForegroundColor Gray
    Write-Host "  REPLAY_DIR          ./data/replay" -ForegroundColor Gray
    Write-Host "  IDENTITIES_DIR      ./data/identities" -ForegroundColor Gray
    Write-Host "  SEALS_DIR           ./data/seals" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\ops\scripts\run.ps1" -ForegroundColor Cyan
    Write-Host "  .\ops\scripts\run.ps1 -Port 8000 -Workers 4" -ForegroundColor Cyan
    Write-Host "  .\ops\scripts\run.ps1 -Module engine.app:app -ServerHost 127.0.0.1" -ForegroundColor Cyan
    return
}

Write-Host "🔥 Six Engines Constellation Server" -ForegroundColor Yellow
Write-Host "🚀 Initializing Sovereign Intelligence Runtime" -ForegroundColor Cyan
Write-Host ""

# Set environment variables for the Six Engines constellation
Write-Host "⚙️  Configuring Environment Variables..." -ForegroundColor Magenta
$env:VECTOR_DIR = "./data/vectors"
$env:VECTOR_NAME = "index.faiss"
$env:CORPUS_DIR = "./data/corpus"
$env:AUDIT_LOG_PATH = "./data/audit.log"
$env:REPLAY_DIR = "./data/replay"
$env:IDENTITIES_DIR = "./data/identities"
$env:SEALS_DIR = "./data/seals"

# Display configuration
Write-Host "📁 Data Directories:" -ForegroundColor White
Write-Host "   Vectors:     $env:VECTOR_DIR" -ForegroundColor Gray
Write-Host "   Corpus:      $env:CORPUS_DIR" -ForegroundColor Gray
Write-Host "   Replay:      $env:REPLAY_DIR" -ForegroundColor Gray
Write-Host "   Identities:  $env:IDENTITIES_DIR" -ForegroundColor Gray
Write-Host "   Seals:       $env:SEALS_DIR" -ForegroundColor Gray
Write-Host "   Audit Log:   $env:AUDIT_LOG_PATH" -ForegroundColor Gray
Write-Host ""

Write-Host "🌐 Server Configuration:" -ForegroundColor White
Write-Host "   Module:      $Module" -ForegroundColor Gray
Write-Host "   Host:        $ServerHost" -ForegroundColor Gray
Write-Host "   Port:        $Port" -ForegroundColor Gray
Write-Host "   Workers:     $Workers" -ForegroundColor Gray
Write-Host ""

Write-Host "🔥 Starting Six Engines Constellation Server..." -ForegroundColor Yellow
Write-Host "   Access at: http://${ServerHost}:${Port}" -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start the uvicorn server
uvicorn $Module --host $ServerHost --port $Port --workers $Workers