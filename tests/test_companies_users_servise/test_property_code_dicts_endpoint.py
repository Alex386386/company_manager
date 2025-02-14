import pytest
from sqlalchemy import select

from common_models.models import PropertyCodeDict
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_property_code_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        property_dict = await session.execute(select(PropertyCodeDict))
        property_dict = property_dict.scalars().first()
    response = await companies_users_client.get(
        f"/api/property_code_dicts/get/{property_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_property_code_dicts(companies_users_client, get_test_headers):
    response = await companies_users_client.get(
        "/api/property_code_dicts/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_property_code_dict(companies_users_client, get_test_headers):
    create_data = {
        "group_code": "test",
        "code": "test"
    }
    response = await companies_users_client.post(
        "/api/property_code_dicts/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_property_code_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        property_dict = await session.execute(select(PropertyCodeDict))
        property_dict = property_dict.scalars().first()
    update_data = {
        "group_code": "test2",
        "code": "test2"
    }
    response = await companies_users_client.patch(
        f"/api/property_code_dicts/update/{property_dict.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_property_code_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        property_dict = await session.execute(select(PropertyCodeDict))
        property_dict = property_dict.scalars().first()
    response = await companies_users_client.delete(
        f"/api/property_code_dicts/delete/{property_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200
