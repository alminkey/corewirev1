#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <git-ref-or-tag>"
  exit 1
fi

TARGET_REF="$1"
COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-corewire}"

git checkout "${TARGET_REF}"

docker compose \
  -p "${COMPOSE_PROJECT_NAME}" \
  -f infra/docker/docker-compose.yml \
  -f infra/docker/docker-compose.prod.yml \
  up -d --build

echo "Rollback deployed for ${TARGET_REF}"
