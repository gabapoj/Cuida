# Alembic Migrations

Schema migrations for the Cuida database.

## Workflow

```bash
# Apply all pending migrations
just db-upgrade

# Generate a new migration from model changes
just db-migrate "add users table"

# Rollback the last migration
just db-downgrade

# Check current revision
cd backend && uv run alembic current

# View migration history
cd backend && uv run alembic history --verbose
```

## Rules

1. **Never hand-edit the schema** — always use `alembic revision --autogenerate`
2. **Always review generated migrations** before committing — autogenerate isn't perfect
3. **One concern per migration** — don't mix schema changes with data migrations
4. **Data migrations** — use a separate revision with raw SQL via `op.execute()`
5. **Downgrade must be reversible** — implement `downgrade()` for every migration
6. **Test before merging** — run `just db-upgrade` + `just db-downgrade` in CI

## env.py Responsibilities

`alembic/env.py`:
- Imports all model modules so `BaseDBModel.metadata` is complete
- Reads `ADMIN_DB_URL` from the app config (sync psycopg2 URL)
- Overrides `sqlalchemy.url` from `alembic.ini` (never commit credentials there)
- Runs migrations synchronously (Alembic doesn't support async)

## Adding a New Model

1. Create `app/<module>/models.py` with your `BaseDBModel` subclass
2. Import it in `app/index.py` and `alembic/env.py`
3. Run `just db-migrate "your description"`
4. Review the generated file in `alembic/versions/`
5. Run `just db-upgrade`
