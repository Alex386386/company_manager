from datetime import date

from pydantic import BaseModel, ConfigDict

from settings_dict.schemas import SettingDictDB


class SettingBase(BaseModel):
    setting_code_id: int
    value: str
    active_from: date
    active_to: date | None = None


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    setting_code_id: int | None = None
    value: str | None = None
    active_from: date | None = None


class SettingDB(SettingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SettingWithModelsDB(SettingDB):
    setting_code: "SettingDictDB"
