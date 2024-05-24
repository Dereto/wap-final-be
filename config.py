import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class DBConfig:
    host = os.getenv('PG_HOST')
    port = os.getenv('PG_PORT')
    username = os.getenv('PG_USERNAME')
    password = os.getenv('PG_PASSWORD')
    db_name = os.getenv('PG_DBNAME')


db_config = DBConfig()
fs_base = os.getenv("FS_HOST") + ":" + os.getenv("FS_PORT")


@lru_cache()
def get_app_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
