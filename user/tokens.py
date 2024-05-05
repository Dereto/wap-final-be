from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas as _schemas
import config as _setting

SECRET_KEY = _setting.SECRET_KEY
ALGORITHM = _setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = _setting.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> _schemas.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id: int = payload.get("id")
        token_data = _schemas.TokenData(id=_id)
        return token_data
    except JWTError:
        raise credentials_exception
