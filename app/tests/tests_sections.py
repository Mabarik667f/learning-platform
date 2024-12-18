import pytest

from .helpers.test_class import BaseTestClass
from httpx import AsyncClient
from loguru import logger


@pytest.mark.usefixtures("create_course")
class TestsForSections(BaseTestClass):

    prefix = "/sections"

    """CRUD (delete in the end of tests)"""

    async def test_create_section(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        data = {
            "title": "Test section 1",
            "describe": "this section test 1",
            "course_id": 1,
            "subsections": [],
            "position": 1,
        }
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 201

        data["course_id"] = 100
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 400

        data = {
            "title": "Test section 2",
            "describe": "this section test 2",
            "course_id": 1,
            "position": 2,
            "subsections": [{"title": "Test subsection 1", "position": 1}],
        }
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )

        assert response.status_code == 201
        assert response.json()["subsections"][0]["title"] == "Test subsection 1"

    @pytest.mark.usefixtures("create_section")
    async def test_patch_section(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        data = {"title": "New test title"}
        response = await client.patch(
            self.get_endpoint(f"patch/{1}"), json=data, headers=headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New test title"
        assert response.json()["describe"] == "this section test 1"

        data["describe"] = "New test describe"
        response = await client.patch(
            self.get_endpoint(f"patch/{1}"), json=data, headers=headers
        )
        assert response.status_code == 200
        assert response.json()["describe"] == "New test describe"

    @pytest.mark.usefixtures("create_section")
    async def test_get_section(self, client: AsyncClient):
        section_id = 1
        response = await client.get(self.get_endpoint(section_id))
        assert response.status_code == 200
        assert response.json().get("subsections")[0]["title"] == "Test subsection 1"

        section_id = 100
        response = await client.get(self.get_endpoint(section_id))
        assert response.status_code == 400

    @pytest.mark.usefixtures("create_section")
    async def test_get_list_sections(self, client: AsyncClient):
        course_id = 1
        response = await client.get(self.get_endpoint(f"list/{course_id}"))
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.usefixtures("create_section")
    async def test_delete_section(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        section_id = 1
        response = await client.delete(
            self.get_endpoint(f"delete/{section_id}"), headers=headers
        )
        assert response.status_code == 204

        response = await client.delete(
            self.get_endpoint(f"delete/{section_id}"), headers=headers
        )
        assert response.status_code == 400

    """End CRUD Tests """
