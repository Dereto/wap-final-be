from typing import List

import fastapi as _fastapi
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .. import oauth2 as _oauth2, schemas as _schemas, services as _services

router = APIRouter(
    prefix="/user",
    default_response_class=_fastapi.responses.JSONResponse,
    tags=['Users']
)


@router.post("/", response_model=_schemas.ShowUser)
async def create_user(user: _schemas.CreateUser,
                      db: AsyncSession = _fastapi.Depends(_services.get_db)):
    return await _services.create_user(user=user, db=db)


@router.get("/", response_model=List[_schemas.ShowUser])
async def get_users(db: AsyncSession = _fastapi.Depends(_services.get_db)):
    # if current_user.Username != "dereto":
    #     raise _fastapi.HTTPException(status_code=403, detail="Forbidden access")
    return await _services.get_all_users(db=db)


@router.get("/{user_id}", response_model=_schemas.User, response_model_exclude_unset=True)
async def get_user(user_id: int,
                   current_user: _schemas.TokenData = _fastapi.Depends(_oauth2.get_current_user),
                   db: AsyncSession = _fastapi.Depends(_services.get_db)):
    if current_user is None:
        raise _fastapi.HTTPException(status_code=401, detail="unauthorized")
    if current_user.id != user_id:
        raise _fastapi.HTTPException(status_code=403, detail="forbidden")
    user = await _services.get_show_user(user_id=user_id, db=db)
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")

    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int,
                      db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    user = await _services.get_user(user_id=user_id, db=db)
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")
    await _services.delete_user(user, db)

    return "Successfully deleted the user"


@router.patch("/{user_id}")
async def update_user(form: _schemas.UpdateForm,
                      user_id: int,
                      current_user: _schemas.TokenData = _fastapi.Depends(_oauth2.get_current_user),
                      db: AsyncSession = _fastapi.Depends(_services.get_db), ):
    if current_user is None:
        raise _fastapi.HTTPException(status_code=401, detail="unauthorized")
    if current_user.id != user_id:
        raise _fastapi.HTTPException(status_code=403, detail="forbidden")
    user = await _services.get_user(user_id=user_id, db=db)
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")
    await _services.update_user(update_form=form, user=user, db=db)
    return "Successfully updated the user"
