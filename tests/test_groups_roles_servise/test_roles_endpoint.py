import pytest
from sqlalchemy import select

from common_models.models import RoleDict
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_role_dict(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()
    response = await groups_client.get(
        f"/api/role_dicts/get/{role.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_role_dicts(groups_client, get_test_headers):
    response = await groups_client.get(
        "/api/role_dicts/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role_dict(groups_client, get_test_headers):
    create_data = {
        "code": "string",
        "name": "string"
    }
    response = await groups_client.post(
        "/api/role_dicts/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_role_dict(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()
    create_data = {
        "code": "string2",
        "name": "string2"
    }
    response = await groups_client.patch(
        f"/api/role_dicts/update/{role.id}", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_role_dict(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()
    response = await groups_client.delete(
        f"/api/role_dicts/delete/{role.id}", headers=get_test_headers
    )
    assert response.status_code == 200
