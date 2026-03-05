# Backend

Litestar ASGI API — Python 3.13, SQLAlchemy 2.0 async, PostgreSQL 16, Redis 7.

## Tech

| Concern        | Choice                          |
|----------------|---------------------------------|
| Framework      | **Litestar** (ASGI)             |
| Python         | **3.13+** via **uv**            |
| ORM            | **SQLAlchemy 2.0** async        |
| DB driver      | **psycopg** (async psycopg3)    |
| Migrations     | **Alembic**                     |
| Validation     | **msgspec** (not Pydantic)      |
| Auth           | Magic link sessions (Phase 2)   |
| Email          | AWS SES + React Email (Phase 2) |
| Background     | **SAQ** + Redis (Phase 2)       |
| OpenAPI        | Litestar built-in               |

## Directory Map

```
backend/
├── app/
│   ├── index.py          # Entry point — model discovery + create_app()
│   ├── factory.py        # create_app() — registers plugins, routes, CORS
│   ├── base/             # BaseDBModel, health route
│   ├── utils/            # Config, logging, exceptions
│   ├── auth/             # Phase 2: magic link auth
│   ├── users/            # Phase 2: user model + CRUD
│   ├── calls/            # Phase 2: call sessions + WebSocket
│   ├── emails/           # Phase 2: SES client + templates
│   ├── queue/            # Phase 2: SAQ workers
│   ├── llm/              # Phase 3: LLM adapters
│   ├── voice/            # Phase 3: STT/TTS adapters
│   └── telephony/        # Phase 3: Telnyx/Twilio adapters
├── alembic/              # Migrations
├── tests/                # pytest
├── scripts/              # start.sh, start-worker.sh
├── pyproject.toml        # uv project
├── Dockerfile            # Production image
└── docker-compose.dev.yml # Local postgres + redis
```

## Conventions

- **App factory** pattern — `create_app(config)` in `factory.py`
- **Model discovery** — `index.py` imports all models before `create_app()` so `BaseDBModel.metadata` is complete for Alembic and SQLAlchemy
- **Env vars** — loaded via `python-dotenv` from `.env.local` in `utils/configure.py`
- **Session injection** — Litestar SQLAlchemy plugin injects `db_session: AsyncSession`
- **Migrations** — always use `alembic revision --autogenerate`; never hand-edit schema
- **Adapters** — AI/voice/telephony use Protocol + factory pattern (see Phase 3 READMEs)

## Workflow

```bash
# First time
cd backend && uv sync --dev

# Start services
just db-start

# Run migrations
just db-upgrade

# Dev server (hot reload on :8000)
just dev-backend

# Tests
just test

# Lint + format
just lint
just fmt
```
