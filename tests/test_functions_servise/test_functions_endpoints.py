import pytest
from sqlalchemy import select

from common_models.models import FunctionDict, RoleDict, RoleFunction
from tests.conftest import TestingSessionLocal


@pytest.mark.asyncio
async def test_get_function(functions_client, get_test_headers):
    async with TestingSessionLocal() as session:
        function = await session.execute(select(FunctionDict))
        function = function.scalars().first()
    response = await functions_client.get(
        f"/api/functions/get/{function.id}", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_functions(functions_client, get_test_headers):
    response = await functions_client.get(
        "/api/functions/get-all", headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_function(functions_client, get_test_headers):
    create_data = {
        "code": "test",
        "version": 1
    }
    response = await functions_client.post(
        "/api/functions/create", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_role_to_function(functions_client, get_test_headers):
    async with TestingSessionLocal() as session:
        function = await session.execute(select(FunctionDict))
        function = function.scalars().first()
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()
    create_data = {
        "function_code_id": function.id,
        "role_id": role.id
    }
    response = await functions_client.post(
        "/api/functions/add-role-to-function", headers=get_test_headers, json=create_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_function(functions_client, get_test_headers):
    async with TestingSessionLocal() as session:
        function = await session.execute(select(FunctionDict))
        function = function.scalars().first()
    update_data = {
        "code": "test2",
        "version": 2
    }
    response = await functions_client.patch(
        f"/api/functions/update/{function.id}", headers=get_test_headers, json=update_data
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_function_role_connection(functions_client, get_test_headers):
    async with TestingSessionLocal() as session:
        function = await session.execute(select(FunctionDict))
        function = function.scalars().first()
        role = await session.execute(select(RoleDict))
        role = role.scalars().first()

        new_role = RoleFunction(function_code_id=function.id, role_id=role.id)
        session.add(new_role)
        await session.commit()

    response = await functions_client.delete(
        f"/api/functions/delete-function-role-connection?function_code_id={function.id}&role_id={role.id}",
        headers=get_test_headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_function(functions_client, get_test_headers):
    async with TestingSessionLocal() as session:
        function = await session.execute(select(FunctionDict))
        function = function.scalars().first()
    response = await functions_client.delete(
        f"/api/functions/delete/{function.id}", headers=get_test_headers
    )
    assert response.status_code == 200
