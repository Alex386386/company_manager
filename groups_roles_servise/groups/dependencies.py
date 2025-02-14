from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from groups.crud import role_crud
from groups.schemas import GroupDB


async def get_group_by_id(
    group_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> GroupDB:
    return await check_exists_and_get_or_return_error(
        db_id=group_id,
        crud=role_crud,
        method_name="get",
        error="Данная группа не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
