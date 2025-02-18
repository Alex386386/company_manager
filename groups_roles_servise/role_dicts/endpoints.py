from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from role_dicts.crud import role_dict_crud
from role_dicts.dependencies import get_role_dict_by_id
from role_dicts.schemas import RoleDictCreate, RoleDictUpdate, RoleDictDB

router = APIRouter(
    prefix="/role_dicts",
    tags=["Role_dicts"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{role_dict_id}",
    response_model=RoleDictDB,
)
async def get_role_dict(role_dict: RoleDictDB = Depends(get_role_dict_by_id)):
    return role_dict


@router.get(
    "/get-all",
    response_model=list[RoleDictDB],
)
async def get_role_dicts(
    session: AsyncSession = Depends(get_async_session),
) -> list[RoleDictDB]:
    return await role_dict_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=RoleDictDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_role_dict(
    role_dict_data: RoleDictCreate,
    session: AsyncSession = Depends(get_async_session),
) -> RoleDictDB:
    return await role_dict_crud.create(create_data=role_dict_data, session=session)


@router.patch(
    "/update/{role_dict_id}",
    response_model=RoleDictDB,
)
async def update_role_dict(
    role_dict_data: RoleDictUpdate,
    role_dict: RoleDictDB = Depends(get_role_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> RoleDictDB:
    return await role_dict_crud.update(db_obj=role_dict, obj_in=role_dict_data, session=session)


@router.delete("/delete/{role_dict_id}")
async def delete_role_dict(
    role_dict: RoleDictDB = Depends(get_role_dict_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await role_dict_crud.remove(db_obj=role_dict, session=session)
