# CoreWire

CoreWire is an autonomous AI news portal MVP that ingests sources, extracts claims, corroborates evidence, drafts cited articles, and applies confidence-based publish gating.

Project working root:

```bash
F:\2026\CoreWire\CooreWireV1
```

## Stack

- `apps/api`: FastAPI-oriented Python API and data models
- `apps/workers`: Python ingest, analysis, drafting, and scheduling pipeline
- `apps/web`: Next.js-oriented public news frontend
- `PostgreSQL`, `Redis`, and `MinIO`: local infrastructure in `infra/docker/docker-compose.yml`

## Local Development

All commands below assume your shell is opened in `F:\2026\CoreWire\CooreWireV1`.

1. Start infrastructure:

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

2. Run migrations and seed demo data:

```bash
powershell -ExecutionPolicy Bypass -File scripts/migrate-local.ps1
python scripts/seed-demo-data.py
```

By default, `scripts/migrate-local.ps1` now targets local PostgreSQL (`postgresql://corewire:corewire@localhost:5432/corewire`). If you explicitly need the SQLite fallback for ad-hoc debugging, pass `-DatabaseUrl "sqlite:///corewire-local.db"`.

3. Run focused verification:

```bash
pnpm test:repo
pnpm --filter corewire-web test
pytest apps/api/tests -v
pytest apps/workers/tests -v
pytest tests/integration -v
```

4. Use the local bootstrap helper when you want the current integrated demo flow:

```bash
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-local.ps1
```

5. Full local runtime contract is documented in:

```bash
docs/runbooks/local-start.md
```

6. For the first real article batches through the composite operator flow, see:

```bash
docs/runbooks/content-batch.md
```

7. For the writer-first flagship analysis evaluation loop, see:

```bash
docs/runbooks/corewire-analysis-evaluation.md
```

8. For the latest full project checkpoint and handoff status, see:

```bash
docs/runbooks/2026-04-11-project-checkpoint.md
```

## Current MVP Capabilities

- RSS ingest with canonical URL deduplication
- HTTP-to-browser extraction fallback
- Claim extraction with supporting quotes
- Story clustering and evidence matching
- Analysis and confidence scoring
- Writer-first `CoreWire Analysis` path for flagship analysis content
- Citation validation before publish
- Publish gate for `published` vs `developing_story`
- Premium command-center homepage and article page skeleton
- Scheduler, retry helper, and audit event helper
- Early integration bootstrap for pipeline orchestration and demo seeding

## Known Limitations

- Frontend dependency installation for full Next.js runtime has been unstable due registry network errors in this environment.
- The current web smoke tests validate file-backed UI structure rather than running a live browser session.
- Alembic migration is still a stub and does not yet materialize the full schema.
