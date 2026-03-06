"""Test configuration and fixtures.

Sets ENV=testing before any app imports so get_config() returns TestConfig,
which points at the test database on port 5433.
"""

import os

# Must be set before app imports — config is instantiated at import time
os.environ.setdefault("ENV", "testing")
os.environ.setdefault("DB_PORT", "5433")  # test DB port

from collections.abc import AsyncGenerator  # noqa: E402

import pytest  # noqa: E402
from litestar import Litestar  # noqa: E402
from litestar.testing import AsyncTestClient  # noqa: E402

from app.index import app  # noqa: E402


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncTestClient[Litestar]]:
    """Async test client for the Litestar app.

    Starts the full Litestar app (including SQLAlchemy plugin) against the
    test database. Requires `just db-start` to have been run first.
    """
    async with AsyncTestClient(app=app) as c:
        yield c
