from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    pk_bs,
    str_60_not_null,
    str_16_not_null,
    pk_int,
    str_4000_not_null,
    create_date,
)

if TYPE_CHECKING:
    from common_models.models.user import User


class StatusDict(Base):
    __tablename__ = "status_dict"
    __table_args__ = (Index("idx_status_dict_code", "code"),)

    id: Mapped[pk_int]
    code: Mapped[str_16_not_null]
    name: Mapped[str_60_not_null]

    # Связи
    users: Mapped[list["User"]] = relationship(
        secondary="user_sendings",
        back_populates="statuses",
        viewonly=True,
    )


class UserSending(Base):
    __tablename__ = "user_sendings"
    __table_args__ = (
        Index(
            "idx_user_sendings_user_id",
            "user_id",
            postgresql_using="btree",
            postgresql_where="user_id IS NOT NULL",
        ),
        Index(
            "idx_user_sendings_status_id",
            "status_id",
            postgresql_using="btree",
            postgresql_where="status_id IS NOT NULL",
        ),
        Index(
            "idx_user_sendings_user_id_status_id_created_date",
            "user_id",
            "status_id",
            "created_date",
        ),
        Index("idx_user_sendings_created_date", "created_date"),
        UniqueConstraint("user_id", "status_id", name="unique_user_status"),
    )

    id: Mapped[pk_bs]
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("status_dict.id", ondelete="CASCADE"), nullable=False
    )
    created_date: Mapped[create_date]
    message: Mapped[str_4000_not_null]
