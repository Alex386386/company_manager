from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from settings.crud import setting_crud
from settings.schemas import SettingDB, SettingWithModelsDB


async def get_setting_by_id(
    setting_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> SettingDB:
    return await check_exists_and_get_or_return_error(
        db_id=setting_id,
        crud=setting_crud,
        method_name="get",
        error="Данное свойство не найдено!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )

async def get_setting_by_id_with_models(
    setting_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> SettingWithModelsDB:
    return await check_exists_and_get_or_return_error(
        db_id=setting_id,
        crud=setting_crud,
        method_name="get_with_models",
        error="Данное свойство не найдено!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
