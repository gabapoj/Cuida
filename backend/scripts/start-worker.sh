#!/usr/bin/env bash
# Production SAQ worker startup script
# Phase 2: uncomment once SAQ is configured in app/queue/
# Used as the ECS worker task entrypoint.

set -euo pipefail

echo "[worker] Starting SAQ worker..."
exec uv run litestar --app app.index:app workers run
