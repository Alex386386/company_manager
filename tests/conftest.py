import asyncio
import os
import sys
from datetime import datetime, timezone, time, timedelta, date

import jwt
import pytest_asyncio
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from common_models.config import settings
from common_models.models import Base
from common_models.models import (
    User,
    TimezoneDict,
    Company,
    UserGroup,
    SettingDict,
    Setting,
    RoleDict,
    FunctionDict,
    PropertyCodeDict,
)
from common_models.pwd_context import get_password_hash

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../auth_service"))
)
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../companies_users_servise")
    )
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../functions_servise"))
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../groups_roles_servise"))
)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../settings_servise"))
)

load_dotenv(find_dotenv())

DATABASE_URL_TEST = os.getenv("TEST_DATABASE_URL")

async_engine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False
)

Base.metadata.bind = async_engine


async def override_get_async_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def load_initial_data(prepare_database):
    """Фикстура для загрузки начальных данных (таймзона, компания, группа, пользователь)"""
    async with TestingSessionLocal() as session:
        dt = datetime.strptime("00:00:00", "%H:%M:%S")
        time_with_tz = time(
            hour=dt.hour, minute=dt.minute, second=dt.second, tzinfo=timezone.utc
        )

        new_timezone = TimezoneDict(timezone_name="UTC", timezone=time_with_tz)
        session.add(new_timezone)
        await session.commit()

        company = Company(name="test", inn="test", kpp="test", ogrn="test", bic="test")
        session.add(company)
        await session.flush()

        group = UserGroup(company_id=company.id, group_name="test")
        session.add(group)
        await session.flush()

        hashed_password = get_password_hash("string")
        user = User(
            company_id=company.id,
            group_id=group.id,
            timezone_id=new_timezone.id,
            username="string",
            firstname="string",
            lastname="string",
            password=hashed_password,
        )
        session.add(user)
        await session.flush()

        setting_dict = SettingDict(code="test", name="test")
        session.add(setting_dict)
        await session.flush()

        setting = Setting(
            setting_code_id=setting_dict.id, value="test", active_from=date.today()
        )
        session.add(setting)
        await session.flush()

        role = RoleDict(code="test", name="test")
        session.add(role)
        await session.flush()

        role = RoleDict(code="test", name="test")
        session.add(role)
        await session.flush()

        group = UserGroup(
            company_id=company.id,
            group_name="test",
        )
        session.add(group)
        await session.flush()

        function = FunctionDict(
            code="test",
            version=1,
        )
        session.add(function)
        await session.flush()

        property_code = PropertyCodeDict(group_code="test", code="test")
        session.add(property_code)
        await session.flush()

        await session.commit()


@pytest_asyncio.fixture
def get_test_headers():
    data = {
        "sub": "string",
        "user_id": 1,
    }
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}


@pytest_asyncio.fixture
def get_test_refresh_headers():
    data = {
        "sub": "string",
        "user_id": 1,
    }
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.refresh_secret_key, algorithm=settings.algorithm
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}
