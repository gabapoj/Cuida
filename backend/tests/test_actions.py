"""Tests for the actions framework."""

from litestar.testing import AsyncTestClient


class TestOrgActions:
    async def test_list_top_level_org_actions(self, authenticated_client: AsyncTestClient):
        """GET /actions/org_actions returns top-level actions (no object context)."""
        response = await authenticated_client.get("/actions/org_actions")
        assert response.status_code == 200

        actions = response.json().get("actions", [])
        action_keys = [a["action"] for a in actions]
        assert "org_actions__invite_user" in action_keys

    async def test_execute_invite_user_action(self, authenticated_client: AsyncTestClient):
        """POST /actions/org_actions executes InviteUser."""
        response = await authenticated_client.post(
            "/actions/org_actions",
            json={"action": "org_actions__invite_user", "data": {"email": "newuser@example.com"}},
        )
        assert response.status_code in [200, 201]
        assert response.json().get("message") is not None


class TestUserActions:
    async def test_list_user_object_actions(self, authenticated_client: AsyncTestClient, user):
        """GET /actions/user_actions/{id} returns object actions for the user."""
        response = await authenticated_client.get(f"/actions/user_actions/{user.id}")
        assert response.status_code == 200

        actions = response.json().get("actions", [])
        action_keys = [a["action"] for a in actions]
        assert "user_actions__update" in action_keys

    async def test_execute_update_user_action(self, authenticated_client: AsyncTestClient, user):
        """POST /actions/user_actions/{id} updates the user."""
        response = await authenticated_client.post(
            f"/actions/user_actions/{user.id}",
            json={"action": "user_actions__update", "data": {"name": "Updated Name"}},
        )
        assert response.status_code in [200, 201]
        assert response.json().get("message") is not None
