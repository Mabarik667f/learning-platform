import asyncio

import aio_pika

from core.config import settings
from rabbit.base import RabbitBase
from loguru import logger


async def pub_m() -> None:
    async with RabbitBase() as rb:
        routing_key = settings.RQ_SUBMISSIONS_QUEUE

        for i in range(5):
            await rb.channel.default_exchange.publish(
                aio_pika.Message(
                    body=f"Hello {routing_key} {i}".encode(), headers={"user_id": i}
                ),
                routing_key=routing_key,
            )
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("CLOSE")
