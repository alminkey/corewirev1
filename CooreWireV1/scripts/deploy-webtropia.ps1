param(
    [string]$ComposeProjectName = "corewire",
    [string]$Domain = "corewire.example.com"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$composeBase = Join-Path $root "infra\docker\docker-compose.yml"
$composeProd = Join-Path $root "infra\docker\docker-compose.prod.yml"

Write-Host "Deploying CoreWire to Webtropia for domain $Domain"

docker compose `
    -p $ComposeProjectName `
    -f $composeBase `
    -f $composeProd `
    pull

docker compose `
    -p $ComposeProjectName `
    -f $composeBase `
    -f $composeProd `
    up -d --build

Write-Host "Running smoke checks..."
Start-Sleep -Seconds 5
Invoke-WebRequest "http://localhost/health" | Out-Null
Invoke-WebRequest "http://localhost/" | Out-Null

Write-Host "Deployment complete."
