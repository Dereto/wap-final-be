from typing import Optional

from pydantic import BaseModel


class _BaseUser(BaseModel):
    Username: str
    Password: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class User(_BaseUser):
    Point: Optional[int] = None
    id: int

    class Config:
        orm_mode = True


class CreateUser(_BaseUser):
    pass


class ShowUser(_BaseUser):
    id: int
    Point: Optional[int] = None

    class Config:
        orm_mode = True


class UpdateForm(BaseModel):
    old_password: str
    new_password: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None