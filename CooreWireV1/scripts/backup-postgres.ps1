param(
    [string]$ComposeProjectName = "corewire",
    [string]$OutputDirectory = ".\\backups"
)

$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Resolve-Path "." -ErrorAction SilentlyContinue
if (-not (Test-Path $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}

$outputPath = Join-Path $OutputDirectory "postgres-$timestamp.sql"

docker compose `
    -p $ComposeProjectName `
    -f infra/docker/docker-compose.yml `
    -f infra/docker/docker-compose.prod.yml `
    exec -T postgres pg_dump -U corewire -d corewire > $outputPath

Write-Host "Backup written to $outputPath"
