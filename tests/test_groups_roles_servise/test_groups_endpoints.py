import pytest
from sqlalchemy import select

from common_models.models import UserGroup, Company
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_group(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        group = await session.execute(select(UserGroup))
        group = group.scalars().first()
    response = await groups_client.get(
        f"/api/groups/get/{group.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_groups(groups_client, get_test_headers):
    response = await groups_client.get(
        "/api/groups/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_group(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        company = await session.execute(select(Company))
        company = company.scalars().first()
    create_data = {
        "company_id": company.id,
        "group_name": "test"
    }
    response = await groups_client.post(
        "/api/groups/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_group(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        group = await session.execute(select(UserGroup))
        group = group.scalars().first()
    update_data = {
        "group_name": "test2",
    }
    response = await groups_client.patch(
        f"/api/groups/update/{group.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_group(groups_client, get_test_headers):
    async with TestingSessionLocal() as session:
        group = await session.execute(select(UserGroup))
        group = group.scalars().first()
    response = await groups_client.delete(
        f"/api/groups/delete/{group.id}", headers=get_test_headers
    )
    assert response.status_code == 200
