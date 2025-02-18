from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from common_models.crud_foundation import CRUDBase
from common_models.models import PropertyCodeDict
from common_models.utils import log_and_raise_error


class PropertyCodeDictCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.group_code,
            self.model.code,
            self.model.name,
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


property_code_dict_crud = PropertyCodeDictCRUD(PropertyCodeDict)
