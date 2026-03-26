param(
    [Parameter(Mandatory = $true)]
    [string]$BackupFile,
    [string]$ComposeProjectName = "corewire"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $BackupFile)) {
    throw "Backup file not found: $BackupFile"
}

Get-Content $BackupFile | docker compose `
    -p $ComposeProjectName `
    -f infra/docker/docker-compose.yml `
    -f infra/docker/docker-compose.prod.yml `
    exec -T postgres psql -U corewire -d corewire

Write-Host "Restore completed from $BackupFile"
