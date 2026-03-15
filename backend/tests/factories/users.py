"""Factories for user-domain models."""

from datetime import UTC, datetime

from polyfactory import Use

from app.users.models import Organization, User

from .base import BaseFactory


class OrgFactory(BaseFactory):
    __model__ = Organization

    name = Use(BaseFactory.__faker__.company)
    created_at = Use(BaseFactory.__faker__.date_time_between, start_date="-1y", end_date="now", tzinfo=UTC)
    updated_at = Use(lambda: datetime.now(tz=UTC))
    deleted_at = None


class UserFactory(BaseFactory):
    __model__ = User

    name = Use(BaseFactory.__faker__.name)
    email = Use(BaseFactory.__faker__.email)
    email_verified = False
    phone = None
    address_id = None
    report_schedule_id = None
    created_at = Use(BaseFactory.__faker__.date_time_between, start_date="-1y", end_date="now", tzinfo=UTC)
    updated_at = Use(lambda: datetime.now(tz=UTC))
    deleted_at = None
