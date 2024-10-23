import pytest

from httpx import AsyncClient
from loguru import logger

from .helpers.test_class import BaseTestClass


@pytest.mark.usefixtures("create_section")
class TestsForSubsections(BaseTestClass):

    prefix = "/subsections"

    """CRUD (delete in the end of tests)"""

    async def test_create_subsection(self, client: AsyncClient, token: dict):

        headers = dict()
        headers.update(token)

        data = {"title": "Test title 1", "section_id": 1, "position": 1}
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 201
        assert response.json().get("title") == "Test title 1"

        data["section_id"] = 100
        response = await client.post(
            self.get_endpoint("create"), json=data, headers=headers
        )
        assert response.status_code == 400

    @pytest.mark.usefixtures("create_subsection")
    async def test_get_subsection(self, client: AsyncClient):
        subsection_id = 1
        response = await client.get(self.get_endpoint(subsection_id))
        assert response.status_code == 200
        assert response.json().get("section_id") == 1

        subsection_id = 100
        response = await client.get(self.get_endpoint(subsection_id))
        assert response.status_code == 400

    @pytest.mark.usefixtures("create_subsection")
    async def test_patch_subsection(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        subsection_id = 1
        data = {"title": "New subsection title"}
        response = await client.patch(
            self.get_endpoint(f"patch/{subsection_id}"), json=data, headers=headers
        )
        assert response.status_code == 200
        assert response.json().get("title") == "New subsection title"

    @pytest.mark.usefixtures("create_subsection")
    async def test_list_subsection(self, client: AsyncClient):
        section_id = 1
        response = await client.get(self.get_endpoint(f"list/{section_id}"))
        assert response.status_code == 200
        assert len(response.json()) == 2

        section_id = 100
        response = await client.get(self.get_endpoint(f"list/{section_id}"))
        assert response.status_code == 400

    @pytest.mark.usefixtures("create_subsection")
    async def test_delete_subsection(self, client: AsyncClient, token: dict):
        headers = dict()
        headers.update(token)

        subsection_id = 1
        response = await client.delete(
            self.get_endpoint(f"delete/{subsection_id}"), headers=headers
        )
        assert response.status_code == 204

        response = await client.get(self.get_endpoint(subsection_id))
        assert response.status_code == 400
