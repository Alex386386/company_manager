import pytest
from sqlalchemy import select

from common_models.models import TimezoneDict
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_timezone_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        timezone_dict = await session.execute(select(TimezoneDict))
        timezone_dict = timezone_dict.scalars().first()
    response = await companies_users_client.get(
        f"/api/timezone_dicts/get/{timezone_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_timezone_dicts(companies_users_client, get_test_headers):
    response = await companies_users_client.get(
        "/api/timezone_dicts/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_timezone_dict(companies_users_client, get_test_headers):
    create_data = {
        "timezone_name": "test",
        "timezone": "00:00:00Z"
    }
    response = await companies_users_client.post(
        "/api/timezone_dicts/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_timezone_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        timezone_dict = await session.execute(select(TimezoneDict))
        timezone_dict = timezone_dict.scalars().first()
    update_data = {
        "timezone_name": "test2",
    }
    response = await companies_users_client.patch(
        f"/api/timezone_dicts/update/{timezone_dict.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_timezone_dict(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        timezone_dict = await session.execute(select(TimezoneDict))
        timezone_dict = timezone_dict.scalars().first()
    response = await companies_users_client.delete(
        f"/api/timezone_dicts/delete/{timezone_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200
