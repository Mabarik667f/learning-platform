import json
from loguru import logger
import pytest
from httpx import AsyncClient

from .helpers.test_class import BaseTestClass
from .helpers.dummy_files import create_dummy_img, create_dummy_txt


@pytest.mark.usefixtures("create_user", "create_categories")
class TestsForCourses(BaseTestClass):
    prefix = "/courses"

    async def test_create_course(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        data = {
            "title": "string",
            "describe": "string",
            "price": 1,
            "difficulty": "easy",
            "categories": [1],
        }
        img = create_dummy_img()

        response = await client.post(
            self.get_endpoint("create"),
            files={"img": img},
            data=data,
            headers=self.headers,
        )
        assert response.status_code == 201
        assert (
            response.json()["img"] == "media/course_media/course_1/course_img/dummy.png"
        )

        response = await client.post(
            self.get_endpoint("create"),
            files={"img": create_dummy_txt()},
            data=data,
            headers=self.headers,
        )
        assert response.status_code == 400

    @pytest.mark.usefixtures("create_course")
    async def test_patch_course(self, client: AsyncClient, token: dict):
        self.headers.update(token)
        course_id = 1
        data = {
            "title": "new title",
            "price": 10,
            "difficulty": "medium",
        }

        img = create_dummy_img("new_img")
        response = await client.patch(
            self.get_endpoint(f"patch/{course_id}"),
            files={"img": img},
            data=data,
            headers=self.headers,
        )
        res = response.json()
        assert response.status_code == 200
        assert (
            res.get("price") == 10
            and res.get("title") == "new title"
            and res.get("difficulty") == "medium"
        )
        assert res.get("describe") == "string"
        assert res.get("img") == "media/course_media/course_1/course_img/new_img.png"

    @pytest.mark.usefixtures("create_course")
    async def test_struct_create(self, client: AsyncClient, token: dict):
        self.headers.update(token)

        course_id = 1

        data = {
            "sections": [
                {
                    "title": "Test Section 1",
                    "describe": "DESCRIBE",
                    "position": 1,
                    "subsections": [
                        {"title": "Test Subsection 1", "position": 1},
                        {"title": "Test Subsection 2", "position": 2},
                    ],
                },
                {
                    "title": "Test Section 2",
                    "describe": "DESCRIBE",
                    "position": 2,
                    "subsections": [
                        {"title": "Test Subsection 1", "position": 1},
                        {"title": "Test Subsection 2", "position": 2},
                    ],
                },
            ]
        }

        response = await client.post(
            self.get_endpoint(f"struct/{course_id}"), json=data, headers=self.headers
        )

        struct = response.json()
        assert response.status_code == 201
        assert len(struct["categories"]) == 1
        assert len(struct["sections"]) == 2
        assert len(struct["sections"][0]["subsections"]) == 2
