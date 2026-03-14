"""Typed dependencies for actions."""

from dataclasses import dataclass

from litestar import Request
from litestar_saq import TaskQueues
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.registry import ActionRegistry
from app.emails.service import EmailService
from app.users.models import User
from app.utils.configure import Config, config
from app.utils.deps import dep


@dataclass
class ActionDeps:
    """Typed dependencies available to all actions."""

    user: User
    request: Request
    transaction: AsyncSession
    config: Config
    email_service: EmailService
    task_queues: TaskQueues


@dep("action_registry", sync_to_thread=False)
def provide_action_registry(
    db_session: AsyncSession,
    request: Request,
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
