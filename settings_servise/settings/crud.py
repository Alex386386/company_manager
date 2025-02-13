from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload

from common_models.crud_foundation import CRUDBase
from common_models.models import Setting, SettingDict
from common_models.utils import log_and_raise_error


class SettingCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.setting_code_id,
            self.model.value,
            self.model.active_from,
            self.model.active_to,
        ]
        self.setting_code_load_fields = [
            SettingDict.id,
            SettingDict.code,
            SettingDict.name,
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

    async def get_with_models(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.id == obj_id)
            .options(
                load_only(*self.load_fields),
                joinedload(self.model.setting_code).load_only(
                    *self.setting_code_load_fields
                ),
            )
        )
        return db_obj.unique().scalars().first()

    async def handle_integrity_error(self, e: IntegrityError) -> None:
        """Обрабатывает ошибки IntegrityError при работе с базой данных."""
        error_message = str(e.orig)
        if "fk_setting_code_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данный код не зарегистрирован в системе.",
                message_log="При попытке создания свойства передан неверный id кода.",
            )
        else:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error=f"{error_message}",
                message_log=f"{error_message}",
            )


setting_crud = SettingCRUD(Setting)
