from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from common_models.models import User
from common_models.utils import log_and_raise_error
from users.crud import user_crud
from users.dependencies import get_user_by_id, get_user_by_id_with_models
from users.schemas import UserCreate, UserUpdate, UserDB, UserRoleBase, UserWithRolesDB

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{user_id}",
    response_model=UserWithRolesDB,
)
async def get_user(user: UserWithRolesDB = Depends(get_user_by_id_with_models)):
    return user


@router.get(
    "/get-all",
    response_model=list[UserDB],
)
async def get_all_users(
    session: AsyncSession = Depends(get_async_session),
) -> list[UserDB]:
    try:
        return await user_crud.get_multi(session=session)
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error=f"{e}",
            message_log=f"{e}",
        )


@router.post(
    "/create",
    response_model=UserDB,
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> UserDB:
    return await user_crud.create(create_data=user_data, session=session)


@router.patch(
    "/update/{user_id}",
    response_model=UserDB,
)
async def update_user(
    user_data: UserUpdate,
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> UserDB:
    return await user_crud.update(db_obj=user, obj_in=user_data, session=session)

@router.post(
    "/add-role-to-user"
)
async def add_role_to_user(
    create_data: UserRoleBase,
    session: AsyncSession = Depends(get_async_session),
):
    return await user_crud.add_role(
        create_data=create_data,
        session=session
    )

@router.delete(
    "/delete-user-role-connection"
)
async def delete_user_role_connection(
    user_id: int = Query(...),
    role_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    result = await user_crud.remove_role_from_user(
        user_id=user_id,
        role_id=role_id,
        session=session
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Данного объекта нет в БД")
    return {"status": "Объект успешно удалён из БД"}


@router.delete("/delete/{user_id}")
async def delete_user(
    user: User = Depends(get_user_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        await user_crud.remove(db_obj=user, session=session)
        return {"status": "Объект успешно удалён из БД"}
    except Exception as e:
        log_and_raise_error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message_error={"status": f"Ошибка при удалении: {e}"},
            message_log=f"{e}",
        )
