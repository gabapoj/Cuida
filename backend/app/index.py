"""Application entry point.

Model discovery happens here — all model modules must be imported before
create_app() so that BaseDBModel.metadata is fully populated for:
  - SQLAlchemy plugin (schema reflection)
  - Alembic autogenerate (migration diffing)

Add an import for each new models.py as modules are added in Phase 2+:
    from app.calls import models as _call_models   # noqa: F401
"""

# ── Model imports (order matters for FK resolution) ──────────────────────────
from app.base import models as _base_models  # noqa: F401
from app.emails import models as _email_models  # noqa: F401
from app.users import models as _user_models  # noqa: F401
from app.auth import models as _auth_models  # noqa: F401

# ── App creation ──────────────────────────────────────────────────────────────
from app.factory import create_app
from app.utils.configure import config

app = create_app(config=config)
