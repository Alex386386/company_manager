from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import Base, pk_bs, active_from_date, str_1000_not_null

if TYPE_CHECKING:
    from common_models.models.company import Company


class License(Base):
    __tablename__ = "license"
    __table_args__ = (
        Index("idx_license_company_id", "company_id"),
        Index("idx_license_company_id_active_from", "company_id", "active_from"),
        Index("idx_license_active_from_active_to", "active_from", "active_to"),
        Index(
            "idx_license_company_id_active_from_active_to",
            "company_id",
            "active_from",
            "active_to",
        ),
    )

    id: Mapped[pk_bs]
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey(column="companies.id", ondelete="CASCADE"), nullable=False
    )
    license_key: Mapped[str_1000_not_null]
    active_from: Mapped[active_from_date]
    active_to: Mapped[active_from_date]

    # Связи
    company: Mapped["Company"] = relationship(back_populates="licenses")
