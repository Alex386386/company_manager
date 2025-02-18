from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from settings_dict.crud import setting_dict_crud
from settings_dict.dependencies import get_setting_dict_by_id
from settings_dict.schemas import SettingDictCreate, SettingDictUpdate, SettingDictDB

router = APIRouter(
    prefix="/setting_dicts",
    tags=["Setting_dicts"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{setting_dict_id}",
    response_model=SettingDictDB,
)
async def get_setting_dict(setting_dict: SettingDictDB = Depends(get_setting_dict_by_id)):
    return setting_dict


@router.get(
    "/get-all",
    response_model=list[SettingDictDB],
)
async def get_setting_dicts(
    session: AsyncSession = Depends(get_async_session),
) -> list[SettingDictDB]:
    return await setting_dict_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=SettingDictDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_setting_dict(
    setting_dict_data: SettingDictCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SettingDictDB:
    return await setting_dict_crud.create(create_data=setting_dict_data, session=session)


@router.patch(
    "/update/{setting_dict_id}",
    response_model=SettingDictDB,
)
async def update_setting_dict(
    setting_dict_data: SettingDictUpdate,
    setting_dict: SettingDictDB = Depends(get_setting_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> SettingDictDB:
    return await setting_dict_crud.update(db_obj=setting_dict, obj_in=setting_dict_data, session=session)


@router.delete("/delete/{setting_dict_id}")
async def delete_setting_dict(
    setting_dict: SettingDictDB = Depends(get_setting_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await setting_dict_crud.remove(db_obj=setting_dict, session=session)
