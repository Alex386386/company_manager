from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error
from settings_dict.crud import setting_dict_crud
from settings_dict.schemas import SettingDictDB


async def get_setting_dict_by_id(
    setting_dict_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> SettingDictDB:
    return await check_exists_and_get_or_return_error(
        db_id=setting_dict_id,
        crud=setting_dict_crud,
        method_name="get",
        error="Данный справочный код настроек не найден!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
