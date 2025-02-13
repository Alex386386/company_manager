from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from functions.crud import function_crud
from functions.schemas import FunctionDB, FunctionWithRolesDB


async def get_function_by_id(
    function_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> FunctionDB:
    return await check_exists_and_get_or_return_error(
        db_id=function_id,
        crud=function_crud,
        method_name="get",
        error="Данная функция не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )


async def get_function_by_id_with_models(
    function_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> FunctionWithRolesDB:
    return await check_exists_and_get_or_return_error(
        db_id=function_id,
        crud=function_crud,
        method_name="get_with_models",
        error="Данная функция не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
