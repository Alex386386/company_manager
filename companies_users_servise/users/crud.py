from fastapi import status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only

from common_models.crud_foundation import CRUDBase
from common_models.models import User, UserRole, RoleDict
from common_models.pwd_context import get_password_hash
from common_models.utils import log_and_raise_error
from users.schemas import UserCreate, UserUpdate, UserRoleBase


class UserCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.company_id,
            self.model.group_id,
            self.model.timezone_id,
            self.model.username,
            self.model.firstname,
            self.model.lastname,
            self.model.patronymic,
            self.model.user_lock,
            self.model.created_date,
            self.model.comment
        ]
        self.roles_load_fields = [
            RoleDict.id, RoleDict.code, RoleDict.name
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
            select(self.model)
            .options(load_only(*self.load_fields))
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
            .options(load_only(*self.load_fields), selectinload(self.model.roles).load_only(*self.roles_load_fields))
        )
        return db_obj.unique().scalars().first()

    async def handle_integrity_error(self, e: IntegrityError) -> None:
        """Обрабатывает ошибки IntegrityError при работе с базой данных."""
        error_message = str(e.orig)
        if "fk_company_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная компания не зарегистрирована в системе.",
                message_log="При попытке создания пользователя передан неверный id компании.",
            )
        elif "fk_group_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная группа не зарегистрирована в системе.",
                message_log="При попытке создания пользователя передан неверный id группы.",
            )
        elif "fk_timezone_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная таймзона не зарегистрирована в системе.",
                message_log="При попытке создания пользователя передан неверный id таймзоны.",
            )
        elif "fk_user_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данного юзера нет в системе.",
                message_log="При попытке создания связи юзера и роли передан неверный id юзера.",
            )
        elif "fk_role_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данной роли нет в системе.",
                message_log="При попытке создания связи юзера и роли передан неверный id роли.",
            )
        elif "unique_user_role" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная роль уже привязана к юзеру.",
                message_log="При попытке создания связи юзера и роли возникла ошибка уникальности.",
            )
        else:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error=f"{error_message}",
                message_log=f"{error_message}",
            )

    async def create(self, create_data: UserCreate, session: AsyncSession):
        create_data = create_data.model_dump()
        hashed_password = get_password_hash(create_data["password"])
        create_data["password"] = hashed_password
        user = self.model(**create_data)
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError as e:
            await session.rollback()
            await self.handle_integrity_error(e)

    async def update(
        self,
        db_obj: User,
        obj_in: UserUpdate,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password", None) is not None:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        try:
            await session.commit()
            await session.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await session.rollback()
            await self.handle_integrity_error(e)

    async def add_role(self, create_data: UserRoleBase, session: AsyncSession):
        try:
            new_role = UserRole(**create_data.model_dump())
            session.add(new_role)
            await session.commit()
            return {"status": "Связь между ролью и пользователем успешно установлена"}
        except IntegrityError as e:
            await session.rollback()
            await self.handle_integrity_error(e)

    @staticmethod
    async def remove_role_from_user(user_id: int, role_id: int, session: AsyncSession):
        result = await session.execute(select(UserRole).where(
            and_(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
        ))
        obj = result.scalar_one_or_none()

        if obj:
            await session.delete(obj)
            await session.commit()
            return True

        return False


user_crud = UserCRUD(User)
