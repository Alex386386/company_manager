from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_30, validate_small_int


class FunctionBase(BaseModel):
    code: validate_str_30
    version: validate_small_int


class FunctionCreate(FunctionBase):
    pass


class FunctionUpdate(FunctionBase):
    code: validate_str_30 | None = None
    version: validate_small_int | None = None


class FunctionDB(FunctionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoleFunctionBase(BaseModel):
    role_id: int
    function_code_id: int


class RoleDictLoad(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str


class FunctionWithRolesDB(FunctionDB):
    roles: list["RoleDictLoad"]
