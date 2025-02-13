from datetime import date

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    company_id: int
    group_id: int
    timezone_id: int
    username: str
    firstname: str
    lastname: str
    patronymic: str | None = None
    comment: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None
    user_lock: bool | None = None
    company_id: int | None = None
    group_id: int | None = None
    timezone_id: int | None = None
    username: str | None = None
    firstname: str | None = None
    lastname: str | None = None


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
