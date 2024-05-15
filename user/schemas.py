from pydantic import BaseModel as _BaseModel, UUID4, AnyUrl
from typing import Optional


class _BaseUser(_BaseModel):
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True


class User(_BaseUser):
    point: Optional[int] = None
    id: int


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
        from_attributes = True
        orm_mode = True


class ShowBook(_BaseBook):
    id: int
    total_pages: int


class CreateBook(_BaseBook):
    pass


class UpdateBook(_BaseBook):
    pass


class _BasePage(_BaseModel):
    book_id: int
    page_number: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True


class CreatePage(_BasePage):
    uuid: UUID4


class ShowPage(_BasePage):
    uuid: UUID4
