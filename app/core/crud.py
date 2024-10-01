from abc import ABC

from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseCrud(ABC):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
