from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from common_models.crud_foundation import CRUDBase
from common_models.models import UserGroup
from common_models.utils import log_and_raise_error


class GroupCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.company_id,
            self.model.group_name,
            self.model.comment,
        ]

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.id == obj_id)
            .options(load_only(*self.load_fields))
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model).options(load_only(*self.load_fields))
        )
        return db_objs.scalars().all()

    async def handle_integrity_error(self, e: IntegrityError) -> None:
        """Обрабатывает ошибки IntegrityError при работе с базой данных."""
        error_message = str(e.orig)
        if "fk_company_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная компания не зарегистрирована в системе.",
                message_log="При попытке создания группы передан неверный id компании.",
            )
        else:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error=f"{error_message}",
                message_log=f"{error_message}",
            )


role_crud = GroupCRUD(UserGroup)
