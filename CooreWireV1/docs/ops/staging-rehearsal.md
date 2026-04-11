# Staging Rehearsal

## Goal

Run a full staging rehearsal before launch signoff so CoreWire proves the publish flow, SEO smoke surfaces, and rollback readiness on a live stack.

## Publish Flow

1. Apply migrations and start API, web, workers, Redis, and PostgreSQL.
2. Seed demo data or replay a controlled story fixture.
3. Verify a high-confidence article appears on the homepage.
4. Verify the article page renders facts, analysis, and sources.
5. Verify a low-confidence story remains off the homepage and stays marked as developing.

## SEO Smoke

1. Open `/sitemap.xml` and confirm article URLs render.
2. Open `/robots.txt` and confirm sitemap disclosure is present.
3. Confirm canonical metadata exists on homepage and article routes.

## Owner Admin Checks

1. Confirm `/api/admin/summary` returns health, autonomy mode, queue counts, and recent activity.
2. Confirm the admin dashboard loads and shows the correct autonomy state.
3. Verify programming controls return current topic targets and interval settings.

## Paperclip Bridge Read Checks

1. `GET /api/operator/bridge/status` — verify `health.system == "ok"` and queue counts are non-negative.
2. `GET /api/operator/bridge/review-queue` — verify response shape includes `totals` and `items`.
3. `GET /api/operator/bridge/published` — verify `total` is an integer and `recent` is a list.
4. `GET /api/operator/bridge/autonomy` — verify `mode` and boolean publish gate flags are present.

## Paperclip Bridge Command Checks

1. Send an `import_external_draft` command with correlation fields (`ticket_id`, `actor_id`, `requested_by`).
2. Confirm response has `accepted: true`, a `review_item`, and the full `correlation` dict echoed back.
3. `GET /api/operator/bridge/review-queue` — confirm the imported draft appears in `pending_drafts` or `flagged_items`.

## Rollback and Signoff

1. Record the rollback command path used by the target environment.
2. Capture operator signoff for publish flow, SEO smoke, metrics reachability, admin checks, and bridge checks.
3. Mark launch signoff only after all staging rehearsal checks pass.
