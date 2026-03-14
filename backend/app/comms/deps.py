from litestar import Request

from app.comms.service.emails import BaseEmailClient, EmailService, LocalEmailClient, SESEmailClient
from app.utils.configure import config
from app.utils.deps import dep


@dep("email_client", sync_to_thread=False)
def provide_email_client() -> BaseEmailClient:
    if config.ALLOW_LOCAL_SES or not config.IS_DEV:
        return SESEmailClient(config)
    return LocalEmailClient()


@dep("email_service", sync_to_thread=False)
def provide_email_service(
    email_client: BaseEmailClient,
    request: Request,
) -> EmailService:
    return EmailService(email_client, request.app.template_engine)  # type: ignore[arg-type]
