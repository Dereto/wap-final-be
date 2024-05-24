from typing import List

import fastapi as _fastapi
import uuid
from fastapi import APIRouter, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from .. import oauth2 as _oauth2, schemas as _schemas, services as _services

router = APIRouter(
    prefix="/book",
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


@router.post("/{book_id}/upload", response_model=_schemas.ShowPage)
async def add_book_page(book_id: int, page_number: int, file: UploadFile = File(...),
                        db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    page_uuid = uuid.uuid4()
    filename = f"{page_uuid}.jpg"
    response = await _services.upload_image(filename=filename, file=file)  # do some check later
    page = _schemas.CreatePage(page_number=page_number, book_id=book_id, uuid=page_uuid)
    page = await _services.create_page(page, db=db)
    return page


@router.get("/{book_id}/pages", response_model=List[_schemas.ShowPage])
async def get_book_pages(book_id: int,
                         current_user: _schemas.TokenData = _fastapi.Depends(_oauth2.get_current_user),
                         db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    if current_user is None:
        raise _fastapi.HTTPException(status_code=401, detail="unauthorized")
    pages = await _services.get_book_pages(book_id=book_id, db=db)
    await _services.create_reading_history(
        record=_schemas.CreateReadingHistory(book_id=book_id, user_id=current_user.id), db=db)

    return pages
