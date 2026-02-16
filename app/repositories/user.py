from .base import CRUDBase
from sqlalchemy import select
from app.models import User, Role
from sqlalchemy.orm import selectinload

class CRUDUser(CRUDBase[User, None, None]):

    async def get_by_email(self, db, email: str) -> User:
        result = await db.execute(
            select(self.model).filter(User.email == email)
            .options(
                selectinload(User.role).selectinload(Role.permissions) # eager load
            )
            .execution_options(populate_existing=False) # disable tracking
        )
        return result.scalars().first()


user_crud = CRUDUser(User)