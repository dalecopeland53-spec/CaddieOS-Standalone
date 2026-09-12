#!/usr/bin/env bash
set -e
: "${DB_SECURE_PASSWORD:?Set DB_SECURE_PASSWORD first}"
docker compose build --no-cache
docker compose up -d
until docker exec caddie_telemetry_db pg_isready -U pro_caddie_admin >/dev/null 2>&1; do sleep 2; done
echo "CaddieOS standalone backend is live on port 8080"
