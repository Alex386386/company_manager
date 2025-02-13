from typing import TYPE_CHECKING

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, relationship

from common_models.models.base import (
    Base,
    pk_bs,
    str_255_not_null,
    create_date,
    str_16_not_null,
    str_9_not_null,
    str_13,
    str_9,
)

if TYPE_CHECKING:
    from common_models.models.property import PropertyCodeDict
    from common_models.models.user import User
    from common_models.models.department import Department
    from common_models.models.license import License
    from common_models.models.module import Module
    from common_models.models.group import UserGroup


class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        Index("idx_companies_inn", "inn"),
        Index("idx_companies_kpp", "kpp"),
        Index("idx_companies_ogrn", "ogrn"),
        Index("idx_companies_bic", "bic"),
        # Index("idx_companies_property_id", "property_id"),
    )

    id: Mapped[pk_bs]
    # property_id: Mapped[int] = mapped_column( Поле устарело и только усложняет взаимодействие с системой
    #     BigInteger,
    #     ForeignKey(
    #         column="property_code_dict.id",
    #         name="fk_property_id",
    #     ),
    #     nullable=False,
    # )
    name: Mapped[str_255_not_null]
    created_date: Mapped[create_date]
    inn: Mapped[str_16_not_null]
    kpp: Mapped[str_9_not_null]
    ogrn: Mapped[str_13 | None]
    bic: Mapped[str_9 | None]

    # Связи O2M
    users: Mapped[list["User"]] = relationship(back_populates="company")
    user_groups: Mapped[list["UserGroup"]] = relationship(back_populates="company")
    licenses: Mapped[list["License"]] = relationship(back_populates="company")
    departments: Mapped[list["Department"]] = relationship(back_populates="company")
    # Связи M2M
    modules: Mapped[list["Module"]] = relationship(
        secondary="module_company_links",
        back_populates="companies",
        viewonly=True,
    )
    properties: Mapped[list["PropertyCodeDict"]] = relationship(
        secondary="company_properties",
        back_populates="companies",
        viewonly=True,
    )
