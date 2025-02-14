from datetime import date

import pytest
from sqlalchemy import select

from common_models.models import SettingDict, Setting
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_setting(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting = await session.execute(select(Setting))
        setting = setting.scalars().first()
    response = await settings_client.get(
        f"/api/settings/get/{setting.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_settings(settings_client, get_test_headers):
    response = await settings_client.get(
        "/api/settings/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_setting(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting_dict = await session.execute(select(SettingDict))
        setting_dict = setting_dict.scalars().first()
    create_data = {
        "setting_code_id": setting_dict.id,
        "value": "test",
        "active_from": str(date.today())
    }
    response = await settings_client.post(
        "/api/settings/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_setting(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting = await session.execute(select(Setting))
        setting = setting.scalars().first()
    create_data = {
        "value": "test2"
    }
    response = await settings_client.patch(
        f"/api/settings/update/{setting.id}", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_setting(settings_client, get_test_headers):
    async with TestingSessionLocal() as session:
        setting = await session.execute(select(Setting))
        setting = setting.scalars().first()
    response = await settings_client.delete(
        f"/api/settings/delete/{setting.id}", headers=get_test_headers
    )
    assert response.status_code == 200
