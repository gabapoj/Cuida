from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.queries import create_organization, create_user, get_user_by_email, get_user_by_id


class UserService:
    def __init__(self, transaction: AsyncSession) -> None:
        self.db = transaction

    async def get_by_id(self, user_id: int) -> User | None:
        return await get_user_by_id(self.db, user_id)

    async def get_or_create_by_email(self, email: str) -> tuple[User, bool]:
        """Return (user, created). If new, auto-creates a personal org."""
        user = await get_user_by_email(self.db, email)
        if user is not None:
            return user, False

        name = email.split("@")[0]
        org = await create_organization(self.db, name=f"{name}'s Organization")
        user = await create_user(self.db, name=name, email=email, organization_id=org.id)
        return user, True


def provide_user_service(transaction: AsyncSession) -> UserService:
    return UserService(transaction)
