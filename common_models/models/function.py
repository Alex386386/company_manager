from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from common_models.models.base import (
    Base,
    pk_ss,
    str_30_not_null,
    not_null_smallint,
)

if TYPE_CHECKING:
    from common_models.models.role import RoleDict


class FunctionDict(Base):
    __tablename__ = "functions_dict"

    id: Mapped[pk_ss]
    code: Mapped[str_30_not_null]
    version: Mapped[not_null_smallint]

    # Связи
    roles: Mapped[list["RoleDict"]] = relationship(
        secondary="role_functions",
        back_populates="functions",
        viewonly=True,
    )
