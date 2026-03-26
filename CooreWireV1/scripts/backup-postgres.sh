#!/usr/bin/env bash
set -euo pipefail

COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-corewire}"
OUTPUT_DIR="${OUTPUT_DIR:-./backups}"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT_PATH="${OUTPUT_DIR}/postgres-${TIMESTAMP}.sql"

mkdir -p "${OUTPUT_DIR}"

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f infra/docker/docker-compose.yml \
  -f infra/docker/docker-compose.prod.yml \
  exec -T postgres pg_dump -U corewire -d corewire > "${OUTPUT_PATH}"

echo "Backup written to ${OUTPUT_PATH}"
