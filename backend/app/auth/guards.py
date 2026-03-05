from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def requires_session(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Guard: requires an authenticated session (user_id in session)."""
    if not connection.session.get("user_id"):
        raise NotAuthorizedException("Authentication required")
