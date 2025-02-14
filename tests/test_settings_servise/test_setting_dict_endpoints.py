import pytest
from sqlalchemy import select

from common_models.models import SettingDict
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_setting_dict(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting_dict = await session.execute(select(SettingDict))
        setting_dict = setting_dict.scalars().first()
    response = await settings_client.get(
        f"/api/setting_dicts/get/{setting_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_setting_dicts(settings_client, get_test_headers):
    response = await settings_client.get(
        "/api/setting_dicts/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_setting_dict(settings_client, get_test_headers):
    create_data = {
        "code": "string",
        "name": "string"
    }
    response = await settings_client.post(
        "/api/setting_dicts/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_setting_dict(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting_dict = await session.execute(select(SettingDict))
        setting_dict = setting_dict.scalars().first()
    create_data = {
        "code": "string2",
        "name": "string2"
    }
    response = await settings_client.patch(
        f"/api/setting_dicts/update/{setting_dict.id}", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_setting_dict(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting_dict = await session.execute(select(SettingDict))
        setting_dict = setting_dict.scalars().first()
    response = await settings_client.delete(
        f"/api/setting_dicts/delete/{setting_dict.id}", headers=get_test_headers
    )
    assert response.status_code == 200
