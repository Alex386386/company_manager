from sqlalchemy import (
    ForeignKey,
    Index,
    SmallInteger,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from common_models.models.base import (
    Base,
    str_255_not_null,
    pk_ss,
    str_30_not_null,
    active_from_date,
    active_to_date,
)


class SettingDict(Base):
    __tablename__ = "settings_dict"
    __table_args__ = (Index("idx_settings_dict_code", "code"),)

    id: Mapped[pk_ss]
    code: Mapped[str_30_not_null]
    name: Mapped[str_255_not_null]

    # Связи
    settings: Mapped[list["Setting"]] = relationship(back_populates="setting_code")


class Setting(Base):
    __tablename__ = "settings"
    __table_args__ = (
        Index("idx_settings_setting_code_id", "setting_code_id"),
        Index("idx_settings_active_from", "active_from"),
        Index("idx_settings_active_to", "active_to"),
        Index("idx_settings_active_from_active_to", "active_from", "active_to"),
        Index(
            "idx_settings_property_code_id_active_from_active_to",
            "setting_code_id",
            "active_from",
            "active_to",
        ),
        Index("idx_settings_setting_code_id_active_to", "setting_code_id", "active_to"),
    )

    id: Mapped[pk_ss]
    setting_code_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey(
            column="settings_dict.id",
            name="fk_setting_code_id",
        ),
        nullable=False,
    )
    value: Mapped[str_255_not_null]
    active_from: Mapped[active_from_date]
    active_to: Mapped[active_to_date | None]

    # Связи
    setting_code: Mapped["SettingDict"] = relationship(back_populates="settings")
