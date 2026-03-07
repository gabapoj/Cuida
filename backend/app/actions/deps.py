"""Typed dependencies for actions."""

from dataclasses import dataclass

from litestar import Request
from litestar_saq import TaskQueues
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.registry import ActionRegistry
from app.emails.service import EmailService
from app.utils.configure import Config


@dataclass
class ActionDeps:
    """Typed dependencies available to all actions.

    These dependencies are injected by the ActionRegistry and provide
    access to common services like database, queues, and request context.
    """

    # Request context
    user: int | None
    request: Request

    # Database
    transaction: AsyncSession

    # Services
    config: Config
    email_service: EmailService
    task_queues: TaskQueues


def provide_action_registry(
    db_session: AsyncSession,
    config: Config,
    request: Request,
    email_service: EmailService,
    task_queues: TaskQueues,
) -> ActionRegistry:
    return ActionRegistry(
        transaction=db_session,
        config=config,
        request=request,
        user=request.user,
        email_service=email_service,
        task_queues=task_queues,
    )
