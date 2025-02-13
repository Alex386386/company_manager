from pydantic import BaseModel, ConfigDict


class FunctionBase(BaseModel):
    code: str
    version: int


class FunctionCreate(FunctionBase):
    pass


class FunctionUpdate(FunctionBase):
    code: str | None = None
    version: int | None = None


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
