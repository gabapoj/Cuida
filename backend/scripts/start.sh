#!/usr/bin/env bash
# Production API startup script
# Runs Alembic migrations before starting the server.
# Used as the ECS task entrypoint (CMD in Dockerfile or ECS task definition).

set -euo pipefail

echo "[start] Running database migrations..."
uv run alembic upgrade head

echo "[start] Starting Litestar API server..."
exec uv run uvicorn app.index:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --loop uvloop \
    --no-access-log
