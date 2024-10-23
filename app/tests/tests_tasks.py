import pytest
import json

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from loguru import logger

from utils.tasks import TaskUtils
from shemas.tasks import TaskType
from .helpers.test_class import BaseTestClass
from .helpers.dummy_files import create_dummy_img, create_dummy_txt, create_dummy_video

from io import BytesIO


@pytest.mark.usefixtures("create_subsection")
class TestsForTasks(BaseTestClass):

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
        self.headers.update(token)

        data = {
            "task_type": json.dumps({"name": "test"}),
            "text": "This text for test-task 1",
            "subsection_id": 1,
        }

        video = create_dummy_video()

        response = await client.post(
            self.get_endpoint("create"),
            files={"video": video},
            data=data,
            headers=self.headers,
        )
        assert response.status_code == 201
        assert (
            response.json().get("video_path")
            == "media/course_media/course_1/task_1/videos/dummy.mp4"
        )

        data = {
            "task_type": json.dumps({"name": "test"}),
            "text": "This text for test-task 2",
            "subsection_id": 1,
            "answers": [
                json.dumps({"text": "first", "is_correct": False}),
                json.dumps({"text": "second", "is_correct": True}),
            ],
        }

        response = await client.post(
            self.get_endpoint("create"),
            files={"video": video},
            data=data,
            headers=self.headers,
        )
        assert response.status_code == 201
        assert len(response.json().get("answers")) == 2

        data = {
            "task_type": json.dumps({"name": "test"}),
            "text": "This text for test-task 2",
            "subsection_id": 1,
        }
        task_tests = [
            ("task_tests", (f"dummy{i}.txt", create_dummy_txt(f"dummy{i}")))
            for i in range(2)
        ]
        files = [("video", ("video.mp4", video))] + task_tests

        response = await client.post(
            self.get_endpoint("create"), files=files, data=data, headers=self.headers
        )
        assert response.status_code == 201
        assert len(response.json().get("task_tests")) == 2
        assert (
            response.json().get("task_tests")[0]["test_file"]
            == "media/course_media/course_1/task_3/tests/dummy0.txt"
        )

    async def test_failed_create_task(self, client: AsyncClient, token: dict):
        self.headers.update(token)
        data = {
            "task_type": json.dumps({"name": "test"}),
            "text": "This text for test-task 1",
            "subsection_id": 1,
        }

        response = await client.post(
                    self.get_endpoint("create"),
                    files={"video": create_dummy_txt()},
                    data=data,
                    headers=self.headers,
                )

        assert response.status_code == 400

    @pytest.mark.usefixtures("create_task")
    async def test_get_task(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        task_id = 1
        response = await client.get(self.get_endpoint(task_id), headers=self.headers)
        res = response.json()
        assert response.status_code == 200
        assert len(res.get("task_tests")) == 2 and len(res.get("answers")) == 2

    @pytest.mark.usefixtures("create_task")
    async def test_delete_task(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        task_id = 1
        response = await client.delete(self.get_endpoint(f'delete/{task_id}'), headers=self.headers)
        assert response.status_code == 204

    @pytest.mark.usefixtures("create_task")
    async def test_patch_task(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        task_id = 1
        data = {
            "task_type": json.dumps({"name": "code"}),
            "text": "New text",
            "scores": 10
        }
        video = create_dummy_video("new_video.mp4")

        response = await client.patch(self.get_endpoint(f"patch/{task_id}"),
            files={"video": video}, data=data, headers=self.headers)
        res = response.json()
        assert response.status_code == 200
        assert res.get('text') == "New text" and res.get("task_type").get("name") == "code"
        assert res.get("video_path") == "media/course_media/course_1/task_1/videos/new_video.mp4"
