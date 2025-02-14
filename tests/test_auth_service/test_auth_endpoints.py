import pytest


@pytest.mark.asyncio
async def test_main_url(auth_client):
    response = await auth_client.get("/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_login_url(auth_client):
    form_data = {
        "grant_type": "password",
        "username": "string",
        "password": "string",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = await auth_client.post(
        "/api/auth/token", data=form_data, headers=headers
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wrong_login_url(auth_client):
    form_data = {
        "grant_type": "password",
        "username": "string2",
        "password": "string2",
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = await auth_client.post(
        "/api/auth/token", data=form_data, headers=headers
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_url(auth_client, get_test_refresh_headers):
    response = await auth_client.post(
        "/api/auth/refresh", headers=get_test_refresh_headers
    )
    assert response.status_code == 200
