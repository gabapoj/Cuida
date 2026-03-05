# Tests

Backend tests using **pytest** + **pytest-asyncio** + Litestar's **AsyncTestClient**.

## Running Tests

```bash
# From project root
just test

# From backend/
cd backend && uv run pytest -v

# Single file
cd backend && uv run pytest tests/test_health.py -v

# With coverage
cd backend && uv run pytest --cov=app --cov-report=term-missing
```

## Requirements

Tests run against the **test database** on port 5433. Start services first:

```bash
just db-start    # starts postgres (5432 + 5433) and redis
just db-upgrade  # runs migrations on dev DB
# test DB migrations run automatically via conftest fixtures
```

## Patterns

### AsyncTestClient

`conftest.py` provides an `AsyncTestClient` fixture scoped to the function.
This starts the full Litestar app (including SQLAlchemy plugin) for each test.

```python
async def test_something(client: AsyncTestClient) -> None:
    response = await client.get("/endpoint")
    assert response.status_code == 200
```

### Database fixtures

For tests that need DB state, use the `AsyncSession` directly:

```python
@pytest.fixture
async def db_session(client: AsyncTestClient):
    # The SQLAlchemy plugin manages session lifecycle
    # Access via dependency injection in route handlers
    ...
```

### Overriding dependencies

```python
from litestar.testing import AsyncTestClient

app.dependency_overrides["some_dep"] = lambda: MockDep()
async with AsyncTestClient(app=app) as client:
    ...
```

## Adding Tests

- Place test files in `tests/` with `test_` prefix
- One test file per app module (e.g., `test_users.py`, `test_calls.py`)
- Use `async def` for all test functions (pytest-asyncio handles the event loop)
