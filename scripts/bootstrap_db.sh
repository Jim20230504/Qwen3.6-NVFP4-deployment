#!/usr/bin/env bash
set -euo pipefail

docker compose up -d postgres
docker compose exec -T postgres psql \
  -U "${POSTGRES_USER}" \
  -d "${POSTGRES_DB}" \
  -f /docker-entrypoint-initdb.d/init.sql
