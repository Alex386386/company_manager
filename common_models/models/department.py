from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    BigInteger,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import Base, pk_bs, str_255_not_null, create_date, not_null_bigint

if TYPE_CHECKING:
    from common_models.models.company import Company


class Department(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('idx_departments_code', 'code'),
        Index('idx_departments_company_id', 'company_id'),
    )

    id: Mapped[pk_bs]
    company_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('companies.id'), nullable=False)
    code: Mapped[not_null_bigint]
    name: Mapped[str_255_not_null]
    created_date: Mapped[create_date]

    # Связи
    company: Mapped["Company"] = relationship(back_populates="departments")
