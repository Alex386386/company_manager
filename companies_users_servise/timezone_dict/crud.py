from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from common_models.crud_foundation import CRUDBase
from common_models.models import TimezoneDict


class TimezoneDictCRUD(CRUDBase):
    def __init__(self, model):
        super().__init__(model)
        self.load_fields = [
            self.model.id,
            self.model.timezone_name,
            self.model.timezone
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


timezone_dict_crud = TimezoneDictCRUD(TimezoneDict)
