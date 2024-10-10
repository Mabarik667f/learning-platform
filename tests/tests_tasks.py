import pytest

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from loguru import logger

from tasks.utils import TaskUtils
from tasks.shemas import TaskType
from .helpers.test_class import BaseTestClass


@pytest.mark.usefixtures("create_subsection")
class TestsForTask(BaseTestClass):

    prefix = "/tasks"

    async def test_get_task_type(self, session: AsyncSession):
        utils = TaskUtils(session)
        task_name = TaskType(name="test")
        task_id = await utils.get_task_type_id(task_name)
        assert task_id == 1

        task_name = TaskType(name="ERROR_NAME")
        with pytest.raises(NoResultFound):
            task_id = await utils.get_task_type_id(task_name)

    async def test_create_task(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        data = {
            "task_type": {"name": "test"},
            "text": "This text for test-task 1",
            "subsection_id": 1,
            "video_path": "test_files/s.txt",
        }

        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 201
        assert response.json().get("video_path") == "test_files/s.txt"

        data = {
            "task_type": {"name": "test"},
            "text": "This text for test-task 2",
            "subsection_id": 1,
            "answers": [
                {"text": "first", "is_correct": False},
                {"text": "second", "is_correct": True},
            ],
        }

        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 201
        assert len(response.json().get("answers")) == 2

        data = {
            "task_type": {"name": "test"},
            "text": "This text for test-task 2",
            "subsection_id": 1,
            "video_path": "test_files/s.txt",
            "task_tests": [
                {"test_file": "test_files/s.txt"},
                {"test_file": "test_files/t.py"},
            ],
        }

        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 201
        assert len(response.json().get("task_tests")) == 2

    async def test_get_task(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        data = {
            "task_type": {"name": "test"},
            "text": "This text for test-task 2",
            "subsection_id": 1,
            "video_path": "test_files/s.txt",
            "task_tests": [
                {"test_file": "test_files/s.txt"},
                {"test_file": "test_files/t.py"},
            ],
            "answers": [
                {"text": "first", "is_correct": False},
                {"text": "second", "is_correct": True},
            ],
        }

        await client.post(self.get_endpoint("create"), json=data, headers=headers)

        task_id = 1
        response = await client.get(self.get_endpoint(task_id), headers=headers)
        res = response.json()
        assert response.status_code == 200
        assert len(res.get("task_tests")) == 2 and len(res.get("answers")) == 2
