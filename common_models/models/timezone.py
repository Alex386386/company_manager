from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import Base, pk_ss, str_255

if TYPE_CHECKING:
    from common_models.models.user import User

class TimezoneDict(Base):
    __tablename__ = "timezone_dict"

    id: Mapped[pk_ss]
    timezone_name: Mapped[str_255 | None]
    timezone: Mapped[time | None] = mapped_column(Time(timezone=True))

    # Связи
    users: Mapped[list["User"]] = relationship(back_populates="timezone")
