from sqlalchemy import Boolean, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base.models import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "users"
    __table_args__ = (Index("ix_users_email", "email", unique=True),)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
