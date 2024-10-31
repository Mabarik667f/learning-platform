import asyncio

from rabbit.base import RabbitBase
from loguru import logger


async def g_r(user_id: int, submission_id: int):

    async with RabbitBase() as rb:
        res_queue = await rb.channel.declare_queue(f"user_{user_id}_queue")
        msg = await res_queue.get(fail=False)
        if msg:
            if (
                msg.headers.get("user_id") == user_id
                and msg.headers.get("submission_id") == submission_id
            ):
                logger.info(msg.body.decode())
                await msg.ack()
                return msg.body.decode()
        else:
            print("Queue empty")


if __name__ == "__main__":
    try:
        asyncio.run(g_r(1, 1))
    except KeyboardInterrupt:
        logger.info("CLOSE")
