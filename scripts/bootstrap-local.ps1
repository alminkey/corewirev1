$ErrorActionPreference = "Stop"

Write-Host "Running local migration..."
& powershell -ExecutionPolicy Bypass -File "scripts/migrate-local.ps1"

Write-Host "Seeding demo data..."
python "scripts/seed-demo-data.py"
