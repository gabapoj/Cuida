"""Litestar application and test client fixtures."""

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from litestar import Litestar
from litestar.connection import ASGIConnection
from litestar.di import Provide
from litestar.middleware.session.server_side import ServerSideSessionConfig
from litestar.stores.memory import MemoryStore
from litestar.testing import AsyncTestClient
from litestar_saq import TaskQueues
from sqlalchemy.ext.asyncio import AsyncSession

from app.factory import create_app
from app.users.models import User
from app.users.queries import get_user_by_id
from app.utils.configure import TestConfig


@pytest.fixture
def test_app(test_config: TestConfig, db_session: AsyncSession) -> Litestar:
    """Litestar app configured for testing.

    Overrides:
    - db_session / transaction: shared test session with savepoint isolation
    - retrieve_user_handler: uses shared session (test fixtures are uncommitted)
    - task_queues: mock (no Redis workers)
    - sessions store: MemoryStore (no Redis)
    - plugins: empty (no SQLAlchemy plugin, no SAQ plugin)
    """

    def provide_shared_db_session() -> AsyncSession:
        return db_session

    async def provide_test_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession]:  # type: ignore[override]
        yield db_session

    def provide_test_task_queues() -> Any:
        mock_queue = Mock()
        mock_queue.enqueue = AsyncMock(return_value=None)
        return TaskQueues({"default": mock_queue})

    async def retrieve_user_handler_test(session: dict, _conn: ASGIConnection) -> User | None:
        user_id = session.get("user_id")
        if not user_id:
            return None
        return await get_user_by_id(db_session, user_id)

    return create_app(
        config=test_config,
        skip_otel_init=True,
        retrieve_user_handler_override=retrieve_user_handler_test,
        dependencies_overrides={
            "db_session": Provide(provide_shared_db_session, sync_to_thread=False),
            "transaction": Provide(provide_test_transaction),
            "task_queues": Provide(provide_test_task_queues, sync_to_thread=False),
        },
        plugins_overrides=[],
        stores_overrides={"sessions": MemoryStore()},
    )


@pytest.fixture
async def test_client(test_app: Litestar) -> AsyncGenerator[AsyncTestClient[Litestar]]:
    session_config = ServerSideSessionConfig(store="sessions", samesite="lax", secure=False, httponly=True)
    async with AsyncTestClient(app=test_app, session_config=session_config, raise_server_exceptions=True) as client:
        yield client
        try:
            await client.set_session_data({})
        except Exception:
            pass


@pytest.fixture
async def authenticated_client(
    test_client: AsyncTestClient[Litestar],
    user,
) -> AsyncGenerator[AsyncTestClient[Litestar]]:
    await test_client.set_session_data({"user_id": user.id})
    yield test_client
