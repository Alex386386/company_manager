from pydantic import BaseModel, ConfigDict


class PropertyCodeDictBase(BaseModel):
    group_code: str
    code: str
    name: str | None = None


class PropertyCodeDictCreate(PropertyCodeDictBase):
    pass


class PropertyCodeDictUpdate(PropertyCodeDictBase):
    group_code: str | None = None
    code: str | None = None


class PropertyCodeDictDB(PropertyCodeDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
