import pytest
from loguru import logger

async def test_async(client):
    response = await client.get("/courses/list")
    logger.debug(response.json())
    assert response.status_code == 200
