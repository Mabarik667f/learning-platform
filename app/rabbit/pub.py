import asyncio

import aio_pika

from .get_connection import get_connection
from loguru import logger

async def pub_m() -> None:
    connection = await get_connection()

    async with connection:
        routing_key = "task_queue"

        channel = await connection.channel()
        for i in range(5):
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=f"Hello {routing_key} {i}".encode(),
                    headers={"user_id": i}
                ),
                routing_key=routing_key,
            )
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("CLOSE")
