from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    pk_bs,
    str_255_not_null,
    str_1000,
)

if TYPE_CHECKING:
    from common_models.models.company import Company
    from common_models.models.user import User


class UserGroup(Base):
    __tablename__ = "user_groups"
    __table_args__ = (Index("idx_user_groups_company_id", "company_id"),)

    id: Mapped[pk_bs]
    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="companies.id",
            name="fk_company_id",
        ),
        nullable=False,
    )
    group_name: Mapped[str_255_not_null]
    comment: Mapped[str_1000 | None]

    # Связи
    company: Mapped["Company"] = relationship(back_populates="user_groups")
    users: Mapped[list["User"]] = relationship(back_populates="group")
