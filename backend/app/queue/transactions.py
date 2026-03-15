"""Transaction helpers for SAQ tasks.

Provides:
  - CommittableTaskError: base class for exceptions that should commit before re-raising
  - task_transaction: async context manager wrapping a single DB transaction
  - @with_transaction: decorator that injects `transaction: AsyncSession` into a task
  - enqueue_after_commit: schedule a task to be enqueued once the session commits
"""

import asyncio
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any

from litestar import Request
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.queue.enums import TaskName


class CommittableTaskError(Exception):
    """Base class for task exceptions that should commit the transaction before re-raising.

    Raise a subclass when a task fails in a way that has already written meaningful
    state to the session (e.g. a FAILED status row) that must be persisted so that
    retries or monitoring can see it.

    Any exception that does NOT inherit from this class will roll back the transaction.
    """


@asynccontextmanager
async def task_transaction(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    """Async context manager that begins a transaction and commits or rolls back.

    Commits on success or on CommittableTaskError (then re-raises).
    Rolls back on all other exceptions.
    """
    async with db_sessionmaker() as session:
        await session.begin()
        try:
            yield session
            await session.commit()
        except CommittableTaskError:
            await session.commit()
            raise
        except Exception:
            await session.rollback()
            raise


def with_transaction(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that injects `transaction: AsyncSession` as a keyword argument.

    The wrapped task function must accept `ctx` as its first positional arg
    and `transaction` as a keyword argument.
    """

    @wraps(fn)
    async def wrapper(ctx: Any, **kwargs: Any) -> Any:
        async with task_transaction(ctx["db_sessionmaker"]) as session:
            return await fn(ctx, transaction=session, **kwargs)

    return wrapper


def enqueue_after_commit(
    transaction: AsyncSession,
    request: Request,
    task_name: TaskName,
    *,
    queue: str = "default",
    **kwargs: Any,
) -> None:
    def _listener(_session: Any) -> None:
        asyncio.ensure_future(request.app.state.task_queues.get(queue).enqueue(task_name, **kwargs))

    event.listen(transaction.sync_session, "after_commit", _listener, once=True)
