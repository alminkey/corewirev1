# Production Readiness Checklist

## Runtime

- [ ] `docker-compose.prod.yml` resolves with `docker compose config`
- [ ] `apps/api`, `apps/web`, and `apps/workers` Docker images build successfully
- [ ] migrations are applied before application rollout
- [ ] API, web, and worker environment variables are defined explicitly

## Reliability

- [ ] `/health`, `/ready`, and `/metrics` are reachable in the target environment
- [ ] scheduler runs as a single logical instance
- [ ] retries are bounded and dead-letter behavior is defined
- [ ] seed/demo data is disabled outside non-production environments

## Security

- [ ] internal publish routes require `COREWIRE_INTERNAL_TOKEN`
- [ ] fetch targets are allowlisted and block metadata/loopback hosts
- [ ] secrets are injected from environment or secret manager, not committed
- [ ] container images run with least privilege adjustments before release

## Deployment

- [ ] `infra/k8s` manifests are reviewed for image tags and environment values
- [ ] ingress hostnames and TLS are configured for the target environment
- [ ] rollback path is documented before first deployment
- [ ] logs and metrics are wired into the target platform
