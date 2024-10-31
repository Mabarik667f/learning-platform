import aio_pika
from aio_pika.abc import AbstractRobustConnection
from core.config import settings

MQ_ROUTING_KEY = "tests_for_code"

async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD
    )
