import sqlalchemy as _sql
from sqlalchemy import ForeignKey

from user import database as _database
import uuid


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


class Page(_database.Base):
    __tablename__ = "pages"
    uuid = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = _sql.Column(_sql.Integer, ForeignKey("books.id"), nullable=False)
    page_number = _sql.Column(_sql.Integer, nullable=False)

    book = _sql.orm.relationship("Book")

    __table_args__ = (
        _sql.UniqueConstraint('book_id', 'page_number'),
    )
