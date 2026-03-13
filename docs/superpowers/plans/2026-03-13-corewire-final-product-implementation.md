# CoreWire Final Product Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a launch-ready CoreWire product with owner admin, autonomy controls, model profiles, analytics, compliance workflows, and production operations readiness.

**Architecture:** Extend the current integrated CoreWire runtime with a dedicated owner control plane, an explicit model-routing layer, a policy-driven editorial workflow, and operational dashboards. Keep public site, control plane, and execution plane separated while preserving a clean future Paperclip bridge through internal operator APIs.

**Tech Stack:** Next.js App Router, FastAPI, Python workers, PostgreSQL, Redis, MinIO or S3-compatible storage, Docker Compose, Kubernetes manifests, analytics event store, model gateway abstraction, Playwright, pytest, Node test runner

---

## File Structure

Create or extend these areas:

- `apps/api/core/admin/*` for owner admin APIs and autonomy settings
- `apps/api/core/operator/*` for operator command endpoints and future Paperclip bridge
- `apps/api/core/analytics/*` for product and operational summaries
- `apps/api/core/compliance/*` for correction, retraction, supersede, and disclosure logic
- `apps/api/core/models/*` or `apps/api/core/llm/*` for agent/model profile routing
- `apps/web/app/admin/*` for owner admin UI
- `apps/web/components/admin/*` for review queue, controls, analytics, and source management
- `apps/workers/core/editorial/*` for structure, style, and standards workflow stages
- `docs/runbooks/*` and `docs/ops/*` for launch and incident operations
- `tests/integration/*`, `apps/api/tests/*`, `apps/web/tests/*`, and `tests/e2e/*` for verification

## Chunk 1: Runtime Closure for Launch

### Task 1: Close the local runtime gap and verify live startup paths

**Files:**
- Modify: `scripts/bootstrap-local.ps1`
- Modify: `docs/runbooks/local-start.md`
- Create: `tests/integration/test_local_runtime_contract.py`
- Modify: `README.md`

- [ ] **Step 1: Write the failing local runtime contract test**

```python
def test_local_runtime_contract_defines_api_web_worker_start_commands():
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_local_runtime_contract.py -v`
Expected: FAIL because local runtime contract is incomplete.

- [ ] **Step 3: Write minimal implementation**

Document exact startup order, env contract, and process commands.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_local_runtime_contract.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts docs README.md tests/integration
git commit -m "docs: close local runtime launch contract"
```

## Chunk 2: Model Gateway and Execution Profiles

### Task 2: Add agent model profiles for economy, balanced, and premium

**Files:**
- Create: `apps/api/core/llm/profiles.py`
- Create: `apps/api/core/llm/router.py`
- Create: `apps/api/tests/test_model_profiles.py`

- [ ] **Step 1: Write the failing model profile test**

```python
def test_balanced_profile_maps_writer_and_research_agents_to_expected_models():
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/api/tests/test_model_profiles.py -v`
Expected: FAIL because profile routing does not exist.

- [ ] **Step 3: Write minimal implementation**

Define `economy`, `balanced`, and `premium` model mappings plus fallback profiles.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/api/tests/test_model_profiles.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/llm apps/api/tests
git commit -m "feat: add model execution profiles"
```

### Task 3: Add per-story profile selection and budget policy

**Files:**
- Modify: `apps/api/core/articles/schemas.py`
- Create: `apps/api/core/policy/budget.py`
- Create: `tests/integration/test_budget_policy.py`

- [ ] **Step 1: Write the failing budget policy test**

```python
def test_flagship_story_can_select_premium_profile_while_standard_story_defaults_to_balanced():
    ...
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_budget_policy.py -v`
Expected: FAIL because story profile policy is missing.

- [ ] **Step 3: Write minimal implementation**

Add story profile metadata and budget enforcement helpers.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_budget_policy.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core tests/integration
git commit -m "feat: add story-level model profile policy"
```

## Chunk 3: Owner Admin and Autonomy Controls

### Task 4: Add owner auth skeleton and admin app shell

**Files:**
- Create: `apps/api/core/admin/auth.py`
- Create: `apps/api/core/admin/router.py`
- Create: `apps/web/app/admin/page.tsx`
- Create: `apps/web/components/admin/admin-shell.tsx`
- Test: `apps/api/tests/test_admin_auth.py`
- Test: `apps/web/tests/admin-shell.test.mjs`

- [ ] **Step 1: Write the failing admin auth and shell tests**

- [ ] **Step 2: Run tests to verify they fail**

Run:
- `pytest apps/api/tests/test_admin_auth.py -v`
- `pnpm --filter corewire-web test`

Expected: FAIL because admin shell and auth are missing.

- [ ] **Step 3: Write minimal implementation**

Add single-owner access gate and initial admin dashboard shell.

- [ ] **Step 4: Run tests to verify they pass**

Run the same commands.
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/admin apps/web/app/admin apps/web/components/admin
git commit -m "feat: add owner admin shell"
```

### Task 5: Add autonomy controls and publish mode settings

**Files:**
- Create: `apps/api/core/admin/settings.py`
- Create: `apps/api/tests/test_autonomy_controls.py`
- Create: `apps/web/components/admin/autonomy-controls.tsx`
- Modify: `apps/web/app/admin/page.tsx`

- [ ] **Step 1: Write the failing autonomy control tests**

- [ ] **Step 2: Run tests to verify they fail**

Run:
- `pytest apps/api/tests/test_autonomy_controls.py -v`
- `pnpm --filter corewire-web test`

Expected: FAIL because autonomy settings do not exist.

- [ ] **Step 3: Write minimal implementation**

Support:
- `manual`
- `hybrid`
- `autonomous`

plus publish toggles and pause switches.

- [ ] **Step 4: Run tests to verify they pass**

Run the same commands.
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/api apps/web
git commit -m "feat: add owner autonomy controls"
```

## Chunk 4: Review Queue and Editorial Operations

### Task 6: Add review queue and draft operation APIs

**Files:**
- Create: `apps/api/core/admin/review.py`
- Create: `apps/api/tests/test_review_queue.py`
- Create: `apps/web/components/admin/review-queue.tsx`
- Test: `apps/web/tests/review-queue.test.mjs`

- [ ] **Step 1: Write the failing review queue tests**

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

Expose:
- pending drafts
- low-confidence queue
- flagged items

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add apps/api apps/web
git commit -m "feat: add editorial review queue"
```

### Task 7: Add article actions for approve, reject, retract, correct, supersede

**Files:**
- Create: `apps/api/core/compliance/actions.py`
- Create: `apps/api/tests/test_article_actions.py`
- Create: `apps/web/components/admin/article-actions.tsx`

- [ ] **Step 1: Write the failing article action tests**

- [ ] **Step 2: Run tests to verify they fail**

- [ ] **Step 3: Write minimal implementation**

Add state transitions and audit recording for article lifecycle changes.

- [ ] **Step 4: Run tests to verify they pass**

- [ ] **Step 5: Commit**

```bash
git add apps/api apps/web
git commit -m "feat: add article lifecycle actions"
```

## Chunk 5: Editorial Quality Pipeline

### Task 8: Add structure editor, style editor, and standards validator stages

**Files:**
- Create: `apps/workers/core/editorial/structure.py`
- Create: `apps/workers/core/editorial/style.py`
- Create: `apps/workers/core/editorial/standards.py`
- Create: `apps/workers/tests/test_editorial_pipeline.py`

- [ ] **Step 1: Write the failing editorial pipeline tests**

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest apps/workers/tests/test_editorial_pipeline.py -v`
Expected: FAIL because editorial stages are missing.

- [ ] **Step 3: Write minimal implementation**

Split final article generation into:
- structure
- draft
- style
- standards validation

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest apps/workers/tests/test_editorial_pipeline.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/editorial apps/workers/tests
git commit -m "feat: add editorial quality stages"
```

### Task 9: Add quality filters for generic and disconnected prose

**Files:**
- Create: `apps/workers/core/editorial/quality.py`
- Create: `apps/workers/tests/test_quality_filters.py`

- [ ] **Step 1: Write the failing quality filter test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Block:
- repeated filler
- unsupported transitions
- thin summary prose

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add apps/workers/core/editorial apps/workers/tests
git commit -m "feat: add article quality filters"
```

## Chunk 6: Analytics and Dashboards

### Task 10: Add product and operational analytics APIs

**Files:**
- Create: `apps/api/core/analytics/router.py`
- Create: `apps/api/core/analytics/service.py`
- Create: `apps/api/tests/test_analytics_api.py`

- [ ] **Step 1: Write the failing analytics API test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Expose:
- page metrics
- queue metrics
- cost metrics
- source health summaries

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/analytics apps/api/tests
git commit -m "feat: add analytics summaries"
```

### Task 11: Add admin analytics dashboard UI

**Files:**
- Create: `apps/web/components/admin/analytics-dashboard.tsx`
- Create: `apps/web/tests/admin-analytics.test.mjs`
- Modify: `apps/web/app/admin/page.tsx`

- [ ] **Step 1: Write the failing admin analytics test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Render:
- article throughput
- queue status
- confidence distribution
- cost summary

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add apps/web
git commit -m "feat: add admin analytics dashboard"
```

## Chunk 7: Compliance and Policies

### Task 12: Add disclosure, correction, and retraction policy surfaces

**Files:**
- Create: `apps/web/app/policies/ai-disclosure/page.tsx`
- Create: `apps/web/app/policies/corrections/page.tsx`
- Create: `apps/api/core/compliance/policies.py`
- Create: `tests/integration/test_policy_surfaces.py`

- [ ] **Step 1: Write the failing policy surface test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Add public policy pages and API-backed policy metadata.

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add apps/web apps/api tests/integration
git commit -m "feat: add public compliance policy surfaces"
```

## Chunk 8: Operator API and Paperclip Preparation

### Task 13: Add internal operator command endpoints

**Files:**
- Create: `apps/api/core/operator/router.py`
- Create: `apps/api/core/operator/schemas.py`
- Create: `apps/api/tests/test_operator_api.py`

- [ ] **Step 1: Write the failing operator API test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Support:
- create story
- rerun analysis
- publish draft
- set autonomy mode
- disable source

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add apps/api/core/operator apps/api/tests
git commit -m "feat: add operator command api"
```

### Task 14: Add Paperclip bridge design docs and callback contract

**Files:**
- Create: `docs/ops/paperclip-bridge.md`
- Create: `tests/integration/test_operator_docs.py`

- [ ] **Step 1: Write the failing operator docs test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Document:
- operator command schema
- callback schema
- auth model
- ticket correlation model

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**

```bash
git add docs tests/integration
git commit -m "docs: add paperclip bridge contract"
```

## Chunk 9: Launch Operations and Final Verification

### Task 15: Add final launch checklist, staging rehearsal docs, and browser smoke closure

**Files:**
- Modify: `docs/ops/production-readiness-checklist.md`
- Create: `docs/ops/staging-rehearsal.md`
- Modify: `tests/e2e/publish-flow.spec.ts`
- Modify: `tests/e2e/seo-smoke.spec.ts`
- Create: `tests/integration/test_launch_docs.py`

- [ ] **Step 1: Write the failing launch docs test**

- [ ] **Step 2: Run test to verify it fails**

- [ ] **Step 3: Write minimal implementation**

Document:
- staging drill
- rollout steps
- rollback steps
- launch signoff checklist

- [ ] **Step 4: Run test to verify it passes**

Run:
- `pytest tests/integration -q`
- `pytest apps/api/tests -q`
- `pytest apps/workers/tests -q`
- `pnpm --filter corewire-web test`
- `pnpm exec playwright test tests/e2e/publish-flow.spec.ts tests/e2e/seo-smoke.spec.ts`

Expected:
- all stable checks PASS
- if Playwright remains environment-blocked, record exact blocker and keep docs/tests ready

- [ ] **Step 5: Commit**

```bash
git add docs tests
git commit -m "docs: add final launch and staging runbooks"
```

## Execution Notes

- Preserve hard-coded editorial gates for citations, fact/analysis separation, and confidence policy.
- Do not let profile selection bypass compliance or standards validation.
- Keep Paperclip integration as a clean internal operator contract, not a public-site dependency.
- Treat `balanced` as the default publishing profile unless explicitly overridden.
- Reserve `premium` for investigations and owner-selected flagship stories.
- Use `economy` only where policy allows reduced quality without trust risk.

## Verification Checklist

- `pnpm test:repo`
- `pytest tests/integration -q`
- `pytest apps/api/tests -q`
- `pytest apps/workers/tests -q`
- `pnpm --filter corewire-web test`
- `docker compose -f infra/docker/docker-compose.yml -f infra/docker/docker-compose.prod.yml config`
- `pnpm exec playwright test tests/e2e/publish-flow.spec.ts tests/e2e/seo-smoke.spec.ts`

## Handoff

Plan complete and saved to `docs/superpowers/plans/2026-03-13-corewire-final-product-implementation.md`. Ready to execute?
