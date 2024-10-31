from aio_pika.abc import (
    AbstractChannel,
    AbstractQueue,
    ExchangeType,
    AbstractIncomingMessage,
    AbstractExchange,
)
from aio_pika import Message
from rabbit.base import RabbitBase


class SendResultToUserRabbitMixin:

    channel: AbstractChannel

    async def declare_user_res_queue(
        self, message: AbstractIncomingMessage, exchange: AbstractExchange
    ) -> AbstractQueue:
        routing_key = f"user_{message.headers.get('user_id')}_queue"
        res_queue = await self.channel.declare_queue(routing_key)
        await res_queue.bind(exchange, routing_key=routing_key)
        return res_queue

    async def declare_users_exchange(self) -> AbstractExchange:
        return await self.channel.declare_exchange(
            "users_exchange", type=ExchangeType.DIRECT
        )

    async def publish_msg_to_users_exchange(
        self,
        msg: AbstractIncomingMessage,
    ):
        exchange = await self.declare_users_exchange()
        res_queue = await self.declare_user_res_queue(msg, exchange)
        await exchange.publish(
            Message(body=f"Result".encode()),
            routing_key=res_queue.name,
        )


class SendResultToUserRabbit(SendResultToUserRabbitMixin, RabbitBase):  # type: ignore
    pass
