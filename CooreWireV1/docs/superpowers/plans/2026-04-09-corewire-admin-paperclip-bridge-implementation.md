# CoreWire Admin Closure and Paperclip Bridge V1 Implementation Plan

> **STATUS: COMPLETE** — All 8 tasks implemented, merged to `master` (`3c1b09a`), and verified on staging (`213.202.216.222`) on 2026-04-11. All bridge read endpoints and `import_external_draft` command confirmed live. Do not re-execute this plan.

> **For agentic workers:** This plan is fully executed. All checkboxes are checked. For current project state see `docs/runbooks/2026-04-11-project-checkpoint.md`.

**Goal:** Finish the practical owner-facing CoreWire site admin and add a narrow Paperclip Bridge V1 that can read CoreWire state and send authenticated commands into the system.

**Architecture:** Keep CoreWire admin as the canonical owner control plane inside the site. Extend the existing admin and operator layers rather than inventing a second control system. Add a narrow bridge surface for Paperclip using explicit read endpoints plus authenticated command endpoints, with optional correlation metadata preserved across the execution path.

**Tech Stack:** FastAPI, Python services, PostgreSQL, existing operator service layer, Next.js App Router, Node test runner, pytest, Docker Compose staging

---

## File Structure

Create or extend these areas:

- `apps/api/core/admin/*` for owner-facing site admin APIs
- `apps/api/core/operator/*` for Paperclip-facing bridge read and command APIs
- `apps/api/core/compliance/*` for article lifecycle actions already used by admin
- `apps/web/app/admin/*` for admin routes
- `apps/web/components/admin/*` for admin UI sections
- `apps/web/lib/*` for typed fetch helpers and bridge-aware shapes
- `docs/ops/*` for integration contract and Paperclip setup notes
- `apps/api/tests/*` and `apps/web/tests/*` for regression coverage

## Chunk 1: Site Admin Closure

### Task 1: Add a compact owner dashboard summary contract

**Files:**
- Modify: `apps/api/core/admin/router.py`
- Create: `apps/api/core/admin/overview.py`
- Modify: `apps/api/tests/test_admin_auth.py`
- Modify: `apps/api/tests/test_analytics_api.py`

- [x] **Step 1: Write the failing admin summary tests**

```python
def test_owner_can_fetch_dashboard_summary_with_health_queue_and_publish_stats():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_admin_auth.py apps/api/tests/test_analytics_api.py -k dashboard_summary -v`
Expected: FAIL because the compact owner summary contract does not exist.

- [x] **Step 3: Write minimal implementation**

Add an owner-only summary response that returns:

- health
- autonomy mode
- pause state
- queue counts
- published counts
- recent activity summary

- [x] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_admin_auth.py apps/api/tests/test_analytics_api.py -k dashboard_summary -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/api/core/admin/router.py apps/api/core/admin/overview.py apps/api/tests/test_admin_auth.py apps/api/tests/test_analytics_api.py
git commit -m "feat: add owner dashboard summary contract"
```

### Task 2: Add article management endpoints for manual owner operations

**Files:**
- Create: `apps/api/core/admin/content.py`
- Modify: `apps/api/core/admin/router.py`
- Modify: `apps/api/tests/test_article_actions.py`
- Create: `apps/api/tests/test_admin_content.py`

- [x] **Step 1: Write the failing admin content tests**

```python
def test_owner_can_list_create_and_update_manual_story_drafts():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_admin_content.py apps/api/tests/test_article_actions.py -v`
Expected: FAIL because admin content endpoints for manual story operations are incomplete.

- [x] **Step 3: Write minimal implementation**

Support owner actions for:

- listing drafts and published items
- creating a manual story draft
- updating headline, dek, body, slug, and tags
- handing off final publish/reject actions to existing lifecycle logic

- [x] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_admin_content.py apps/api/tests/test_article_actions.py -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/api/core/admin/content.py apps/api/core/admin/router.py apps/api/tests/test_admin_content.py apps/api/tests/test_article_actions.py
git commit -m "feat: add owner article management endpoints"
```

### Task 3: Add topic and interval policy controls

**Files:**
- Create: `apps/api/core/admin/programming.py`
- Modify: `apps/api/core/admin/settings.py`
- Create: `apps/api/tests/test_admin_programming.py`

- [x] **Step 1: Write the failing programming control tests**

```python
def test_owner_can_configure_topic_targets_and_generation_intervals():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_admin_programming.py apps/api/tests/test_autonomy_controls.py -v`
Expected: FAIL because programming controls do not exist.

- [x] **Step 3: Write minimal implementation**

Support owner-defined:

- topic targets
- recurring intervals
- basic scheduling windows
- enable/disable state for those rules

- [x] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_admin_programming.py apps/api/tests/test_autonomy_controls.py -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/api/core/admin/programming.py apps/api/core/admin/settings.py apps/api/tests/test_admin_programming.py apps/api/tests/test_autonomy_controls.py
git commit -m "feat: add owner programming controls"
```

### Task 4: Wire the missing admin UI sections

**Files:**
- Modify: `apps/web/app/admin/page.tsx`
- Modify: `apps/web/components/admin/admin-shell.tsx`
- Create: `apps/web/components/admin/article-manager.tsx`
- Create: `apps/web/components/admin/programming-controls.tsx`
- Modify: `apps/web/lib/api.ts`
- Modify: `apps/web/lib/types.ts`
- Create: `apps/web/tests/article-manager.test.mjs`
- Create: `apps/web/tests/programming-controls.test.mjs`
- Modify: `apps/web/tests/admin-shell.test.mjs`

- [x] **Step 1: Write the failing admin UI tests**

```javascript
test("admin shell renders article manager and programming controls", async () => {
  ...
});
```

- [x] **Step 2: Run test to verify it fails**

Run: `pnpm --dir apps/web test -- admin-shell article-manager programming-controls`
Expected: FAIL because the new admin surfaces are missing.

- [x] **Step 3: Write minimal implementation**

Render:

- owner summary
- article manager
- programming controls
- existing review and autonomy sections with the new data contract

- [x] **Step 4: Run test to verify it passes**

Run: `pnpm --dir apps/web test -- admin-shell article-manager programming-controls`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/web/app/admin/page.tsx apps/web/components/admin/admin-shell.tsx apps/web/components/admin/article-manager.tsx apps/web/components/admin/programming-controls.tsx apps/web/lib/api.ts apps/web/lib/types.ts apps/web/tests/article-manager.test.mjs apps/web/tests/programming-controls.test.mjs apps/web/tests/admin-shell.test.mjs
git commit -m "feat: close owner admin surface"
```

## Chunk 2: Paperclip Bridge V1

### Task 5: Add Paperclip bridge read endpoints

**Files:**
- Create: `apps/api/core/operator/bridge.py`
- Modify: `apps/api/core/operator/router.py`
- Modify: `apps/api/core/operator/schemas.py`
- Create: `apps/api/tests/test_operator_bridge.py`

- [x] **Step 1: Write the failing bridge read tests**

```python
def test_internal_bridge_can_read_corewire_status_summary():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_operator_bridge.py -k read -v`
Expected: FAIL because bridge read endpoints do not exist.

- [x] **Step 3: Write minimal implementation**

Add internal read endpoints for:

- status summary
- review queue summary
- published summary
- autonomy state

All protected by `x-internal-token`.

- [x] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_operator_bridge.py -k read -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/api/core/operator/bridge.py apps/api/core/operator/router.py apps/api/core/operator/schemas.py apps/api/tests/test_operator_bridge.py
git commit -m "feat: add paperclip bridge read endpoints"
```

### Task 6: Harden command ingestion for Paperclip correlation and external drafts

**Files:**
- Modify: `apps/api/core/operator/service.py`
- Modify: `apps/api/core/operator/schemas.py`
- Modify: `apps/api/tests/test_operator_api.py`
- Modify: `apps/api/tests/test_operator_service.py`

- [x] **Step 1: Write the failing command enrichment tests**

```python
def test_operator_command_preserves_paperclip_correlation_metadata():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_operator_api.py apps/api/tests/test_operator_service.py -k correlation -v`
Expected: FAIL because correlation metadata and optional external draft import are incomplete.

- [x] **Step 3: Write minimal implementation**

Extend command handling so it preserves:

- `ticket_id`
- `actor_id`
- `company_id`
- `correlation_id`
- `requested_by`

And optionally supports:

- `import_external_draft`

that creates a CoreWire draft from a Paperclip-provided body without bypassing review and compliance rules.

- [x] **Step 4: Run tests to verify they pass**

Run: `pytest apps/api/tests/test_operator_api.py apps/api/tests/test_operator_service.py -k correlation -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add apps/api/core/operator/service.py apps/api/core/operator/schemas.py apps/api/tests/test_operator_api.py apps/api/tests/test_operator_service.py
git commit -m "feat: preserve paperclip bridge metadata"
```

### Task 7: Document and smoke-test the HTTP adapter bridge flow

**Files:**
- Modify: `docs/ops/paperclip-bridge.md`
- Create: `docs/runbooks/paperclip-http-adapter.md`
- Modify: `tests/integration/test_operator_docs.py`

- [x] **Step 1: Write the failing docs test**

```python
def test_paperclip_bridge_docs_cover_read_endpoints_http_adapter_and_auth():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_operator_docs.py -v`
Expected: FAIL because the bridge docs do not yet describe the V1 read path and adapter setup.

- [x] **Step 3: Write minimal implementation**

Document:

- Paperclip role vs CoreWire role
- HTTP adapter setup
- read endpoints
- command endpoints
- auth model
- correlation fields
- staging smoke flow

- [x] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_operator_docs.py -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add docs/ops/paperclip-bridge.md docs/runbooks/paperclip-http-adapter.md tests/integration/test_operator_docs.py
git commit -m "docs: finalize paperclip bridge v1 contract"
```

## Chunk 3: End-to-End Verification

### Task 8: Rehearse owner admin and Paperclip bridge on staging

**Files:**
- Modify: `docs/ops/staging-rehearsal.md`
- Create: `tests/integration/test_admin_bridge_contract.py`

- [x] **Step 1: Write the failing integration contract test**

```python
def test_staging_rehearsal_covers_owner_admin_and_paperclip_bridge_v1():
    ...
```

- [x] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_admin_bridge_contract.py -v`
Expected: FAIL because the combined rehearsal contract is not yet documented.

- [x] **Step 3: Write minimal implementation**

Document and verify:

- owner admin checks
- programming control checks
- bridge read checks
- bridge command checks
- expected staging smoke order

- [x] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_admin_bridge_contract.py tests/integration/test_operator_docs.py -v`
Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add docs/ops/staging-rehearsal.md tests/integration/test_admin_bridge_contract.py
git commit -m "docs: add admin and paperclip bridge staging rehearsal"
```

## Verification Checklist

- `pytest apps/api/tests/test_admin_auth.py apps/api/tests/test_admin_content.py apps/api/tests/test_admin_programming.py apps/api/tests/test_article_actions.py apps/api/tests/test_autonomy_controls.py apps/api/tests/test_operator_api.py apps/api/tests/test_operator_bridge.py apps/api/tests/test_operator_service.py -q`
- `pytest tests/integration/test_operator_docs.py tests/integration/test_admin_bridge_contract.py -q`
- `pnpm --dir apps/web test -- admin-shell article-manager programming-controls`
- `docker compose -f infra/docker/docker-compose.prod.yml config`

## Completion Record

**Completed:** 2026-04-11  
**Merge commit:** `3c1b09a` on `master`  
**Staging verified:** `213.202.216.222`

All tasks passed verification:

- 113 API tests pass on master
- 3 integration tests pass (`test_operator_docs`, `test_admin_bridge_contract`)
- All 4 bridge read endpoints live and responding
- `import_external_draft` command with full correlation echo confirmed on staging
- `master` pushed to `origin`, staging redeployed from master

**Next canonical document:** `docs/runbooks/2026-04-11-project-checkpoint.md`
