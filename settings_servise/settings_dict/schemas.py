from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_30, validate_str_255


class SettingDictBase(BaseModel):
    code: validate_str_30
    name: validate_str_255


class SettingDictCreate(SettingDictBase):
    pass


class SettingDictUpdate(SettingDictBase):
    code: validate_str_30 | None = None
    name: validate_str_255 | None = None


class SettingDictDB(SettingDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
