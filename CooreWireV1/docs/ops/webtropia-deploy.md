# Webtropia Deploy Runbook

This runbook documents the production deploy path for CoreWire on the existing Webtropia Cloud VPS M2.

## Overview

CoreWire runs on one VPS with Docker Compose services for:

- `caddy`
- `web`
- `api`
- `workers`
- `scheduler`
- `postgres`
- `redis`
- `minio`

## DNS

For staging over raw IP, set:

- `COREWIRE_SITE_ADDRESS=http://213.202.216.222`
- `COREWIRE_SITE_URL=http://213.202.216.222`

For a domain-based deploy, point the production domain to the VPS public IP:

- `A corewire.example.com -> <webtropia-vps-ip>`

If you use the root domain instead, point the root `A` record to the same VPS IP and keep `www` as a redirect in the DNS or proxy layer.

## TLS

`Caddy` can serve plain HTTP for raw-IP staging and can terminate TLS automatically once DNS is pointing to the VPS and ports `80/443` are reachable.

Before first deploy:

1. Open ports `80` and `443` in the VPS firewall.
2. For domain mode, set `COREWIRE_SITE_ADDRESS` to the real hostname and `COREWIRE_SITE_URL` to the public HTTPS origin.
3. Replace the placeholder ops email via `COREWIRE_OPS_EMAIL`.

## Deploy

Run from the project root on the VPS.

Linux VPS:

```bash
./scripts/check-webtropia-env.sh
./scripts/deploy-webtropia.sh
```

Windows or PowerShell-driven automation:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/deploy-webtropia.ps1
```

The deploy scripts run the merged `docker compose` stack, rebuild changed services, and perform basic smoke checks against the local reverse proxy.

## Environment Contract

Before any deploy, validate the VPS environment with:

```bash
./scripts/check-webtropia-env.sh
```

At minimum, production must define:

- `COREWIRE_DATABASE_URL`
- `COREWIRE_INTERNAL_TOKEN`
- `COREWIRE_OWNER_TOKEN`
- `OPENROUTER_API_KEY`
- `COREWIRE_SITE_URL`
- `COREWIRE_SITE_ADDRESS`

## Startup Order

The production compose stack expects this order:

1. `postgres`, `redis`, `minio`
2. `api`, `workers`, `scheduler`
3. `web`
4. `caddy`

The compose file encodes those dependencies, but use this order when debugging partial restarts.

## Backups

At minimum back up:

- PostgreSQL database dumps
- `postgres_data` volume snapshots
- `minio_data` object storage
- `.env` and deploy secrets

Take a database backup before each release tag deployment.

Linux backup command:

```bash
./scripts/backup-postgres.sh
```

Linux restore command:

```bash
./scripts/restore-postgres.sh ./backups/postgres-YYYYMMDD-HHMMSS.sql
```

## Smoke Checks

After deploy confirm:

- `https://corewire.example.com/`
- `https://corewire.example.com/health`
- `https://corewire.example.com/articles/<known-slug>`
- owner-only admin route login

Automated smoke path:

```bash
BASE_URL=https://corewire.example.com ./scripts/smoke-webtropia.sh
```

## Rollback

If a release is unhealthy:

1. Checkout the previous git tag.
2. Re-run `scripts/deploy-webtropia.ps1`.
3. Restore the previous database backup if a migration introduced incompatible data changes.

This rollback path should be rehearsed on staging before the first public launch.

Linux rollback path:

```bash
./scripts/rollback-webtropia.sh v0.1.0
```
