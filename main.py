from typing import TYPE_CHECKING

import fastapi as _fastapi
from fastapi.middleware.cors import CORSMiddleware

from user.routers import authentication as _authentication, users as _users, books as _books

if TYPE_CHECKING:
    pass

app = _fastapi.FastAPI(root_path="/api/")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(_authentication.router)
app.include_router(_users.router)
app.include_router(_books.router)
