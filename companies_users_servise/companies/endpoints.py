from fastapi import APIRouter, status
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common_models.db import get_async_session
from common_models.jwt_dependency import get_credentials
from companies.crud import company_crud
from companies.dependencies import get_company_by_id, get_company_by_id_with_models
from companies.schemas import CompanyCreate, CompanyUpdate, CompanyDB, CompanyWithPropertiesDB

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
    dependencies=[Depends(get_credentials)],
)


@router.get(
    "/get/{company_id}",
    response_model=CompanyWithPropertiesDB,
)
async def get_company(company: CompanyWithPropertiesDB = Depends(get_company_by_id_with_models)):
    return company


@router.get(
    "/get-all",
    response_model=list[CompanyDB],
)
async def get_companies(
    session: AsyncSession = Depends(get_async_session),
) -> list[CompanyDB]:
    return await company_crud.get_multi(session=session)


@router.post(
    "/create",
    response_model=CompanyDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_company(
    company_data: CompanyCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CompanyDB:
    return await company_crud.create(create_data=company_data, session=session)


@router.patch(
    "/update/{company_id}",
    response_model=CompanyDB,
)
async def update_company(
    company_data: CompanyUpdate,
    company: CompanyDB = Depends(get_company_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> CompanyDB:
    return await company_crud.update(db_obj=company, obj_in=company_data, session=session)

@router.post(
    "/add-property-to-company"
)
async def add_property_to_company(
    property_code_id: int = Query(...),
    company_id: int = Query(...),
    value: str | None = Query(None),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await company_crud.add_property(
        company_id=company_id,
        property_code_id=property_code_id,
        value=value,
        session=session
    )

@router.delete(
    "/delete-property-company-connection"
)
async def delete_property_company_connection(
    property_code_id: int = Query(...),
    company_id: int = Query(...),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await company_crud.remove_property_from_company(
        company_id=company_id,
        property_code_id=property_code_id,
        session=session
    )


@router.delete("/delete/{company_id}")
async def delete_company(
    company: CompanyDB = Depends(get_company_by_id),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    return await company_crud.remove(db_obj=company, session=session)
