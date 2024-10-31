import asyncio

from aio_pika.abc import AbstractIncomingMessage

from core.config import settings
from rabbit.common.users_rabbit import SendResultToUserRabbit
from rabbit.common.submissions_rabbit import NewSubmissionsRabbit
from loguru import logger


async def process_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        async with SendResultToUserRabbit() as rb:
            await rb.publish_msg_to_users_exchange(message)
            logger.info(message.body)


async def run_submissions_consumer() -> None:
    logger.info("Start Consumer")
    async with NewSubmissionsRabbit() as rb:
        await rb.consume_messages(
            process_message, settings.RQ_SUBMISSIONS_QUEUE, prefetch_count=10
        )


if __name__ == "__main__":
    try:
        asyncio.run(run_submissions_consumer())
    except KeyboardInterrupt:
        logger.info("CLOSE")
