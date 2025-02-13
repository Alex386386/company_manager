from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from common_models.utils import log_and_raise_error
from groups.crud import role_crud
from groups.dependencies import get_role_by_id
from groups.schemas import GroupCreate, GroupUpdate, GroupDB

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{company_id}",
    response_model=GroupDB,
)
async def get_group(group: GroupDB = Depends(get_role_by_id)):
    return group


@router.get(
    "/get-all",
    response_model=list[GroupDB],
)
async def get_groups(
    session: AsyncSession = Depends(get_async_session),
) -> list[GroupDB]:
    try:
        return await role_crud.get_multi(session=session)
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error=f"{e}",
            message_log=f"{e}",
        )


@router.post(
    "/create",
    response_model=GroupDB,
)
async def create_group(
    group_data: GroupCreate,
    session: AsyncSession = Depends(get_async_session),
) -> GroupDB:
    return await role_crud.create(create_data=group_data, session=session)


@router.patch(
    "/update/{company_id}",
    response_model=GroupDB,
)
async def update_group(
    group_data: GroupUpdate,
    group: GroupDB = Depends(get_role_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> GroupDB:
    return await role_crud.update(db_obj=group, obj_in=group_data, session=session)


@router.delete("/delete/{company_id}")
async def delete_group(
    group: GroupDB = Depends(get_role_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        await role_crud.remove(db_obj=group, session=session)
        return {"status": "Объект успешно удалён из БД"}
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error={"status": f"Ошибка при удалении: {e}"},
            message_log=f"{e}",
        )
