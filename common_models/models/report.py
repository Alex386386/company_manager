from typing import TYPE_CHECKING

from sqlalchemy import (
    Index,
    Integer,
    ForeignKey,
    BigInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common_models.models.base import (
    Base,
    pk_int,
    str_30_not_null,
    str_255_not_null,
    text,
    not_null_int,
    pk_bs,
    create_date,
    active_from_date,
    active_to_date,
)

if TYPE_CHECKING:
    from common_models.models.user import User


class ShablonDict(Base):
    __tablename__ = "shablon_dict"
    __table_args__ = (Index("idx_shablon_dict_code", "code"),)

    id: Mapped[pk_int]
    code: Mapped[str_30_not_null]
    name: Mapped[str_255_not_null]
    value: Mapped[text | None]

    # Связи
    reports: Mapped[list["Report"]] = relationship(back_populates="shablon")


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("idx_reports_code", "code"),
        Index("idx_reports_code_version", "code", "version"),
    )

    id: Mapped[pk_int]
    code: Mapped[str_30_not_null]
    name: Mapped[str_255_not_null]
    version: Mapped[not_null_int]
    shablon_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("shablon_dict.id"), nullable=False
    )

    # Связи
    shablon: Mapped["ShablonDict"] = relationship(back_populates="reports")
    report_links: Mapped[list["UserReportLink"]] = relationship(back_populates="report")


class UserReportLink(Base):
    __tablename__ = "user_report_links"
    __table_args__ = (
        Index("idx_user_report_links_user_id", "user_id"),
        Index(
            "idx_user_report_links_report_id",
            "report_id",
            postgresql_using="btree",
            postgresql_where="report_id IS NOT NULL",
        ),
        Index("idx_user_report_links_created_date", "created_date"),
        Index("idx_user_report_links_acive_from", "acive_from"),
        Index("idx_user_report_links_active_to", "active_to"),
        Index("idx_user_report_links_acive_from_active_to", "acive_from", "active_to"),
        Index("idx_user_report_links_user_id_active_to", "user_id", "active_to"),
        Index(
            "idx_user_report_links_user_id_acive_from_active_to",
            "user_id",
            "acive_from",
            "active_to",
        ),
        Index("idx_user_report_links_id", "id"),
        UniqueConstraint("user_id", "report_id", name="unique_user_report"),
    )

    id: Mapped[pk_bs]
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            column="users.id",
            name="fk_user_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    report_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column="reports.id",
            name="fk_report_id_secondary",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    created_date: Mapped[create_date]
    acive_from: Mapped[active_from_date]
    active_to: Mapped[active_to_date | None]

    # Связи
    user: Mapped["User"] = relationship(back_populates="report_links")
    report: Mapped["Report"] = relationship(back_populates="report_links")
