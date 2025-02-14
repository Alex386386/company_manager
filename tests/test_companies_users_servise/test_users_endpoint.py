from datetime import date

import pytest
from sqlalchemy import select

from common_models.models import User, RoleDict, TimezoneDict, UserGroup, Company
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_user(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        user = await session.execute(select(User))
        user = user.scalars().first()
    response = await companies_users_client.get(
        f"/api/users/get/{user.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users(companies_users_client, get_test_headers):
    response = await companies_users_client.get(
        "/api/users/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_user(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        group = await session.execute(select(UserGroup))
        group = group.scalars().first()
        tz = await session.execute(select(TimezoneDict))
        tz = tz.scalars().first()
        company = await session.execute(select(Company))
        company = company.scalars().first()
    create_data = {
        "company_id": company.id,
        "group_id": group.id,
        "timezone_id": tz.id,
        "username": "test",
        "firstname": "test",
        "lastname": "test",
        "password": "test",
    }
    response = await companies_users_client.post(
        "/api/users/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_role_to_user(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        user = await session.execute(select(User))
        user = user.scalars().first()
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()
    create_data = {
        "user_id": user.id,
        "role_id": role.id,
        "active_from": str(date.today())
    }
    response = await companies_users_client.post(
        "/api/users/add-role-to-user", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        user = await session.execute(select(User))
        user = user.scalars().first()
    update_data = {
        "code": "test2",
        "version": 2
    }
    response = await companies_users_client.patch(
        f"/api/users/update/{user.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user_role_connection(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        user = await session.execute(select(User))
        user = user.scalars().first()
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()

    response = await companies_users_client.delete(
        f"/api/users/delete-user-role-connection?user_id={user.id}&role_id={role.id}",
        headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(companies_users_client, get_test_headers):
    async with TestingSessionLocal() as session:
        user = await session.execute(select(User))
        user = user.scalars().first()
    response = await companies_users_client.delete(
        f"/api/users/delete/{user.id}", headers=get_test_headers
    )
    assert response.status_code == 200
