from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_30, validate_str_60


class RoleDictBase(BaseModel):
    code: validate_str_30
    name: validate_str_60


class RoleDictCreate(RoleDictBase):
    pass


class RoleDictUpdate(RoleDictBase):
    code: validate_str_30 | None = None
    name: validate_str_60 | None = None


class RoleDictDB(RoleDictBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
