from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.base import BaseObjectAction, action_group_factory
from app.actions.deps import ActionDeps
from app.actions.enums import ActionGroupType, ActionIcon
from app.actions.schemas import ActionExecutionResponse
from app.users.enums import UserActions
from app.users.models import User
from app.users.schemas import UserUpdateSchema
from app.utils.db import update_model

user_actions = action_group_factory(ActionGroupType.UserActions, model_type=User)


@user_actions
class UpdateUser(BaseObjectAction[User, UserUpdateSchema]):
    action_key = UserActions.update
    label = "Edit Profile"
    priority = 50
    icon = ActionIcon.edit

    @classmethod
    def is_available(cls, obj: User | None, deps: ActionDeps) -> bool:
        return obj is not None and deps.user is not None and obj.id == deps.user.id

    @classmethod
    async def execute(
        cls, obj: User, data: UserUpdateSchema, transaction: AsyncSession, deps: ActionDeps
    ) -> ActionExecutionResponse:
        await update_model(session=transaction, model_instance=obj, update_vals=data)
        return ActionExecutionResponse(message="Profile updated")
