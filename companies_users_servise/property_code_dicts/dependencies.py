from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from property_code_dicts.crud import property_code_dict_crud
from property_code_dicts.schemas import PropertyCodeDictDB
from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error


async def get_property_code_dict_by_id(
    property_code_dict_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> PropertyCodeDictDB:
    return await check_exists_and_get_or_return_error(
        db_id=property_code_dict_id,
        crud=property_code_dict_crud,
        method_name="get",
        error="Данная функция не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
