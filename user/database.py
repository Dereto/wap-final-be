from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import DBConfig

DATABASE_URL = "postgresql+asyncpg://"+DBConfig.username+":"+DBConfig.password+"@"+DBConfig.host+"/"+DBConfig.db_name

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
