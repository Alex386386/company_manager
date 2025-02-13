from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.crud_foundation import CRUDBase
from common_models.models import User


class AuthCRUD(CRUDBase):

    async def get_db_credentials_by_username(self, username: str, session: AsyncSession):
        user_query = await session.execute(
            select(self.model)
            .where(self.model.username == username)
        )
        return user_query.scalars().first()

auth_crud = AuthCRUD(User)
