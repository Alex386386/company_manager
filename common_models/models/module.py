from typing import TYPE_CHECKING

from sqlalchemy import (
    Index,
    Integer,
    ForeignKey,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from common_models.models.base import (
    Base,
    str_30_not_null,
    str_60_not_null,
    pk_int,
    pk_bs,
    active_from_date,
    active_to_date,
)

if TYPE_CHECKING:
    from common_models.models.company import Company


class Module(Base):
    __tablename__ = "modules"
    __table_args__ = (Index("idx_modules_code", "code"),)

    id: Mapped[pk_int]
    code: Mapped[str_30_not_null]
    name: Mapped[str_60_not_null]

    # Связи
    companies: Mapped[list["Company"]] = relationship(
        secondary="module_company_links",
        back_populates="modules",
        viewonly=True,
    )


class ModuleCompanyLink(Base):
    __tablename__ = "module_company_links"
    __table_args__ = (
        Index("idx_module_company_links_company_id", "company_id"),
        Index("idx_module_company_links_module_id", "module_id"),
        Index("idx_module_company_links_active_from", "active_from"),
        Index("idx_module_company_links_active_to", "active_to"),
        Index(
            "idx_module_company_links_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
        UniqueConstraint("company_id", "module_id", name="unique_company_module"),
    )

    id: Mapped[pk_bs]
    module_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="modules.id", name="fk_module_id_secondary", ondelete="CASCADE"
        ),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="companies.id", name="fk_company_id_secondary", ondelete="CASCADE"
        ),
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    active_from: Mapped[active_from_date]
    active_to: Mapped[active_to_date | None]
