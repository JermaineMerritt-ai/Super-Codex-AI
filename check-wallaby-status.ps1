#!/usr/bin/env pwsh

Write-Host "🔥 CODEX Wallaby.js Setup Status" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if Wallaby.js is installed
$orchestratorInstalled = Test-Path "orchestrator\node_modules\wallaby"
$frontendInstalled = Test-Path "codex-flame\packages\frontend\node_modules\wallaby"

Write-Host "📦 Installation Status:" -ForegroundColor Yellow
Write-Host "  Orchestrator (Jest + TypeScript): " -NoNewline
if ($orchestratorInstalled) {
    Write-Host "✅ INSTALLED" -ForegroundColor Green
} else {
    Write-Host "❌ NOT INSTALLED" -ForegroundColor Red
}

Write-Host "  Frontend (Vitest + Vue 3): " -NoNewline
if ($frontendInstalled) {
    Write-Host "✅ INSTALLED" -ForegroundColor Green
} else {
    Write-Host "❌ NOT INSTALLED" -ForegroundColor Red
}

Write-Host ""
Write-Host "🛠️  Configuration Files:" -ForegroundColor Yellow
$configs = @(
    @{ Path = "orchestrator\wallaby.js"; Name = "Orchestrator Wallaby Config" },
    @{ Path = "orchestrator\jest.config.js"; Name = "Orchestrator Jest Config" },
    @{ Path = "codex-flame\packages\frontend\wallaby.js"; Name = "Frontend Wallaby Config" },
    @{ Path = ".vscode\extensions.json"; Name = "VS Code Extensions" },
    @{ Path = ".vscode\settings.json"; Name = "VS Code Settings" }
)

foreach ($config in $configs) {
    Write-Host "  $($config.Name): " -NoNewline
    if (Test-Path $config.Path) {
        Write-Host "✅ EXISTS" -ForegroundColor Green
    } else {
        Write-Host "❌ MISSING" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Install VS Code extension: WallabyJs.wallaby-vscode"
Write-Host "  2. Open Command Palette (Ctrl+Shift+P)"
Write-Host "  3. Type: 'Wallaby.js: Start'"
Write-Host "  4. Select your project (orchestrator or frontend)"
Write-Host "  5. Watch tests run in real-time! ⚡"

Write-Host ""
Write-Host "📚 Documentation: " -NoNewline -ForegroundColor Yellow
Write-Host "WALLABY_SETUP_README.md" -ForegroundColor Cyan

Write-Host ""
Write-Host "🎉 Happy Testing!" -ForegroundColor Green