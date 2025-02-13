from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from timezone_dict.crud import timezone_dict_crud
from timezone_dict.schemas import TimezoneDictDB
from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error


async def get_timezone_dict_by_id(
    timezone_dict_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> TimezoneDictDB:
    return await check_exists_and_get_or_return_error(
        db_id=timezone_dict_id,
        crud=timezone_dict_crud,
        method_name="get",
        error="Такой таймзоны нет в системе!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )