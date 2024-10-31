import asyncio
from typing import Any, Awaitable, Callable
from aio_pika.abc import AbstractChannel, AbstractIncomingMessage, AbstractQueue
from loguru import logger

from rabbit.base import RabbitBase


class NewSubmissionsRabbitMixin:

    channel: "AbstractChannel"

    async def declare_queue_for_new_tasks(
        self,
        queue_name: str = "",
        exclusive: bool = False
    ) -> AbstractQueue:
        queue = await self.channel.declare_queue(
            name=queue_name,
            exclusive=exclusive
        )
        return queue

    async def consume_messages(
        self,
        message_callback: Callable[[AbstractIncomingMessage], Awaitable[Any]],
        queue_name: str = "",
        prefetch_count: int = 1
    ):
        await self.channel.set_qos(prefetch_count=prefetch_count)
        queue = await self.declare_queue_for_new_tasks(queue_name=queue_name)
        await queue.consume(message_callback)
        await asyncio.Future()


class NewSubmissionsRabbit(NewSubmissionsRabbitMixin, RabbitBase): #type: ignore
    pass
