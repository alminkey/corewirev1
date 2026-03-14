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

## Rollback and Signoff

1. Record the rollback command path used by the target environment.
2. Capture operator signoff for publish flow, SEO smoke, and metrics reachability.
3. Mark launch signoff only after all staging rehearsal checks pass.
