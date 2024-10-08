from loguru import logger
import pytest
from httpx import AsyncClient

from .helpers.test_class import BaseTestClass


@pytest.mark.usefixtures("create_user", "create_course")
class TestsForCourseApi(BaseTestClass):
    prefix = "/courses"

    async def test_struct_create(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

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
            self.get_endpoint(f"struct/{course_id}"), json=data, headers=headers
        )

        struct = response.json()
        assert response.status_code == 201
        assert len(struct["categories"]) == 1
        assert len(struct["sections"]) == 2
        assert len(struct["sections"][0]["subsections"]) == 2
        logger.info(f"result = {response.json()}")
