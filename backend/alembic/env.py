"""Alembic environment — loads app config, discovers models, runs migrations."""

from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from alembic import context

# ── Model discovery ───────────────────────────────────────────────────────────
# Import all model modules so BaseDBModel.metadata is fully populated.
# Add imports here as new model modules are created in Phase 2+.
from app.auth import models as _auth_models  # noqa: F401
from app.base import models as _base_models  # noqa: F401
from app.base.models import BaseDBModel
from app.emails import models as _email_models  # noqa: F401
from app.users import models as _user_models  # noqa: F401
from app.utils.configure import config as app_config

# ── Alembic config ────────────────────────────────────────────────────────────
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use the admin (sync psycopg2) URL — overrides sqlalchemy.url in alembic.ini
target_metadata = BaseDBModel.metadata
database_url = app_config.ADMIN_DB_URL


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generates SQL without connecting)."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connects to DB and applies changes)."""
    connectable = create_engine(database_url)
    with connectable.connect() as connection:
        do_run_migrations(connection)
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
