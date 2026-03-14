"""Typed dependencies for actions."""

from dataclasses import dataclass
from typing import Any

from litestar import Request
from litestar_saq import TaskQueues
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.registry import ActionRegistry
from app.emails.service import EmailService
from app.users.models import User
from app.utils.configure import Config, config


@dataclass
class ActionDeps:
    """Typed dependencies available to all actions.

    These dependencies are injected by the ActionRegistry and provide
    access to common services like database, queues, and request context.
    """

    # Request context
    user: User
    request: Request[User, Any, Any]

    # Database
    transaction: AsyncSession

    # Services
    config: Config
    email_service: EmailService
    task_queues: TaskQueues


def provide_action_registry(
    db_session: AsyncSession,
    request: Request[User, Any, Any],
    user: User,
    email_service: EmailService,
    task_queues: TaskQueues,
) -> ActionRegistry:
    return ActionRegistry(
        transaction=db_session,
        config=config,
        request=request,
        user=user,
        email_service=email_service,
        task_queues=task_queues,
    )
