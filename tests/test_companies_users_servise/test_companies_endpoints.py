import pytest
from sqlalchemy import select

from common_models.models import Company, PropertyCodeDict
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_company(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
    response = await companies_users_client.get(
        f"/api/companies/get/{company.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_companies(companies_users_client, get_test_headers):
    response = await companies_users_client.get(
        "/api/companies/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_company(companies_users_client, get_test_headers):
    create_data = {
        "name": "test",
        "inn": "test",
        "kpp": "test",
    }
    response = await companies_users_client.post(
        "/api/companies/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_property_to_company(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
        property_dict = await session.execute(select(PropertyCodeDict))
        property_dict = property_dict.scalars().first()
    response = await companies_users_client.post(
        f"/api/companies/add-property-to-company?property_code_id={property_dict.id}&company_id={company.id}",
        headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_company(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
    update_data = {
        "name": "test2",
        "inn": "test2",
        "kpp": "test2",
    }
    response = await companies_users_client.patch(
        f"/api/companies/update/{company.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def delete_property_company_connection(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
        property_dict = await session.execute(select(PropertyCodeDict))
        property_dict = property_dict.scalars().first()

    response = await companies_users_client.delete(
        f"/api/companies/delete-property-company-connection?company_id={company.id}&property_code_id={property_dict.id}",
        headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_company(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
    response = await companies_users_client.delete(
        f"/api/companies/delete/{company.id}", headers=get_test_headers
    )
    assert response.status_code == 200
