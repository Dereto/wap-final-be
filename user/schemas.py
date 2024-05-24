from pydantic import BaseModel as _BaseModel, UUID4
from datetime import date, datetime
from typing import Optional


class _BaseUser(_BaseModel):
    username: str
    password: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True


class User(_BaseUser):
    point: int
    id: int
    gender: str
    birthday: Optional[date] = None
    self_description: Optional[str] = None


class CreateUser(_BaseUser):
    gender: Optional[str] = None
    birthday: Optional[date] = None
    self_description: Optional[str] = None
    pass


class ShowUser(_BaseUser):
    point: int
    id: int
    gender: str
    birthday: Optional[date] = None
    self_description: Optional[str] = None


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


class _BaseReadingHistory(_BaseModel):
    book_id: int
    user_id: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True


class ReadingHistory(_BaseReadingHistory):
    id: int
    opened_at: datetime


class CreateReadingHistory(_BaseReadingHistory):
    pass


class ShowReadingHistory(_BaseReadingHistory):
    id: int
    opened_at: datetime


class UserReadCount(_BaseModel):
    user_id: int
    username: str
    read_count: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True


class BookReadCount(_BaseModel):
    book_id: int
    title: str
    read_count: int

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        orm_mode = True
