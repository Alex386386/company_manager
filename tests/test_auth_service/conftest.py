from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from auth_service.auth_main import app
from common_models.db import get_async_session
from tests.conftest import override_get_async_session


@pytest_asyncio.fixture
async def auth_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()
