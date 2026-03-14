from typing import Any

from litestar import Request
from litestar.exceptions import NotAuthorizedException

from app.users.models import User


def provide_current_user(request: Request[User | None, Any, Any]) -> User:
    if request.user is None:
        raise NotAuthorizedException()
    return request.user
