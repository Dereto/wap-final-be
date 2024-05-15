from fastapi import HTTPException, status
from fastapi import Header

from . import tokens as _token, schemas as _schemas


def get_current_user(access_token: str = Header(None, convert_underscores=True)) -> _schemas.TokenData | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        return None

    return _token.verify_token(access_token, credentials_exception)
