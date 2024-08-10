from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings

sync_engine = create_engine(str(settings.SYNC_DB_URI), echo=True)
async_engine = create_async_engine(str(settings.ASYNC_DB_URI), echo=True)


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
