import pytest

from .helpers.auth_middleware import get_auth_header
from httpx import AsyncClient
from loguru import logger

@pytest.mark.usefixtures("create_user", "create_course")
class TestsForSections:

    prefix = "/sections/"

    @classmethod
    def get_endpoint(cls, url: str | int): # rewrite to fixture
        return f"{cls.prefix}{url}"

    async def get_section(
        self,
        client: AsyncClient,
        section_id: int,
        headers: dict = dict()
    ):
        response = await client.get(self.get_endpoint(section_id))
        return response.json()

    """CRUD (delete in the end of tests)"""
    async def test_create_section(self, client: AsyncClient, token: str):
        headers = dict()
        headers.update(get_auth_header(token))

        data = {"title": "Test section 1", "describe": "this section test 1", "course_id": 1, "subsections": []}
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers)
        assert response.status_code == 201

        data["course_id"] = 100
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers)
        assert response.status_code == 400

        data = {"title": "Test section 2",
            "describe": "this section test 2", "course_id": 1,
            "subsections": [{"title": "Test subsection 1"}]
        }
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers)
        assert response.status_code == 201
        assert response.json()["subsections"][0]['title'] == "Test subsection 1"

    async def test_patch_section(self, client: AsyncClient, token: str):
        headers = dict()
        headers.update(get_auth_header(token))

        data = {"title": "New test title"}
        response = await client.patch(
            self.get_endpoint(f"patch/{1}"), json=data, headers=headers)
        assert response.status_code == 200
        assert response.json()["title"] == "New test title"
        assert response.json()["describe"] == "this section test 1"

        data["describe"] = "New test describe"
        response = await client.patch(
            self.get_endpoint(f"patch/{1}"), json=data, headers=headers)
        assert response.status_code == 200
        assert response.json()["describe"] == "New test describe"

    async def test_get_section(self, client: AsyncClient):
        section_id = 2
        response = await client.get(self.get_endpoint(section_id))
        assert response.status_code == 200
        assert response.json().get("subsections")[0]['title'] == "Test subsection 1"

        section_id = 100
        response = await client.get(self.get_endpoint(section_id))
        assert response.status_code == 400

    async def test_get_list_sections(self, client: AsyncClient):
        course_id = 1
        response = await client.get(self.get_endpoint(f"list/{course_id}"))
        assert response.status_code == 200
        assert len(response.json()) == 2

    """End CRUD Tests (delete end) """

    async def test_add_subsection_to_section(self, client: AsyncClient, token: str):
        headers = dict()
        headers.update(get_auth_header(token))

        section_id = 1
        added_subsection = {"title": "Added subsection 1"}
        response = await client.put(self.get_endpoint(f"add-subsection/{section_id}"),
           json=added_subsection, headers=headers)

        assert response.status_code == 200
        assert len(response.json().get('subsections')) == 1

    # async def test_bulk_create_sections(self, client: AsyncClient):
    #     # create course
    #     data = {"title": "Test section 1", "describe": "this section test 1", "course_id": 0}
    #     response = await client.get("/users/me")
    #     assert response.status_code == 200


    """DELETE"""

    async def test_delete_section(self, client: AsyncClient, token: str):
        headers = dict()
        headers.update(get_auth_header(token))

        section_id = 1
        response = await client.delete(
            self.get_endpoint(f"delete/{section_id}"), headers=headers)
        assert response.status_code == 204


        section_id = 2
        response = await client.delete(
            self.get_endpoint(f"delete/{section_id}"), headers=headers)
        assert response.status_code == 204

        response = await client.delete(
            self.get_endpoint(f"delete/{section_id}"), headers=headers)
        assert response.status_code == 400
