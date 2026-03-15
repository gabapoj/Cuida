from app.utils.exceptions import ApplicationError


class InvalidInvitationError(ApplicationError):
    status_code = 400
    detail = "Invitation is invalid or has expired"


class DuplicateInvitationError(ApplicationError):
    status_code = 409
    detail = "An invitation has already been sent to this address"
