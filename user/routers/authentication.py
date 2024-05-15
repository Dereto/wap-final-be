import fastapi as _fastapi
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from fastapi import APIRouter, Request, Form, Response

from user import models as _models, tokens as _token, services as _services
from user.hashing import Hash

router = APIRouter(tags=['Authentication'],
                   default_response_class=_fastapi.responses.JSONResponse,)


@router.get("/")
async def homepage(request: Request):
    return {"message": "hello from fastapi."}


@router.post('/login')
async def login(username: str = Form(...),
                password: str = Form(...),
                db: _orm.Session = _fastapi.Depends(_services.get_db)):
    results = await db.execute(_sql.select(_models.User).where(_models.User.username == username))
    user = results.scalars().first()
    if user is None:
        raise _fastapi.HTTPException(status_code=404, detail="User does not exist")
    if not Hash.verify(user.password, password):
        raise _fastapi.HTTPException(status_code=401, detail="Password incorrect")

    access_token = _token.create_access_token({"id": user.id})
    data = {"token": access_token, "user_id": user.id}

    return data
