from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from common_models.utils import log_and_raise_error
from timezone_dict.crud import timezone_dict_crud
from timezone_dict.dependencies import get_timezone_dict_by_id
from timezone_dict.schemas import TimezoneDictCreate, TimezoneDictUpdate, TimezoneDictDB

router = APIRouter(
    prefix="/timezone_dicts",
    tags=["Timezone_dicts"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{timezone_dict_id}",
    response_model=TimezoneDictDB,
)
async def get_timezone_dict_by_id(timezone_dict: TimezoneDictDB = Depends(get_timezone_dict_by_id)):
    return timezone_dict


@router.get(
    "/get-all",
    response_model=list[TimezoneDictDB],
)
async def get_all_timezone_dicts(
    session: AsyncSession = Depends(get_async_session),
) -> list[TimezoneDictDB]:
    try:
        return await timezone_dict_crud.get_multi(session=session)
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error=f"{e}",
            message_log=f"{e}",
        )


@router.post(
    "/create",
    response_model=TimezoneDictDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_timezone_dict(
    timezone_dict_data: TimezoneDictCreate,
    session: AsyncSession = Depends(get_async_session),
) -> TimezoneDictDB:
    return await timezone_dict_crud.create(create_data=timezone_dict_data, session=session)


@router.patch(
    "/update/{timezone_dict_id}",
    response_model=TimezoneDictDB,
)
async def update_timezone_dict(
    timezone_dict_data: TimezoneDictUpdate,
    timezone_dict: TimezoneDictDB = Depends(get_timezone_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> TimezoneDictDB:
    return await timezone_dict_crud.update(db_obj=timezone_dict, obj_in=timezone_dict_data, session=session)


@router.delete("/delete/{timezone_dict_id}")
async def delete_timezone_dict(
    timezone_dict: TimezoneDictDB = Depends(get_timezone_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        await timezone_dict_crud.remove(db_obj=timezone_dict, session=session)
        return {"status": "Объект успешно удалён из БД"}
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error={"status": f"Ошибка при удалении: {e}"},
            message_log=f"{e}",
        )
