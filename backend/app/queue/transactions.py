import asyncio
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, cast

from litestar import Request
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.comms.clients.email import LocalEmailClient, SESEmailClient
from app.queue.enums import TaskName
from app.queue.exceptions import CommittableTaskError
from app.queue.registry import get_registry
from app.queue.types import AppContext
from app.utils.configure import config


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

    If `transaction` is already present in kwargs (e.g. passed by dispatch_task in
    sync mode), the function is called directly — the caller owns the session lifecycle.
    """

    @wraps(fn)
    async def wrapper(ctx: Any, **kwargs: Any) -> Any:
        if "transaction" in kwargs:
            return await fn(ctx, **kwargs)
        async with task_transaction(ctx["db_sessionmaker"]) as session:
            return await fn(ctx, transaction=session, **kwargs)

    return wrapper


async def dispatch_task(
    transaction: AsyncSession,
    request: Request,
    task_name: TaskName,
    *,
    queue: str = "default",
    **kwargs: Any,
) -> None:
    """Dispatch a task either inline (QUEUE_SYNC=true) or via the SAQ queue.

    In sync mode the task runs immediately, reusing the caller's session so no
    extra DB connection or commit is needed. If the task raises, the exception
    propagates and the outer transaction rolls back.

    In async mode the task is enqueued after the session commits.
    """
    if config.QUEUE_SYNC:
        fn = get_registry().get_task_by_name(task_name)
        if fn is None:
            raise ValueError(f"No task registered for {task_name!r}")
        email_client: LocalEmailClient | SESEmailClient = (
            SESEmailClient(config) if config.ALLOW_LOCAL_SES or not config.IS_DEV else LocalEmailClient()
        )
        ctx = cast(AppContext, {"config": config, "email_client": email_client})
        await fn(ctx, transaction=transaction, **kwargs)
    else:

        def _listener(_session: Any) -> None:
            asyncio.ensure_future(request.app.state.task_queues.get(queue).enqueue(task_name, **kwargs))

        event.listen(transaction.sync_session, "after_commit", _listener, once=True)
