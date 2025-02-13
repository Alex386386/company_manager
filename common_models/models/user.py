from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
    SmallInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    pk_bs,
    str_60_not_null,
    create_date,
    str_1000,
    str_255_not_null,
    str_60,
    bool_false_not_null,
)

if TYPE_CHECKING:
    from common_models.models.timezone import TimezoneDict
    from common_models.models.report import UserReportLink
    from common_models.models.role import RoleDict
    from common_models.models.company import Company, UserGroup
    from common_models.models.property import UserProperty
    from common_models.models.status import StatusDict


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_group_id", "group_id"),
        Index("idx_users_timezone_id", "timezone_id"),
        Index("idx_users_company_id", "company_id"),
        Index("idx_users_username", "username"),
        Index("idx_users_company_id_group_id", "company_id", "group_id"),
        Index("idx_users_username_user_lock", "username", "user_lock"),
        Index("idx_users_id_company_id", "id", "company_id"),
        Index("idx_users_id_group_id", "id", "group_id"),
    )

    id: Mapped[pk_bs]
    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="companies.id",
            name="fk_company_id",
        ),
        nullable=False,
    )
    group_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="user_groups.id",
            name="fk_group_id",
        ),
        nullable=False,
    )
    timezone_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="timezone_dict.id",
            name="fk_timezone_id",
        ),
        nullable=False,
    )
    username: Mapped[str_60_not_null]
    firstname: Mapped[str_60_not_null]
    lastname: Mapped[str_60_not_null]
    patronymic: Mapped[str_60 | None]
    created_date: Mapped[create_date]
    user_lock: Mapped[bool_false_not_null]
    password: Mapped[str_255_not_null]
    comment: Mapped[str_1000 | None]

    # Связи O2M
    company: Mapped["Company"] = relationship(back_populates="users")
    group: Mapped["UserGroup"] = relationship(back_populates="users")
    timezone: Mapped["TimezoneDict"] = relationship(back_populates="users")
    properties: Mapped[list["UserProperty"]] = relationship(back_populates="user")
    report_links: Mapped[list["UserReportLink"]] = relationship(back_populates="user")
    # Связи M2M
    roles: Mapped[list["RoleDict"]] = relationship(
        secondary="user_roles",
        back_populates="users",
        viewonly=True,
    )
    statuses: Mapped[list["StatusDict"]] = relationship(
        secondary="user_sendings",
        back_populates="users",
        viewonly=True,
    )
