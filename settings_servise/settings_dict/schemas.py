from pydantic import BaseModel, ConfigDict


class SettingDictBase(BaseModel):
    code: str
    name: str


class SettingDictCreate(SettingDictBase):
    pass


class SettingDictUpdate(SettingDictBase):
    code: str | None = None
    name: str | None = None


class SettingDictDB(SettingDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
