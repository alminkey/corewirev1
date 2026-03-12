# CoreWire Integration and Hardening Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current CoreWire MVP skeleton into a localhost-runnable, SEO-ready, operationally observable, security-hardened, vendor-neutral deployable system.

**Architecture:** Keep the existing modular monolith and wire it into a real runtime: FastAPI for public and internal APIs, Next.js for public pages and metadata, Python workers for pipeline execution, PostgreSQL and Redis for durable coordination, and object storage for artifacts. Integration comes first, then hardening layers are added on top of the working runtime.

**Tech Stack:** FastAPI, Next.js App Router, TypeScript, Python 3.12, SQLAlchemy, Alembic, PostgreSQL, Redis, MinIO or S3-compatible storage, Docker Compose, Docker multi-stage builds, Playwright, pytest, Vitest or Node smoke tests, OpenTelemetry-ready logging and metrics, Helm or Kubernetes manifests

---

## File Structure

Create or extend these areas:

- `apps/api/app.py` and `apps/api/core/*` for real FastAPI startup, routing, repositories, and health endpoints
- `apps/workers/main.py` and `apps/workers/core/*` for queue consumers, orchestration, retries, and metrics
- `apps/web/app/*` and `apps/web/lib/*` for live API fetches, metadata, sitemap, robots, and structured data
- `apps/*/config/*` or shared config files for strict environment validation
- `infra/docker/*` for runtime compose overlays and service Dockerfiles
- `infra/k8s/*` or `infra/helm/*` for vendor-neutral deployment manifests
- `scripts/*` for seed, migrate, bootstrap, and smoke-run helpers
- `tests/integration/*` and `tests/e2e/*` for full stack verification
- `docs/runbooks/*` and `docs/ops/*` for local and production operations

## Chunk 1: Runtime Bootstrap

### Task 1: Wire the real FastAPI application entrypoint

**Files:**
- Create: `apps/api/app.py`
- Create: `apps/api/core/config.py`
- Create: `apps/api/core/dependencies.py`
- Modify: `apps/api/pyproject.toml`
- Test: `apps/api/tests/test_app_boot.py`

- [ ] **Step 1: Write the failing FastAPI bootstrap test**

```python
def test_app_exposes_health_and_article_routes(client):
    assert client.get("/health").status_code == 200
    assert client.get("/api/articles").status_code in {200, 404}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_app_boot.py -v`
Expected: FAIL because `app.py` and startup wiring do not exist.

- [ ] **Step 3: Write minimal implementation**

```python
app = FastAPI(title="CoreWire API")
app.include_router(article_router, prefix="/api")
app.include_router(system_router)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_app_boot.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api
git commit -m "feat: wire fastapi runtime bootstrap"
```

### Task 2: Add real worker and scheduler entrypoints

**Files:**
- Create: `apps/workers/main.py`
- Create: `apps/workers/scheduler.py`
- Create: `apps/workers/core/config.py`
- Modify: `apps/workers/pyproject.toml`
- Test: `apps/workers/tests/test_worker_boot.py`

- [ ] **Step 1: Write the failing worker bootstrap test**

```python
def test_worker_loads_config_and_registers_pipeline_jobs():
    worker = build_worker()
    assert "ingest_source" in worker.job_names
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_worker_boot.py -v`
Expected: FAIL because runtime bootstrap does not exist.

- [ ] **Step 3: Write minimal implementation**

```python
def build_worker() -> WorkerRuntime:
    return WorkerRuntime(job_names=["ingest_source", "run_pipeline"])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_worker_boot.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers
git commit -m "feat: add worker and scheduler entrypoints"
```

## Chunk 2: Persistence and State Wiring

### Task 3: Replace in-memory paths with database repositories

**Files:**
- Create: `apps/api/core/db/session.py`
- Create: `apps/api/core/repositories/articles.py`
- Create: `apps/api/core/repositories/stories.py`
- Create: `apps/workers/core/repositories/pipeline.py`
- Test: `tests/integration/test_persistence_flow.py`

- [ ] **Step 1: Write the failing persistence integration test**

```python
def test_publish_flow_persists_story_and_article_records(db_session):
    result = persist_published_story(...)
    assert result.article_id is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_persistence_flow.py -v`
Expected: FAIL because persistence is still stubbed or incomplete.

- [ ] **Step 3: Write minimal implementation**

```python
class ArticleRepository:
    def create_published_article(self, payload):
        ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_persistence_flow.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core apps/workers/core tests/integration
git commit -m "feat: persist pipeline and article state"
```

### Task 4: Replace the Alembic stub with a real initial migration set

**Files:**
- Modify: `apps/api/alembic/versions/0001_initial_corewire_schema.py`
- Create: `apps/api/alembic/env.py`
- Create: `scripts/migrate-local.ps1`
- Test: `tests/integration/test_migrations.py`

- [ ] **Step 1: Write the failing migration test**

```python
def test_initial_migration_creates_required_tables(engine):
    assert "published_articles" in inspect(engine).get_table_names()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_migrations.py -v`
Expected: FAIL because the migration is incomplete.

- [ ] **Step 3: Write minimal implementation**

```python
def upgrade():
    op.create_table("published_articles", ...)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_migrations.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/alembic scripts tests/integration
git commit -m "feat: add real database migrations"
```

## Chunk 3: End-to-End Pipeline Integration

### Task 5: Wire queue-backed orchestration for ingest-to-publish

**Files:**
- Create: `apps/workers/core/jobs/pipeline.py`
- Modify: `apps/workers/core/jobs/scheduler.py`
- Modify: `apps/workers/core/audit/service.py`
- Test: `tests/integration/test_pipeline_orchestration.py`

- [ ] **Step 1: Write the failing orchestration test**

```python
def test_scheduler_enqueues_and_worker_advances_story_to_publish_state():
    assert run_full_pipeline(...) == "published"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_pipeline_orchestration.py -v`
Expected: FAIL because the pipeline is not fully wired.

- [ ] **Step 3: Write minimal implementation**

```python
def run_pipeline(source_item_id: str) -> str:
    return publish_validated_story(...)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_pipeline_orchestration.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core tests/integration
git commit -m "feat: wire queue-backed pipeline orchestration"
```

### Task 6: Add seed data and demo bootstrap flow

**Files:**
- Create: `scripts/seed-demo-data.py`
- Create: `scripts/bootstrap-local.ps1`
- Create: `tests/integration/test_seed_flow.py`
- Modify: `README.md`

- [ ] **Step 1: Write the failing seed-flow test**

```python
def test_seed_flow_creates_homepage_story_and_developing_story():
    assert seeded_counts["published_articles"] >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_seed_flow.py -v`
Expected: FAIL because there is no real seed workflow.

- [ ] **Step 3: Write minimal implementation**

```python
def seed_demo_data():
    create_source(...)
    create_story(...)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_seed_flow.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts README.md tests/integration
git commit -m "feat: add local seed and bootstrap flow"
```

## Chunk 4: Web and API Live Data Integration

### Task 7: Expose live homepage and article API payloads

**Files:**
- Create: `apps/api/core/articles/schemas.py`
- Modify: `apps/api/core/articles/service.py`
- Modify: `apps/api/core/articles/router.py`
- Test: `apps/api/tests/test_article_queries.py`

- [ ] **Step 1: Write the failing API query tests**

```python
def test_homepage_endpoint_returns_live_published_and_developing_sections(client):
    payload = client.get("/api/articles").json()
    assert "lead_story" in payload
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_article_queries.py -v`
Expected: FAIL because current API responses are incomplete or stubbed.

- [ ] **Step 3: Write minimal implementation**

```python
@router.get("/articles")
def list_articles(...) -> HomepagePayload:
    return article_service.build_homepage_payload()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_article_queries.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/articles apps/api/tests
git commit -m "feat: expose live article query payloads"
```

### Task 8: Replace placeholder frontend data with live server-side fetches

**Files:**
- Create: `apps/web/lib/api.ts`
- Create: `apps/web/lib/types.ts`
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Test: `apps/web/tests/live-data-pages.test.mjs`

- [ ] **Step 1: Write the failing live-data page test**

```js
test("homepage and article page call the API client", async () => {
  assert.ok(source.includes("getHomepage"));
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter corewire-web test`
Expected: FAIL because the pages still use static placeholders.

- [ ] **Step 3: Write minimal implementation**

```ts
const homepage = await getHomepage()
const article = await getArticleBySlug(params.slug)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter corewire-web test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: connect web pages to live api data"
```

## Chunk 5: SEO and Search Integrity

### Task 9: Implement metadata, canonical, sitemap, and robots

**Files:**
- Create: `apps/web/app/sitemap.ts`
- Create: `apps/web/app/robots.ts`
- Create: `apps/web/lib/seo.ts`
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Test: `apps/web/tests/seo-routes.test.mjs`

- [ ] **Step 1: Write the failing SEO route tests**

```js
test("sitemap and robots routes exist and article pages define canonical metadata", async () => {
  assert.ok(fs.existsSync("app/sitemap.ts"))
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter corewire-web test`
Expected: FAIL because SEO assets are missing.

- [ ] **Step 3: Write minimal implementation**

```ts
export default function robots() {
  return { rules: [{ userAgent: "*", allow: "/" }] }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter corewire-web test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: add technical seo routes and metadata"
```

### Task 10: Add structured data and low-confidence index controls

**Files:**
- Create: `apps/web/components/seo/article-json-ld.tsx`
- Modify: `apps/web/components/article/article-header.tsx`
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Test: `apps/web/tests/structured-data.test.mjs`

- [ ] **Step 1: Write the failing structured-data test**

```js
test("article pages emit json-ld and low-confidence stories are marked for controlled indexing", async () => {
  assert.match(source, /NewsArticle|Article/)
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter corewire-web test`
Expected: FAIL because structured data and index controls are missing.

- [ ] **Step 3: Write minimal implementation**

```tsx
<script type="application/ld+json">{JSON.stringify(articleSchema)}</script>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter corewire-web test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: add structured article seo and index controls"
```

## Chunk 6: Observability and Security Baseline

### Task 11: Add structured logging, metrics, and readiness probes

**Files:**
- Create: `apps/api/core/observability/logging.py`
- Create: `apps/api/core/observability/metrics.py`
- Create: `apps/workers/core/observability/logging.py`
- Modify: `apps/api/app.py`
- Modify: `apps/workers/main.py`
- Test: `tests/integration/test_observability.py`

- [ ] **Step 1: Write the failing observability test**

```python
def test_api_exposes_readiness_and_metrics_endpoints(client):
    assert client.get("/ready").status_code == 200
    assert client.get("/metrics").status_code == 200
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_observability.py -v`
Expected: FAIL because observability surfaces do not exist.

- [ ] **Step 3: Write minimal implementation**

```python
@router.get("/metrics")
def metrics():
    return PlainTextResponse(render_metrics())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_observability.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api apps/workers tests/integration
git commit -m "feat: add observability endpoints and structured logging"
```

### Task 12: Add internal route protection and crawler guardrails

**Files:**
- Create: `apps/api/core/security/internal_auth.py`
- Create: `apps/workers/core/acquire/guards.py`
- Modify: `apps/api/core/dependencies.py`
- Modify: `apps/workers/core/acquire/http_fetch.py`
- Test: `tests/integration/test_security_controls.py`

- [ ] **Step 1: Write the failing security control tests**

```python
def test_internal_publish_route_requires_internal_token(client):
    assert client.post("/internal/publish").status_code == 401
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_security_controls.py -v`
Expected: FAIL because internal auth and fetch guards are missing.

- [ ] **Step 3: Write minimal implementation**

```python
def validate_fetch_target(url: str) -> None:
    assert url.hostname in allowed_domains
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_security_controls.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/security apps/workers/core/acquire tests/integration
git commit -m "feat: add internal auth and crawler guardrails"
```

## Chunk 7: Deployment and Scaling

### Task 13: Add production-grade service Dockerfiles and compose overlays

**Files:**
- Create: `apps/api/Dockerfile`
- Create: `apps/workers/Dockerfile`
- Create: `apps/web/Dockerfile`
- Create: `infra/docker/docker-compose.prod.yml`
- Modify: `infra/docker/docker-compose.yml`
- Test: `tests/integration/test_container_configs.py`

- [ ] **Step 1: Write the failing container config test**

```python
def test_all_runtime_services_have_dockerfiles_and_prod_compose_entries():
    assert Path("apps/api/Dockerfile").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_container_configs.py -v`
Expected: FAIL because production container assets are missing.

- [ ] **Step 3: Write minimal implementation**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_container_configs.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps infra/docker tests/integration
git commit -m "feat: add production container assets"
```

### Task 14: Add vendor-neutral Kubernetes or Helm manifests

**Files:**
- Create: `infra/k8s/namespace.yaml`
- Create: `infra/k8s/api-deployment.yaml`
- Create: `infra/k8s/web-deployment.yaml`
- Create: `infra/k8s/workers-deployment.yaml`
- Create: `infra/k8s/ingress.yaml`
- Test: `tests/integration/test_k8s_manifests.py`

- [ ] **Step 1: Write the failing manifest test**

```python
def test_k8s_manifests_define_web_api_and_worker_deployments():
    assert Path("infra/k8s/api-deployment.yaml").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_k8s_manifests.py -v`
Expected: FAIL because manifests do not exist.

- [ ] **Step 3: Write minimal implementation**

```yaml
kind: Deployment
metadata:
  name: corewire-api
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_k8s_manifests.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add infra/k8s tests/integration
git commit -m "feat: add vendor-neutral deployment manifests"
```

## Chunk 8: Final Verification and Operations Docs

### Task 15: Add full-stack browser smoke and production-readiness runbooks

**Files:**
- Modify: `tests/e2e/publish-flow.spec.ts`
- Create: `tests/e2e/seo-smoke.spec.ts`
- Create: `docs/runbooks/local-start.md`
- Create: `docs/ops/production-readiness-checklist.md`
- Create: `docs/ops/seo-readiness-checklist.md`

- [ ] **Step 1: Write the failing browser and ops verification tests**

```ts
test("homepage, article page, sitemap, and robots are reachable on a live stack", async () => {})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm exec playwright test tests/e2e/publish-flow.spec.ts tests/e2e/seo-smoke.spec.ts`
Expected: FAIL because the live stack bootstrap is incomplete.

- [ ] **Step 3: Write minimal implementation**

```md
## Local startup
1. Start infra
2. Run migrations
3. Seed data
4. Start api, workers, and web
5. Run smoke checks
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm exec playwright test tests/e2e/publish-flow.spec.ts tests/e2e/seo-smoke.spec.ts`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/e2e docs/runbooks docs/ops
git commit -m "docs: add runtime and production readiness runbooks"
```

## Execution Notes

- Keep all existing editorial rules: every factual claim must remain traceable to cited sources.
- Do not reintroduce large placeholder data paths once live API integration is in place.
- Treat SEO as a product correctness concern, not as a content growth detour.
- Prefer server-rendered metadata and public-route stability over client-only enhancements.
- Preserve vendor neutrality in deployment artifacts and secret handling.
- Keep `developing_story` behavior explicit in APIs, UI, and search indexing policy.

## Verification Checklist

- `pnpm test:repo`
- `docker compose -f infra/docker/docker-compose.yml config`
- `docker compose -f infra/docker/docker-compose.prod.yml config`
- `pytest apps/api/tests -v`
- `pytest apps/workers/tests -v`
- `pytest tests/integration -v`
- `pnpm --filter corewire-web test`
- `pnpm exec playwright test tests/e2e/publish-flow.spec.ts tests/e2e/seo-smoke.spec.ts`
- `docker build -f apps/api/Dockerfile .`
- `docker build -f apps/workers/Dockerfile .`
- `docker build -f apps/web/Dockerfile .`

## Handoff

Plan complete and saved to `docs/superpowers/plans/2026-03-11-corewire-integration-hardening-implementation.md`. Ready to execute?
