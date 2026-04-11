# CoreWire Media-Tech Reset Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current public/admin redesign direction with a more radical modern media-tech platform identity while keeping the existing data flow and admin capabilities intact.

**Architecture:** Treat this as a visual reset, not a polish pass. Rebuild the shared token system, then reshape homepage, article pages, and admin shell around a product-grade UI language. Reuse the current routes and backend wiring, but do not stay constrained by the previous editorial/newspaper layout assumptions.

**Tech Stack:** Next.js App Router, React server components, CSS in `apps/web/app/globals.css`, existing CoreWire components and server actions, existing homepage/article/admin routes.

---

## File Structure

**Modify heavily:**
- `apps/web/app/globals.css`
- `apps/web/app/page.tsx`
- `apps/web/app/articles/[slug]/page.tsx`
- `apps/web/app/admin/page.tsx`
- `apps/web/components/public/public-header.tsx`
- `apps/web/components/home/hero-story.tsx`
- `apps/web/components/home/story-grid.tsx`
- `apps/web/components/home/intelligence-rail.tsx`
- `apps/web/components/home/developing-stories.tsx`
- `apps/web/components/article/article-header.tsx`
- `apps/web/components/article/article-body.tsx`
- `apps/web/components/admin/admin-shell.tsx`
- `apps/web/components/admin/article-manager.tsx`
- `apps/web/components/admin/review-queue.tsx`
- `apps/web/components/admin/programming-controls.tsx`
- `apps/web/components/admin/analytics-dashboard.tsx`
- `apps/web/components/admin/autonomy-controls.tsx`

**Test:**
- `apps/web/tests/homepage.test.mjs`
- `apps/web/tests/article-page.test.mjs`
- `apps/web/tests/admin-shell.test.mjs`
- `apps/web/tests/article-manager.test.mjs`

---

## Chunk 1: Replace the Shared Visual System

### Task 1: Lock failing tests for the new media-tech shell hooks

**Files:**
- Modify: `apps/web/tests/homepage.test.mjs`
- Modify: `apps/web/tests/article-page.test.mjs`
- Modify: `apps/web/tests/admin-shell.test.mjs`

- [ ] **Step 1: Write failing expectations for the new product-style hooks**

Add checks for hooks such as:

```js
assert.match(source, /cw-platform-hero/);
assert.match(source, /cw-signal-chip/);
assert.match(source, /cw-control-plane/);
assert.match(source, /cw-module-card/);
```

- [ ] **Step 2: Run the web tests to confirm failure**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: FAIL because the new hooks do not exist yet.

- [ ] **Step 3: Replace token foundations in `globals.css`**

Implement:

- cooler base palette
- stronger contrast surfaces
- modern sans-led typography
- product-style shadows/radii
- chips/pills/button styles
- module/card primitives

- [ ] **Step 4: Add minimal wrapper hooks into existing admin/public/article shells**

- [ ] **Step 5: Run the web tests and confirm pass**

- [ ] **Step 6: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/globals.css apps/web/tests/homepage.test.mjs apps/web/tests/article-page.test.mjs apps/web/tests/admin-shell.test.mjs apps/web/app/page.tsx apps/web/app/articles/[slug]/page.tsx apps/web/app/admin/page.tsx
git -C CooreWireV1 commit -m "feat: add media-tech design foundation"
```

---

## Chunk 2: Homepage Platform Reset

### Task 2: Rebuild homepage around a platform hero and signal modules

**Files:**
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/components/public/public-header.tsx`
- Modify: `apps/web/components/home/hero-story.tsx`
- Modify: `apps/web/components/home/story-grid.tsx`
- Modify: `apps/web/components/home/intelligence-rail.tsx`
- Modify: `apps/web/components/home/developing-stories.tsx`
- Modify: `apps/web/tests/homepage.test.mjs`

- [ ] **Step 1: Expand failing tests for platform hero and module card structure**

Cover:

- stronger product top bar
- platform hero with CTA cluster
- signal/live desk modules
- modular story cards

- [ ] **Step 2: Run homepage tests to confirm failure**

- [ ] **Step 3: Implement homepage reset**

Target outcomes:

- hero feels like a product surface, not a news-paper lead
- right rail becomes signal/live desk
- cards feel like modules, not paper boxes
- optional video block integrates naturally

- [ ] **Step 4: Add subtle product motion**

- [ ] **Step 5: Run full web tests and confirm pass**

- [ ] **Step 6: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/page.tsx apps/web/components/public/public-header.tsx apps/web/components/home/hero-story.tsx apps/web/components/home/story-grid.tsx apps/web/components/home/intelligence-rail.tsx apps/web/components/home/developing-stories.tsx apps/web/app/globals.css apps/web/tests/homepage.test.mjs
git -C CooreWireV1 commit -m "feat: reset homepage to media-tech platform layout"
```

---

## Chunk 3: Article Page Platform Reading Experience

### Task 3: Shift article pages from editorial paper feel to platform reading feel

**Files:**
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Modify: `apps/web/components/article/article-header.tsx`
- Modify: `apps/web/components/article/article-body.tsx`
- Modify: article support components as needed
- Modify: `apps/web/tests/article-page.test.mjs`

- [ ] **Step 1: Write failing tests for the new reading surface hooks**

Cover:

- stronger headline module
- cleaner prose container
- integrated facts/sources modules

- [ ] **Step 2: Run article tests to confirm failure**

- [ ] **Step 3: Implement article reset**

Target outcomes:

- more product-like article framing
- less classic editorial styling
- cleaner reading width and spacing
- better hierarchy between body and support modules

- [ ] **Step 4: Run full web tests and confirm pass**

- [ ] **Step 5: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/articles/[slug]/page.tsx apps/web/components/article/article-header.tsx apps/web/components/article/article-body.tsx apps/web/app/globals.css apps/web/tests/article-page.test.mjs
git -C CooreWireV1 commit -m "feat: reset article pages to platform reading layout"
```

---

## Chunk 4: Admin Control Plane Reset

### Task 4: Rebuild admin as a cleaner control plane

**Files:**
- Modify: `apps/web/app/admin/page.tsx`
- Modify: `apps/web/components/admin/admin-shell.tsx`
- Modify: `apps/web/components/admin/article-manager.tsx`
- Modify: `apps/web/components/admin/review-queue.tsx`
- Modify: `apps/web/components/admin/programming-controls.tsx`
- Modify: `apps/web/components/admin/analytics-dashboard.tsx`
- Modify: `apps/web/components/admin/autonomy-controls.tsx`
- Modify: `apps/web/tests/admin-shell.test.mjs`
- Modify: `apps/web/tests/article-manager.test.mjs`

- [ ] **Step 1: Write failing tests for control-plane hooks**

Cover:

- darker/stronger nav rail
- system chip bar
- clearer workspace modules
- editor as product workspace

- [ ] **Step 2: Run admin tests to confirm failure**

- [ ] **Step 3: Implement admin reset**

Target outcomes:

- looks like a product dashboard
- faster scan hierarchy
- reduced visual softness/blog feel
- stronger separation of queue/editor/programming

- [ ] **Step 4: Run full web tests and confirm pass**

- [ ] **Step 5: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/admin/page.tsx apps/web/components/admin/admin-shell.tsx apps/web/components/admin/article-manager.tsx apps/web/components/admin/review-queue.tsx apps/web/components/admin/programming-controls.tsx apps/web/components/admin/analytics-dashboard.tsx apps/web/components/admin/autonomy-controls.tsx apps/web/app/globals.css apps/web/tests/admin-shell.test.mjs apps/web/tests/article-manager.test.mjs
git -C CooreWireV1 commit -m "feat: reset admin to media-tech control plane"
```

---

## Chunk 5: Verification, Deploy, and Baseline Update

### Task 5: Verify the reset and make it the new baseline

**Files:**
- Possibly modify: `docs/runbooks/2026-04-10-project-checkpoint.md`

- [ ] **Step 1: Run the full web suite**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: PASS

- [ ] **Step 2: Manually inspect**

Check:

- `/`
- `/admin`
- `/articles/[slug]`
- `/admin/review/[id]`

Look for:

- real visual break from current design
- improved product feeling
- readability
- coherent identity

- [ ] **Step 3: Commit polish fixes if needed**

- [ ] **Step 4: Push and redeploy staging**

- [ ] **Step 5: Update checkpoint docs to mark the older redesign as superseded**

---

Plan complete and saved to `docs/superpowers/plans/2026-04-12-corewire-media-tech-reset-implementation.md`. Ready to execute?
