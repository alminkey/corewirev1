# CoreWire Local Start

Run all commands in this document from:

```text
F:\2026\CoreWire\CooreWireV1
```

## Goal

Start the current integrated CoreWire stack locally, seed demo data, and run smoke verification.

## Prerequisites

- Docker Desktop or compatible Docker runtime
- Python 3.12+
- Node.js and `pnpm`

## Startup Order

1. Start infrastructure:

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

2. Run migrations:

```bash
powershell -ExecutionPolicy Bypass -File scripts/migrate-local.ps1
```

3. Seed demo data:

```bash
python scripts/seed-demo-data.py
```

Set local environment:

```bash
$env:COREWIRE_API_BASE_URL="http://localhost:8000/api"
$env:COREWIRE_SITE_URL="http://localhost:3000"
$env:COREWIRE_INTERNAL_TOKEN="corewire-internal-token"
```

4. Start API:

```bash
python -m uvicorn app:app --app-dir apps/api --host 0.0.0.0 --port 8000
```

5. Start workers:

```bash
python apps/workers/main.py
```

6. Start web:

```bash
pnpm --dir apps/web dev
```

## Smoke Verification

Run:

```bash
pytest tests/integration -q
pytest apps/api/tests -q
pytest apps/workers/tests -q
pnpm --filter corewire-web test
```

## Expected Local URLs

- Web: `http://localhost:3000`
- API: `http://localhost:8000`
- API metrics: `http://localhost:8000/metrics`
- API readiness: `http://localhost:8000/ready`
- MinIO console: `http://localhost:9001`

## Runtime Contract

- `COREWIRE_API_BASE_URL` should point the web app to the local API
- `COREWIRE_SITE_URL` should reflect the public local web origin
- `COREWIRE_INTERNAL_TOKEN` should match the token expected by internal operator routes
- API process command:
  - `python -m uvicorn app:app --app-dir apps/api --host 0.0.0.0 --port 8000`
- Worker process command:
  - `python apps/workers/main.py`
- Web process command:
  - `pnpm --dir apps/web dev`
