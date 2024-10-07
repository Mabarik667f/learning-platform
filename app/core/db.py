from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine, BigInteger, Identity
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated

from .config import settings

sync_engine = create_engine(str(settings.SYNC_DB_URI), echo=settings.ECHO_DB)
async_engine = create_async_engine(str(settings.ASYNC_DB_URI), echo=settings.ECHO_DB)


pk = Annotated[int, mapped_column(BigInteger, Identity(), primary_key=True)]


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
