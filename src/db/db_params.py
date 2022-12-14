from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import environ

from contextlib import contextmanager

load_dotenv()

DB_USER = environ.get("DB_USER")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
DB_PORT = environ.get("DB_PORT") or "5432"


SYNC_SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://{user}:{pasw}@{host}:{port}/{name}".format(
        user=DB_USER,
        pasw=DB_PASSWORD,
        host=DB_HOST,
        name=DB_NAME,
        port=DB_PORT,
    )
)

JDBC_SQLALCHEMY_DATABASE_URL = "jdbc:postgresql://{host}:{port}/{name}".format(
    host=DB_HOST,
    name=DB_NAME,
    port=DB_PORT,
)

engine = create_engine(SYNC_SQLALCHEMY_DATABASE_URL, echo=True)

# тут ещё есть автокоммит, помимо expire_on_commit
# стоит посмотреть надо ли оно вообще

create_session = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()
