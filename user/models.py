import sqlalchemy as _sql
from user import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True, nullable=False)
    password = _sql.Column(_sql.String, nullable=False)
    point = _sql.Column(_sql.Integer, nullable=False, default=0)


class Book(_database.Base):
    __tablename__ = "books"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String)
    author = _sql.Column(_sql.String)
    description = _sql.Column(_sql.TEXT)
    total_pages = _sql.Column(_sql.Integer, nullable=False)
