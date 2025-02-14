from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from common_models.db import get_async_session
from companies_users_servise.companies_users_main import app
from tests.conftest import override_get_async_session


@pytest_asyncio.fixture
async def companies_users_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()
