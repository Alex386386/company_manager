from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from groups.crud import role_crud
from groups.dependencies import get_group_by_id
from groups.schemas import GroupCreate, GroupUpdate, GroupDB

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{group_id}",
    response_model=GroupDB,
)
async def get_group(group: GroupDB = Depends(get_group_by_id)):
    return group


@router.get(
    "/get-all",
    response_model=list[GroupDB],
)
async def get_groups(
    session: AsyncSession = Depends(get_async_session),
) -> list[GroupDB]:
    return await role_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=GroupDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    group_data: GroupCreate,
    session: AsyncSession = Depends(get_async_session),
) -> GroupDB:
    return await role_crud.create(create_data=group_data, session=session)


@router.patch(
    "/update/{group_id}",
    response_model=GroupDB,
)
async def update_group(
    group_data: GroupUpdate,
    group: GroupDB = Depends(get_group_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> GroupDB:
    return await role_crud.update(db_obj=group, obj_in=group_data, session=session)


@router.delete("/delete/{group_id}")
async def delete_group(
    group: GroupDB = Depends(get_group_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await role_crud.remove(db_obj=group, session=session)
