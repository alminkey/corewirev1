# CoreWire Final Product Design

**Date:** 2026-03-13
**Status:** Approved for planning
**Scope:** Final launch-ready CoreWire product with owner admin, configurable autonomy, analytics, compliance, deployment operations, and Paperclip bridge preparation

## Goal

Turn CoreWire from an integrated autonomous news system into a launch-ready AI media product with owner-controlled autonomy, newsroom operations, compliance controls, analytics, and production deployment discipline.

## Product Objective

CoreWire should function as a professional AI-native media operation, not just a pipeline that can publish articles.

The final product must support:

- a public news site with high-trust presentation
- an owner-only control plane for all publishing and autonomy settings
- sustainable operating cost through selectable model profiles
- auditable editorial and compliance workflows
- a clean future bridge into Paperclip as a newsroom orchestration system

## Product Modes

CoreWire must support three top-level operating modes:

### 1. `Manual`

- no autonomous publishing
- drafts and developing stories wait for owner action
- useful for launch rehearsals, incident recovery, and sensitive coverage

### 2. `Hybrid`

- ingest and analysis stay autonomous
- low-risk publication paths can auto-run
- certain categories, low-confidence stories, or flagged items require owner review

### 3. `Autonomous`

- CoreWire may ingest, analyze, draft, validate, and publish according to policy
- owner still retains override, pause, correction, and rollback control

These modes must be configurable in the admin control plane, not hardcoded in infrastructure.

## Owner Control Plane

The final product should include a single-owner admin surface with these sections:

### `Overview`

- system health
- publish mode
- queue depth
- recent failures
- source health
- cost summaries

### `Review Queue`

- drafts awaiting approval
- low-confidence stories
- disagreement-heavy stories
- compliance-flagged items

### `Article Operations`

- approve / reject
- publish / unpublish
- retract
- correct
- supersede
- promote or demote homepage placement

### `Autonomy Controls`

- global autonomy mode
- homepage auto-publish toggle
- developing story auto-publish toggle
- pause ingest
- pause publish
- per-source and per-topic overrides

### `Source Registry`

- enable / disable sources
- trust tier
- crawl policy
- scrape allowlists
- source notes and health state

### `Audit and Compliance`

- who or what triggered each action
- which model profile was used
- confidence and validation reasons
- correction history
- disclosure and policy state

## Editorial Quality Design

CoreWire must be optimized for natural, coherent, human-like articles rather than generic LLM prose.

That requires a layered editorial pipeline:

1. `Research packet`
   verified facts, timeline, disagreement notes, evidence map, quote sheet
2. `Structure editor`
   builds article outline from evidence only
3. `Writer`
   produces full narrative draft
4. `Style editor`
   improves flow, rhythm, paragraphing, and readability
5. `Standards validator`
   blocks unsupported, generic, or policy-breaking content

### Writing Principles

- final prose must read like a connected article, not a stitched summary
- facts and analysis remain visibly separated
- repetitive LLM filler and vague transitions are treated as quality failures
- article generation must be prompt- and rule-constrained by editorial templates

## Model Profile Design

CoreWire must support selectable execution profiles per story, per workflow, or per policy rule.

### `Economy`

Used for:

- developing stories
- low-priority topics
- internal briefs

Target:

- lower token cost
- acceptable article quality
- smaller model passes

### `Balanced`

Default profile for standard publication.

Used for:

- most public articles
- daily coverage
- explainers and standard updates

Target:

- strong quality
- sustainable token spend
- predictable output

### `Premium`

Used selectively for:

- flagship stories
- investigations
- highly visible homepage features

Target:

- highest editorial quality
- deeper research
- optional extra polish pass

## Recommended Model Strategy

### `Research and source expansion`

Primary direction: Perplexity

Why:

- strong research grounding
- source discovery
- follow-up evidence expansion

### `Writing and style`

Primary direction: Claude family

Why:

- stronger long-form prose quality
- more natural article flow
- better editorial shaping

### `Controller and validator`

Primary direction: structured-output capable control model

Why:

- schema-safe outputs
- routing, validation, and policy checks
- deterministic system interfaces

### `Hard rules`

Critical editorial and compliance gates must remain in code, not delegated to a model.

## Model Routing Architecture

CoreWire should not bind agent roles directly to providers.

Instead, introduce:

- `agent_profile`
- `model_profile`
- `provider_profile`
- `budget_policy`

This allows:

- direct provider calls where needed
- OpenRouter-based routing for experimentation and fallback
- per-story profile selection from admin
- future cost optimization without refactoring agent logic

## Analytics Design

Two analytics layers are required:

### `Product analytics`

- page views
- homepage CTR
- article CTR
- citation click-through
- topic interest
- returning visitor behavior

### `Operational analytics`

- ingest success rate
- extraction failures
- draft-to-publish conversion
- confidence distribution
- cost per article
- correction and retraction frequency
- source health trends

## Compliance Design

The final product must include:

- AI disclosure policy
- correction workflow
- retraction workflow
- supersede workflow
- audit retention
- policy page content
- owner-visible compliance flags

Compliance rules must be visible in admin and enforceable in publish workflow.

## Deployment and Operations Design

The final product must be deployment-ready with:

- production image build flow
- environment contract
- backups and restore strategy
- alerting and readiness checks
- incident response runbooks
- release checklist
- staging rehearsal path

## Paperclip Bridge Preparation

Paperclip should remain external to the public site.

Recommended future role:

- newsroom orchestration
- org structure
- ticketing
- governance
- budget oversight
- command routing

CoreWire should prepare for this through an internal operator API:

- story creation
- re-analysis
- publish draft
- source enable/disable
- autonomy toggle
- pause/resume actions

This bridge is designed for V1.5 or Phase 2, not as a blocker to V1 launch.

## Final Release Scope

Included:

- owner login and admin control plane
- autonomy controls
- review queue
- article operation controls
- model profile selection
- analytics dashboards
- compliance workflows
- production runbooks and deployment discipline
- operator API foundation

Excluded:

- multi-user RBAC
- subscriptions/paywall
- native mobile apps
- advanced personalization
- direct conversational Codex publishing as a first-class product feature

## Risks and Controls

- `Generic article prose`
  Control: structure -> writer -> style -> validator pipeline
- `High cost per article`
  Control: economy/balanced/premium profiles with policy-driven selection
- `Unsafe autonomy`
  Control: owner admin, mode toggles, pause/resume, approval gates
- `Compliance gaps`
  Control: visible audit, correction flow, hard publish gates
- `Paperclip coupling too early`
  Control: operator API prep only; no hard dependency for launch
