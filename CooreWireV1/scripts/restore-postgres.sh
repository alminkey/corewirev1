#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup-file>"
  exit 1
fi

COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-corewire}"
BACKUP_FILE="$1"

if [[ ! -f "${BACKUP_FILE}" ]]; then
  echo "Backup file not found: ${BACKUP_FILE}"
  exit 1
fi

cat "${BACKUP_FILE}" | docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f infra/docker/docker-compose.yml \
  -f infra/docker/docker-compose.prod.yml \
  exec -T postgres psql -U corewire -d corewire

echo "Restore completed from ${BACKUP_FILE}"
