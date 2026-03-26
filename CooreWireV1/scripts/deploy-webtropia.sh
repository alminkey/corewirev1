#!/usr/bin/env bash
set -euo pipefail

COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-corewire}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/infra/docker/docker-compose.prod.yml"

echo "Deploying CoreWire to Webtropia with project ${COMPOSE_PROJECT_NAME}"

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f "${COMPOSE_FILE}" \
  pull

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f "${COMPOSE_FILE}" \
  up -d --build

sleep 5
curl -fsS http://localhost/health >/dev/null
curl -fsS http://localhost/ >/dev/null

echo "Deployment complete."
