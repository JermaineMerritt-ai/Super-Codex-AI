# ops/deploy.ps1
param(
  [Parameter(Mandatory=$true)][string]$ApiBase,
  [Parameter(Mandatory=$true)][string]$Token,
  [Parameter(Mandatory=$true)][string]$ArtifactDir
)

$ErrorActionPreference = "Stop"
$ApiBase = $ApiBase.TrimEnd('/')

function Hash-File([string]$Path) {
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $fs = [System.IO.File]::OpenRead($Path)
  try { -join ($sha.ComputeHash($fs) | ForEach-Object { $_.ToString("x2") }) }
  finally { $fs.Dispose(); $sha.Dispose() }
}

$manifestPath = Join-Path $ArtifactDir "manifest.json"
$uiDir = Join-Path $ArtifactDir "ui"
$svcDir = Join-Path $ArtifactDir "services"
$dbDir = Join-Path $ArtifactDir "db"

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$headersJson = @{ "Authorization" = $Token; "Content-Type" = "application/json" }

# Build steps (placeholder commands; wire to your builders)
Write-Host "==> Building UI" -ForegroundColor Cyan
# e.g., pushd $uiDir; npm ci; npm run build; popd

Write-Host "==> Packaging backend" -ForegroundColor Cyan
# e.g., zip services.zip services\*

Write-Host "==> Register artifact" -ForegroundColor Cyan
$payload = @{
  artifactId = $manifest.artifactId
  title      = $manifest.title
  version    = $manifest.version
  type       = $manifest.type
  files      = @{ ui = "ui/"; backend = "services/"; schema = "db/" }
  hash       = Hash-File $manifestPath
}
$response1 = Invoke-RestMethod -Method POST -Uri "$ApiBase$($manifest.routes.register)" -Headers $headersJson -Body ($payload | ConvertTo-Json)

Write-Host "==> Upload bundles" -ForegroundColor Cyan
$form = @{
  "artifactId" = $manifest.artifactId
  "version"    = $manifest.version
  "manifest"   = Get-Item $manifestPath
}
$response2 = Invoke-RestMethod -Method POST -Uri "$ApiBase/upload/artifact" -Headers @{ "Authorization" = $Token } -Form $form

Write-Host "==> Dispatch release" -ForegroundColor Cyan
$dispatchBody = @{
  artifactId = $manifest.artifactId
  version    = $manifest.version
  audience   = $manifest.audience
  route      = $manifest.routes.replay
} | ConvertTo-Json
$response3 = Invoke-RestMethod -Method POST -Uri "$ApiBase$($manifest.routes.dispatch)" -Headers $headersJson -Body $dispatchBody

Write-Host "==> Seal replay" -ForegroundColor Cyan
$response4 = Invoke-RestMethod -Method POST -Uri "$ApiBase/seal/artifact/$($manifest.artifactId)" -Headers $headersJson

Write-Host "==> Complete. Radiant URL:" -ForegroundColor Green
$response3