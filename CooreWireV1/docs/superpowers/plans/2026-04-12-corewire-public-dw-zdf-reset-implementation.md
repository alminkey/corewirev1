# CoreWire Public DW/ZDF Reset Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the public frontend so it behaves like a denser, active international news service with a ZDF-like header and DW-like homepage rhythm.

**Architecture:** Keep existing routes and API contracts, but replace the public shell, homepage composition, and article presentation with a new component and CSS structure. Treat the previous clean-slate luxury landing as superseded. Use TDD on the web rendering tests before implementation.

**Tech Stack:** Next.js App Router, React server components, shared API client, global CSS, Node test runner for web rendering tests.

---

## File Structure

### Public shell and navigation

- Modify: `apps/web/components/public/public-header.tsx`
  - Replace current header with ZDF-like utility and navigation rows
- Modify: `apps/web/app/globals.css`
  - Replace public-facing shell/layout styles with denser DW/ZDF reset styles

### Homepage composition

- Modify: `apps/web/app/page.tsx`
  - Recompose homepage around lead cluster, latest desk, top secondary band, analysis zone, section bands, lower feed
- Modify: `apps/web/components/home/hero-story.tsx`
  - Replace current luxury landing hero with lead cluster implementation
- Modify: `apps/web/components/home/story-grid.tsx`
  - Turn repeated grid cards into stronger section-band modules
- Modify: `apps/web/components/home/intelligence-rail.tsx`
  - Rework into active latest/live desk companion
- Modify: `apps/web/components/home/developing-stories.tsx`
  - Rebuild lower live/current feed

### Article presentation

- Modify: `apps/web/app/articles/[slug]/page.tsx`
  - Recompose page structure for the new article shell
- Modify: `apps/web/components/article/article-header.tsx`
  - Replace current stage treatment with more practical international-news hero frame
- Modify: `apps/web/components/article/article-body.tsx`
  - Tighten reading surface hierarchy
- Modify: `apps/web/components/article/facts-section.tsx`
  - Adjust support module structure/styling hooks
- Modify: `apps/web/components/article/analysis-section.tsx`
  - Adjust support module structure/styling hooks
- Modify: `apps/web/components/article/sources-section.tsx`
  - Adjust support module structure/styling hooks

### Tests

- Modify: `apps/web/tests/home-page.test.mjs`
- Modify: `apps/web/tests/article-page.test.mjs`

---

## Chunk 1: Lock the new public contract

### Task 1: Rewrite homepage rendering expectations

**Files:**
- Modify: `apps/web/tests/home-page.test.mjs`

- [ ] **Step 1: Write the failing test**

Update homepage expectations to require new hooks such as:

- `cw-zdf-topbar`
- `cw-zdf-nav`
- `cw-dw-lead-cluster`
- `cw-latest-desk`
- `cw-top-band`
- `cw-analysis-zone`
- `cw-section-band`
- `cw-current-feed`

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --dir apps/web test`
Expected: homepage test fails because old hooks are no longer correct

- [ ] **Step 3: Commit**

```bash
git add apps/web/tests/home-page.test.mjs
git commit -m "test: lock dw zdf public homepage contract"
```

### Task 2: Rewrite article rendering expectations

**Files:**
- Modify: `apps/web/tests/article-page.test.mjs`

- [ ] **Step 1: Write the failing test**

Update article expectations to require new hooks such as:

- `cw-article-hero-frame`
- `cw-article-reading-shell`
- `cw-context-column`
- `cw-support-zone`

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --dir apps/web test`
Expected: article page test fails against current implementation

- [ ] **Step 3: Commit**

```bash
git add apps/web/tests/article-page.test.mjs
git commit -m "test: lock dw zdf article contract"
```

## Chunk 2: Rebuild header and homepage

### Task 3: Rebuild the public header

**Files:**
- Modify: `apps/web/components/public/public-header.tsx`
- Modify: `apps/web/app/globals.css`

- [ ] **Step 1: Implement utility row and nav row**

Create a compact header with:

- top utility line
- strong brand anchor
- clearer section navigation
- utility actions

- [ ] **Step 2: Add required CSS hooks**

Ensure markup includes:

- `cw-zdf-topbar`
- `cw-zdf-nav`

- [ ] **Step 3: Run web tests**

Run: `pnpm --dir apps/web test`
Expected: header-related expectations still fail only on missing homepage/article structure

- [ ] **Step 4: Commit**

```bash
git add apps/web/components/public/public-header.tsx apps/web/app/globals.css
git commit -m "feat: rebuild public header with zdf style structure"
```

### Task 4: Recompose homepage around DW-style density

**Files:**
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/components/home/hero-story.tsx`
- Modify: `apps/web/components/home/story-grid.tsx`
- Modify: `apps/web/components/home/intelligence-rail.tsx`
- Modify: `apps/web/components/home/developing-stories.tsx`
- Modify: `apps/web/app/globals.css`

- [ ] **Step 1: Implement lead cluster**

Add homepage lead area with:

- `cw-dw-lead-cluster`
- `cw-latest-desk`

- [ ] **Step 2: Implement top secondary band**

Add:

- `cw-top-band`
- larger secondary story surfaces

- [ ] **Step 3: Implement analysis and section bands**

Add:

- `cw-analysis-zone`
- repeated `cw-section-band` blocks for key categories

- [ ] **Step 4: Implement lower current feed**

Add:

- `cw-current-feed`

- [ ] **Step 5: Run web tests**

Run: `pnpm --dir apps/web test`
Expected: homepage tests pass, article tests may still fail

- [ ] **Step 6: Commit**

```bash
git add apps/web/app/page.tsx apps/web/components/home/hero-story.tsx apps/web/components/home/story-grid.tsx apps/web/components/home/intelligence-rail.tsx apps/web/components/home/developing-stories.tsx apps/web/app/globals.css
git commit -m "feat: rebuild homepage with dw style editorial density"
```

## Chunk 3: Rebuild article presentation

### Task 5: Recompose article page shell

**Files:**
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Modify: `apps/web/components/article/article-header.tsx`
- Modify: `apps/web/components/article/article-body.tsx`
- Modify: `apps/web/components/article/facts-section.tsx`
- Modify: `apps/web/components/article/analysis-section.tsx`
- Modify: `apps/web/components/article/sources-section.tsx`
- Modify: `apps/web/app/globals.css`

- [ ] **Step 1: Implement new article hero frame**

Add:

- `cw-article-hero-frame`

- [ ] **Step 2: Implement reading shell**

Add:

- `cw-article-reading-shell`
- `cw-context-column`
- `cw-support-zone`

- [ ] **Step 3: Integrate support modules**

Ensure facts, analysis, and sources feel like the same page system

- [ ] **Step 4: Run web tests**

Run: `pnpm --dir apps/web test`
Expected: homepage and article tests pass

- [ ] **Step 5: Commit**

```bash
git add apps/web/app/articles/[slug]/page.tsx apps/web/components/article/article-header.tsx apps/web/components/article/article-body.tsx apps/web/components/article/facts-section.tsx apps/web/components/article/analysis-section.tsx apps/web/components/article/sources-section.tsx apps/web/app/globals.css
git commit -m "feat: rebuild article shell for dw zdf public reset"
```

## Chunk 4: Verify, deploy, and update docs

### Task 6: Verify local rendering

**Files:**
- No file changes required

- [ ] **Step 1: Run web test suite**

Run: `pnpm --dir apps/web test`
Expected: all tests pass

- [ ] **Step 2: Commit if needed**

No commit if unchanged

### Task 7: Deploy staging and verify live markup

**Files:**
- No file changes required

- [ ] **Step 1: Push branch to master according to current workflow**

Use the established merge/push flow once implementation is complete.

- [ ] **Step 2: Redeploy VPS**

Use the existing deployment command/runbook for `213.202.216.222`.

- [ ] **Step 3: Verify live homepage**

Check for:

- `cw-zdf-topbar`
- `cw-dw-lead-cluster`
- `cw-current-feed`

- [ ] **Step 4: Verify live article page**

Check for:

- `cw-article-hero-frame`
- `cw-article-reading-shell`

- [ ] **Step 5: Commit docs update if any**

```bash
git add docs/runbooks/2026-04-11-project-checkpoint.md
git commit -m "docs: update checkpoint for dw zdf public reset"
```

Plan complete and saved to `docs/superpowers/plans/2026-04-12-corewire-public-dw-zdf-reset-implementation.md`. Ready to execute?
