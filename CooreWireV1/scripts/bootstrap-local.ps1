$ErrorActionPreference = "Stop"

Write-Host "Using PostgreSQL by default for local migrations."
Write-Host "Override with:"
Write-Host 'powershell -ExecutionPolicy Bypass -File "scripts/migrate-local.ps1" -DatabaseUrl "sqlite:///corewire-local.db"'

Write-Host "Running local migration..."
& powershell -ExecutionPolicy Bypass -File "scripts/migrate-local.ps1"

Write-Host "Seeding demo data..."
python "scripts/seed-demo-data.py"

Write-Host "Start API:"
Write-Host "python -m uvicorn app:app --app-dir apps/api --host 0.0.0.0 --port 8000"

Write-Host "Start workers:"
Write-Host "python apps/workers/main.py"

Write-Host "Start web:"
Write-Host "pnpm --dir apps/web dev"
