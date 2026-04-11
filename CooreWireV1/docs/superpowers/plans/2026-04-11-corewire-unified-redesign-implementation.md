# CoreWire Unified Redesign Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the public frontend and owner admin so CoreWire has one modern visual system, a real admin app shell, and a clearer premium editorial public experience.

**Architecture:** Keep the current routing and data flow, but replace the visual foundation and page composition. Build shared design tokens and reusable primitives first, then reshape admin into an app shell and public pages into a lighter editorial layout. Preserve current functionality while changing hierarchy, spacing, typography, and interaction patterns.

**Tech Stack:** Next.js App Router, React server components, CSS in `apps/web/app/globals.css`, existing CoreWire components, existing server actions and API helpers.

---

## File Structure

**Modify:**
- `apps/web/app/globals.css`
  - replace retro-heavy tokens with new shared visual system
  - add shared typography, panel, button, form, motion, and shell primitives
- `apps/web/app/page.tsx`
  - reshape homepage composition around the new editorial hierarchy
- `apps/web/app/articles/[slug]/page.tsx`
  - align article shell with the new frontend system
- `apps/web/app/admin/page.tsx`
  - convert the admin page from stacked sections to a shell/workspace layout
- `apps/web/components/public/public-header.tsx`
  - modernize public header and meta bar
- `apps/web/components/home/hero-story.tsx`
  - support image-led hero and stronger CTA hierarchy
- `apps/web/components/home/story-grid.tsx`
  - shift from sparse text cards to stronger media-led cards
- `apps/web/components/home/intelligence-rail.tsx`
  - simplify right rail scanning and hierarchy
- `apps/web/components/home/developing-stories.tsx`
  - align supporting lists with the new public system
- `apps/web/components/article/article-header.tsx`
  - improve article title, dek, meta, and opening rhythm
- `apps/web/components/admin/admin-shell.tsx`
  - convert overview hero into admin shell header/sidebar primitives
- `apps/web/components/admin/article-manager.tsx`
  - fit into workspace layout with cleaner inventory/editor proportions
- `apps/web/components/admin/programming-controls.tsx`
  - convert to dashboard-style operational panel
- `apps/web/components/admin/review-queue.tsx`
  - convert to inbox/task panel styling
- `apps/web/components/admin/analytics-dashboard.tsx`
  - restyle as stats/summary cards instead of article-like sections
- `apps/web/components/admin/autonomy-controls.tsx`
  - align controls with app shell and card system

**Test:**
- `apps/web/tests/admin-shell.test.mjs`
- `apps/web/tests/article-manager.test.mjs`
- `apps/web/tests/review-queue.test.mjs`
- `apps/web/tests/article-page.test.mjs`
- add one new public-home layout regression test if needed

---

## Chunk 1: Shared Visual Foundation

### Task 1: Add failing regression coverage for new shell class hooks

**Files:**
- Modify: `apps/web/tests/admin-shell.test.mjs`
- Modify: `apps/web/tests/article-page.test.mjs`

- [ ] **Step 1: Write the failing tests**

Add expectations for new shared hooks/classes such as:

```js
assert.match(html, /cw-surface/);
assert.match(html, /cw-app-shell/);
assert.match(html, /cw-editorial-shell/);
```

- [ ] **Step 2: Run targeted tests to verify they fail**

Run:

```powershell
pnpm --dir apps/web test -- --runInBand admin-shell article-page
```

Expected: FAIL because new classes are not rendered yet.

- [ ] **Step 3: Add shared layout and token classes to CSS**

Implement in `apps/web/app/globals.css`:

- warm light tokens
- serif + sans split
- shared panel/card/button/input styles
- subtle motion tokens
- app shell primitives
- editorial shell primitives

- [ ] **Step 4: Add minimal class hooks in existing layouts/components**

Add the new wrapper classes to the admin and article page/component shells without full restructuring yet.

- [ ] **Step 5: Run targeted tests to verify they pass**

Run:

```powershell
pnpm --dir apps/web test -- --runInBand admin-shell article-page
```

Expected: PASS

- [ ] **Step 6: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/globals.css apps/web/tests/admin-shell.test.mjs apps/web/tests/article-page.test.mjs apps/web/app/admin/page.tsx apps/web/app/articles/[slug]/page.tsx
git -C CooreWireV1 commit -m "feat: add unified redesign foundation"
```

---

## Chunk 2: Admin App Shell

### Task 2: Convert `/admin` from stacked page to shell layout

**Files:**
- Modify: `apps/web/app/admin/page.tsx`
- Modify: `apps/web/components/admin/admin-shell.tsx`
- Modify: `apps/web/components/admin/article-manager.tsx`
- Modify: `apps/web/components/admin/programming-controls.tsx`
- Modify: `apps/web/components/admin/review-queue.tsx`
- Modify: `apps/web/components/admin/analytics-dashboard.tsx`
- Modify: `apps/web/components/admin/autonomy-controls.tsx`
- Test: `apps/web/tests/admin-shell.test.mjs`
- Test: `apps/web/tests/article-manager.test.mjs`

- [ ] **Step 1: Write the failing admin shell and workspace tests**

Add checks for:

- sidebar navigation
- top status bar
- main workspace container
- reduced duplicated published summary rendering

Example:

```js
assert.match(html, /Owner Workspace/);
assert.match(html, /cw-admin-sidebar/);
assert.match(html, /cw-admin-main/);
```

- [ ] **Step 2: Run targeted tests to verify failure**

Run:

```powershell
pnpm --dir apps/web test -- --runInBand admin-shell article-manager
```

Expected: FAIL because the new admin shell markup does not exist yet.

- [ ] **Step 3: Implement the app shell layout**

Reshape the admin into:

- left persistent sidebar
- top utility bar
- stat cards row
- main content panels

Keep all existing functionality and data flow intact.

- [ ] **Step 4: Refit the draft editor into the workspace**

Ensure `ArticleManager` becomes:

- inventory panel
- focused editor panel
- cleaner published panel

without route changes.

- [ ] **Step 5: Run targeted tests to verify pass**

Run:

```powershell
pnpm --dir apps/web test -- --runInBand admin-shell article-manager
```

Expected: PASS

- [ ] **Step 6: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/admin/page.tsx apps/web/components/admin/admin-shell.tsx apps/web/components/admin/article-manager.tsx apps/web/components/admin/programming-controls.tsx apps/web/components/admin/review-queue.tsx apps/web/components/admin/analytics-dashboard.tsx apps/web/components/admin/autonomy-controls.tsx apps/web/tests/admin-shell.test.mjs apps/web/tests/article-manager.test.mjs apps/web/app/globals.css
git -C CooreWireV1 commit -m "feat: redesign admin as owner app shell"
```

---

## Chunk 3: Public Homepage Redesign

### Task 3: Reshape homepage into premium editorial layout

**Files:**
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/components/public/public-header.tsx`
- Modify: `apps/web/components/home/hero-story.tsx`
- Modify: `apps/web/components/home/story-grid.tsx`
- Modify: `apps/web/components/home/intelligence-rail.tsx`
- Modify: `apps/web/components/home/developing-stories.tsx`
- Test: add or modify public homepage test if present

- [ ] **Step 1: Write failing homepage structure tests**

Cover:

- upgraded public header
- hero media region
- cleaner rail container
- story card media/thumb support

Example:

```js
assert.match(html, /cw-home-hero-media/);
assert.match(html, /cw-public-header-bar/);
assert.match(html, /cw-story-card-media/);
```

- [ ] **Step 2: Run the targeted tests to verify failure**

Run the homepage-related web tests.

Expected: FAIL because new hooks are not present.

- [ ] **Step 3: Implement public header and homepage composition**

Change layout to:

- cleaner top bar
- stronger hero
- improved rail
- media-led card grid
- placeholder video feature block if supported cleanly by existing data shape

- [ ] **Step 4: Add subtle motion states**

Use CSS only for now:

- reveal on load
- hover lift
- better click affordance

- [ ] **Step 5: Run homepage tests and verify pass**

- [ ] **Step 6: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/page.tsx apps/web/components/public/public-header.tsx apps/web/components/home/hero-story.tsx apps/web/components/home/story-grid.tsx apps/web/components/home/intelligence-rail.tsx apps/web/components/home/developing-stories.tsx apps/web/app/globals.css
git -C CooreWireV1 commit -m "feat: redesign public homepage"
```

---

## Chunk 4: Article Page Readability Pass

### Task 4: Align article pages with the new editorial system

**Files:**
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Modify: `apps/web/components/article/article-header.tsx`
- Modify: article supporting components as needed
- Test: `apps/web/tests/article-page.test.mjs`

- [ ] **Step 1: Write failing article readability/layout tests**

Add checks for:

- editorial shell classes
- improved article header structure
- cleaner body container hooks

- [ ] **Step 2: Run targeted article tests and verify failure**

- [ ] **Step 3: Implement the article page redesign**

Focus on:

- title hierarchy
- dek rhythm
- readable body width
- cleaner section spacing
- reduced visual clutter

- [ ] **Step 4: Run targeted article tests and verify pass**

- [ ] **Step 5: Commit**

```powershell
git -C CooreWireV1 add apps/web/app/articles/[slug]/page.tsx apps/web/components/article/article-header.tsx apps/web/app/globals.css apps/web/tests/article-page.test.mjs
git -C CooreWireV1 commit -m "feat: redesign article presentation"
```

---

## Chunk 5: Full Web Regression and Staging Validation

### Task 5: Verify the redesign end to end

**Files:**
- No major code changes expected
- Update docs only if visual system references need refresh

- [ ] **Step 1: Run full web test suite**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: PASS

- [ ] **Step 2: Review core pages locally**

Check:

- `/`
- `/articles/[slug]`
- `/admin`
- `/admin/review/[id]`

Look for:

- broken hierarchy
- overflow
- dead links
- unreadable contrast
- mobile regressions

- [ ] **Step 3: Commit any polish fixes**

```powershell
git -C CooreWireV1 add apps/web
git -C CooreWireV1 commit -m "fix: polish unified redesign regressions"
```

- [ ] **Step 4: Push and redeploy staging**

Run the existing CoreWire staging deploy flow after verification.

- [ ] **Step 5: Update checkpoint docs if needed**

If the redesign becomes the new baseline, add it to:

- `docs/runbooks/2026-04-10-project-checkpoint.md`

---

Plan complete and saved to `docs/superpowers/plans/2026-04-11-corewire-unified-redesign-implementation.md`. Ready to execute?
