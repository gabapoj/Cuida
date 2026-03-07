#!/usr/bin/env bash
# Production SAQ worker startup script
# Used as the ECS worker task entrypoint.

set -euo pipefail

echo "[worker] Starting SAQ worker..."
exec litestar --app app.index:app workers run
