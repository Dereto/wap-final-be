from typing import Optional

from pydantic import BaseModel as _BaseModel


class _BaseUser(_BaseModel):
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class User(_BaseUser):
    point: Optional[int] = None
    id: int

    class Config:
        orm_mode = True


class CreateUser(_BaseUser):
    pass


class ShowUser(_BaseUser):
    id: int
    point: Optional[int] = None

    class Config:
        orm_mode = True


class UpdateForm(_BaseModel):
    old_password: str
    new_password: Optional[str] = None


class Login(_BaseModel):
    username: str
    password: str


class TokenData(_BaseModel):
    id: Optional[int] = None


class _BaseBook(_BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class ShowBook(_BaseBook):
    id: int
    total_pages: int


class CreateBook(_BaseBook):
    pass


class UpdateBook(_BaseBook):
    pass
