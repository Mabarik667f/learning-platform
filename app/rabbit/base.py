from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from aio_pika import connect_robust
from .exc import RabbitException
from core.config import settings

class RabbitBase:

    def __init__(
        self,
        url: str = settings.RABBIT_URI
    ) -> None:
        self.url = url
        self._channel: AbstractChannel | None = None
        self._connection: AbstractRobustConnection | None = None

    async def get_connection(self) -> AbstractRobustConnection:
        return await connect_robust(url=self.url)

    @property
    def channel(self) -> AbstractChannel:
        if self._channel is None:
            raise RabbitException("Use context manager")
        return self._channel

    async def __aenter__(self):
        self._connection = await self.get_connection()
        self._channel = await self._connection.channel()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self._channel, AbstractChannel) and not self._channel.is_closed:
            await self._channel.close()
        if isinstance(self._connection, AbstractRobustConnection) and not self._connection.is_closed:
            await self._connection.close()
