# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands are run via `just` (Justfile at repo root) or directly.

### Backend
```bash
just install          # uv sync --dev
just db-start         # start postgres + redis via Docker Compose
just db-upgrade       # alembic upgrade head
just db-migrate <msg> # create new migration
just dev-backend      # litestar on :8000 with hot reload
just dev-worker       # SAQ worker with hot reload
just test             # pytest (all tests)
just lint             # ruff check
just fmt              # ruff format
just typecheck        # basedpyright
```

Run a single test:
```bash
cd backend && uv run pytest tests/test_health.py -v
uv run pytest -k "test_name" -v
```

### Frontend (web app)
```bash
just dev-web          # vite on :5173
just codegen          # orval (requires backend running at :8000)
cd web && pnpm lint
cd web && pnpm type-check
```

### Landing page
```bash
just dev-landing      # next.js on :3000
just codegen-landing  # orval for landing
```

### Local services (Docker)
- Postgres dev: `localhost:5432` (db: cuida)
- Postgres test: `localhost:5433` (db: cuida)
- Redis: `localhost:6379`

## Architecture

### Backend (`backend/app/`)

**Entry point flow:** `app/index.py` → discovers all models via `discover_and_import()` → calls `create_app()` from `factory.py`. Models must be imported before `create_app()` runs so SQLAlchemy metadata is populated for Alembic.

**`factory.py`** wires together: SQLAlchemy async plugin, CORS, ServerSideSessionConfig (Redis store), email template engine (Jinja2 → `templates/emails-react/`), SAQ queue, OpenTelemetry, and exception handlers.

**Config** (`app/utils/configure.py`): `Config` dataclass loaded from `.env.local`. `get_config()` returns `TestConfig` (port 5433) when `ENV=testing`. Tests set `ENV=testing` before any app imports via `conftest.py`.

**Database patterns:**
- All models extend `BaseDBModel` (`id: Mapped[int]` PK, `created_at`, `updated_at`, `deleted_at`)
- `db_session: AsyncSession` injected via Litestar's SQLAlchemy plugin (keyword arg name is `db_session`)
- SQLAlchemy imports come from `advanced_alchemy.extensions.litestar` (not `litestar.plugins.sqlalchemy`)
- New models must be explicitly imported in both `app/index.py` and `alembic/env.py`

**Auth:** Magic link tokens → HMAC-SHA256 hashed in DB. Sessions stored server-side in Redis. `requires_session` guard checks `session["user_id"]`. `ServerSideSessionConfig` uses `secure=` (not `https_only=`).

**Module structure:** Each domain module (`auth/`, `users/`, `calls/`, etc.) typically has `models.py`, `routes.py`, `service.py`, `queries.py`, `schemas.py`, `deps.py`.

**Validation:** msgspec (not Pydantic). Schemas in `schemas.py` per module.

**Email:** `app/emails/client.py` has `LocalEmailClient` (dev, logs to console) and `SESEmailClient` (prod). Templates are pre-compiled React Email → Jinja2 in `templates/emails-react/`.

**AI/Voice adapter pattern** (`llm/`, `voice/`, `telephony/`): each follows `protocol.py` → `factory.py` → `*_provider.py`. Switching providers = one env var change.

### Frontend (`web/src/`)

**Routing** (TanStack Router):
```
root → publicLayout (/_public)
         ├── /auth
         ├── /auth/magic-link/verify
         └── /invite
     → authenticatedLayout (/_authenticated)
         ├── /dashboard
         ├── /clients
         ├── /calls
         └── /settings
```

Root loader checks auth → redirects to `/dashboard` (authed) or `/auth`. `requireAuth()` calls `queryClient.ensureQueryData(getAuthMeMeQueryOptions())` — any error redirects to `/auth`.

**API client:** Orval generates `src/openapi/` from the backend's live OpenAPI schema at `http://localhost:8000/schema/openapi.json`. Output mode is `tags-split` (one file per OpenAPI tag) with `react-query` client. All queries use `useSuspenseQuery`. `custom-instance.ts` adapts fetch-style Orval output to use Axios internally and must not be overwritten by codegen.

**Tailwind v4:** No `tailwind.config.js`. CSS theme vars mapped to utilities via `@theme inline { --color-*: var(--*) }` in `index.css`. shadcn uses `@/*` path aliases — both `tsconfig.json` and `components.json` must define them.

**Dev proxy:** Vite proxies `/api` → `http://localhost:8000` (configured in `vite.config.ts`).

### Fullstack workflow (backend → frontend)

When adding or changing a backend endpoint, the frontend API client must be regenerated:

1. Add/modify the route in `backend/app/<module>/routes.py` — Litestar auto-generates OpenAPI from type annotations and response models
2. Ensure the route is registered in `factory.py`
3. Start the backend: `just dev-backend`
4. Regenerate the client: `just codegen` (runs Orval against `:8000/schema/openapi.json`)
5. The updated hooks/types appear in `web/src/openapi/<tag>/` — import and use them

**Using generated hooks:**
- Queries: `use<OperationId>Suspense()` — wrap the component in `<Suspense>`
- Mutations: `use<OperationId>()` → `mutation.mutate({ data: { ... } })` (body always in `data` key)
- Types: exported from `web/src/openapi/cuidaAPI.schemas.ts`

**Never manually edit** files in `web/src/openapi/` except `custom-instance.ts` — they are overwritten on every `just codegen`.

### Alembic
- `alembic/` has **no `__init__.py`** (would shadow the installed package)
- `alembic.ini` has `prepend_sys_path = .` so `app` is importable from `alembic/env.py`

### CI/CD (`.github/workflows/`)
GitHub Actions with change detection — only deploys when backend or infra changes. Uses AWS OIDC (no long-lived credentials). Pipeline: detect changes → test → build Docker image → Terraform → ECS deploy.
