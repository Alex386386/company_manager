from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    str_255,
    pk_bs,
    pk_ss,
    str_30_not_null,
    str_100,
)

if TYPE_CHECKING:
    from common_models.models.company import Company
    from common_models.models.user import User


class PropertyCodeDict(Base):
    __tablename__ = "property_code_dict"
    __table_args__ = (
        Index("idx_property_code_dict_code", "code"),
        Index("idx_property_code_dict_group_code_code", "group_code", "code"),
    )

    id: Mapped[pk_ss]
    group_code: Mapped[str_30_not_null]
    code: Mapped[str_30_not_null]
    name: Mapped[str_100 | None]

    # Связи
    user_properties: Mapped[list["UserProperty"]] = relationship(
        back_populates="property_code"
    )
    companies: Mapped[list["Company"]] = relationship(
        secondary="company_properties",
        back_populates="properties",
        viewonly=True,
    )


class CompanyProperty(Base):
    __tablename__ = "company_properties"
    __table_args__ = (
        Index("idx_company_properties_property_code_id", "property_code_id", unique=True),
        Index("idx_company_properties_company_id", "company_id"),
        Index(
            "idx_company_properties_company_id_property_code_id",
            "company_id",
            "property_code_id",
        ),
        UniqueConstraint("company_id", "property_code_id", name="unique_company_property"),
    )

    id: Mapped[pk_bs]
    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="companies.id", name="fk_company_id_secondary", ondelete="CASCADE"
        ),
        nullable=False,
    )
    property_code_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="property_code_dict.id",
            name="fk_property_code_id_secondary",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    value: Mapped[str_255 | None]


class UserProperty(Base):
    __tablename__ = "user_properties"
    __table_args__ = (
        UniqueConstraint(
            "property_code_id", name="idx_user_properties_property_code_id"
        ),
        Index("idx_user_properties_property_id", "user_id"),
        Index(
            "idx_user_properties_property_id_property_code_id",
            "user_id",
            "property_code_id",
        ),
        UniqueConstraint("user_id", "property_code_id", name="unique_user_property"),
    )

    id: Mapped[pk_bs]
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(column="users.id", name="fk_user_id_secondary", ondelete="CASCADE"),
        nullable=False,
    )
    property_code_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="property_code_dict.id",
            name="fk_property_code_id_secondary",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    value: Mapped[str_255 | None]

    # Связи
    user: Mapped["User"] = relationship(back_populates="properties")
    property_code: Mapped["PropertyCodeDict"] = relationship(
        back_populates="user_properties"
    )
