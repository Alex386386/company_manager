from pydantic import BaseModel, ConfigDict


class RoleDictBase(BaseModel):
    code: str
    name: str


class RoleDictCreate(RoleDictBase):
    pass


class RoleDictUpdate(RoleDictBase):
    code: str | None = None
    name: str | None = None


class RoleDictDB(RoleDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
