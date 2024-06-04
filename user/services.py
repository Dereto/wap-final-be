from typing import TYPE_CHECKING, List
import requests

import fastapi as _fastapi
import sqlalchemy as _sql
from fastapi import UploadFile, File
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from requests import Response

from . import database as _database, models as _models, schemas as _schemas
from .hashing import Hash
from config import fs_base

if TYPE_CHECKING:
    pass


def _add_tables():
    return _database.Base.metadata.create_all(bind=_database.engine)


async def get_db() -> AsyncSession:
    async with _database.engine.begin() as conn:
        await conn.run_sync(_database.Base.metadata.create_all)
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def create_user(user: _schemas.CreateUser, db: AsyncSession) -> _schemas.ShowUser:
    user = _models.User(**user.dict())
    user.password = Hash.bcrypt(user.password)
    user.point = 0
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=e.orig)
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))

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


async def delete_user(user: _models.User, db: AsyncSession) -> None:
    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))


async def update_user(update_form: _schemas.UpdateForm, user: _models.User, db: AsyncSession) -> _schemas.ShowUser:
    if update_form.new_password is not None and update_form.new_password != "":
        if not Hash.verify(user.password, update_form.old_password):
            raise _fastapi.HTTPException(status_code=401, detail="Password incorrect")
        user.password = Hash.bcrypt(update_form.new_password)
    if update_form.username is not None:
        user.username = update_form.username
    if update_form.birthday is not None:
        user.birthday = update_form.birthday
    if update_form.gender is not None:
        user.gender = update_form.gender
    if update_form.self_description is not None:
        user.self_description = update_form.self_description

    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=str(e.orig))

    return _schemas.ShowUser.from_orm(user)


async def create_book(book: _schemas.CreateBook, db: AsyncSession) -> _schemas.ShowBook:
    book = _models.Book(**book.dict())
    try:
        db.add(book)
        await db.commit()
        await db.refresh(book)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=str(e.orig))
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))

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


async def delete_book(book: _models.Book, db: AsyncSession) -> None:
    try:
        await db.delete(book)
        await db.commit()
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=str(e))


async def update_book(update_form: _schemas.UpdateBook, book: _models.Book, db: AsyncSession) -> _schemas.ShowBook:
    for field, value in update_form.dict().items():
        if value is not None:
            setattr(book, field, value)

    try:
        await db.commit()
        await db.refresh(book)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=str(e.orig))
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))

    return _schemas.ShowBook.from_orm(book)


async def get_book_pages(book_id: int, db: AsyncSession) -> List[_schemas.ShowPage]:
    # noinspection PyTypeChecker
    q = select(_models.Page).filter(_models.Page.book_id == book_id)
    result = await db.execute(q)
    pages = [_schemas.ShowPage.from_orm(row) for row in result.scalars()]
    return pages


async def create_page(page: _schemas.CreatePage, db: AsyncSession) -> _schemas.ShowPage:
    page = _models.Page(**page.dict())
    try:
        db.add(page)
        await db.commit()
        await db.refresh(page)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=str(e.orig))
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))

    page = _schemas.ShowPage.from_orm(page)
    return page


async def upload_image(filename: str, file: UploadFile = File(...)) -> Response:
    url = f"http://{fs_base}/upload"

    files = {"image": (filename, file.file)}
    response = requests.post(url, files=files)

    return response


async def create_reading_history(record: _schemas.CreateReadingHistory, db: AsyncSession) -> None:
    record = _models.ReadingHistory(**record.dict())
    try:
        db.add(record)
        await db.commit()
        await db.refresh(record)
    except IntegrityError as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=409, detail=str(e.orig))
    except Exception as e:
        await db.rollback()
        raise _fastapi.HTTPException(status_code=500, detail=str(e))


async def get_user_reading_history(user_id: int, db: AsyncSession) -> List[_schemas.ShowReadingHistory]:
    # noinspection PyTypeChecker
    q = select(_models.ReadingHistory).where(_models.ReadingHistory.user_id == user_id)
    result = await db.execute(q)
    records = [_schemas.ShowReadingHistory.from_orm(row) for row in result.scalars()]
    return records


async def get_users_read_count(db: AsyncSession):
    result = await db.execute(text(
        fr'SELECT u.id AS user_id, u.username, COUNT(rh.book_id) AS books_read '
        fr'FROM users u '
        fr'LEFT JOIN reading_history rh ON u.id = rh.user_id '
        fr'GROUP BY u.id, u.username '
        fr'ORDER BY COUNT(rh.book_id) DESC;'
    ))

    users_books_read = [{"user_id": row.user_id, "username": row.username, "read_count": row.books_read} for row in
                        result]
    return users_books_read


async def get_books_read_count(db: AsyncSession):
    result = await db.execute(text(
        fr'SELECT b.id AS book_id, b.title, COUNT(rh.user_id) AS users_read '
        fr'FROM books b '
        fr'LEFT JOIN reading_history rh ON b.id = rh.book_id '
        fr'GROUP BY b.id, b.title '
        fr'ORDER BY COUNT(rh.user_id) DESC;'
    ))

    books_users_read = [{"book_id": row.book_id, "title": row.title, "read_count": row.users_read} for row in result]
    return books_users_read
