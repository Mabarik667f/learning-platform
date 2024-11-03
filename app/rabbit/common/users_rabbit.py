from aio_pika.abc import (
    AbstractChannel,
    AbstractQueue,
    ExchangeType,
    AbstractIncomingMessage,
    AbstractExchange,
)
from aio_pika import Message
from sqlalchemy.ext.asyncio import AsyncSession
from services.task_checkers import SubmissionChecker
from crud.submissions import SubmissionCrud
from rabbit.base import RabbitBase
from core.deps import get_async_session_maker, get_db
from loguru import logger

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
        res_of_sub = await self.check_sub_res(msg)
        await exchange.publish(
            Message(
                body=f"{res_of_sub}".encode(),
                headers={
                    "user_id": msg.headers.get("user_id"),
                    "submission_id": int(msg.body),
                },
            ),
            routing_key=res_queue.name,
        )

    async def check_sub_res(self, msg: AbstractIncomingMessage):
        async for session in get_db():
            sub = await SubmissionCrud(session).get_submission(int(msg.body))
            return await SubmissionChecker(session, sub).check()


class SendResultToUserRabbit(SendResultToUserRabbitMixin, RabbitBase):  # type: ignore
    pass
