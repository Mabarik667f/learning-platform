import asyncio

from aio_pika.abc import AbstractQueueIterator

from rabbit.base import RabbitBase
from loguru import logger


async def get_submission_result(user_id: int, submission_id: int):

    async with RabbitBase() as rb:
        res_queue = await rb.channel.declare_queue(f"user_{user_id}_queue")
        async with res_queue.iterator() as q_it:
            return await check_messages(q_it, user_id, submission_id)


async def check_messages(q_it: AbstractQueueIterator, user_id: int, submission_id: int):
    while True:
        try:
            msg = await asyncio.wait_for(q_it.__anext__(), timeout=0.1)
            logger.info(msg)
            if (
                msg.headers.get("user_id") == user_id
                and msg.headers.get("submission_id") == submission_id
            ):
                logger.info(msg.body.decode())
                await msg.ack()
                return msg.body.decode()
        except asyncio.TimeoutError:
            logger.info("Timeout reached")
            break
        except Exception as e:
            logger.info(e)
            break
