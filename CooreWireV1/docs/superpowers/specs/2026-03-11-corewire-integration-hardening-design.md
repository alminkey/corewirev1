# CoreWire Integration and Hardening Design

**Date:** 2026-03-11
**Status:** Approved for planning
**Scope:** Runtime integration, SEO readiness, observability, security baseline, vendor-neutral deployment, and scaling guidance

## Goal

Turn the current CoreWire MVP skeleton into a locally runnable, operationally verifiable, vendor-neutral system that can be hardened for production without changing the core product architecture.

## Current Baseline

CoreWire already has:

- ingest, extraction, claims, clustering, analysis, drafting, and publish-gate skeletons
- homepage and article page UI skeletons
- initial data models, scheduler helpers, audit helpers, and smoke tests

CoreWire does not yet have:

- a fully wired FastAPI runtime
- a fully wired Next.js runtime serving live backend data
- real persistence across the full ingest-to-publish path
- real queue-backed orchestration for the main pipeline
- production-grade SEO, observability, security, or deployment assets

## Continuation Boundaries

Included in this phase:

- localhost-ready integrated runtime
- database and queue wiring for the main pipeline
- live API-to-web data flow
- seed/demo data and operator runbooks
- technical SEO and search integrity controls
- observability, health probes, and operational verification
- security baseline for crawling and internal services
- vendor-neutral containerization and deployment manifests
- horizontal scaling strategy for web, API, and workers

Excluded from this phase:

- admin CMS
- user accounts and subscriptions
- monetization
- multilingual publishing
- recommendation/personalization systems
- multi-region deployment
- human editorial workflow tooling

## Recommended Continuation Approach

Use a two-stage continuation inside one plan:

1. `Integration`
   Make the existing services real, connected, and runnable.
2. `Hardening`
   Add operational quality, security, SEO, and deployment readiness on top of the integrated runtime.

This keeps priorities correct: first make the system actually run, then harden what already works.

## Runtime Architecture

The continuation keeps the modular monolith shape but closes the gaps between services.

- `apps/api`
  FastAPI app entrypoint, dependency injection, DB session management, routers, internal pipeline triggers, health and readiness endpoints
- `apps/workers`
  queue consumer, scheduler runner, pipeline orchestrator, artifact persistence, retry/dead-letter handling
- `apps/web`
  Next.js runtime with server-side data fetching, live homepage/article rendering, metadata generation, sitemap, robots, and structured data
- `PostgreSQL`
  source of truth for sources, source items, documents, claims, evidence, analyses, articles, pipeline runs, and operational state
- `Redis`
  queue backend, job coordination, rate limiting state, and short-lived caches
- `Object storage`
  raw page snapshots, extraction artifacts, model outputs, and audit payloads

## Integration Principles

- the same code path should serve local, CI, and production execution
- in-memory implementations must be removed from primary runtime paths
- pipeline state transitions must be persisted and inspectable
- frontend trust UI must be backed by live article and citation payloads
- seed flows must create representative articles for local verification

## Runtime Data Flow

1. scheduler enqueues ingest jobs for active sources
2. workers fetch RSS or scraper candidates and persist source items
3. acquisition and extraction persist documents and raw artifacts
4. claim extraction persists claims and supporting quote spans
5. clustering and corroboration persist story cluster and evidence state
6. analysis and confidence scoring persist structured analysis outputs
7. drafting and citation validation create draft records
8. publish gate writes published articles and article-claim links
9. API exposes article lists, article details, developing stories, and trust metadata
10. web renders homepage/article pages from API responses with full metadata and citation affordances

## SEO Design

SEO in this phase is technical and editorially safe, not growth-focused.

### Technical SEO

- canonical URL generation for all articles
- `sitemap.xml` and `robots.txt`
- metadata generation for article and homepage routes
- Open Graph and Twitter/X card tags
- news/article `schema.org` markup
- breadcrumb schema if routing structure justifies it
- stable slug policy and redirect rules for superseded articles

### Search Integrity Rules

- `developing_story` pages should have explicit canonical handling and controlled indexability
- thin or invalid draft pages must never be indexable
- superseded or corrected articles must preserve search integrity through explicit status handling
- duplicate story variants must resolve to a single canonical article where possible

### Performance SEO

- page weight and Core Web Vitals budgets
- image and font loading strategy
- caching headers for public routes
- server-rendered metadata and content critical path

## Observability Design

Required observability surfaces:

- structured JSON logs from API, workers, and scheduler
- request IDs and pipeline run IDs propagated across services
- metrics endpoint for HTTP, job success/failure, queue depth, publish outcomes, and extraction failure rate
- tracing hooks for future OpenTelemetry export
- health and readiness endpoints for API and worker processes
- audit retention policy for pipeline decisions and model outputs

## Security Design

This phase adds a baseline, not a full zero-trust platform.

### Application Security

- typed config with strict env validation
- authenticated or network-restricted internal publish/orchestration routes
- SSRF protections for fetchers and browser-based acquisition
- domain allowlists and crawl policy enforcement
- request size and timeout guardrails

### Supply Chain and Runtime Security

- pinned dependency policy where practical
- dependency scanning hooks
- container image hardening basics
- non-root containers where feasible
- secret injection via environment/runtime secret store abstraction

## Deployment Design

Deployment remains vendor-neutral.

Artifacts to produce:

- multi-stage Dockerfiles for `web`, `api`, and `workers`
- local and production compose overlays
- Kubernetes or Helm-compatible manifests for vendor-neutral deployment
- environment contract documentation
- migration and startup order rules

## Scaling Model

- `web` scales horizontally behind a reverse proxy or ingress
- `api` scales horizontally if background orchestration is not stored in process memory
- `workers` scale by queue type and throughput bottleneck
- scheduler remains singleton or leader-elected
- queue backpressure policies protect extraction and model-cost spikes
- object storage and Postgres remain shared managed-state dependencies

## Verification Strategy

This phase requires four verification layers:

1. `unit and contract`
   config, repositories, serializers, metadata generators
2. `integration`
   DB, Redis, API, worker, and seed flow behavior
3. `browser smoke`
   homepage, article page, citation UI, sitemap, robots
4. `operational`
   startup, migrations, health probes, logs, metrics, and rollback-safe deployment scripts

## Deliverables

- continuation implementation plan
- live runtime bootstrap for web, API, and workers
- seed data and local runbook
- SEO readiness assets and policies
- observability and security baseline
- vendor-neutral deployment manifests
- production readiness checklist

## Risks and Controls

- runtime wiring drift between local and production
  Control: shared config, single compose entry path, startup verification
- crawl abuse or SSRF exposure
  Control: source allowlists, protocol restrictions, fetch guardrails
- search penalties from duplicate or low-confidence pages
  Control: canonical rules, noindex strategy, structured metadata discipline
- operational blind spots
  Control: request IDs, metrics, health endpoints, structured logs
- cost spikes from analysis/publishing loops
  Control: queue limits, retry caps, dead-letter queues, reprocessing thresholds
