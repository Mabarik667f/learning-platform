import asyncio

import aio_pika

from core.config import settings
from rabbit.base import RabbitBase
from loguru import logger


async def pub_m(submission_id: int, user_id: int) -> None:
    async with RabbitBase() as rb:
        routing_key = settings.RQ_SUBMISSIONS_QUEUE

        await rb.channel.default_exchange.publish(
            aio_pika.Message(
                body=f"{submission_id}".encode(), headers={"user_id": user_id}
            ),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("CLOSE")
