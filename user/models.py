import datetime

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
    gender = _sql.Column(_sql.String, nullable=False, default="Other")
    birthday = _sql.Column(_sql.DATE)
    self_description = _sql.Column(_sql.String)


class Book(_database.Base):
    __tablename__ = "books"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String)
    cover = _sql.Column(_sql.UUID(as_uuid=True), ForeignKey("pages.uuid"))
    author = _sql.Column(_sql.String)
    publisher = _sql.Column(_sql.String)
    isbn = _sql.Column(_sql.String)
    description = _sql.Column(_sql.TEXT)
    total_pages = _sql.Column(_sql.Integer, nullable=False)

    pages = _sql.orm.relationship("Page", foreign_keys="[Page.book_id]")


class Page(_database.Base):
    __tablename__ = "pages"
    uuid = _sql.Column(_sql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = _sql.Column(_sql.Integer, ForeignKey("books.id"), nullable=False)
    page_number = _sql.Column(_sql.Integer, nullable=False)

    book = _sql.orm.relationship("Book", foreign_keys="[Page.book_id]")

    __table_args__ = (
        _sql.UniqueConstraint('book_id', 'page_number'),
    )


class ReadingHistory(_database.Base):
    __tablename__ = "reading_history"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    book_id = _sql.Column(_sql.Integer, ForeignKey("books.id"), nullable=False)
    user_id = _sql.Column(_sql.Integer, ForeignKey("users.id"), nullable=False)
    opened_at = _sql.Column(_sql.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)

    book = _sql.orm.relationship("Book")
    user = _sql.orm.relationship("User")
