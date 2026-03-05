# Scripts

Production startup scripts for ECS tasks.

| Script | Purpose |
|---|---|
| `start.sh` | API task: runs `alembic upgrade head` then starts uvicorn |
| `start-worker.sh` | Worker task: starts the SAQ worker process (Phase 2) |

## Usage

These scripts are the entrypoints for ECS Fargate tasks. In local dev, use the
Justfile commands instead (`just dev-backend`, `just dev-worker`).

To test a script locally:

```bash
cd backend
chmod +x scripts/start.sh
./scripts/start.sh
```

## Why run migrations in start.sh?

Running `alembic upgrade head` on startup ensures the schema is always up-to-date
before the app begins serving traffic. This is safe for single-instance deployments.

For multi-instance blue/green deployments, consider running migrations as a separate
ECS task before the new service version is promoted.
