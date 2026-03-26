#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost}"
ARTICLE_SLUG="${ARTICLE_SLUG:-corewire-launched-the-pipeline}"

curl -fsS "${BASE_URL}/health" >/dev/null
curl -fsS "${BASE_URL}/" >/dev/null
curl -fsS "${BASE_URL}/articles/${ARTICLE_SLUG}" >/dev/null
curl -fsS "${BASE_URL}/newsletter" >/dev/null

echo "Smoke checks passed for ${BASE_URL}"
