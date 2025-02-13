from typing import Annotated

from fastapi import Depends, status
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from companies.crud import company_crud
from companies.schemas import CompanyDB, CompanyWithPropertiesDB
from common_models.db import get_async_session
from common_models.utils import check_exists_and_get_or_return_error


async def get_company_by_id(
    company_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> CompanyDB:
    return await check_exists_and_get_or_return_error(
        db_id=company_id,
        crud=company_crud,
        method_name="get",
        error="Данная компания не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )


async def get_company_by_id_with_models(
    company_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
) -> CompanyWithPropertiesDB:
    return await check_exists_and_get_or_return_error(
        db_id=company_id,
        crud=company_crud,
        method_name="get_with_models",
        error="Данная компания не найдена!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )
