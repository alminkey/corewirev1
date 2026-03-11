# CoreWire

CoreWire is an autonomous AI news portal MVP that ingests sources, extracts claims, corroborates evidence, drafts cited articles, and applies confidence-based publish gating.

## Stack

- `apps/api`: FastAPI-oriented Python API and data models
- `apps/workers`: Python ingest, analysis, drafting, and scheduling pipeline
- `apps/web`: Next.js-oriented public news frontend
- `PostgreSQL`, `Redis`, and `MinIO`: local infrastructure in `infra/docker/docker-compose.yml`

## Local Development

1. Start infrastructure:

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

2. Run focused verification:

```bash
pnpm test:repo
pnpm --filter corewire-web test
pytest apps/api/tests -v
pytest apps/workers/tests -v
```

3. Explore the worktree branch used for implementation:

```bash
git worktree list
```

## Current MVP Capabilities

- RSS ingest with canonical URL deduplication
- HTTP-to-browser extraction fallback
- Claim extraction with supporting quotes
- Story clustering and evidence matching
- Analysis and confidence scoring
- Citation validation before publish
- Publish gate for `published` vs `developing_story`
- Premium command-center homepage and article page skeleton
- Scheduler, retry helper, and audit event helper

## Known Limitations

- Frontend dependency installation for full Next.js runtime has been unstable due registry network errors in this environment.
- The current web smoke tests validate file-backed UI structure rather than running a live browser session.
- Alembic migration is still a stub and does not yet materialize the full schema.
