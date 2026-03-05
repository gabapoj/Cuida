"""Smoke test for the /health endpoint."""

from litestar.testing import AsyncTestClient


async def test_health_returns_ok(client: AsyncTestClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_response_shape(client: AsyncTestClient) -> None:
    response = await client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "ok"
