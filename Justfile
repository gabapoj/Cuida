# Cuida Justfile — https://just.systems

# List available commands
default:
    @just --list

# ─── Install ──────────────────────────────────────────────────────────────────

# Check and install macOS prerequisites (Homebrew, just, uv, psql, container runtime)
bootstrap:
    bash scripts/bootstrap.sh

# Install backend dependencies
install:
    cd backend && uv sync --dev

# ─── Database ─────────────────────────────────────────────────────────────────

# Start postgres (dev + test) and redis via Docker
db-start:
    cd backend && docker compose -f docker-compose.dev.yml up -d

# Stop all Docker services
db-stop:
    cd backend && docker compose -f docker-compose.dev.yml down

# Run alembic migrations (upgrade to head)
db-upgrade:
    cd backend && uv run alembic upgrade head

# Create a new migration from model changes
db-migrate message:
    cd backend && uv run alembic revision --autogenerate -m "{{message}}"

# Downgrade by one revision
db-downgrade:
    cd backend && uv run alembic downgrade -1

# Drop and recreate the dev database volume (destructive!)
db-clean:
    cd backend && docker compose -f docker-compose.dev.yml down -v
    just db-start
    just db-upgrade

# Connect to the dev database via psql
db-psql:
    psql postgresql://postgres:postgres@localhost:5432/postgres

# ─── Development ──────────────────────────────────────────────────────────────

# Start Litestar backend with hot reload
dev-backend:
    cd backend && uv run litestar --app app.index:app run -r -d -p 8000

# Start Next.js landing page dev server
dev-landing:
    cd landing && pnpm dev

# Start Vite web app dev server
dev-web:
    cd web && pnpm dev

# Start SAQ worker with hot reload (Phase 2: uncomment once SAQ is configured)
dev-worker:
    cd backend && uv run litestar --app app.index:app workers run

# ─── Tests ────────────────────────────────────────────────────────────────────

# Run backend tests
test:
    cd backend && uv run pytest -v

# ─── Code Quality ─────────────────────────────────────────────────────────────

# Lint backend code
lint:
    cd backend && uv run ruff check .

# Format backend code
fmt:
    cd backend && uv run ruff format .

# Type-check backend code
typecheck:
    cd backend && uv run basedpyright

# ─── Codegen ──────────────────────────────────────────────────────────────────

# Generate API client for web app (requires backend running)
codegen:
    cd web && pnpm codegen

# Generate API client for landing page (requires backend running)
codegen-landing:
    cd landing && pnpm codegen

# ─── Docker ───────────────────────────────────────────────────────────────────

# Build backend Docker image
docker-build:
    cd backend && docker build -t cuida-api:local .
