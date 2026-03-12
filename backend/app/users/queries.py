from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Organization, User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_users_by_org(db: AsyncSession, organization_id: int) -> list[User]:
    result = await db.execute(
        select(User).where(
            User.organization_id == organization_id,
            User.deleted_at.is_(None),
        )
    )
    return list(result.scalars().all())


async def create_organization(db: AsyncSession, name: str) -> Organization:
    org = Organization(name=name)
    db.add(org)
    await db.flush()
    return org


async def create_user(db: AsyncSession, *, name: str, email: str, organization_id: int) -> User:
    user = User(name=name, email=email, email_verified=False, organization_id=organization_id)
    db.add(user)
    await db.flush()
    return user
