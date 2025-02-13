from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
    SmallInteger, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    pk_ss,
    str_30_not_null,
    str_60_not_null,
    active_from_date,
    active_to_date,
    pk_int,
)

if TYPE_CHECKING:
    from common_models.models.user import User
    from common_models.models.function import FunctionDict


class RoleDict(Base):
    __tablename__ = "roles_dict"

    id: Mapped[pk_ss]
    code: Mapped[str_30_not_null]
    name: Mapped[str_60_not_null]

    # Связи
    users: Mapped[list["User"]] = relationship(
        secondary="user_roles",
        back_populates="roles",
        viewonly=True,
    )
    functions: Mapped[list["FunctionDict"]] = relationship(
        secondary="role_functions",
        back_populates="roles",
        viewonly=True,
    )


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (
        Index("idx_user_roles_user_id", "user_id"),
        Index("idx_user_roles_role_id", "role_id"),
        Index(
            "idx_user_roles_user_id_role_id_active_to",
            "user_id",
            "role_id",
            "active_to",
        ),
        Index("idx_user_roles_active_from", "active_from"),
        Index("idx_user_roles_active_to", "active_to"),
        UniqueConstraint("user_id", "role_id", name="unique_user_role"),
    )

    id: Mapped[pk_int]
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="users.id",
            name="fk_user_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="roles_dict.id",
            name="fk_role_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    active_from: Mapped[active_from_date]
    active_to: Mapped[active_to_date | None]


class RoleFunction(Base):
    __tablename__ = "role_functions"
    __table_args__ = (
        Index("idx_role_functions_role_id", "role_id"),
        Index("idx_role_functions_function_code_id", "function_code_id"),
        UniqueConstraint("function_code_id", "role_id", name="unique_function_role"),
    )

    id: Mapped[pk_ss]
    role_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="roles_dict.id",
            name="fk_role_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    function_code_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="functions_dict.id",
            name="fk_function_code_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
