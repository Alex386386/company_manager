from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from common_models.utils import log_and_raise_error
from property_code_dicts.crud import property_code_dict_crud
from property_code_dicts.dependencies import get_property_code_dict_by_id
from property_code_dicts.schemas import (
    PropertyCodeDictDB,
    PropertyCodeDictCreate,
    PropertyCodeDictUpdate
)

router = APIRouter(
    prefix="/property_code_dicts",
    tags=["Property_code_dicts"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{property_code_dict_id}",
    response_model=PropertyCodeDictDB,
)
async def get_property_code_dict(property_code_dict: PropertyCodeDictDB = Depends(get_property_code_dict_by_id)):
    return property_code_dict


@router.get(
    "/get-all",
    response_model=list[PropertyCodeDictDB],
)
async def get_property_code_dicts(
    session: AsyncSession = Depends(get_async_session),
) -> list[PropertyCodeDictDB]:
    try:
        return await property_code_dict_crud.get_multi(session=session)
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error=f"{e}",
            message_log=f"{e}",
        )


@router.post(
    "/create",
    response_model=PropertyCodeDictDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_property_code_dict(
    property_code_dict_data: PropertyCodeDictCreate,
    session: AsyncSession = Depends(get_async_session),
) -> PropertyCodeDictDB:
    return await property_code_dict_crud.create(create_data=property_code_dict_data, session=session)


@router.patch(
    "/update/{property_code_dict_id}",
    response_model=PropertyCodeDictDB,
)
async def update_property_code_dict(
    property_code_dict_data: PropertyCodeDictUpdate,
    property_code_dict: PropertyCodeDictDB = Depends(get_property_code_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> PropertyCodeDictDB:
    return await property_code_dict_crud.update(db_obj=property_code_dict, obj_in=property_code_dict_data, session=session)


@router.delete("/delete/{property_code_dict_id}")
async def delete_property_code_dict(
    property_code_dict: PropertyCodeDictDB = Depends(get_property_code_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        await property_code_dict_crud.remove(db_obj=property_code_dict, session=session)
        return {"status": "Объект успешно удалён из БД"}
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error={"status": f"Ошибка при удалении: {e}"},
            message_log=f"{e}",
        )
