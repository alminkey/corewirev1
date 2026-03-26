#!/usr/bin/env bash
set -euo pipefail

COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-corewire}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Deploying CoreWire to Webtropia with project ${COMPOSE_PROJECT_NAME}"

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f "${ROOT_DIR}/infra/docker/docker-compose.yml" \
  -f "${ROOT_DIR}/infra/docker/docker-compose.prod.yml" \
  pull

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f "${ROOT_DIR}/infra/docker/docker-compose.yml" \
  -f "${ROOT_DIR}/infra/docker/docker-compose.prod.yml" \
  up -d --build

sleep 5
curl -fsS http://localhost/health >/dev/null
curl -fsS http://localhost/ >/dev/null

echo "Deployment complete."
