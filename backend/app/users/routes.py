from litestar import Router, get
from litestar.exceptions import NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.enums import ActionGroupType
from app.actions.registry import ActionRegistry
from app.auth.guards import requires_session
from app.users.models import User
from app.users.queries import get_users_by_org
from app.users.schemas import UserSchema


@get("/{user_id:int}")
async def get_user(
    user_id: int,
    transaction: AsyncSession,
    action_registry: ActionRegistry,
) -> UserSchema:
    result = await transaction.get(User, user_id)
    if result is None:
        raise NotFoundException()

    action_group = action_registry.get_class(ActionGroupType.UserActions)
    actions = action_group.get_available_actions(obj=result)

    return UserSchema(
        id=result.id,
        name=result.name,
        email=result.email,
        email_verified=result.email_verified,
        phone=result.phone,
        created_at=result.created_at,
        updated_at=result.updated_at,
        actions=actions,
    )


@get("")
async def list_users(
    user: User,
    transaction: AsyncSession,
    action_registry: ActionRegistry,
) -> list[UserSchema]:
    users = await get_users_by_org(transaction, user.organization_id)
    action_group = action_registry.get_class(ActionGroupType.UserActions)

    return [
        UserSchema(
            id=u.id,
            name=u.name,
            email=u.email,
            email_verified=u.email_verified,
            phone=u.phone,
            created_at=u.created_at,
            updated_at=u.updated_at,
            actions=action_group.get_available_actions(obj=u),
        )
        for u in users
    ]


user_router = Router(
    path="/users",
    route_handlers=[get_user, list_users],
    guards=[requires_session],
    tags=["users"],
)
