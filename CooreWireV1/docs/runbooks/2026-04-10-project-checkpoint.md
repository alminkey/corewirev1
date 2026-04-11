# CoreWire Project Checkpoint

**Date:** 2026-04-10  
**Purpose:** Durable handoff document for any future agent or engineer joining the project.  
**Status:** SUPERSEDED — this document describes a state that no longer exists (split worktrees, unmerged branches).

> **Read instead: [2026-04-11-project-checkpoint.md](2026-04-11-project-checkpoint.md)**  
> All worktrees are merged into `master`. Staging runs `master`. This document is kept for historical reference only.

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
  - intended to read CoreWire state and send commands into CoreWire through a bridge

This separation is now deliberate and documented. CoreWire admin remains the canonical owner control plane. Paperclip is an external caller and future agency OS layer.

---

## 2. Canonical Documents to Read First

These are the current high-value docs. A future agent should start here before changing anything major.

### Product and launch baseline

- [2026-03-13-corewire-final-product-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-03-13-corewire-final-product-design.md)
- [2026-03-13-corewire-final-product-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-03-13-corewire-final-product-implementation.md)

These remain valid for broad product scope, infrastructure, admin, deploy, compliance, and future Paperclip preparation.

### Analysis engine baseline

- [2026-04-01-corewire-analysis-doctrine-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-01-corewire-analysis-doctrine-design.md)
- [2026-04-01-corewire-analysis-engine-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-04-01-corewire-analysis-engine-implementation.md)

These are the canonical documents for the flagship analysis generation path.

### Flagship analysis quality follow-up

- [2026-04-06-flagship-insight-engine-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-06-flagship-insight-engine-design.md)
- [2026-04-06-flagship-insight-engine-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-04-06-flagship-insight-engine-implementation.md)
- [2026-04-07-lead-insight-flagship-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-07-lead-insight-flagship-design.md)
- [2026-04-07-lead-insight-flagship-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-04-07-lead-insight-flagship-implementation.md)

These describe the transition from generic structured analysis drafts toward flagship pieces built around one dominant insight.

### Current admin and Paperclip baseline

- [2026-04-09-corewire-admin-paperclip-bridge-design.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/specs/2026-04-09-corewire-admin-paperclip-bridge-design.md)
- [2026-04-09-corewire-admin-paperclip-bridge-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-04-09-corewire-admin-paperclip-bridge-implementation.md)

These are the canonical docs for:

- owner admin closure on the site
- the first narrow Paperclip bridge

### Operational bridge contract

- [paperclip-bridge.md](/f:/2026/CoreWire/CooreWireV1/docs/ops/paperclip-bridge.md)

This documents the original internal operator contract that Paperclip integration builds on.

---

## 3. Current Branch and Worktree Reality

This project is currently split across multiple git worktrees. A future agent must understand this before making assumptions about what is merged and what is only implemented on a feature branch.

### Main repo root

- repo root: [CoreWire](/f:/2026/CoreWire)
- main project root: [CooreWireV1](/f:/2026/CoreWire/CooreWireV1)
- current `master` commit in root checkout:
  - `1b91113` `docs: define corewire admin and paperclip bridge v1`

### Active worktrees

- [lead-insight-flagship worktree](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1)
  - branch: `lead-insight-flagship`
  - current commit: `fbfb66e`
  - purpose: flagship analysis engine and editorial narrator work

- [admin-paperclip-bridge-v1 worktree](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1)
  - branch: `admin-paperclip-bridge-v1`
  - current commit: `158df5c`
  - purpose: owner admin closure and Paperclip Bridge v1 work

Other worktrees exist but are not central to the current product roadmap:

- `.worktrees/corewire-localhost`
- `.worktrees/codex-videeditor-bootstrap`

### Important git truth

- `master` is ahead of `origin/master`
- `lead-insight-flagship` tracks `origin/lead-insight-flagship`
- `admin-paperclip-bridge-v1` is local and unmerged

This means:

- not everything implemented is on `master`
- not everything on staging is on `master`
- a future agent must check the relevant worktree branch before assuming functionality is missing

---

## 4. What Is Live on Staging Right Now

Staging server:

- host: `213.202.216.222`
- current deployed branch: `lead-insight-flagship`
- deployed commit: `fbfb66e`
- health check: `http://213.202.216.222/health` returned `200` during this checkpoint

Important implication:

- staging currently reflects the flagship analysis/editorial narrator work
- staging does **not** yet reflect the unmerged `admin-paperclip-bridge-v1` worktree changes

If a future agent wants the new admin/Paperclip work on staging, they must explicitly merge or cherry-pick from the `admin-paperclip-bridge-v1` branch and redeploy.

---

## 5. What Has Been Implemented So Far

### 5.1 Public site and article rendering

Implemented and working:

- public homepage and article pages
- redesigned public frontend with light premium/editorial direction
- clickable homepage sections
- shared public header and article layout
- full flagship article body rendering
- fixed article facts/analysis duplicate-key issue

Key files include:

- [page.tsx](/f:/2026/CoreWire/CooreWireV1/apps/web/app/page.tsx)
- [page.tsx](/f:/2026/CoreWire/CooreWireV1/apps/web/app/articles/[slug]/page.tsx)
- [globals.css](/f:/2026/CoreWire/CooreWireV1/apps/web/app/globals.css)
- [article-page.test.mjs](/f:/2026/CoreWire/CooreWireV1/apps/web/tests/article-page.test.mjs)
- [homepage.test.mjs](/f:/2026/CoreWire/CooreWireV1/apps/web/tests/homepage.test.mjs)

### 5.2 Review queue and owner review flow

Implemented and working:

- owner review queue
- low-confidence review detail page
- approve / reject / rerun actions
- doctrine diagnostics on review detail
- decision-ready review UI

Key files include:

- [review.py](/f:/2026/CoreWire/CooreWireV1/apps/api/core/admin/review.py)
- [page.tsx](/f:/2026/CoreWire/CooreWireV1/apps/web/app/admin/review/[id]/page.tsx)
- [actions.ts](/f:/2026/CoreWire/CooreWireV1/apps/web/app/admin/review/[id]/actions.ts)
- [test_review_queue.py](/f:/2026/CoreWire/CooreWireV1/apps/api/tests/test_review_queue.py)
- [review-queue.test.mjs](/f:/2026/CoreWire/CooreWireV1/apps/web/tests/review-queue.test.mjs)

### 5.3 Analysis engine and flagship writing system

This is the most important intellectual part of the product.

Implemented on the `lead-insight-flagship` branch:

- writer-first analysis engine
- dossier building
- actor mapping
- thesis generation
- doctrine validator
- evaluation scoring
- insight-engine and lead-insight extensions
- editorial narrator pass
- proof-stack style flagship composition improvements

Key analysis engine files live primarily in the `lead-insight-flagship` worktree:

- [dossier.py](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis/dossier.py)
- [thesis.py](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis/thesis.py)
- [writer.py](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis/writer.py)
- [doctrine.py](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis/doctrine.py)
- [evaluation.py](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis/evaluation.py)

Key recent commits on that branch:

- `506e828` `feat: rewrite flagship opening as editorial lead`
- `56f2a55` `feat: replace actor profiles with editorial proof paragraphs`
- `7c10159` `feat: strengthen editorial transitions in flagship analysis`
- `86ce604` `feat: harden flagship editorial closing cadence`
- `10762af` `fix: stabilize editorial narrator flagship regressions`
- `fbfb66e` `fix: stabilize editorial narrator flagship regressions`

Current honest status of this area:

- much better than the original structured-output scaffolding
- still not considered “final flagship quality”
- acceptable as a starting point
- expected to improve further through live iteration

### 5.4 Owner admin closure work

This work is implemented on the `admin-paperclip-bridge-v1` branch.

Already implemented there:

- richer owner dashboard summary contract
- manual owner article/draft management endpoints
- programming controls for topics, intervals, and schedule windows
- admin UI surfaces for:
  - article manager
  - programming controls
  - improved admin shell wiring

Key backend files in the admin worktree:

- [overview.py](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin/overview.py)
- [content.py](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin/content.py)
- [programming.py](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin/programming.py)
- [router.py](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin/router.py)
- [settings.py](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin/settings.py)

Key frontend files in the admin worktree:

- [page.tsx](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/app/admin/page.tsx)
- [admin-shell.tsx](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/components/admin/admin-shell.tsx)
- [article-manager.tsx](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/components/admin/article-manager.tsx)
- [programming-controls.tsx](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/components/admin/programming-controls.tsx)
- [api.ts](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/lib/api.ts)
- [types.ts](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/lib/types.ts)

Recent commits on that branch:

- `7bf33cf` `feat: add owner dashboard summary contract`
- `86831e1` `feat: add owner article management endpoints`
- `6ff4978` `feat: add owner programming controls`
- `158df5c` `feat: close owner admin surface`

Current honest status of this area:

- owner admin is significantly more complete than before
- still not merged to `master`
- still not deployed to staging

### 5.5 Operator API and Paperclip preparation

Already present before the new bridge phase:

- internal operator command API
- command types for creating stories, reruns, publish actions, autonomy changes, and source control
- base Paperclip bridge contract document

Key files:

- [router.py](/f:/2026/CoreWire/CooreWireV1/apps/api/core/operator/router.py)
- [schemas.py](/f:/2026/CoreWire/CooreWireV1/apps/api/core/operator/schemas.py)
- [service.py](/f:/2026/CoreWire/CooreWireV1/apps/api/core/operator/service.py)
- [paperclip-bridge.md](/f:/2026/CoreWire/CooreWireV1/docs/ops/paperclip-bridge.md)

Current honest status:

- the original operator contract exists
- the dedicated `Paperclip Bridge v1` read endpoints and correlation-hardened command layer are **not done yet**

---

## 6. What Is Still Left to Do

This section is the most important roadmap summary.

### A. Paperclip Bridge V1

Still pending from [2026-04-09-corewire-admin-paperclip-bridge-implementation.md](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans/2026-04-09-corewire-admin-paperclip-bridge-implementation.md):

1. `Task 5`
   - add Paperclip bridge read endpoints
   - likely file: `apps/api/core/operator/bridge.py`
   - expose:
     - status summary
     - review queue summary
     - published summary
     - autonomy state

2. `Task 6`
   - preserve correlation metadata in operator command ingestion
   - support optional `import_external_draft`

3. `Task 7`
   - update bridge docs for HTTP adapter flow
   - add Paperclip runbook

4. `Task 8`
   - staging rehearsal for owner admin + Paperclip bridge flow

### B. Merge and deployment discipline

Still pending:

- decide how to merge `lead-insight-flagship` into `master`
- decide how to merge `admin-paperclip-bridge-v1` into `master`
- redeploy staging from the chosen integration branch rather than leaving production truth split across worktrees

### C. Flagship analysis quality

Still pending in product terms:

- more original insight density
- less memo-like middle sections
- stronger “aha” editorial value
- continued live iteration from real article feedback

This is not a blocker to proceed with admin and Paperclip work, but it remains a core product objective.

### D. Admin UX beyond current closure

Still pending if the team wants a fuller owner CMS experience:

- richer edit forms
- create draft UI actions rather than only inventory display
- stronger scheduling UX
- more complete analytics views

These are improvements, not blockers to starting the Paperclip bridge.

---

## 7. Current Recommended Execution Order

If a future agent joins today, the safest next order is:

1. finish `Paperclip Bridge v1`
2. merge or cherry-pick `admin-paperclip-bridge-v1`
3. decide whether staging should stay on `lead-insight-flagship` or move to an integrated branch
4. continue iterative flagship analysis quality improvement

This avoids reopening old ambiguity between:

- “admin on the site”
- “Paperclip as a separate agency layer”

That boundary is now clear and should stay clear.

---

## 8. Practical Notes for Future Agents

### Do not assume `master` is the full truth

The project is currently split across worktrees. Always inspect:

- root checkout
- `lead-insight-flagship`
- `admin-paperclip-bridge-v1`

before deciding a feature is missing.

### Staging is not the same thing as `master`

At this checkpoint:

- staging runs `lead-insight-flagship`
- `admin-paperclip-bridge-v1` is local-only

### Owner admin vs Paperclip is settled

Do not rebuild this debate unless the product direction changes:

- CoreWire admin = site owner control plane
- Paperclip = external bridge caller and future broader agency OS

### Windows environment note

This repo has repeatedly been worked from PowerShell on Windows.

Practical gotchas observed:

- PowerShell does not accept `&&` as a statement separator in older shells; use `;`
- local localhost/runtime behavior has been unstable enough that staging became the primary verification surface

### Verification habits already in use

The project has been using:

- `pytest` for API and worker logic
- `node --test` or `pnpm --dir apps/web test` for web source tests
- live staging checks for final behavior

Continue that pattern.

---

## 9. Minimal “Where to Look” Map

If a future agent needs to move fast, start here.

### Public site

- [app](/f:/2026/CoreWire/CooreWireV1/apps/web/app)
- [components/home](/f:/2026/CoreWire/CooreWireV1/apps/web/components/home)
- [components/article](/f:/2026/CoreWire/CooreWireV1/apps/web/components/article)

### Owner admin

- root version: [admin api](/f:/2026/CoreWire/CooreWireV1/apps/api/core/admin)
- worktree version with newest admin closure: [admin api worktree](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/api/core/admin)
- worktree admin UI: [admin web worktree](/f:/2026/CoreWire/.worktrees/admin-paperclip-bridge-v1/CooreWireV1/apps/web/app/admin)

### Analysis engine

- root planning docs: [analysis plans](/f:/2026/CoreWire/CooreWireV1/docs/superpowers/plans)
- live implementation branch: [analysis core worktree](/f:/2026/CoreWire/.worktrees/lead-insight-flagship/CooreWireV1/apps/api/core/analysis)

### Paperclip bridge and operator path

- [operator core](/f:/2026/CoreWire/CooreWireV1/apps/api/core/operator)
- [bridge contract doc](/f:/2026/CoreWire/CooreWireV1/docs/ops/paperclip-bridge.md)

---

## 10. Bottom-Line Status

At this checkpoint:

- CoreWire exists as a real staging-backed AI news portal
- the flagship analysis engine has undergone a major redesign and is now usable as a starting point
- the owner admin has been materially expanded in a dedicated worktree
- the Paperclip direction is clarified but not finished
- the biggest unfinished engineering slice is `Paperclip Bridge v1`
- the biggest unfinished product slice is continued improvement of flagship article quality

This is not an early prototype anymore.  
It is a working system with split active branches and a clear next path.
