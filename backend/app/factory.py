import logging

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.template.config import TemplateConfig

from app.base.models import BaseDBModel
from app.base.routes import system_router
from app.emails.client import provide_email_client
from app.emails.service import provide_email_service
from app.utils.configure import Config
from app.utils.exceptions import ApplicationError, exception_to_http_response
from app.utils.logging import create_logging_config

logger = logging.getLogger(__name__)


def create_app(config: Config) -> Litestar:
    """Create and configure the Litestar application.

    Registers:
    - SQLAlchemy async plugin (connects to postgres)
    - CORS configuration
    - OpenAPI docs at /schema
    - Health route at /health
    - ApplicationError exception handler

    Phase 2 additions: session auth, SAQ plugin, email client dependency.
    Phase 3 additions: LLM/voice/telephony provider dependencies.
    """
    logging_config = create_logging_config(config)

    # ─── CORS ─────────────────────────────────────────────────────────────────
    cors_config = CORSConfig(
        allow_origins=[config.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ─── SQLAlchemy ───────────────────────────────────────────────────────────
    sqlalchemy_plugin = SQLAlchemyPlugin(
        config=SQLAlchemyAsyncConfig(
            connection_string=config.ASYNC_DATABASE_URL,
            metadata=BaseDBModel.metadata,
            session_config=AsyncSessionConfig(
                expire_on_commit=False,
                autoflush=False,
            ),
            create_all=False,  # Schema managed by Alembic
        )
    )

    # ─── OpenAPI ──────────────────────────────────────────────────────────────
    openapi_config = OpenAPIConfig(
        title="Cuida API",
        description="Cuida backend API",
        version="0.1.0",
        render_plugins=[ScalarRenderPlugin()],
    )

    # ─── Email templates (Jinja2) ─────────────────────────────────────────────
    template_config = TemplateConfig(
        directory=config.EMAIL_TEMPLATES_DIR,
        engine=JinjaTemplateEngine,
    )

    return Litestar(
        route_handlers=[system_router],
        plugins=[sqlalchemy_plugin],
        cors_config=cors_config,
        openapi_config=openapi_config,
        template_config=template_config,
        dependencies={
            "config": Provide(lambda: config, sync_to_thread=False),
            "email_client": Provide(provide_email_client, sync_to_thread=False),
            "email_service": Provide(provide_email_service, sync_to_thread=False),
        },
        exception_handlers={ApplicationError: exception_to_http_response},  # type: ignore[dict-item]
        debug=config.IS_DEV,
        logging_config=logging_config,
    )
