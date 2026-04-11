# Owner Editor and Admin Completion Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current article manager inside `/admin` into a real single-page owner editor for creating, editing, saving, and publishing manual drafts.

**Architecture:** Reuse the existing manual draft model and current admin content endpoints instead of adding a second CMS path. Extend the backend with editor-ready fetch and action endpoints, then replace the passive article manager UI with a two-column inventory + editor workspace inside the existing `/admin` route.

**Tech Stack:** FastAPI, existing admin services, PostgreSQL-backed draft models, Next.js App Router, React server/client components, pytest, Node test runner

---

## File Structure

Create or extend these areas:

- `apps/api/core/admin/content.py` for owner draft CRUD and owner publish/archive actions
- `apps/api/core/admin/router.py` for owner admin content routes
- `apps/api/tests/*` for owner editor backend regression coverage
- `apps/web/components/admin/article-manager.tsx` for the inventory + editor workspace shell
- `apps/web/components/admin/*` for focused editor subcomponents
- `apps/web/lib/api.ts` and `apps/web/lib/types.ts` for owner editor client contracts
- `apps/web/tests/*` for source-level admin editor coverage

## Chunk 1: Backend Editor Contract

### Task 1: Add editor-ready draft fetch endpoint

**Files:**
- Modify: `apps/api/core/admin/content.py`
- Modify: `apps/api/core/admin/router.py`
- Create: `apps/api/tests/test_admin_content.py`

- [ ] **Step 1: Write the failing draft-detail test**

```python
def test_owner_can_fetch_one_manual_draft_in_editor_shape():
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_admin_content.py -k editor_shape -v`
Expected: FAIL because a single draft fetch endpoint does not exist.

- [ ] **Step 3: Write minimal implementation**

Add:

- `GET /api/admin/content/drafts/{draft_id}`

Return:

- `id`
- `headline`
- `dek`
- `slug`
- `tags`
- `body`
- `status`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_admin_content.py -k editor_shape -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/admin/content.py apps/api/core/admin/router.py apps/api/tests/test_admin_content.py
git commit -m "feat: add owner draft editor fetch endpoint"
```

### Task 2: Add owner publish and archive actions for manual drafts

**Files:**
- Modify: `apps/api/core/admin/content.py`
- Modify: `apps/api/core/admin/router.py`
- Modify: `apps/api/tests/test_admin_content.py`

- [ ] **Step 1: Write the failing action tests**

```python
def test_owner_can_publish_manual_draft_from_editor():
    ...

def test_owner_can_archive_manual_draft_from_editor():
    ...
```

- [ ] **Step 2: Run test to verify they fail**

Run: `pytest apps/api/tests/test_admin_content.py -k "publish_manual_draft or archive_manual_draft" -v`
Expected: FAIL because manual editor actions do not exist.

- [ ] **Step 3: Write minimal implementation**

Add owner actions:

- `POST /api/admin/content/drafts/{draft_id}/publish`
- `POST /api/admin/content/drafts/{draft_id}/archive`

Use the existing draft model and existing publish semantics where possible.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_admin_content.py -k "publish_manual_draft or archive_manual_draft" -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/admin/content.py apps/api/core/admin/router.py apps/api/tests/test_admin_content.py
git commit -m "feat: add owner manual draft actions"
```

## Chunk 2: Single-Page Owner Editor UI

### Task 3: Replace passive article manager with inventory + editor workspace

**Files:**
- Modify: `apps/web/components/admin/article-manager.tsx`
- Create: `apps/web/components/admin/article-editor.tsx`
- Create: `apps/web/tests/article-editor.test.mjs`
- Modify: `apps/web/tests/article-manager.test.mjs`

- [ ] **Step 1: Write the failing UI tests**

```javascript
test("renders single-page owner editor with inventory and form fields", () => {
  ...
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --dir apps/web test -- article-manager article-editor`
Expected: FAIL because the article manager is still passive inventory only.

- [ ] **Step 3: Write minimal implementation**

Render:

- left inventory
- right editor
- fields for headline, dek, slug, tags, body
- action buttons for save and publish

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --dir apps/web test -- article-manager article-editor`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web/components/admin/article-manager.tsx apps/web/components/admin/article-editor.tsx apps/web/tests/article-manager.test.mjs apps/web/tests/article-editor.test.mjs
git commit -m "feat: add single-page owner editor workspace"
```

### Task 4: Wire admin API client and page state for the editor workflow

**Files:**
- Modify: `apps/web/lib/api.ts`
- Modify: `apps/web/lib/types.ts`
- Modify: `apps/web/app/admin/page.tsx`
- Modify: `apps/web/tests/admin-shell.test.mjs`

- [ ] **Step 1: Write the failing API wiring tests**

```javascript
test("admin page wires draft editor client calls and owner actions", () => {
  ...
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pnpm --dir apps/web test -- admin-shell`
Expected: FAIL because the page does not wire editor-specific client calls.

- [ ] **Step 3: Write minimal implementation**

Add client helpers for:

- fetch draft detail
- create draft
- update draft
- publish draft
- archive draft

Wire the admin page to the new editor workspace contract.

- [ ] **Step 4: Run test to verify it passes**

Run: `pnpm --dir apps/web test -- admin-shell`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/web/lib/api.ts apps/web/lib/types.ts apps/web/app/admin/page.tsx apps/web/tests/admin-shell.test.mjs
git commit -m "feat: wire owner editor workflow into admin page"
```

## Chunk 3: Verification and Handoff

### Task 5: Verify owner editor end-to-end contract

**Files:**
- Modify: `apps/api/tests/test_admin_content.py`
- Modify: `apps/web/tests/article-manager.test.mjs`
- Modify: `docs/runbooks/2026-04-11-project-checkpoint.md`

- [ ] **Step 1: Add final verification coverage**

Add or extend tests to confirm:

- create draft
- fetch draft
- update draft
- publish draft
- archive draft
- admin page references the single-page editor workspace

- [ ] **Step 2: Run backend verification**

Run: `pytest apps/api/tests/test_admin_content.py apps/api/tests/test_article_actions.py -q`
Expected: PASS.

- [ ] **Step 3: Run frontend verification**

Run: `pnpm --dir apps/web test -- admin-shell article-manager article-editor`
Expected: PASS.

- [ ] **Step 4: Update project checkpoint**

Record that the owner admin now has a real single-page editor and note that the next admin phase is stronger programming save/apply workflow.

- [ ] **Step 5: Commit**

```bash
git add apps/api/tests/test_admin_content.py apps/web/tests/article-manager.test.mjs apps/web/tests/article-editor.test.mjs docs/runbooks/2026-04-11-project-checkpoint.md
git commit -m "docs: record owner editor admin completion"
```

## Verification Checklist

- `pytest apps/api/tests/test_admin_content.py apps/api/tests/test_article_actions.py -q`
- `pnpm --dir apps/web test -- admin-shell article-manager article-editor`

## Handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-11-owner-editor-admin-completion-implementation.md`. Ready to execute?
