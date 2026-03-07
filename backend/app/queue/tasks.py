"""Placeholder task — verifies the SAQ queue system is wired correctly."""

from app.queue.registry import task
from app.queue.types import AppContext


@task
async def health_check_task(ctx: AppContext) -> dict[str, str]:
    """Smoke-test task: enqueue this to confirm the worker is alive."""
    return {"status": "ok"}
