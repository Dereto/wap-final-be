from typing import TYPE_CHECKING

import fastapi as _fastapi
from user.routers import authentication as _authentication, users as _users, books as _books

if TYPE_CHECKING:
    pass

app = _fastapi.FastAPI()
app.include_router(_authentication.router)
app.include_router(_users.router)
app.include_router(_books.router)
