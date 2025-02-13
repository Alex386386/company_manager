from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from role_dicts.crud import role_dict_crud
from role_dicts.schemas import RoleDictDB


async def get_role_dict_by_id(
    role_dict_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> RoleDictDB:
    return await check_exists_and_get_or_return_error(
        db_id=role_dict_id,
        crud=role_dict_crud,
        method_name="get",
        error="Данная роль не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
