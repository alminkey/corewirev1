param(
    [string]$ComposeProjectName = "corewire",
    [string]$Domain = "corewire.example.com"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$composeProd = Join-Path $root "infra\docker\docker-compose.prod.yml"

Write-Host "Deploying CoreWire to Webtropia for domain $Domain"

docker compose `
    -p $ComposeProjectName `
    -f $composeProd `
    pull

docker compose `
    -p $ComposeProjectName `
    -f $composeProd `
    up -d --build

docker compose `
    -p $ComposeProjectName `
    -f $composeProd `
    exec -T api sh -lc 'cd /app && PYTHONPATH=/app/apps/api COREWIRE_DATABASE_URL="${COREWIRE_DATABASE_URL}" DATABASE_URL="${COREWIRE_DATABASE_URL}" alembic -c apps/api/alembic.ini upgrade head'

Write-Host "Running smoke checks..."
Start-Sleep -Seconds 5
Invoke-WebRequest "http://localhost/health" | Out-Null
Invoke-WebRequest "http://localhost/" | Out-Null

Write-Host "Deployment complete."
