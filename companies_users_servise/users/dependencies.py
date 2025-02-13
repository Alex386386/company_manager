from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from users.crud import user_crud
from users.schemas import UserDB, UserWithRolesDB


async def get_user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> UserDB:
    return await check_exists_and_get_or_return_error(
        db_id=user_id,
        crud=user_crud,
        method_name="get",
        error="Пользователь не найден!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )


async def get_user_by_id_with_models(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> UserWithRolesDB:
    return await check_exists_and_get_or_return_error(
        db_id=user_id,
        crud=user_crud,
        method_name="get_with_models",
        error="Пользователь не найден!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )