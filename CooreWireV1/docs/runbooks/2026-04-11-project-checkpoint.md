# CoreWire Project Checkpoint

**Date:** 2026-04-11  
**Purpose:** Durable handoff document for any future agent or engineer joining the project.  
**Supersedes:** `docs/runbooks/2026-04-10-project-checkpoint.md`  
**Status:** Current. Read this document first before touching anything.

---

## 1. What CoreWire Is

CoreWire is an AI-driven news portal with two distinct control layers:

- `CoreWire site + owner admin`
  - the public news product
  - the article generation and publishing system
  - the owner-facing control plane for operating the portal

- `Paperclip`
  - an external orchestration and governance environment
  - not part of the public CoreWire frontend
  - reads CoreWire state and sends commands through the Paperclip Bridge
  - does NOT have its own admin UI inside CoreWire

This boundary is settled and deliberate. Do not rebuild the debate unless product direction changes.

---

## 2. Current Git State

**Single source of truth: `master`**

- `master` commit: `392cd55` (merge: integrate owner-editor-admin into master)
- `origin/master` is in sync — pushed 2026-04-11
- **All worktrees are now stale.** Their content is merged into master.
  - `lead-insight-flagship` — merged ✓
  - `admin-paperclip-bridge-v1` — merged ✓
  - `.worktrees/corewire-localhost` — unrelated, still local
  - `.worktrees/codex-videeditor-bootstrap` — unrelated, still local

A future agent should work from the main repo root at `F:\2026\CoreWire\CooreWireV1`. No worktree context-switching is needed.

---

## 3. What Is Live on Staging

- Host: `213.202.216.222`
- Deployed branch: `master`
- Deployed commit: `e28e9e5`
- Deploy method: `bash scripts/deploy-webtropia.sh` via SSH with key `~/.ssh/corewire_staging_nopass`
- Health check: `http://213.202.216.222/health` — returns `200 OK`

**Current frontend/admin baseline**

- the previous light editorial redesign is superseded
- the active live baseline is now the `media-tech platform reset`
- homepage, article pages, and admin now use the newer product-style hook family:
  - `cw-platform-grid`
  - `cw-reading-surface`
  - `cw-control-plane`

**Note on Caddy + gzip:** Bridge endpoints return compressed responses by default through Caddy. Always pass `Accept-Encoding: identity` when curl-testing from outside, or the body will appear empty.

---

## 4. What Has Been Implemented — Full Picture

### 4.1 Public site and article rendering

- public homepage and article pages
- premium/editorial frontend design
- full flagship article body rendering (facts, analysis, sources, disagreements)
- SEO: canonical metadata, sitemap, robots.txt

Key files:
- [apps/web/app/page.tsx](../../../apps/web/app/page.tsx)
- [apps/web/app/articles/[slug]/page.tsx](../../../apps/web/app/articles/%5Bslug%5D/page.tsx)
- [apps/web/app/globals.css](../../../apps/web/app/globals.css)

### 4.2 Review queue and owner review flow

- owner review queue (pending drafts, low-confidence, flagged)
- article review detail page
- approve / reject / rerun actions
- doctrine diagnostics on review detail

Key files:
- [apps/api/core/admin/review.py](../../../apps/api/core/admin/review.py)
- [apps/web/app/admin/review/[id]/page.tsx](../../../apps/web/app/admin/review/%5Bid%5D/page.tsx)

### 4.3 Flagship analysis engine

The most important intellectual part of the product. Complete and on master.

- writer-first analysis: dossier → actor map → thesis → article
- lead insight extraction and centering
- editorial narrator pass
- proof-stack structure
- doctrine validator and evaluation scorer
- rerun-on-weak-output scoring

Key files:
- [apps/api/core/analysis/dossier.py](../../../apps/api/core/analysis/dossier.py)
- [apps/api/core/analysis/writer.py](../../../apps/api/core/analysis/writer.py)
- [apps/api/core/analysis/doctrine.py](../../../apps/api/core/analysis/doctrine.py)
- [apps/api/core/analysis/evaluation.py](../../../apps/api/core/analysis/evaluation.py)

Current honest status: acceptable starting point, not considered "final flagship quality". Expected to improve through live iteration on real articles.

### 4.4 Owner admin

Complete and on master, including the final launch-ready owner workflow.

- compact dashboard summary contract (`/api/admin/summary`)
- article/draft management endpoints:
  - list
  - fetch one draft
  - create
  - update
  - publish
  - archive
- programming controls (topic targets, intervals, scheduling windows)
- admin UI:
  - improved admin shell
  - single-page article manager workspace
  - manual draft inventory
  - editor form for `headline`, `dek`, `slug`, `tags`, `body`
  - `New Draft`, `Save Draft`, `Publish`, `Archive`
  - programming `Apply Changes` workflow inside `/admin`

Key files:
- [apps/api/core/admin/overview.py](../../../apps/api/core/admin/overview.py)
- [apps/api/core/admin/content.py](../../../apps/api/core/admin/content.py)
- [apps/api/core/admin/programming.py](../../../apps/api/core/admin/programming.py)
- [apps/api/core/admin/router.py](../../../apps/api/core/admin/router.py)
- [apps/web/components/admin/article-manager.tsx](../../../apps/web/components/admin/article-manager.tsx)
- [apps/web/components/admin/programming-controls.tsx](../../../apps/web/components/admin/programming-controls.tsx)

### 4.5 Paperclip Bridge V1

Complete, on master, and verified live on staging on 2026-04-11.

**Bridge read endpoints** (all require `x-internal-token` header):

| Endpoint | Returns |
|---|---|
| `GET /api/operator/bridge/status` | health, autonomy, pause state, queue counts, recent activity |
| `GET /api/operator/bridge/review-queue` | pending drafts, low-confidence, flagged — with totals |
| `GET /api/operator/bridge/published` | total count + 10 most recent |
| `GET /api/operator/bridge/autonomy` | mode and all publish gate flags |

**Command endpoint:** `POST /api/operator/commands`

Supported command types include `import_external_draft` (routes through review/compliance, never auto-publishes). Full correlation metadata preserved on every command response:
- `ticket_id`, `actor_id`, `company_id`, `correlation_id`, `requested_by`

Key files:
- [apps/api/core/operator/bridge.py](../../../apps/api/core/operator/bridge.py)
- [apps/api/core/operator/service.py](../../../apps/api/core/operator/service.py)
- [apps/api/core/operator/schemas.py](../../../apps/api/core/operator/schemas.py)
- [docs/ops/paperclip-bridge.md](../ops/paperclip-bridge.md)
- [docs/runbooks/paperclip-http-adapter.md](paperclip-http-adapter.md)

---

## 5. What Is Left To Do

### 5.1 Worktree cleanup (quick, low-risk)

The two merged worktrees are stale and can be removed:

```bash
git worktree remove .worktrees/admin-paperclip-bridge-v1
git worktree remove .worktrees/lead-insight-flagship
# Optional: delete the remote branches if no longer needed
git push origin --delete lead-insight-flagship
git push origin --delete admin-paperclip-bridge-v1
```

### 5.2 Flagship analysis quality (ongoing product work)

Not a blocker for anything. Expected to iterate continuously from real article output:

- more original insight density
- less memo-like middle sections
- stronger "aha" editorial value
- tighter consequence and ending paragraphs

This is live-feedback iteration, not a structured engineering task.

### 5.3 Richer admin UX (future product work)

Low priority, no dependencies:

- add/remove rows for topics, intervals, and schedule windows
- richer save feedback and validation states in admin forms
- fuller analytics views

---

## 6. Canonical Documents

### Current reference docs

- **This file** — current project state and starting point
- [docs/ops/paperclip-bridge.md](../ops/paperclip-bridge.md) — Paperclip bridge contract V1
- [docs/runbooks/paperclip-http-adapter.md](paperclip-http-adapter.md) — Paperclip HTTP adapter setup
- [docs/ops/staging-rehearsal.md](../ops/staging-rehearsal.md) — staging smoke checklist

### Completed plan docs (do not re-execute)

- [2026-04-09-corewire-admin-paperclip-bridge-implementation.md](../superpowers/plans/2026-04-09-corewire-admin-paperclip-bridge-implementation.md) — **COMPLETE 2026-04-11**
- [2026-04-11-owner-editor-admin-completion-implementation.md](../superpowers/plans/2026-04-11-owner-editor-admin-completion-implementation.md) — **COMPLETE 2026-04-11**
- [2026-04-08-editorial-narrator-pass-implementation.md](../superpowers/plans/2026-04-08-editorial-narrator-pass-implementation.md) — complete
- [2026-04-07-lead-insight-flagship-implementation.md](../superpowers/plans/2026-04-07-lead-insight-flagship-implementation.md) — complete
- [2026-03-13-corewire-final-product-implementation.md](../superpowers/plans/2026-03-13-corewire-final-product-implementation.md) — complete

---

## 7. Practical Notes for Future Agents

### Where to start

1. Read this document.
2. Check `git log --oneline -10` on `master` — that is the full truth.
3. Look at the relevant area under `apps/api/core/` or `apps/web/` directly.

### Deploy

```bash
ssh -i ~/.ssh/corewire_staging_nopass root@213.202.216.222
cd /opt/corewire/app/CooreWireV1
git pull origin master
bash scripts/deploy-webtropia.sh
```

### Test suite

```bash
# API tests (from apps/api/)
pytest tests/ -q

# Integration tests (from CooreWireV1/)
pytest tests/integration/ -q

# Web tests (from CooreWireV1/)
pnpm --dir apps/web test
```

### Verification habits

- `pytest` for API and worker logic
- `pnpm --dir apps/web test` for web source tests
- live staging curl checks for final behavior (use `Accept-Encoding: identity` with curl through Caddy)

### Windows environment note

This repo is worked from PowerShell on Windows. Bash commands in this document use Unix syntax — run them via git bash or WSL, not PowerShell directly. Local localhost behavior has been unstable; staging is the primary verification surface.

### Owner admin vs Paperclip is settled

- CoreWire admin = site owner control plane (canonical)
- Paperclip = external bridge caller, future broader agency OS

Do not rebuild this boundary unless product direction changes.

---

## 8. Bottom-Line Status

As of 2026-04-11:

- CoreWire is a working, staging-backed AI news portal
- `master` is the single source of truth — all work is merged
- Paperclip Bridge V1 is live on staging
- the flagship analysis engine is functional and ready for quality iteration
- the owner admin is launch-ready for core operations
- there are no unmerged active branches blocking anything

This is a clean, integrated, deployable codebase.
