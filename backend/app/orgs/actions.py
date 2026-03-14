from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.base import BaseTopLevelAction, action_group_factory
from app.actions.deps import ActionDeps
from app.actions.enums import ActionGroupType, ActionIcon
from app.actions.schemas import ActionExecutionResponse
from app.orgs.enums import OrgActions
from app.orgs.exceptions import DuplicateInvitationError
from app.orgs.schemas import InviteUserSchema
from app.orgs.service import OrgService

org_actions = action_group_factory(ActionGroupType.ORG_ACTIONS)


@org_actions
class InviteUser(BaseTopLevelAction[InviteUserSchema]):
    action_key = OrgActions.INVITE_USER
    label = "Invite User"
    icon = ActionIcon.ADD
    priority = 10

    @classmethod
    def is_available(cls, obj, deps: ActionDeps) -> bool:
        return deps.user is not None

    @classmethod
    async def execute(
        cls, data: InviteUserSchema, transaction: AsyncSession, deps: ActionDeps
    ) -> ActionExecutionResponse:
        org_service = OrgService(transaction, deps.email_service)
        try:
            await org_service.invite_user(data.email, invited_by=deps.user)
        except DuplicateInvitationError:
            return ActionExecutionResponse(message="Invitation already sent")
        return ActionExecutionResponse(message="Invitation sent")
