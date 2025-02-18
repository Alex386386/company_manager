from fastapi import status, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload

from common_models.crud_foundation import CRUDBase
from common_models.models import FunctionDict, RoleFunction, RoleDict
from common_models.utils import log_and_raise_error
from functions.schemas import RoleFunctionBase


class FunctionCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.code,
            self.model.version,
        ]
        self.roles_load_fields = [RoleDict.id, RoleDict.code, RoleDict.name]

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
        try:
            db_objs = await session.execute(
                select(self.model).options(load_only(*self.load_fields))
            )
            return db_objs.scalars().all()
        except Exception as e:
            log_and_raise_error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message_error=f"{e}",
                message_log=f"{e}",
            )

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
                selectinload(self.model.roles).load_only(*self.roles_load_fields),
            )
        )
        return db_obj.unique().scalars().first()

    async def handle_integrity_error(self, e: IntegrityError) -> None:
        """Обрабатывает ошибки IntegrityError при работе с базой данных."""
        error_message = str(e.orig)
        if "fk_role_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная роль не зарегистрирована в системе.",
                message_log="При попытке создания связи роли и функции передан неверный id роли.",
            )
        elif "fk_function_code_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная функция не зарегистрирована в системе.",
                message_log="При попытке создания связи роли и функции передан неверный id роли.",
            )
        elif "unique_function_role" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная роль уже привязана к функции.",
                message_log="При попытке создания связи роли и функции возникла ошибка уникальности.",
            )
        else:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error=f"{error_message}",
                message_log=f"{error_message}",
            )

    async def add_role(self, create_data: RoleFunctionBase, session: AsyncSession):
        try:
            new_role = RoleFunction(**create_data.model_dump())
            session.add(new_role)
            await session.commit()
            return {"status": "Связь между ролью и функцией успешно установлена"}
        except IntegrityError as e:
            await session.rollback()
            await self.handle_integrity_error(e)

    @staticmethod
    async def remove_role_from_function(
        role_id: int, function_code_id: int, session: AsyncSession
    ):
        result = await session.execute(
            select(RoleFunction).where(
                and_(
                    RoleFunction.role_id == role_id,
                    RoleFunction.function_code_id == function_code_id,
                )
            )
        )
        obj = result.scalar_one_or_none()

        if obj:
            await session.delete(obj)
            await session.commit()
            return {"status": "Объект успешно удалён из БД"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данного объекта нет в БД")

function_crud = FunctionCRUD(FunctionDict)
