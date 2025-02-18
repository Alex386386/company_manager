from fastapi import status, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only

from common_models.crud_foundation import CRUDBase
from common_models.models import Company, CompanyProperty, PropertyCodeDict
from common_models.utils import log_and_raise_error


class CompanyCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.name,
            self.model.inn,
            self.model.kpp,
            self.model.ogrn,
            self.model.bic,
            self.model.created_date
        ]
        self.properties_load_fields = [
            PropertyCodeDict.id, PropertyCodeDict.group_code, PropertyCodeDict.code, PropertyCodeDict.name
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
        try:
            db_objs = await session.execute(
                select(self.model)
                .options(load_only(*self.load_fields))
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
                selectinload(self.model.properties).load_only(*self.properties_load_fields)
            )
        )
        return db_obj.unique().scalars().first()

    async def handle_integrity_error(self, e: IntegrityError) -> None:
        """Обрабатывает ошибки IntegrityError при работе с базой данных."""
        error_message = str(e.orig)
        if "fk_property_code_id" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данное свойство не зарегистрирована в системе.",
                message_log="При попытке создания компании передан неверный id свойства.",
            )
        elif "fk_property_code_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данное свойство не зарегистрирована в системе.",
                message_log="При попытке создания связи компании и свойства передан неверный id свойства.",
            )
        elif "fk_company_id_secondary" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данная компания не зарегистрирована в системе.",
                message_log="При попытке создания связи компании и свойства передан неверный id компании.",
            )
        elif "unique_company_property" in error_message:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error="Данное свойство уже привязано к компании.",
                message_log="При попытке создания связи компании и свойства возникла ошибка уникальности.",
            )
        else:
            log_and_raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message_error=f"{error_message}",
                message_log=f"{error_message}",
            )

    async def add_property(self, company_id: int, property_code_id: int, value: str | None, session: AsyncSession):
        try:
            new_property = CompanyProperty(
                company_id=company_id,
                property_code_id=property_code_id,
                value=value,
            )
            session.add(new_property)
            await session.commit()
            return {"status": "Связь между компанией и зависимостью успешно установлена"}
        except IntegrityError as e:
            await session.rollback()
            await self.handle_integrity_error(e)

    @staticmethod
    async def remove_property_from_company(company_id: int, property_code_id: int, session: AsyncSession):
        result = await session.execute(select(CompanyProperty).where(
            and_(
                CompanyProperty.company_id == company_id,
                CompanyProperty.property_code_id == property_code_id,
            )
        ))
        obj = result.scalar_one_or_none()

        if obj:
            await session.delete(obj)
            await session.commit()
            return {"status": "Объект успешно удалён из БД"}

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данного объекта нет в БД")


company_crud = CompanyCRUD(Company)
