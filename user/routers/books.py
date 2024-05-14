from typing import List

import fastapi as _fastapi
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas as _schemas, services as _services

router = APIRouter(
    prefix="/books",
    default_response_class=_fastapi.responses.JSONResponse,
    tags=['Books']
)


@router.post("/", response_model=_schemas.ShowBook)
async def create_book(book: _schemas.CreateBook,
                      db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    return await _services.create_book(book=book, db=db)


@router.get("/", response_model=List[_schemas.ShowBook])
async def get_books(db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    return await _services.get_all_books(db=db)


@router.get("/{book_id}", response_model=_schemas.ShowBook)
async def get_book(book_id: int,
                   db: AsyncSession = _fastapi.Depends(_services.get_db)):
    book = await _services.get_show_book(book_id=book_id, db=db)

    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int,
                      db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    book = await _services.get_book(book_id=book_id, db=db)
    if book is None:
        raise _fastapi.HTTPException(status_code=404, detail="Book does not exist")
    await _services.delete_book(book, db)

    return "Successfully deleted the book"


@router.patch("/{book_id}")
async def update_book(update_form: _schemas.UpdateBook,
                      book_id: int,
                      db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    book = await _services.get_book(book_id=book_id, db=db)
    if book is None:
        raise _fastapi.HTTPException(status_code=404, detail="Book does not exist")
    await _services.update_book(update_form=update_form, book=book, db=db)
    return "Successfully updated the book"