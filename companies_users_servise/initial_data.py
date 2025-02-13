from datetime import datetime, timezone

from sqlalchemy import select

from common_models.db import AsyncSessionLocal
from common_models.logger import logger
from common_models.models import TimezoneDict, Company, UserGroup, User
from common_models.pwd_context import get_password_hash


async def load_initial_data() -> None:
    async with AsyncSessionLocal() as session:
        db_obj = await session.execute(select(TimezoneDict))
        db_obj = db_obj.scalars().first()
        if db_obj:
            logger.debug("Попытка загрузки данных во второй раз!")
            return
        dt = datetime.strptime("00:00:00", "%H:%M:%S")
        time_with_tz = dt.replace(tzinfo=timezone.utc)
        new_timezone = TimezoneDict(timezone_name="UTC", timezone=time_with_tz)
        session.add(new_timezone)
        logger.debug("Таймзона добавлена в сессию.")
        await session.flush()

        company = Company(
            name="test",
            inn="test",
            kpp="test",
            ogrn="test",
            bic="test",
        )
        session.add(company)
        logger.debug("Компания добавлена в сессию.")
        await session.flush()

        group = UserGroup(
            company_id=company.id,
            group_name="test"
        )
        session.add(group)
        await session.flush()
        logger.debug("Группа добавлена в сессию.")

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
        await session.commit()
    logger.debug("Первичные данные успешно загружены в БД.")
