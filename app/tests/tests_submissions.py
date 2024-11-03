import asyncio
import pytest
from tests.helpers.test_class import BaseTestClass
from httpx import AsyncClient

from loguru import logger


@pytest.mark.usefixtures("create_task")
class TestsForSubmission(BaseTestClass):

    prefix = "/submissions"

    async def test_new_submission(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        data = {
            "user_id": 1,
            "task_id": 1,
            "submission_answer": "test answer",
            "submission_code": "dasda",
        }

        response = await client.post(
            self.get_endpoint(f"new-submission"), json=data, headers=self.headers
        )
        resp_js = response.json()
        assert response.status_code == 200
        assert resp_js.get("submission_answer") == "test answer"

        await asyncio.sleep(10)
