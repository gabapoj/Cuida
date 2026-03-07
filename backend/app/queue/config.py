"""SAQ queue configuration.

Wires up the queue startup hook, auto-discovers task modules, and builds the
QueueConfig list consumed by SAQPlugin in factory.py.
"""

import logging
from datetime import UTC
from typing import cast

from litestar_saq import QueueConfig
from saq.types import ReceivesContext
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.queue.registry import get_registry
from app.queue.types import AppContext
from app.utils.configure import config
from app.utils.discovery import discover_and_import

logger = logging.getLogger(__name__)


async def queue_startup(ctx: AppContext) -> None:  # type: ignore[override]
    """SAQ startup hook — inject shared resources into the task context."""
    engine = create_async_engine(
        config.ASYNC_DATABASE_URL,
        pool_size=0,  # no persistent connections — tasks are short-lived
        max_overflow=5,
    )
    ctx["db_sessionmaker"] = async_sessionmaker(engine, expire_on_commit=False)
    ctx["config"] = config
    logger.info("Queue worker started — DB sessionmaker injected into context")


# Trigger @task / @scheduled_task decorator registration across all tasks.py files
discover_and_import(["tasks.py"], base_path="app")

registry = get_registry()


def get_queue_config() -> list[QueueConfig]:
    return [
        QueueConfig(
            name="default",
            dsn=config.REDIS_URL,
            tasks=registry.get_all_tasks(),
            scheduled_tasks=registry.get_all_scheduled_tasks(),  # type: ignore[reportArgumentType]
            cron_tz=UTC,
            startup=cast(ReceivesContext, queue_startup),
            concurrency=10,
        )
    ]


queue_config = get_queue_config()
