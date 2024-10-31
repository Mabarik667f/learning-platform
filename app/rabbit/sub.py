import asyncio

from aio_pika import Message
from aio_pika.abc import AbstractIncomingMessage, ExchangeType

from get_connection import get_connection
from loguru import logger

async def process_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        connection = await get_connection()
        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange("users_exchange", type=ExchangeType.DIRECT)
            routing_key = f"user_{message.headers.get('user_id')}_queue"
            res_queue = await channel.declare_queue(routing_key)
            await res_queue.bind(exchange, routing_key=routing_key)
            await exchange.publish(
                Message(body=f"Result".encode()),
                routing_key=res_queue.name,
            )
            logger.info(message.body)
            #logger.info(message)

async def main() -> None:
    connection = await get_connection()

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        task_queue = await channel.declare_queue("task_queue")
        await task_queue.consume(process_message)
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("CLOSE")
