# CoreWire MVP Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an English-only CoreWire MVP that autonomously ingests sources, extracts and corroborates claims, generates cited articles, and publishes a premium public news experience with confidence gating.

**Architecture:** Build a greenfield modular monolith with a Next.js frontend, FastAPI API, Python workers, PostgreSQL, Redis, and object-storage-backed artifacts. Keep article traceability explicit from source document to claim to evidence to rendered article block, and enforce confidence-based publishing rules in code and UI.

**Tech Stack:** Next.js App Router, TypeScript, Tailwind CSS, FastAPI, Python 3.12, SQLAlchemy, Alembic, PostgreSQL, Redis, RQ or Arq workers, Playwright, Trafilatura/Readability-style extraction, OpenAI API, pytest, Vitest, Playwright E2E, Docker Compose

---

## File Structure

Create these top-level areas:

- `apps/web` for Next.js UI
- `apps/api` for FastAPI read/write API
- `apps/workers` for job consumers and pipeline logic
- `packages/config` for shared typed configuration
- `packages/contracts` for shared schemas and enums
- `infra/docker` for local services
- `docs/adr` for architectural decisions discovered during implementation
- `tests/e2e` for end-to-end smoke coverage

## Chunk 1: Repository Foundation

### Task 1: Bootstrap the monorepo structure

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `apps/web/package.json`
- Create: `apps/api/pyproject.toml`
- Create: `apps/workers/pyproject.toml`
- Create: `packages/config/package.json`
- Create: `packages/contracts/package.json`
- Create: `infra/docker/docker-compose.yml`
- Create: `.env.example`

- [ ] **Step 1: Write the failing repo smoke checks**

Create a minimal structure test script in `package.json` that expects `apps/web`, `apps/api`, and `apps/workers` to exist.

```json
{
  "scripts": {
    "test:repo": "node scripts/test-repo-structure.mjs"
  }
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm test:repo`
Expected: FAIL because structure files do not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create the workspace files and service manifests with placeholder scripts:

```json
{
  "name": "corewire-web",
  "scripts": {
    "dev": "next dev",
    "build": "next build"
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm test:repo`
Expected: PASS with all required directories present.

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "chore: bootstrap corewire monorepo"
```

### Task 2: Add local infrastructure for DB, Redis, and object storage

**Files:**
- Create: `infra/docker/docker-compose.yml`
- Create: `infra/docker/postgres/init.sql`
- Create: `infra/docker/minio/.gitkeep`
- Test: `infra/docker/docker-compose.yml`

- [ ] **Step 1: Write the failing infrastructure check**

Document a compose smoke command that should fail before the file exists.

```yaml
services: {}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `docker compose -f infra/docker/docker-compose.yml config`
Expected: FAIL because the compose file is not defined yet.

- [ ] **Step 3: Write minimal implementation**

Add services for `postgres`, `redis`, and `minio`.

```yaml
services:
  postgres:
    image: postgres:16
  redis:
    image: redis:7
  minio:
    image: minio/minio
```

- [ ] **Step 4: Run test to verify it passes**

Run: `docker compose -f infra/docker/docker-compose.yml config`
Expected: PASS and resolved service definitions.

- [ ] **Step 5: Commit**

```bash
git add infra/docker
git commit -m "chore: add local infrastructure stack"
```

## Chunk 2: Shared Contracts and Database

### Task 3: Define shared enums and payload contracts

**Files:**
- Create: `packages/contracts/src/pipeline.ts`
- Create: `packages/contracts/src/article.ts`
- Create: `packages/contracts/src/index.ts`
- Test: `packages/contracts/src/article.ts`

- [ ] **Step 1: Write the failing schema test**

Add a contract test for article status and confidence values.

```ts
expect(articleStatus.safeParse("published").success).toBe(true)
expect(articleStatus.safeParse("bad").success).toBe(false)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter @corewire/contracts test`
Expected: FAIL because schemas are missing.

- [ ] **Step 3: Write minimal implementation**

Define Zod enums and payload schemas:

```ts
export const articleStatus = z.enum(["published", "developing_story", "retracted", "superseded"])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter @corewire/contracts test`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add packages/contracts
git commit -m "feat: add shared pipeline and article contracts"
```

### Task 4: Create initial database schema and migrations

**Files:**
- Create: `apps/api/core/db/models/source.py`
- Create: `apps/api/core/db/models/document.py`
- Create: `apps/api/core/db/models/claim.py`
- Create: `apps/api/core/db/models/story.py`
- Create: `apps/api/alembic/versions/0001_initial_corewire_schema.py`
- Test: `apps/api/tests/db/test_models.py`

- [ ] **Step 1: Write the failing database model tests**

Cover minimum relationships:

```python
def test_document_belongs_to_source_item(): ...
def test_published_article_tracks_status_and_homepage_flag(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/db/test_models.py -v`
Expected: FAIL because models and migrations do not exist.

- [ ] **Step 3: Write minimal implementation**

Create SQLAlchemy models for `sources`, `source_items`, `documents`, `claims`, `claim_evidence`, `story_clusters`, `story_analysis`, `article_drafts`, `published_articles`, `article_claim_links`, `pipeline_runs`, and `model_artifacts`.

```python
class PublishedArticle(Base):
    __tablename__ = "published_articles"
    id = mapped_column(UUID, primary_key=True)
    status = mapped_column(Enum("published", "developing_story", name="article_status"))
    homepage_eligible = mapped_column(Boolean, default=False, nullable=False)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/db/test_models.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api
git commit -m "feat: add initial database schema"
```

## Chunk 3: Ingest and Extraction

### Task 5: Implement source registry and RSS ingest

**Files:**
- Create: `apps/api/core/sources/service.py`
- Create: `apps/workers/core/ingest/rss.py`
- Create: `apps/workers/tests/test_rss_ingest.py`
- Modify: `apps/api/core/db/models/source.py`

- [ ] **Step 1: Write the failing RSS ingest tests**

```python
def test_rss_entry_creates_source_item_once_per_canonical_url(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_rss_ingest.py -v`
Expected: FAIL because ingest service is missing.

- [ ] **Step 3: Write minimal implementation**

Implement feed fetch, URL canonicalization, and insert-or-ignore behavior.

```python
def ingest_feed(source: Source, entries: list[dict]) -> int:
    return upsert_source_items(source.id, normalize_entries(entries))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_rss_ingest.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/sources apps/workers/core/ingest
git commit -m "feat: add source registry and rss ingest"
```

### Task 6: Implement scraping acquisition with extractor fallback

**Files:**
- Create: `apps/workers/core/acquire/http_fetch.py`
- Create: `apps/workers/core/acquire/browser_fetch.py`
- Create: `apps/workers/core/extract/service.py`
- Create: `apps/workers/tests/test_extraction_fallback.py`

- [ ] **Step 1: Write the failing extraction fallback tests**

```python
def test_browser_fetch_runs_after_failed_simple_extraction(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_extraction_fallback.py -v`
Expected: FAIL because fallback chain is missing.

- [ ] **Step 3: Write minimal implementation**

Implement ordered fallback:

```python
def acquire_and_extract(url: str) -> ExtractedDocument:
    return try_rss() or try_http_extract() or try_browser_extract()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_extraction_fallback.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/acquire apps/workers/core/extract
git commit -m "feat: add acquisition and extraction fallback pipeline"
```

## Chunk 4: Claims, Clustering, and Corroboration

### Task 7: Implement claim extraction pipeline

**Files:**
- Create: `apps/workers/core/claims/prompts.py`
- Create: `apps/workers/core/claims/service.py`
- Create: `apps/workers/tests/test_claim_extraction.py`
- Create: `apps/workers/tests/fixtures/extracted_document.json`

- [ ] **Step 1: Write the failing claim extraction tests**

```python
def test_claim_extraction_returns_supporting_quote_for_each_claim(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_claim_extraction.py -v`
Expected: FAIL because claim extraction does not exist.

- [ ] **Step 3: Write minimal implementation**

Implement structured model call and validation:

```python
def extract_claims(document: ExtractedDocument) -> list[ClaimCandidate]:
    return validated_claims_from_model(document.body_text)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_claim_extraction.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/claims
git commit -m "feat: add claim extraction pipeline"
```

### Task 8: Implement story clustering and evidence matching

**Files:**
- Create: `apps/workers/core/clustering/service.py`
- Create: `apps/workers/core/corroboration/service.py`
- Create: `apps/workers/tests/test_story_clustering.py`
- Create: `apps/workers/tests/test_corroboration.py`

- [ ] **Step 1: Write the failing clustering and corroboration tests**

```python
def test_related_claims_join_same_story_cluster(): ...
def test_claim_gets_support_and_contradiction_links(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_story_clustering.py apps/workers/tests/test_corroboration.py -v`
Expected: FAIL because the services are missing.

- [ ] **Step 3: Write minimal implementation**

Implement similarity-based cluster assignment and relation scoring.

```python
def match_evidence(claim: Claim) -> list[EvidenceMatch]:
    return score_candidate_evidence(claim, related_documents)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_story_clustering.py apps/workers/tests/test_corroboration.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/clustering apps/workers/core/corroboration
git commit -m "feat: add story clustering and corroboration"
```

## Chunk 5: Analysis, Drafting, and Publish Gating

### Task 9: Implement structured story analysis and confidence scoring

**Files:**
- Create: `apps/workers/core/analysis/prompts.py`
- Create: `apps/workers/core/analysis/service.py`
- Create: `apps/workers/core/confidence/service.py`
- Create: `apps/workers/tests/test_story_analysis.py`

- [ ] **Step 1: Write the failing analysis tests**

```python
def test_analysis_separates_verified_facts_from_why_analysis(): ...
def test_low_source_diversity_reduces_confidence(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_story_analysis.py -v`
Expected: FAIL because analysis services are missing.

- [ ] **Step 3: Write minimal implementation**

Implement structured analysis generation plus confidence policy:

```python
def score_confidence(evidence: EvidenceBundle) -> ConfidenceResult:
    return ConfidenceResult(level="low", homepage_eligible=False)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_story_analysis.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/analysis apps/workers/core/confidence
git commit -m "feat: add analysis and confidence scoring"
```

### Task 10: Implement article drafting and citation validation

**Files:**
- Create: `apps/workers/core/drafting/prompts.py`
- Create: `apps/workers/core/drafting/service.py`
- Create: `apps/workers/core/validation/citations.py`
- Create: `apps/workers/tests/test_article_validation.py`

- [ ] **Step 1: Write the failing draft validation tests**

```python
def test_article_validation_fails_when_fact_block_has_no_citation(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_article_validation.py -v`
Expected: FAIL because citation validation is missing.

- [ ] **Step 3: Write minimal implementation**

Generate article sections from evidence payloads and validate traceability:

```python
def validate_article(draft: DraftPayload) -> ValidationResult:
    return ValidationResult(valid=all(block.citations for block in draft.fact_blocks))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_article_validation.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/drafting apps/workers/core/validation
git commit -m "feat: add article drafting and citation validation"
```

### Task 11: Implement publish gate and article APIs

**Files:**
- Create: `apps/api/core/articles/service.py`
- Create: `apps/api/core/articles/router.py`
- Create: `apps/api/tests/test_publish_gate.py`
- Modify: `apps/api/core/db/models/story.py`

- [ ] **Step 1: Write the failing publish gate tests**

```python
def test_low_confidence_story_publishes_as_developing_story_and_not_homepage(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_publish_gate.py -v`
Expected: FAIL because publishing rules are not implemented.

- [ ] **Step 3: Write minimal implementation**

Implement publish-state branching:

```python
if confidence.is_low:
    status = "developing_story"
    homepage_eligible = False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_publish_gate.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/articles apps/api/tests
git commit -m "feat: add publish gating and article api"
```

## Chunk 6: Frontend Experience

### Task 12: Build homepage using the approved command-center design reference

**Files:**
- Create: `apps/web/app/page.tsx`
- Create: `apps/web/components/home/hero-story.tsx`
- Create: `apps/web/components/home/story-grid.tsx`
- Create: `apps/web/components/home/intelligence-rail.tsx`
- Create: `apps/web/components/home/developing-stories.tsx`
- Create: `apps/web/app/globals.css`
- Test: `apps/web/tests/homepage.test.tsx`

- [ ] **Step 1: Write the failing homepage tests**

```tsx
it("renders hero story, intelligence rail, and developing stories section", () => {})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter web test homepage`
Expected: FAIL because the page and components do not exist.

- [ ] **Step 3: Write minimal implementation**

Use `F:\2026\CoreWire\code.html` and `F:\2026\CoreWire\screen.png` as design references for panel layout, palette, and mono typography while adapting labels and cards to CoreWire data.

```tsx
export default function HomePage() {
  return <main><HeroStory /><StoryGrid /><IntelligenceRail /><DevelopingStories /></main>
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter web test homepage`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: build homepage command center ui"
```

### Task 13: Build article page with fact, analysis, and citations separation

**Files:**
- Create: `apps/web/app/articles/[slug]/page.tsx`
- Create: `apps/web/components/article/article-header.tsx`
- Create: `apps/web/components/article/facts-section.tsx`
- Create: `apps/web/components/article/analysis-section.tsx`
- Create: `apps/web/components/article/sources-section.tsx`
- Create: `apps/web/components/article/disagreement-section.tsx`
- Test: `apps/web/tests/article-page.test.tsx`

- [ ] **Step 1: Write the failing article page tests**

```tsx
it("renders facts and analysis in separate labeled sections", () => {})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --filter web test article-page`
Expected: FAIL because the article page does not exist.

- [ ] **Step 3: Write minimal implementation**

Render trust and citation UI explicitly:

```tsx
<FactsSection blocks={article.facts} />
<AnalysisSection blocks={article.analysis} />
<SourcesSection citations={article.citations} />
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --filter web test article-page`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web/app/articles apps/web/components/article
git commit -m "feat: build article page with trust and citation ui"
```

## Chunk 7: Scheduling, Observability, and Verification

### Task 14: Add scheduler, retries, and pipeline audit logging

**Files:**
- Create: `apps/workers/core/jobs/scheduler.py`
- Create: `apps/workers/core/jobs/retries.py`
- Create: `apps/workers/core/audit/service.py`
- Create: `apps/workers/tests/test_scheduler.py`

- [ ] **Step 1: Write the failing scheduler tests**

```python
def test_scheduler_enqueues_ingest_jobs_for_active_sources(): ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_scheduler.py -v`
Expected: FAIL because scheduler jobs do not exist.

- [ ] **Step 3: Write minimal implementation**

Implement recurring enqueue and pipeline run tracking.

```python
def enqueue_ingest_jobs(active_sources: list[Source]) -> int:
    return sum(queue.enqueue("ingest_source", source.id) for source in active_sources)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_scheduler.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/jobs apps/workers/core/audit
git commit -m "feat: add scheduler retries and audit logging"
```

### Task 15: Add end-to-end smoke coverage and operator docs

**Files:**
- Create: `tests/e2e/publish-flow.spec.ts`
- Create: `README.md`
- Create: `docs/adr/0001-corewire-mvp-stack.md`
- Test: `tests/e2e/publish-flow.spec.ts`

- [ ] **Step 1: Write the failing end-to-end smoke test**

```ts
test("high confidence story reaches homepage and low confidence story stays off homepage", async () => {})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm exec playwright test tests/e2e/publish-flow.spec.ts`
Expected: FAIL because the stack and routes are incomplete.

- [ ] **Step 3: Write minimal implementation**

Document local setup, pipeline stages, and architecture decision records needed to operate the system.

```md
## Local Development
1. Start docker compose
2. Run API, workers, and web app
3. Seed sources
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm exec playwright test tests/e2e/publish-flow.spec.ts`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/e2e README.md docs/adr
git commit -m "test: add end-to-end publish flow coverage"
```

## Execution Notes

- Keep article drafting downstream of structured evidence only.
- Treat `analysis` and `facts` as separate backend and frontend content types.
- Do not add admin tooling during MVP execution.
- Use the approved design references at `F:\2026\CoreWire\code.html` and `F:\2026\CoreWire\screen.png` for homepage/article styling decisions.
- Prefer evaluation fixtures over live scraping during early test runs.

## Verification Checklist

- `pnpm test:repo`
- `docker compose -f infra/docker/docker-compose.yml config`
- `pytest apps/api/tests -v`
- `pytest apps/workers/tests -v`
- `pnpm --filter @corewire/contracts test`
- `pnpm --filter web test`
- `pnpm exec playwright test tests/e2e`

## Handoff

Plan complete and saved to `docs/superpowers/plans/2026-03-10-corewire-mvp-implementation.md`. Ready to execute?
