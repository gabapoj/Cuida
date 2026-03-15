import logging
from typing import Any

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.connection import ASGIConnection
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.contrib.opentelemetry import OpenTelemetryConfig, OpenTelemetryPlugin
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.middleware.session.base import ONE_DAY_IN_SECONDS
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.security.session_auth import SessionAuth
from litestar.stores.base import Store
from litestar.stores.redis import RedisStore
from litestar.template.config import TemplateConfig
from litestar_saq import SAQConfig, SAQPlugin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.actions.routes import action_router
from app.auth.routes import auth_router
from app.base.models import BaseDBModel
from app.base.routes import system_router
from app.orgs.routes import invite_router
from app.queue.config import queue_config
from app.users.models import User
from app.users.queries import get_user_by_id
from app.users.routes import user_router
from app.utils.configure import Config
from app.utils.deps import get_dependencies
from app.utils.discovery import discover_and_import
from app.utils.exceptions import ApplicationError, exception_to_http_response
from app.utils.logging import create_logging_config

logger = logging.getLogger(__name__)


def _shutdown_otel_if_enabled(config: Config) -> None:
    if config.OTEL_ENABLED:
        from app.utils.otel import shutdown_opentelemetry  # noqa: PLC0415

        shutdown_opentelemetry()


discover_and_import(["deps.py"])


def create_app(
    config: Config,
    *,
    skip_otel_init: bool = False,
    dependencies_overrides: dict | None = None,
    plugins_overrides: list | None = None,
    stores_overrides: dict | None = None,
    retrieve_user_handler_override: Any = None,
) -> Litestar:
    """Create and configure the Litestar application."""
    if not skip_otel_init:
        from app.utils.otel import initialize_opentelemetry  # noqa: PLC0415

        initialize_opentelemetry(config)

    logging_config = create_logging_config(config)

    # ─── CORS ─────────────────────────────────────────────────────────────────
    cors_config = CORSConfig(
        allow_origins=[config.FRONTEND_ORIGIN],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ─── SQLAlchemy ───────────────────────────────────────────────────────────
    # Engine is created explicitly so retrieve_user_handler can share the pool.
    engine = create_async_engine(config.ASYNC_DATABASE_URL)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

    sqlalchemy_plugin = SQLAlchemyPlugin(
        config=SQLAlchemyAsyncConfig(
            engine_instance=engine,
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

    # ─── Session auth ─────────────────────────────────────────────────────────
    async def retrieve_user_handler(session: dict, _conn: ASGIConnection) -> User | None:
        user_id = session.get("user_id")
        if not user_id:
            return None
        async with session_factory() as db:
            return await get_user_by_id(db, user_id)

    stores: dict[str, Store] = {"sessions": RedisStore.with_client(url=config.REDIS_URL)}

    session_auth = SessionAuth[User, Any](
        retrieve_user_handler=retrieve_user_handler_override or retrieve_user_handler,
        session_backend_config=ServerSideSessionConfig(
            store="sessions",
            samesite="lax",
            secure=not config.IS_DEV,
            httponly=True,
            max_age=ONE_DAY_IN_SECONDS * 14,
        ),
        exclude=["^/health", "^/erd", "^/auth/magic-link/", "^/auth/logout", "^/schema", "^/invite"],
    )

    saq_config = SAQConfig(
        queue_configs=queue_config,
        web_enabled=config.IS_DEV,
        use_server_lifespan=True,
    )
    saq_plugin = SAQPlugin(config=saq_config)

    async def _setup_task_queues(app: Litestar) -> None:
        app.state.task_queues = saq_config.get_queues()

    default_plugins: list[Any] = [sqlalchemy_plugin, saq_plugin]

    if config.OTEL_ENABLED:
        default_plugins.append(
            OpenTelemetryPlugin(
                config=OpenTelemetryConfig(
                    tracer_provider=None,
                    meter_provider=None,
                    exclude=["/health"],
                )
            )
        )

    all_plugins = plugins_overrides if plugins_overrides is not None else default_plugins
    all_stores = {**stores, **(stores_overrides or {})}
    all_deps = {**get_dependencies(), **(dependencies_overrides or {})}

    # Only set up SAQ task queues when using real plugins (not in tests)
    on_startup: list[Any] = []
    if plugins_overrides is None:
        on_startup.append(_setup_task_queues)

    return Litestar(
        route_handlers=[system_router, auth_router, action_router, user_router, invite_router],
        plugins=all_plugins,
        on_app_init=[session_auth.on_app_init],
        on_startup=on_startup,
        on_shutdown=[lambda: _shutdown_otel_if_enabled(config)],
        stores=all_stores,
        cors_config=cors_config,
        openapi_config=openapi_config,
        template_config=template_config,
        middleware=[
            session_auth.middleware,
            LoggingMiddlewareConfig(
                exclude=["/health"],
                request_log_fields=["method", "path", "query"],
                response_log_fields=["status_code"],
            ).middleware,
        ],
        dependencies=all_deps,
        exception_handlers={ApplicationError: exception_to_http_response},  # type: ignore[dict-item]
        debug=config.IS_DEV,
        logging_config=logging_config,
    )
