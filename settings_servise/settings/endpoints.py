from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from settings.crud import setting_crud
from settings.dependencies import get_setting_by_id, get_setting_by_id_with_models
from settings.schemas import SettingCreate, SettingUpdate, SettingDB, SettingWithModelsDB

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{setting_id}",
    response_model=SettingWithModelsDB,
)
async def get_setting(setting: SettingWithModelsDB = Depends(get_setting_by_id_with_models)):
    return setting


@router.get(
    "/get-all",
    response_model=list[SettingDB],
)
async def get_settings(
    session: AsyncSession = Depends(get_async_session),
) -> list[SettingDB]:
    return await setting_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=SettingDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_setting(
    setting_data: SettingCreate,
    session: AsyncSession = Depends(get_async_session),
) -> SettingDB:
    return await setting_crud.create(create_data=setting_data, session=session)


@router.patch(
    "/update/{setting_id}",
    response_model=SettingDB,
)
async def update_setting(
    setting_data: SettingUpdate,
    setting: SettingDB = Depends(get_setting_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> SettingDB:
    return await setting_crud.update(db_obj=setting, obj_in=setting_data, session=session)


@router.delete("/delete/{setting_id}")
async def delete_setting(
    setting: SettingDB = Depends(get_setting_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await setting_crud.remove(db_obj=setting, session=session)
