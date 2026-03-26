#!/usr/bin/env bash
set -euo pipefail

required_vars=(
  COREWIRE_DATABASE_URL
  COREWIRE_INTERNAL_TOKEN
  COREWIRE_OWNER_TOKEN
  OPENROUTER_API_KEY
  COREWIRE_SITE_URL
)

missing=0
for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Missing required env var: ${var_name}"
    missing=1
  fi
done

if [[ "${missing}" -ne 0 ]]; then
  exit 1
fi

echo "Environment looks ready for Webtropia deploy."
