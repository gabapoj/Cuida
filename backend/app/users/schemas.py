from datetime import datetime

from app.actions.schemas import ActionDTO
from app.base.schemas import BaseSchema


class UserSchema(BaseSchema):
    id: int
    name: str
    email: str
    email_verified: bool
    phone: str | None
    created_at: datetime
    updated_at: datetime
    actions: list[ActionDTO]


class UserUpdateSchema(BaseSchema):
    name: str | None = None
    phone: str | None = None
