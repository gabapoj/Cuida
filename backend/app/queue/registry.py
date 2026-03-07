"""Task registry — @task and @scheduled_task decorators.

Tasks registered here are picked up by queue/config.py and passed to SAQ's
QueueConfig at startup. Register a task by decorating an async function:

    @task
    async def my_task(ctx: AppContext, *, arg: str) -> None:
        ...

    @scheduled_task(cron="0 * * * *")
    async def hourly_task(ctx: AppContext) -> None:
        ...
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from saq import CronJob
from saq.types import Function


@dataclass
class TaskRegistry:
    _tasks: list[Function] = field(default_factory=list)
    _scheduled_tasks: list[CronJob] = field(default_factory=list)

    def get_all_tasks(self) -> list[Function]:
        return list(self._tasks)

    def get_all_scheduled_tasks(self) -> list[CronJob]:
        return list(self._scheduled_tasks)


_registry = TaskRegistry()


def get_registry() -> TaskRegistry:
    return _registry


def task(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Register fn as a plain background task."""
    _registry._tasks.append(fn)
    return fn


def scheduled_task(cron: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Register fn as a cron-scheduled task.

    Args:
        cron: Cron expression (e.g., "0 * * * *" for every hour).
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        _registry._scheduled_tasks.append(CronJob(function=fn, cron=cron))
        return fn

    return decorator
