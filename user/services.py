from typing import TYPE_CHECKING, List
import requests

import fastapi as _fastapi
import sqlalchemy as _sql
from fastapi import UploadFile, File
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import database as _database, models as _models, schemas as _schemas
from .hashing import Hash
from config import fs_base

if TYPE_CHECKING:
    pass


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


async def get_db():
    async with _database.engine.begin() as conn:
        await conn.run_sync(_database.Base.metadata.create_all)
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def create_user(user: _schemas.CreateUser, db: AsyncSession) -> _schemas.ShowUser:
    user = _models.User(**user.dict())
    user.Password = Hash.bcrypt(user.Password)
    user.Point = 0
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return _schemas.ShowUser.from_orm(user)


async def get_all_users(db: AsyncSession) -> List[_schemas.ShowUser]:
    q = select(_models.User)
    result = await db.execute(q)
    users = [_schemas.ShowUser.from_orm(row) for row in result.scalars()]
    return users


async def get_show_user(user_id: int, db: AsyncSession) -> _schemas.ShowUser:
    # noinspection PyTypeChecker
    results = await db.execute(_sql.select(_models.User).where(_models.User.id == user_id))
    user = results.scalars().first()
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail='User not found')
    return _schemas.ShowUser.from_orm(user)


async def get_user(user_id: int, db: AsyncSession) -> _models.User:
    # noinspection PyTypeChecker
    results = await db.execute(_sql.select(_models.User).where(_models.User.id == user_id))
    user = results.scalars().first()
    return user


async def delete_user(user: _models.User, db: AsyncSession):
    await db.delete(user)
    await db.commit()


async def update_user(update_form: _schemas.UpdateForm, user: _models.User, db: AsyncSession) -> _schemas.ShowUser:
    if not Hash.verify(user.Password, update_form.old_password):
        raise _fastapi.HTTPException(status_code=404, detail="Password incorrect")
    if update_form.new_password != "":
        user.Password = Hash.bcrypt(update_form.new_password)

    await db.commit()
    await db.refresh(user)

    return _schemas.ShowUser.from_orm(user)


async def create_book(book: _schemas.CreateBook, db: AsyncSession) -> _schemas.ShowBook:
    book = _models.Book(**book.dict())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return _schemas.ShowBook.from_orm(book)


async def get_all_books(db: AsyncSession) -> List[_schemas.ShowBook]:
    q = select(_models.Book)
    result = await db.execute(q)
    books = [_schemas.ShowBook.from_orm(row) for row in result.scalars()]
    return books


async def get_show_book(book_id: int, db: AsyncSession) -> _schemas.ShowBook:
    # noinspection PyTypeChecker
    results = await db.execute(_sql.select(_models.Book).where(_models.Book.id == book_id))
    book = results.scalars().first()
    if book is None:
        raise _fastapi.HTTPException(status_code=404, detail='Book not found')
    return _schemas.ShowBook.from_orm(book)


async def get_book(book_id: int, db: AsyncSession) -> _models.Book:
    # noinspection PyTypeChecker
    results = await db.execute(_sql.select(_models.Book).where(_models.Book.id == book_id))
    book = results.scalars().first()
    return book


async def delete_book(book: _models.Book, db: AsyncSession):
    await db.delete(book)
    await db.commit()


async def update_book(update_form: _schemas.UpdateBook, book: _models.Book, db: AsyncSession) -> _schemas.ShowBook:
    for field, value in update_form.dict().items():
        if value is not None:
            setattr(book, field, value)

    await db.commit()
    await db.refresh(book)

    return _schemas.ShowBook.from_orm(book)


async def get_book_pages(book_id: int, db: AsyncSession) -> List[_schemas.ShowPage]:
    q = select(_models.Page).filter(_models.Page.book_id == book_id)
    result = await db.execute(q)
    pages = [_schemas.ShowPage.from_orm(row) for row in result.scalars()]
    return pages


async def create_page(page: _schemas.CreatePage, db: AsyncSession) -> _schemas.ShowPage:
    page = _models.Page(**page.dict())
    db.add(page)
    await db.commit()
    await db.refresh(page)
    page = _schemas.ShowPage.from_orm(page)
    return page


async def upload_image(filename: str, file: UploadFile = File(...)):
    url = f"http://{fs_base}/upload"

    files = {"image": (filename, file.file)}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        return {"message": "File uploaded successfully."}
    else:
        return {"error": "Failed to upload file to server."}
