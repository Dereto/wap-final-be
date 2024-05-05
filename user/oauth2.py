from fastapi import HTTPException, status
from fastapi import Request

from . import tokens as _token, schemas as _schemas


def get_current_user(request: Request) -> _schemas.TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    access_token = request.cookies.get("access_token")
    if access_token is None:
        return _schemas.TokenData(id=None)

    return _token.verify_token(access_token, credentials_exception)
