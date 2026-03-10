# CoreWire MVP Design

**Date:** 2026-03-10
**Status:** Approved for planning
**Scope:** English-only MVP for autonomous ingest, analysis, and publishing

## Goal

Build CoreWire as an autonomous AI news portal that ingests multiple sources, extracts and compares claims, produces cited investigative-style articles, and publishes them with explicit confidence labeling.

## Product Boundaries

Included in MVP:

- Autonomous ingest from RSS and active scraping targets
- Full-text extraction and normalization
- Claim extraction and cross-source corroboration
- Why-analysis separated from factual reporting
- Automated article drafting with citations and links
- Public homepage, article page, and developing stories page
- Confidence-based publish gating

Excluded from MVP:

- Admin CMS and manual newsroom workflows
- User accounts and subscriptions
- Monetization features
- Multi-language publishing
- Native mobile apps

## Source and Publishing Rules

- Every public-facing factual claim must be traceable to at least one linked source.
- Analysis must be clearly labeled as analysis, not fact.
- High-confidence stories can be published to the homepage.
- Low-confidence stories may be published only as clearly labeled `developing_story` items and must not appear on the homepage.
- If citation validation fails, the story is not published.

## Recommended Architecture

CoreWire should start as a modular monolith with separate runtime roles:

- `apps/web`: Next.js public-facing frontend
- `apps/api`: FastAPI application exposing read APIs, orchestration endpoints, and internal publishing actions
- `apps/workers`: Python worker runtime for ingest, extraction, clustering, corroboration, analysis, and draft generation
- `PostgreSQL`: system of record for sources, documents, claims, evidence, analyses, and published content
- `Redis`: job queue, retries, dedupe helpers, and short-lived cache
- `Object storage`: raw HTML snapshots, extraction outputs, model artifacts, and audit files
- `Scheduler`: recurring job triggers for ingest and re-analysis

This architecture prioritizes rapid MVP delivery, operational clarity, and a strong Python pipeline for scraping and AI orchestration while keeping a premium frontend in Next.js.

## AI Model Strategy

Primary provider for MVP: `OpenAI`

Reasoning:

- strongest structured output reliability for claim extraction and article synthesis
- good fit for multi-step validation pipelines
- lower early integration risk than multi-provider abstraction on day one

Future direction:

- define an internal provider interface so OpenRouter or DeepSeek can be added later for fallback or cost optimization

## Core Components

### 1. Source Registry

Stores approved feeds, scraping seeds, crawl policy, language, and trust metadata per source.

### 2. Ingest Engine

Discovers URLs from RSS and scraper targets, canonicalizes them, deduplicates them, and records acquisition attempts.

### 3. Extraction Engine

Attempts extraction in this order:

1. RSS body when sufficient
2. HTTP fetch + article extraction
3. Browser rendering via Playwright for JS-heavy pages

### 4. Claim Engine

Turns extracted documents into atomic claims with evidence spans, source attribution, and extraction confidence.

### 5. Story Clustering and Corroboration

Groups related documents and claims into story clusters, then measures support, contradiction, and source diversity.

### 6. Analysis Engine

Produces structured outputs for:

- what happened
- what is verified
- what remains uncertain
- why it matters
- where sources disagree

### 7. Drafting and Validation Engine

Generates article drafts only from structured evidence packages, then validates citation coverage, confidence thresholds, and editorial rules.

### 8. Publishing Engine

Publishes either:

- `published` stories eligible for homepage placement
- `developing_story` items excluded from homepage

### 9. Public Frontend

Renders a premium reading experience with visible trust metadata, citation anchors, confidence labels, and article timelines.

## Data Model

### `sources`

Publisher/feed configuration:

- id
- name
- domain
- rss_url
- crawl_type
- language
- trust_tier
- active

### `source_items`

Discovered content unit:

- id
- source_id
- original_url
- canonical_url
- discovered_at
- published_at
- acquisition_status
- raw_html_object_key

### `documents`

Normalized extracted article:

- id
- source_item_id
- title
- dek
- byline
- language
- body_text
- extraction_quality_score
- extracted_at

### `claims`

Atomic factual unit:

- id
- document_id
- claim_text
- claim_type
- subject
- predicate
- object
- supporting_quote
- extraction_confidence

### `claim_evidence`

Cross-source relationship:

- id
- claim_id
- evidence_document_id
- relation_type (`supports`, `contradicts`, `context`)
- evidence_quote
- evidence_strength
- source_diversity_weight

### `story_clusters`

Event/topic grouping:

- id
- cluster_key
- topic_label
- status
- first_seen_at
- last_updated_at

### `story_analysis`

Structured AI analysis per cluster:

- id
- story_cluster_id
- verified_facts_json
- open_questions_json
- why_analysis_text
- disagreement_summary
- overall_confidence
- low_confidence_reasons_json

### `article_drafts`

Generated draft:

- id
- story_analysis_id
- headline
- dek
- body_json
- facts_json
- analysis_json
- citations_json
- validation_status

### `published_articles`

Public article record:

- id
- article_draft_id
- slug
- status
- homepage_eligible
- published_at
- updated_at
- rendered_snapshot_json

### `article_claim_links`

Traceability bridge between article content and evidence:

- id
- published_article_id
- article_block_key
- claim_id
- claim_evidence_id

### `pipeline_runs`

Audit trail:

- id
- run_type
- target_id
- model_name
- prompt_version
- status
- started_at
- finished_at
- error_json

### `model_artifacts`

Stored model I/O:

- id
- pipeline_run_id
- artifact_type
- object_key
- schema_validation_status

## Pipeline

1. `discover_sources`
   Fetch RSS entries and scraper candidates from active sources.
2. `acquire_content`
   Fetch raw page content and persist snapshots.
3. `extract_document`
   Produce clean article text and metadata.
4. `extract_claims`
   Produce claim records with supporting spans and confidence scores.
5. `cluster_story`
   Group claims and documents into event-centric clusters.
6. `corroborate`
   Find confirming, conflicting, and contextual evidence across sources.
7. `analyze`
   Generate structured summary, what-is-verified, and why-analysis.
8. `draft_article`
   Build article sections from structured evidence only.
9. `validate`
   Enforce citations, labels, and confidence thresholds.
10. `publish`
   Publish as `published` or `developing_story`.
11. `revisit`
   Re-run analysis when new evidence appears.

## Autonomous Agent Workflow

The system should behave as a pipeline of focused worker roles:

- `Scout`: finds and deduplicates candidate URLs
- `Extractor`: turns raw pages into clean documents
- `Corroborator`: matches claims across sources
- `Analyst`: builds structured interpretations and uncertainty summaries
- `Publisher`: validates and publishes or holds output

Queue stages:

`discovered -> acquired -> extracted -> claims_ready -> clustered -> corroborated -> analyzed -> drafted -> validated -> published`

## UI Design Direction

The approved UI direction should explicitly reference:

- [code.html](/f:/2026/CoreWire/code.html)
- [screen.png](/f:/2026/CoreWire/screen.png)

These references establish the visual language for MVP:

- dark command-center aesthetic
- mono-heavy typography
- orange signal/accent color on near-black surfaces
- panelized layout with intelligence-terminal framing
- technical status language and operational dashboard cues

The product adaptation for news UX should preserve that visual identity while adding trust-specific affordances:

- confidence badges
- citation counts
- source diversity indicators
- labeled `FACTS` and `ANALYSIS` blocks
- dedicated `DEVELOPING STORY` treatment

### Homepage Layout

- lead hero story with headline, dek, confidence, and source count
- secondary story grid
- right-side or lower intelligence rail for latest updates
- developing stories section separated from homepage lead stack
- topic bands for major coverage areas

### Article Page Layout

- headline and metadata header
- `What is verified` section near the top
- main article narrative
- clearly separated `Analysis`
- `Where sources disagree`
- source list with outbound links
- update timeline for evolving stories

## Development Milestones

1. Foundation and repo bootstrap
2. Ingest and extraction
3. Claims and clustering
4. Corroboration and analysis
5. Drafting and publish validation
6. Public frontend
7. Scheduler, retries, and observability
8. Quality tuning and evaluation

## Risks and Controls

- Scraping instability: mitigate with source policy, retries, extractor fallback, and snapshot retention
- Hallucinated synthesis: mitigate by drafting only from structured evidence payloads
- Weak corroboration: route to `developing_story`
- Citation gaps: block publication
- Visual ambiguity between fact and analysis: enforce distinct UI components and backend content types

## Open Deferred Items

- source reputation scoring model
- provider failover strategy
- human-in-the-loop editorial tooling
- monetization and account system
