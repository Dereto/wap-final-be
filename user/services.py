from typing import TYPE_CHECKING, List

import fastapi as _fastapi
import sqlalchemy as _sql
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import database as _database, models as _models, schemas as _schemas
from .hashing import Hash

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

    return _schemas.ShowUser.model_validate(user)
