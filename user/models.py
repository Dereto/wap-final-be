import sqlalchemy as _sql
from user import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    Username = _sql.Column(_sql.String, unique=True)
    Password = _sql.Column(_sql.String)
    Point = _sql.Column(_sql.Integer)
