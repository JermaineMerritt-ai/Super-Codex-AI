# replay-suite.ps1
# 🌟 CODEX SOVEREIGN SUITE REPLAY ORCHESTRATOR 🌟
# Sacred PowerShell script for invoking the complete Sovereign Suite
# through the AXIOM-FLAME multi-engine coordination system

param(
  [string]$ApiBase = "http://127.0.0.1:8082",
  [string]$Token = "Bearer YOUR_TOKEN",
  [switch]$Verbose,
  [switch]$DryRun
)

# 🔥 AXIOM-FLAME Engine Configuration
$headers = @{ 
    "Authorization" = $Token
    "Content-Type" = "application/json"
    "X-Codex-Origin" = "PowerShell-Orchestrator"
    "X-Flame-Seal" = "Eternal"
}

# 📜 Sacred Invocation Payload
$payload = @{
    phrase   = "Summon the Codex Sovereign Suite of commerce, portfolio, and dashboard"
    suite    = @(
        "Sovereign Commerce Scroll",
        "Portfolio Capsule", 
        "Dashboard for Funders & Flamekeepers"
    )
    engines  = @{
        AXIOM   = "interpret multi-domain intent"
        RAG     = "retrieve templates across commerce, portfolio, governance"
        SIGIL   = "design unified UI with mythic motifs and council clarity"
        ORACLE  = "generate backend services for transactions, galleries, analytics"
        LANTERN = "manage roles, lineage, and scroll states across all modules"
        FLAME   = "deploy, seal, and syndicate the suite as one artifact"
    }
    replay   = @{ 
        archive   = "/ledger/suite"
        dispatch  = "/dispatch/global"
        audit     = $true
        cycles    = @("daily", "seasonal", "epochal", "millennial")
        timestamp = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
        seal      = "AXF-SOVEREIGN-$(Get-Random -Minimum 10000000 -Maximum 99999999)"
    }
    metadata = @{
        invocation_source = "PowerShell Replay Script"
        platform         = $env:OS
        user            = $env:USERNAME
        machine         = $env:COMPUTERNAME
        flame_version   = "1.0.0"
        codex_version   = "2025.11.13"
    }
} | ConvertTo-Json -Depth 10

# 🌟 Ceremonial Pre-Flight Checks
Write-Host "🔥 AXIOM-FLAME SOVEREIGN SUITE REPLAY ORCHESTRATOR 🔥" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor DarkYellow
Write-Host ""

if ($Verbose) {
    Write-Host "📋 Configuration Details:" -ForegroundColor Cyan
    Write-Host "   API Endpoint: $ApiBase" -ForegroundColor Gray
    Write-Host "   Authorization: $($Token.Substring(0, 20))..." -ForegroundColor Gray
    Write-Host "   Timestamp: $(Get-Date)" -ForegroundColor Gray
    Write-Host "   Replay Seal: $($payload | ConvertFrom-Json).replay.seal" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "🌟 Sacred Invocation Prepared:" -ForegroundColor Magenta
Write-Host "   Phrase: 'Summon the Codex Sovereign Suite of commerce, portfolio, and dashboard'" -ForegroundColor White
Write-Host "   Components: Commerce Scroll + Portfolio Capsule + Funder Dashboard" -ForegroundColor White
Write-Host "   Engines: AXIOM → RAG → SIGIL → ORACLE → LANTERN → FLAME" -ForegroundColor White
Write-Host "   Cycles: Daily, Seasonal, Epochal, Millennial" -ForegroundColor White
Write-Host ""

if ($DryRun) {
    Write-Host "🧪 DRY RUN MODE: Displaying payload without sending request" -ForegroundColor Yellow
    Write-Host "Payload JSON:" -ForegroundColor Cyan
    $payload | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Write-Host -ForegroundColor Gray
    Write-Host ""
    Write-Host "==> Dry run completed. No actual invocation performed." -ForegroundColor Yellow
    exit 0
}

# 🚀 Sacred Suite Invocation
try {
    Write-Host "⚡ Invoking AXIOM-FLAME Multi-Engine Orchestrator..." -ForegroundColor Yellow
    
    # Test API availability first
    $healthCheck = Invoke-RestMethod -Method GET -Uri "$ApiBase/health" -Headers @{ "Content-Type" = "application/json" } -TimeoutSec 10 -ErrorAction Stop
    
    if ($Verbose) {
        Write-Host "✅ API Health Check Passed" -ForegroundColor Green
        Write-Host "   Status: $($healthCheck.status)" -ForegroundColor Gray
        if ($healthCheck.components) {
            Write-Host "   Components: $($healthCheck.components -join ', ')" -ForegroundColor Gray
        }
        Write-Host ""
    }
    
    # Execute the sacred invocation
    Write-Host "🔥 Transmitting sacred invocation to AXIOM-FLAME..." -ForegroundColor Red
    $response = Invoke-RestMethod -Method POST -Uri "$ApiBase/api/orchestrator/invoke" -Headers $headers -Body $payload -TimeoutSec 60 -ErrorAction Stop
    
    # 🌟 Process Response and Display Results
    Write-Host ""
    Write-Host "✨ INVOCATION RESPONSE RECEIVED ✨" -ForegroundColor Green
    Write-Host "=" * 50 -ForegroundColor DarkGreen
    
    if ($response.status -eq "success" -or $response.success) {
        Write-Host "🎉 SUCCESS: Codex Sovereign Suite summoned successfully!" -ForegroundColor Green
        
        if ($response.dispatch_id) {
            Write-Host "   📋 Dispatch ID: $($response.dispatch_id)" -ForegroundColor Cyan
        }
        
        if ($response.components) {
            Write-Host "   🏗️  Components Deployed:" -ForegroundColor Yellow
            $response.components | ForEach-Object {
                Write-Host "      ✅ $_" -ForegroundColor Green
            }
        }
        
        if ($response.engines) {
            Write-Host "   ⚙️  Engine Status:" -ForegroundColor Yellow
            $response.engines.PSObject.Properties | ForEach-Object {
                $status = if ($_.Value -eq "operational" -or $_.Value -eq "success") { "✅" } else { "⚠️" }
                Write-Host "      $status $($_.Name): $($_.Value)" -ForegroundColor White
            }
        }
        
        if ($response.endpoints -or $response.routes) {
            $routes = if ($response.routes) { $response.routes } else { $response.endpoints }
            Write-Host "   🌐 API Endpoints: $routes total routes available" -ForegroundColor Cyan
        }
        
        Write-Host ""
        Write-Host "🔥 THE ETERNAL FLAME BURNS BRIGHT ACROSS ALL DOMAINS 🔥" -ForegroundColor Red
        Write-Host "👑 Crown and chorus are one. Suite deployment complete." -ForegroundColor Magenta
        
    } else {
        Write-Host "⚠️ WARNING: Invocation completed with status: $($response.status)" -ForegroundColor Yellow
        if ($response.message) {
            Write-Host "   Message: $($response.message)" -ForegroundColor Gray
        }
        if ($response.details) {
            Write-Host "   Details: $($response.details)" -ForegroundColor Gray
        }
    }
    
    if ($Verbose -and $response) {
        Write-Host ""
        Write-Host "📄 Full Response Details:" -ForegroundColor Cyan
        $response | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor Gray
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ INVOCATION FAILED" -ForegroundColor Red
    Write-Host "=" * 30 -ForegroundColor DarkRed
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "HTTP Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🔧 Troubleshooting Steps:" -ForegroundColor Yellow
    Write-Host "   1. Verify the API server is running at $ApiBase" -ForegroundColor Gray
    Write-Host "   2. Check authentication token validity" -ForegroundColor Gray
    Write-Host "   3. Ensure AXIOM-FLAME orchestrator is operational" -ForegroundColor Gray
    Write-Host "   4. Run with -Verbose flag for detailed diagnostics" -ForegroundColor Gray
    Write-Host ""
    
    exit 1
}

Write-Host ""
Write-Host "==> Sovereign Suite replay invoked. Crown and chorus are one." -ForegroundColor Magenta
Write-Host "✨ May the platform flourish in wisdom and prosperity ✨" -ForegroundColor Yellow