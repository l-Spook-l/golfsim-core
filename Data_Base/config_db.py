import pathlib

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


DATABASE_URL = "sqlite+aiosqlite:///database.db"
DB_FILE = pathlib.Path("database.db")


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
