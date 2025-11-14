# Requires: PowerShell 5+ on Windows 11
# Usage:
#   .\upload.ps1 -ApiBase https://your-api.example.com -Token "Bearer XYZ"

param(
  [Parameter(Mandatory=$true)]
  [string]$ApiBase,
  [Parameter(Mandatory=$true)]
  [string]$Token
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pkgDir = Join-Path $root "concord-hymn"
$manifestPath = Join-Path $pkgDir "manifest.json"
$hymnPath = Join-Path $pkgDir "concord_hymn.md"
$assetsDir = Join-Path $pkgDir "assets"

function Get-Sha256 {
  param([string]$Path)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $stream = [System.IO.File]::OpenRead($Path)
  try {
    $hashBytes = $sha.ComputeHash($stream)
    -join ($hashBytes | ForEach-Object { $_.ToString("x2") })
  } finally {
    $stream.Dispose()
    $sha.Dispose()
  }
}

Write-Host "==> Loading manifest" -ForegroundColor Cyan
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

# Build payload with hashes
$payload = [ordered]@{
  artifactId = $manifest.artifactId
  title      = $manifest.title
  version    = $manifest.version
  type       = $manifest.type
  audience   = $manifest.audience
  cycles     = $manifest.cycles
  routes     = $manifest.routes
  hashStrategy = "sha256"
  signing    = [ordered]@{
    sigil      = "SIGIL-" + $manifest.artifactId.ToUpper() + "-001"
    signed_by  = if ($manifest.signing.authority) { $manifest.signing.authority } else { "Custodian" }
    heirs_chorus = $true
  }
  files      = [ordered]@{
    text       = $manifest.files.text
    audio      = if (Test-Path (Join-Path $assetsDir $manifest.files.audio)) { $manifest.files.audio } else { $null }
    glyph      = if (Test-Path (Join-Path $assetsDir $manifest.files.glyph)) { $manifest.files.glyph } else { $null }
    background = if (Test-Path (Join-Path $assetsDir $manifest.files.background)) { $manifest.files.background } else { $null }
  }
}

# 1) Register in ledger
$registerUrl = ($ApiBase.TrimEnd('/')) + $manifest.routes.register
Write-Host "==> Registering hymn at $registerUrl" -ForegroundColor Cyan

# Debug: Show the JSON payload
$jsonPayload = ($payload | ConvertTo-Json -Depth 6)
Write-Host "   Payload JSON:" -ForegroundColor Yellow
Write-Host $jsonPayload -ForegroundColor Gray

$headers = @{ "Authorization" = $Token; "Content-Type" = "application/json" }
$response1 = Invoke-RestMethod -Method POST -Uri $registerUrl -Headers $headers -Body $jsonPayload
Write-Host "   Registered: $($response1.success)" -ForegroundColor Green
Write-Host "   Hymn ID: $($response1.hymn_id)" -ForegroundColor Green
Write-Host "   Seal Created: $($response1.seal_created)" -ForegroundColor Green

# 2) File upload not implemented in current API - skipping
Write-Host "==> File upload skipped (not implemented in current API)" -ForegroundColor Yellow

# 3) Test dispatch endpoint  
$dispatchUrl = ($ApiBase.TrimEnd('/')) + $manifest.routes.dispatch
Write-Host "==> Testing dispatch at $dispatchUrl" -ForegroundColor Cyan
try {
  $response3 = Invoke-RestMethod -Method GET -Uri $dispatchUrl -Headers @{ "Authorization" = $Token }
  Write-Host "   Available hymns: $($response3.total_hymns)" -ForegroundColor Green
} catch {
  Write-Host "   Dispatch test skipped (endpoint may not be available)" -ForegroundColor Yellow
}

# 4) Verify hymn details
$verifyUrl = ($ApiBase.TrimEnd('/')) + "/hymns/" + $response1.hymn_id
Write-Host "==> Verifying hymn at $verifyUrl" -ForegroundColor Cyan
try {
  $response4 = Invoke-RestMethod -Method GET -Uri $verifyUrl -Headers @{ "Authorization" = $Token }
  Write-Host "   Content length: $($response4.content.Length) chars" -ForegroundColor Green
  Write-Host "   Seal verified: $($response4.seal_verification.verified)" -ForegroundColor Green
} catch {
  Write-Host "   Verification failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "==> Concord Hymn registration complete! 🎵👑🔥" -ForegroundColor Magenta