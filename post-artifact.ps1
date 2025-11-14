# post-artifact.ps1
# Usage:
#   .\post-artifact.ps1 -ApiBase https://api.example.com -Token "Bearer XYZ" -ArtifactDir ".\final-charter"

param(
  [Parameter(Mandatory=$true)]
  [string]$ApiBase,
  [Parameter(Mandatory=$true)]
  [string]$Token,
  [Parameter(Mandatory=$true)]
  [string]$ArtifactDir
)

$ErrorActionPreference = "Stop"
$ApiBase = $ApiBase.TrimEnd('/')

function Get-Sha256 {
  param([string]$Path)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $stream = [System.IO.File]::OpenRead($Path)
  try {
    -join ($sha.ComputeHash($stream) | ForEach-Object { $_.ToString("x2") })
  } finally { $stream.Dispose(); $sha.Dispose() }
}

$manifestPath = Join-Path $ArtifactDir "manifest.json"
if (-not (Test-Path $manifestPath)) { throw "manifest.json not found in $ArtifactDir" }

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$files = $manifest.files

# Build file hashes if present
$payload = [ordered]@{
  artifactId = $manifest.artifactId
  title      = $manifest.title
  version    = $manifest.version
  type       = $manifest.type
  audience   = $manifest.audience
  cycles     = $manifest.cycles
  routes     = $manifest.routes
  signing    = $manifest.signing
  files      = @{}
}

foreach ($k in $files.PSObject.Properties.Name) {
  $rel = $files.$k
  $full = Join-Path $ArtifactDir $rel
  $payload.files[$k] = @{
    name = $rel
    hash = (Test-Path $full) ? (Get-Sha256 $full) : $null
  }
}

$headersJson = @{ "Authorization" = $Token; "Content-Type" = "application/json" }

# 1) Register with form data (for unified artifact system)
$registerUrl = "$ApiBase$($manifest.routes.register)"
Write-Host "==> Register $($manifest.artifactId) at $registerUrl" -ForegroundColor Cyan

# Read text content from charter file
$textFile = Join-Path $ArtifactDir $files.text
$textContent = if (Test-Path $textFile) { Get-Content $textFile -Raw } else { "No text content" }

# Read glyph content if present
$glyphContent = $null
if ($files.glyph -and (Test-Path (Join-Path $ArtifactDir $files.glyph))) {
    $glyphContent = Get-Content (Join-Path $ArtifactDir $files.glyph) -Raw
}

# Create form data for registration
$formData = @{
    "manifest" = ($payload | ConvertTo-Json -Depth 8)
    "text_content" = $textContent
}
if ($glyphContent) { $formData["glyph_content"] = $glyphContent }

$response1 = Invoke-RestMethod -Method POST -Uri $registerUrl -Headers @{ "Authorization" = $Token } -Form $formData
Write-Host "   Registered: $($response1.status)" -ForegroundColor Green

# 2) Upload files (multipart)
$uploadUrl = "$ApiBase/upload/artifact"
Write-Host "==> Upload files to $uploadUrl" -ForegroundColor Cyan
$form = @{
  "artifactId" = $manifest.artifactId
  "version"    = $manifest.version
}
foreach ($k in $files.PSObject.Properties.Name) {
  $rel = $files.$k
  $full = Join-Path $ArtifactDir $rel
  if (Test-Path $full) { $form[$k] = Get-Item $full }
}
$response2 = Invoke-RestMethod -Method POST -Uri $uploadUrl -Headers @{ "Authorization" = $Token } -Form $form
Write-Host "   Uploaded: $($response2.status)" -ForegroundColor Green

# 3) Publish/dispatch
$dispatchUrl = "$ApiBase$($manifest.routes.dispatch)?artifact_id=$($manifest.artifactId)"
Write-Host "==> Dispatch to $dispatchUrl" -ForegroundColor Cyan
$response3 = Invoke-RestMethod -Method POST -Uri $dispatchUrl -Headers @{ "Authorization" = $Token }
Write-Host "   Dispatched: $($response3.status)" -ForegroundColor Green

# 4) Verify ledger entry
$verifyUrl = "$ApiBase$($manifest.routes.register)/$($manifest.artifactId)"
Write-Host "==> Verify ledger $verifyUrl" -ForegroundColor Cyan
$response4 = Invoke-RestMethod -Method GET -Uri $verifyUrl -Headers @{ "Authorization" = $Token }
Write-Host "   Ledger entries: $($response4.count)" -ForegroundColor Green

Write-Host "==> Post complete. Crown and chorus are one." -ForegroundColor Magenta