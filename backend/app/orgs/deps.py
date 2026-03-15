from sqlalchemy.ext.asyncio import AsyncSession

from app.comms.service.emails import EmailService
from app.orgs.service import OrgService
from app.utils.deps import dep


@dep("org_service", sync_to_thread=False)
def provide_org_service(
    transaction: AsyncSession,
    email_service: EmailService,
) -> OrgService:
    return OrgService(transaction, email_service)
