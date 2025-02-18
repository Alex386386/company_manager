from datetime import date

from pydantic import BaseModel, ConfigDict

from common_models.fields_validation import validate_str_60, validate_str_255, validate_str_1000


class UserBase(BaseModel):
    company_id: int
    group_id: int
    timezone_id: int
    username: validate_str_60
    firstname: validate_str_60
    lastname: validate_str_60
    patronymic: validate_str_60 | None = None
    comment: validate_str_1000 | None = None


class UserCreate(UserBase):
    password: validate_str_255


class UserUpdate(UserBase):
    password: str | None = None
    user_lock: bool | None = None
    company_id: int | None = None
    group_id: int | None = None
    timezone_id: int | None = None
    username: validate_str_60 | None = None
    firstname: validate_str_60 | None = None
    lastname: validate_str_60 | None = None


class UserDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_lock: bool
    created_date: date


class RoleDict(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    name: str


class UserWithRolesDB(UserDB):
    roles: list[RoleDict]


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int
    active_from: date
    active_to: date | None = None
