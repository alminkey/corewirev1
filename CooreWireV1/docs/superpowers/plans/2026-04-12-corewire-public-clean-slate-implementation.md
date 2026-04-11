# CoreWire Public Clean-Slate Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current public frontend with a genuinely new luxury digital front page and article experience while keeping existing routes and backend data unchanged.

**Architecture:** Treat the current public layout as disposable. Rebuild homepage and article presentation around a new lead-first composition, new supporting modules, and a new visual system, but keep the current fetch layer, slugs, and public routes intact. Admin is out of scope except for regression safety.

**Tech Stack:** Next.js App Router, React server components, CSS in `apps/web/app/globals.css`, existing homepage/article API calls, current public components.

---

## File Structure

**Modify heavily:**
- `apps/web/app/page.tsx`
- `apps/web/app/articles/[slug]/page.tsx`
- `apps/web/app/globals.css`
- `apps/web/components/public/public-header.tsx`
- `apps/web/components/home/hero-story.tsx`
- `apps/web/components/home/story-grid.tsx`
- `apps/web/components/home/intelligence-rail.tsx`
- `apps/web/components/home/developing-stories.tsx`
- `apps/web/components/article/article-header.tsx`
- `apps/web/components/article/article-body.tsx`
- article support modules as needed

**Leave functionally intact unless required by tests:**
- `apps/web/app/admin/page.tsx`
- admin components

**Tests:**
- `apps/web/tests/homepage.test.mjs`
- `apps/web/tests/article-page.test.mjs`
- `apps/web/tests/admin-shell.test.mjs`

---

## Chunk 1: Lock the New Public Contract

### Task 1: Write failing tests for the clean-slate public shell

**Files:**
- Modify: `apps/web/tests/homepage.test.mjs`
- Modify: `apps/web/tests/article-page.test.mjs`
- Regression check: `apps/web/tests/admin-shell.test.mjs`

- [ ] **Step 1: Expand homepage test to require clean-slate hooks**

Add expectations for hooks that the current layout does not satisfy, such as:

```js
assert.match(pageSource, /cw-lead-stage/);
assert.match(heroSource, /cw-lead-frame/);
assert.match(gridSource, /cw-support-strip/);
assert.match(globalStyles, /\.cw-lead-stage/);
```

- [ ] **Step 2: Expand article test to require new reading hooks**

Add expectations such as:

```js
assert.match(pageSource, /cw-feature-reading/);
assert.match(headerSource, /cw-article-stage/);
assert.match(bodySource, /cw-reading-column/);
```

- [ ] **Step 3: Run the full web suite to confirm failure**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: FAIL on new homepage/article hooks.

- [ ] **Step 4: Commit the failing-contract tests**

```powershell
git -C CooreWireV1 add apps/web/tests/homepage.test.mjs apps/web/tests/article-page.test.mjs
git -C CooreWireV1 commit -m "test: lock clean-slate public frontend contract"
```

---

## Chunk 2: Rebuild the Homepage From Scratch

### Task 2: Replace the public homepage composition

**Files:**
- Modify: `apps/web/app/page.tsx`
- Modify: `apps/web/components/public/public-header.tsx`
- Modify: `apps/web/components/home/hero-story.tsx`
- Modify: `apps/web/components/home/story-grid.tsx`
- Modify: `apps/web/components/home/intelligence-rail.tsx`
- Modify: `apps/web/components/home/developing-stories.tsx`
- Modify: `apps/web/app/globals.css`

- [ ] **Step 1: Replace homepage shell markup with new zones**

Move to:

- minimal top frame
- giant lead stage
- supporting story strip
- feature block
- curated lower feed

- [ ] **Step 2: Remove legacy homepage assumptions**

Explicitly delete or stop using the old:

- current hero composition
- current right-rail logic if it still reads like the old product
- dense equal-weight card rhythm

- [ ] **Step 3: Implement the new lead story stage**

Build one dominant visual stage with:

- one large image
- one giant headline
- dek
- metadata
- CTA

- [ ] **Step 4: Implement supporting story strip**

Use fewer, stronger supporting modules instead of the old grid rhythm.

- [ ] **Step 5: Implement feature block and lower feed**

Keep the page curated and spacious.

- [ ] **Step 6: Add subtle motion only where it helps**

Examples:

- staged reveal
- image hover lift
- CTA transitions

- [ ] **Step 7: Run the web suite and confirm pass**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: PASS

- [ ] **Step 8: Commit homepage rewrite**

```powershell
git -C CooreWireV1 add apps/web/app/page.tsx apps/web/components/public/public-header.tsx apps/web/components/home/hero-story.tsx apps/web/components/home/story-grid.tsx apps/web/components/home/intelligence-rail.tsx apps/web/components/home/developing-stories.tsx apps/web/app/globals.css
git -C CooreWireV1 commit -m "feat: rebuild public homepage as clean-slate lead-first layout"
```

---

## Chunk 3: Rebuild Article Pages as Premium Feature Reading

### Task 3: Replace the article presentation shell

**Files:**
- Modify: `apps/web/app/articles/[slug]/page.tsx`
- Modify: `apps/web/components/article/article-header.tsx`
- Modify: `apps/web/components/article/article-body.tsx`
- Modify: `apps/web/components/article/facts-section.tsx`
- Modify: `apps/web/components/article/analysis-section.tsx`
- Modify: `apps/web/components/article/sources-section.tsx`
- Modify: `apps/web/app/globals.css`

- [ ] **Step 1: Replace article opening with a feature-stage layout**

The article top should include:

- visual moment
- stronger headline placement
- cleaner metadata layout

- [ ] **Step 2: Rebuild the reading body**

The reading area should become:

- more spacious
- more luxurious
- less modular in feel

- [ ] **Step 3: Reframe support modules**

Facts, analysis, disagreements, and sources should feel integrated but secondary.

- [ ] **Step 4: Run the web suite and confirm pass**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: PASS

- [ ] **Step 5: Commit article rewrite**

```powershell
git -C CooreWireV1 add apps/web/app/articles/[slug]/page.tsx apps/web/components/article/article-header.tsx apps/web/components/article/article-body.tsx apps/web/components/article/facts-section.tsx apps/web/components/article/analysis-section.tsx apps/web/components/article/sources-section.tsx apps/web/app/globals.css
git -C CooreWireV1 commit -m "feat: rebuild article pages as premium feature surfaces"
```

---

## Chunk 4: Verification and Staging Rollout

### Task 4: Verify that the product is truly different, then deploy

**Files:**
- Optionally modify: `docs/runbooks/2026-04-11-project-checkpoint.md`

- [ ] **Step 1: Run the full web suite**

Run:

```powershell
pnpm --dir apps/web test
```

Expected: PASS

- [ ] **Step 2: Manual browser verification**

Check:

- `/`
- `/articles/[slug]`
- `/admin` only for regression

Look for:

- totally new public composition
- dominant lead story
- obvious break from the old demo structure

- [ ] **Step 3: Push and redeploy staging**

Use the existing Webtropia runbook:

```bash
git push origin master
ssh -i ~/.ssh/corewire_staging_nopass root@213.202.216.222
cd /opt/corewire/app/CooreWireV1
git pull origin master
bash scripts/deploy-webtropia.sh
```

- [ ] **Step 4: Smoke check live pages**

Confirm:

- `/` returns `200`
- article page returns `200`
- live HTML includes the new clean-slate hooks

- [ ] **Step 5: Update checkpoint docs if needed**

Mark earlier public redesign assumptions as superseded.

---

Plan complete and saved to `docs/superpowers/plans/2026-04-12-corewire-public-clean-slate-implementation.md`. Ready to execute?
