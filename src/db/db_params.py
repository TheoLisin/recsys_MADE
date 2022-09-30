from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import environ

load_dotenv()

DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
DB_PORT = environ.get("DB_PORT") or "1234"


SYNC_SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://{user}:{pasw}@{host}:{port}/{name}".format(
    user=DB_USER,
    pasw=DB_PASSWORD,
    host=DB_HOST,
    name=DB_NAME,
    port=DB_PORT,
)

engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL)

# тут ещё есть автокоммит, помимо expire_on_commit
# стоит посмотреть надо ли оно вообще

session = sessionmaker(engine, expire_on_commit=False)


def get_session() -> Session:
    """Session generator."""
    with session() as new_session:
        yield new_session
