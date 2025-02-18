from fastapi import APIRouter, status
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from functions.crud import function_crud
from functions.dependencies import get_function_by_id, get_function_by_id_with_models
from functions.schemas import FunctionCreate, FunctionUpdate, FunctionDB, RoleFunctionBase, FunctionWithRolesDB

router = APIRouter(
    prefix="/functions",
    tags=["Functions"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{function_id}",
    response_model=FunctionWithRolesDB,
)
async def get_function(function: FunctionWithRolesDB = Depends(get_function_by_id_with_models)):
    return function


@router.get(
    "/get-all",
    response_model=list[FunctionDB],
)
async def get_functions(
    session: AsyncSession = Depends(get_async_session),
) -> list[FunctionDB]:
    return await function_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=FunctionDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_function(
    function_data: FunctionCreate,
    session: AsyncSession = Depends(get_async_session),
) -> FunctionDB:
    return await function_crud.create(create_data=function_data, session=session)


@router.patch(
    "/update/{function_id}",
    response_model=FunctionDB,
)
async def update_function(
    function_data: FunctionUpdate,
    function: FunctionDB = Depends(get_function_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> FunctionDB:
    return await function_crud.update(db_obj=function, obj_in=function_data, session=session)

@router.post(
    "/add-role-to-function"
)
async def add_role_to_function(
    create_data: RoleFunctionBase,
    session: AsyncSession = Depends(get_async_session),
):
    return await function_crud.add_role(
        create_data=create_data,
        session=session
    )

@router.delete(
    "/delete-function-role-connection"
)
async def delete_function_role_connection(
    function_code_id: int = Query(...),
    role_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
):
    return await function_crud.remove_role_from_function(
        function_code_id=function_code_id,
        role_id=role_id,
        session=session
    )


@router.delete("/delete/{function_id}")
async def delete_function(
    function: FunctionDB = Depends(get_function_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await function_crud.remove(db_obj=function, session=session)
